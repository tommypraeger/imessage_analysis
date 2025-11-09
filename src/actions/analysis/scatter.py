from types import SimpleNamespace
from typing import Dict, List, Tuple

import pandas as pd

from src import functions
from src.utils import helpers
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


def _compute_points_custom(df: pd.DataFrame, args, chat_members: List[str]) -> Tuple[List[Tuple[str, float, float]], str, str, str]:
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
    return points, title, subtitle, slug


def _compute_points_lfwt(df: pd.DataFrame, args, chat_members: List[str]) -> Tuple[List[Tuple[str, float, float]], str, str, str]:
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
        x = helpers.safe_divide(conv_started, conv_participated)
        y = participation_rate
        points.append((member, x, y))

    title = "Leader/Feeder vs Walker/Talker"
    subtitle = "conversations started/conversations participated in vs conversations participation rate"
    slug = "lfwt"
    return points, title, subtitle, slug


def run_scatter(df: pd.DataFrame, args, chat_members: List[str]) -> Dict[str, str]:
    # Determine mode: preset or custom
    if getattr(args, "scatter_preset", None):
        preset = args.scatter_preset.lower()
        if preset == "lfwt":
            points, title, subtitle, slug = _compute_points_lfwt(df, args, chat_members)
        else:
            raise ValueError(f"Unknown scatter preset: {preset}")
    else:
        # Custom X/Y metrics from functions/categories
        if not (getattr(args, "x_function", None) and getattr(args, "x_category", None) and getattr(args, "y_function", None) and getattr(args, "y_category", None)):
            raise ValueError("Custom scatter requires x-function, x-category, y-function, and y-category")
        points, title, subtitle, slug = _compute_points_custom(df, args, chat_members)

    # Generate image
    return generate_scatter_image(
        points,
        x_label=title.split(" vs ")[0] if " vs " in title else "X",
        y_label=title.split(" vs ")[1] if " vs " in title else "Y",
        title=title,
        subtitle=subtitle or None,
        slug=slug,
        add_regression=getattr(args, "scatter_regression", False),
        add_residuals=getattr(args, "scatter_residuals", False),
    )

