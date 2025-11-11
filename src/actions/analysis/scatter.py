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


def _aggregate_rroe_inputs(df: pd.DataFrame, members: List[str]):
    """Gather per-member aggregates for RROE in a descriptive way.

    Returns a tuple:
      originals_df, total_reactions_sent, messages_per_member, reactions_received_per_member,
      reactions_sent_by_member, total_messages
    """
    originals_df = helpers.add_reactions_for_each_message(df)

    # Total reaction rows in dataset
    msg_type = df["message_type"].astype("string")
    is_reaction = msg_type.isin(constants.REACTION_TYPES)
    total_reactions_sent = int(is_reaction.sum())

    # Per-member message counts (non-reaction originals) and reactions received
    messages_per_member: Dict[str, int] = {}
    reactions_received_per_member: Dict[str, int] = {}
    for name in members:
        own_originals = originals_df[originals_df["sender"] == name]
        messages_per_member[name] = int(len(own_originals))
        reactions_received_per_member[name] = int(own_originals["reaction_count"].sum())

    # Reactions sent per member (from reaction rows only)
    reactions_sent_by_member: Dict[str, int] = (
        df[is_reaction].groupby("sender").size().astype(int).to_dict()
    )

    total_messages = int(len(originals_df))
    return (
        originals_df,
        total_reactions_sent,
        messages_per_member,
        reactions_received_per_member,
        reactions_sent_by_member,
        total_messages,
    )


def _scale_expected_to_match_actual_mean(
    expected_values_list: List[float],
    actual_values_list: List[float],
    message_counts_by_member: Dict[str, int],
    member_order: List[str],
) -> List[float]:
    """
    Make the expected scale comparable to the observed (actual) scale by multiplying all
    expected values by a single scalar so that the group mean of expected matches the
    group mean of actual.

    Why: The baseline formula gives relative expectations. A single scalar preserves
    relative differences between members while lining up expected and actual magnitudes.

    Implementation:
    - Consider only members who have at least one original message; otherwise the mean
      would be skewed by empty participants.
    - k = mean(actual) / mean(expected) over those members
    - Return expected_scaled_i = k * expected_i
    """
    nonzero_mask = [message_counts_by_member.get(name, 0) > 0 for name in member_order]
    if not any(nonzero_mask):
        return expected_values_list

    expected_included = [v for v, include in zip(expected_values_list, nonzero_mask) if include]
    actual_included = [v for v, include in zip(actual_values_list, nonzero_mask) if include]
    if not expected_included:
        return expected_values_list

    expected_mean = sum(expected_included) / len(expected_included)
    actual_mean = sum(actual_included) / len(actual_included) if actual_included else 0.0
    if expected_mean <= 0:
        return expected_values_list

    k = actual_mean / expected_mean
    return [v * k for v in expected_values_list]


def _clamp_share(value: float, eps: float = 1e-6) -> float:
    """Clamp a proportion into (eps, 1-eps) to avoid edge behaviour in powers."""
    return max(eps, min(1 - eps, value))


def _compute_points_rroe(
    df: pd.DataFrame, args, chat_members: List[str]
) -> Tuple[List[Tuple[str, float, float]], str, str, str, str, str]:
    """
    Compute scatter points for the RROE preset.

    Returns (points, title, subtitle, slug, x_label, y_label) where:
    - points: list of (member_name, expected_per_message, actual_per_message)
      • actual_per_message = reactions_received_on_member_messages / original_messages_sent
      • expected_per_message = a smooth baseline: (1 - message_share)^alpha * (1 - reaction_sent_share)^beta,
        scaled afterward so its mean matches the mean of actual_per_message.
    """
    title = "Reactions Received Over Expected (rroe)"
    subtitle = "actual vs expected reactions per message"
    slug = "rroe"
    x_label = "Expected reactions per message"
    y_label = "Actual reactions per message"
    (
        originals_df,
        total_reactions_sent,
        messages_per_member,
        reactions_received_per_member,
        reactions_sent_by_member,
        total_original_messages,
    ) = _aggregate_rroe_inputs(df, chat_members)

    # If no messages or no reactions are present, return zeros
    if total_original_messages == 0 or total_reactions_sent == 0:
        zero_points = [(name, 0.0, 0.0) for name in chat_members]
        return (zero_points, title, subtitle, slug, x_label, y_label)

    # Parameters for the baseline (intentionally simple and smooth)
    # Allow frontend-configured smoothing exponents; default preserves prior behavior
    alpha = float(getattr(args, "alpha", 1) or 1)  # weight for (1 - message_share)
    beta = float(getattr(args, "beta", 1) or 1)    # weight for (1 - reaction_sent_share)

    # Compute per-member actuals and expected baseline
    actual_values_list: List[float] = []
    expected_values_list: List[float] = []
    member_order: List[str] = []

    for name in chat_members:
        messages_sent = messages_per_member.get(name, 0)
        reactions_sent = int(reactions_sent_by_member.get(name, 0))

        # Shares of group totals (clamped to avoid 0 or 1 exactly)
        message_share = _clamp_share(
            (messages_sent / total_original_messages) if total_original_messages > 0 else 0.0
        )
        reaction_sent_share = _clamp_share(
            (reactions_sent / total_reactions_sent) if total_reactions_sent > 0 else 0.0
        )

        attention_factor = (1.0 - message_share) ** alpha
        supply_factor = (1.0 - reaction_sent_share) ** beta
        # We omit the base scale here and rely on the subsequent scaling step to
        # align expected to actual magnitudes, keeping only relative effects.
        expected_values_list.append(attention_factor * supply_factor)

        actual_values_list.append(
            helpers.safe_divide(reactions_received_per_member.get(name, 0), messages_sent)
        )
        member_order.append(name)

    # Normalize expected to match actual means (over members with at least one message)
    expected_values_list = _scale_expected_to_match_actual_mean(
        expected_values_list, actual_values_list, messages_per_member, member_order
    )

    # Build points preserving the member order
    points = [(n, x, y) for n, x, y in zip(member_order, expected_values_list, actual_values_list)]

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
