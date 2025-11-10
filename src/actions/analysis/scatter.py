from types import SimpleNamespace
from typing import Dict, List, Tuple

import pandas as pd

from src import functions
from src.utils import helpers, constants
from src.utils.graph_utils import generate_scatter_image


def _copy_args(args, **overrides):
    d = vars(args).copy()
    d.update(overrides)
    return SimpleNamespace(**d)


def _run_function_table(df: pd.DataFrame, args, chat_members: List[str], fn_name: str) -> Dict:
    fn = functions.get_function_class_by_name(fn_name)
    table_args = _copy_args(args, function=fn_name, table=True, graph=False, scatter=False)
    result_dict, _ = fn.run(df, table_args, chat_members)
    return result_dict


def _series_by_member(result_dict: Dict, category: str) -> Dict[str, float]:
    names = result_dict.get("names", [])
    values = result_dict.get(category, [])
    return dict(zip(names, values))


def _compute_points_custom(df: pd.DataFrame, args, chat_members: List[str]) -> Tuple[List[Tuple[str, float, float]], str, str, str, str, str]:
    # X metric
    x_results = _run_function_table(df, args, chat_members, args.x_function)
    x_map = _series_by_member(x_results, args.x_category)
    # Y metric
    y_results = _run_function_table(df, args, chat_members, args.y_function)
    y_map = _series_by_member(y_results, args.y_category)

    # Join by member name
    points = []
    for name in set(x_map.keys()).intersection(y_map.keys()):
        points.append((name, x_map[name], y_map[name]))

    title = f"{args.x_category} vs {args.y_category}"
    subtitle = ""
    slug = "custom"
    x_label = args.x_category
    y_label = args.y_category
    return points, title, subtitle, slug, x_label, y_label


def _compute_points_lfwt(df: pd.DataFrame, args, chat_members: List[str]) -> Tuple[List[Tuple[str, float, float]], str, str, str, str, str]:
    # Ensure conversation columns according to new rules
    df = helpers.compute_conversation_columns(df, minutes_threshold=args.minutes_threshold)

    # Total conversations in the dataset
    total_conversations = len(pd.unique(df["conversation number"])) if len(df) > 0 else 0

    points = []
    for member in chat_members:
        msgs = helpers.get_messages(df, member_name=member)
        conv_started = int(msgs["is conversation starter?"].sum())
        conv_participated = len(pd.unique(msgs["conversation number"])) if len(msgs) > 0 else 0
        participation_rate = helpers.safe_divide_as_pct(conv_participated, total_conversations)
        # x as percentage: conversations started / conversations participated in
        x = helpers.safe_divide(conv_started, conv_participated) * 100
        y = participation_rate
        points.append((member, x, y))

    title = "Leader/Feeder vs Walker/Talker"
    # subtitle = "conversations started/conversations participated in vs conversations participation rate"
    subtitle = """Leader/Feeder: how often you start the conversations you take part in
    Walker/Talker: how often you participate in conversations"""
    slug = "lfwt"
    x_label = "Conversations started / Conversations participated in (%)"
    y_label = "Conversation participation in / Total conversations (%)"
    return points, title, subtitle, slug, x_label, y_label


def _compute_points_rroe(df: pd.DataFrame, args, chat_members: List[str]) -> Tuple[List[Tuple[str, float, float]], str, str, str, str, str]:
    """
    Reactions Received Over Expected (RROE) preset.

    - Y (actual): reactions received per non-reaction message sent by the member
    - X (expected): expected reactions per message from a smooth baseline
      expected_i = base * (1 - s_react_i)^beta * (1 - s_msg_i)^alpha
      where base = R_sent / M, s_msg_i = m_i/M, s_react_i = r_sent_i/R_sent, and alpha=beta=0.5
      Then normalize expected so that mean(expected) == mean(actual) across members with m_i>0
    """
    # Build per-original-message table with reaction counts
    base = helpers.add_reactions_for_each_message(df)

    # Totals for shares
    mt = df["message_type"].astype("string")
    is_reaction = mt.isin(constants.REACTION_TYPES)
    R_sent = int(is_reaction.sum())
    M = int(len(base))

    # Guard: avoid division by zero
    if M == 0 or R_sent == 0:
        # Degenerate case: everyone has expected=0 and actual=0
        points: List[Tuple[str, float, float]] = [(member, 0.0, 0.0) for member in chat_members]
        title = "Reactions Received Over Expected (rroe)"
        subtitle = "actual vs expected reactions per message"
        slug = "rroe"
        x_label = "Expected reactions per message"
        y_label = "Actual reactions per message"
        return points, title, subtitle, slug, x_label, y_label

    # Reactions sent per member
    reactions_sent_by_member = (
        df[is_reaction]
        .groupby("sender")
        .size()
        .astype(int)
        .to_dict()
    )

    alpha = 1
    beta = 1
    EPS = 1e-6
    base_rate = R_sent / M

    actuals: List[float] = []
    expected: List[float] = []
    member_order: List[str] = []

    # Pre-compute messages per member (non-reaction) and reactions received
    msgs_per_member = {name: 0 for name in chat_members}
    reacts_received_per_member = {name: 0 for name in chat_members}
    for member in chat_members:
        b = base[base["sender"] == member]
        msgs_per_member[member] = int(len(b))
        reacts_received_per_member[member] = int(b["reaction_count"].sum())

    # Compute expected and actual per member
    for member in chat_members:
        m_i = msgs_per_member.get(member, 0)
        r_sent_i = int(reactions_sent_by_member.get(member, 0))
        s_msg_i = m_i / M if M > 0 else 0.0
        s_react_i = r_sent_i / R_sent if R_sent > 0 else 0.0
        # clamp
        s_msg_i = max(EPS, min(1 - EPS, s_msg_i))
        s_react_i = max(EPS, min(1 - EPS, s_react_i))

        attn = (1.0 - s_msg_i) ** alpha
        supply = (1.0 - s_react_i) ** beta
        exp_i = base_rate * supply * attn
        expected.append(exp_i)

        y_i = helpers.safe_divide(reacts_received_per_member.get(member, 0), m_i)
        actuals.append(y_i)
        member_order.append(member)

    # Normalize expected to match mean actual among members with m_i>0
    nonzero_mask = [msgs_per_member[m] > 0 for m in member_order]
    if any(nonzero_mask):
        exp_mean = sum(exp_i for exp_i, nz in zip(expected, nonzero_mask) if nz) / max(1, sum(1 for nz in nonzero_mask if nz))
        act_mean = sum(a for a, nz in zip(actuals, nonzero_mask) if nz) / max(1, sum(1 for nz in nonzero_mask if nz))
        if exp_mean > 0:
            k = act_mean / exp_mean
            expected = [exp_i * k for exp_i in expected]

    points: List[Tuple[str, float, float]] = [
        (name, exp_i, act_i) for name, exp_i, act_i in zip(member_order, expected, actuals)
    ]

    title = "Reactions Received Over Expected (rroe)"
    subtitle = "actual vs expected reactions per message"
    slug = "rroe"
    x_label = "Expected reactions per message"
    y_label = "Actual reactions per message"
    return points, title, subtitle, slug, x_label, y_label


def run_scatter(df: pd.DataFrame, args, chat_members: List[str]) -> Dict[str, str]:
    # Determine mode: preset or custom
    preset_lower = (getattr(args, "scatter_preset", None) or "").lower()
    if preset_lower:
        if preset_lower == "lfwt":
            points, title, subtitle, slug, x_label, y_label = _compute_points_lfwt(df, args, chat_members)
        elif preset_lower == "rroe":
            points, title, subtitle, slug, x_label, y_label = _compute_points_rroe(df, args, chat_members)
        else:
            raise ValueError(f"Unknown scatter preset: {preset_lower}")
    else:
        # Custom X/Y metrics from functions/categories
        if not (getattr(args, "x_function", None) and getattr(args, "x_category", None) and getattr(args, "y_function", None) and getattr(args, "y_category", None)):
            raise ValueError("Custom scatter requires x-function, x-category, y-function, and y-category")
        points, title, subtitle, slug, x_label, y_label = _compute_points_custom(df, args, chat_members)

    # Compute date range text: prefer explicit args; fallback to df time bounds
    def _fmt_date(d):
        try:
            return d.strftime("%Y-%m-%d")
        except Exception:
            return str(d)

    try:
        start_dt = helpers.parse_date(args.from_date)
    except Exception:
        start_dt = pd.to_datetime(df["time"].min())
    try:
        end_dt = helpers.parse_date(args.to_date)
    except Exception:
        end_dt = pd.to_datetime(df["time"].max())
    date_range_text = f"Date range: {_fmt_date(start_dt)} — {_fmt_date(end_dt)}"

    # Generate image
    return generate_scatter_image(
        points,
        x_label=x_label,
        y_label=y_label,
        title=title,
        subtitle=subtitle or None,
        slug=slug,
        add_regression=getattr(args, "scatter_regression", False),
        add_residuals=(getattr(args, "scatter_regression", False) and getattr(args, "scatter_residuals", False)),
        x_percent=(preset_lower == "lfwt"),
        y_percent=(preset_lower == "lfwt"),
        add_quadrant_axes=(preset_lower == "lfwt"),
        x_left_label=("← Feeder" if preset_lower == "lfwt" else None),
        x_right_label=("Leader →" if preset_lower == "lfwt" else None),
        y_bottom_label=("Walker ↓" if preset_lower == "lfwt" else None),
        y_top_label=("Talker ↑" if preset_lower == "lfwt" else None),
        footer_text=date_range_text,
        add_identity_line=(preset_lower == "rroe"),
        residuals_to_identity=(preset_lower == "rroe"),
    )
