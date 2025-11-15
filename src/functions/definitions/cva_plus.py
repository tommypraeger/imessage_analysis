from typing import Dict, Optional, Tuple

import pandas as pd

from src.functions import Function
from src.utils import helpers, constants

CVA_PLUS_CATEGORY = "CVA+ Rating"
VOLUME_COMPONENT_CATEGORY = "Volume component"
EFFICIENCY_COMPONENT_CATEGORY = "Efficiency component"

CVA_DEFAULT_VOLUME_WEIGHT = 50.0
CVA_DEFAULT_EFFICIENCY_WEIGHT = 50.0
CVA_REACTION_EFFICIENCY_WEIGHTS = {
    "love": 1.2,
    "like": 0.5,
    "dislike": 0.0,
    "laugh": 1.2,
    "emphasize": 1.0,
    "question": 0.0,
    "custom emoji": 1.2,
}

VOLUME_METRIC_KEYS = [
    "messages_sent",
    "conversations_started",
    "conversations_participated",
    "reactions_received",
    "reactions_sent",
]
CVA_METRIC_WEIGHTS = {
    "messages_sent": 1.0,
    "conversations_started": 1.5,
    "conversations_participated": 1.0,
    "reactions_received": 0.5,
    "reactions_sent": 1.0,
    "weighted_reactions_per_message": 1.5,
    "non_solo_conversation_rate": 1.0,
}
EFFICIENCY_METRIC_KEYS = [
    "weighted_reactions_per_message",
    "non_solo_conversation_rate",
]


class CVAPlus(Function):
    def __init__(self):
        self._original_messages_df: Optional[pd.DataFrame] = None
        self._member_stats_cache: Dict[str, Dict[str, Dict[str, float]]] = {}
        self._score_cache: Dict[Tuple[str, float, float], Dict[str, Dict[str, float]]] = {}

    @staticmethod
    def get_function_name():
        return "cva_plus"

    @staticmethod
    def get_categories():
        return [
            CVA_PLUS_CATEGORY,
            VOLUME_COMPONENT_CATEGORY,
            EFFICIENCY_COMPONENT_CATEGORY,
        ]

    @staticmethod
    def get_categories_allowing_graph_total():
        return []

    def process_messages_df(self, df, args):
        minutes_threshold = getattr(args, "minutes_threshold", None)
        df = helpers.compute_conversation_columns(df, minutes_threshold=minutes_threshold)
        self._original_messages_df = helpers.add_reactions_for_each_message(df)
        self._member_stats_cache.clear()
        self._score_cache.clear()
        return df

    def _get_weight_split(self, args) -> Tuple[float, float]:
        volume_weight = getattr(args, "cva_volume_weight", None)
        efficiency_weight = getattr(args, "cva_efficiency_weight", None)
        if volume_weight is None and efficiency_weight is None:
            volume_weight = CVA_DEFAULT_VOLUME_WEIGHT
            efficiency_weight = CVA_DEFAULT_EFFICIENCY_WEIGHT
        elif volume_weight is None:
            efficiency_weight = max(0.0, min(100.0, float(efficiency_weight or 0.0)))
            volume_weight = 100.0 - efficiency_weight
        elif efficiency_weight is None:
            volume_weight = max(0.0, min(100.0, float(volume_weight or 0.0)))
            efficiency_weight = 100.0 - volume_weight
        else:
            volume_weight = max(0.0, float(volume_weight))
            efficiency_weight = max(0.0, float(efficiency_weight))
            total = volume_weight + efficiency_weight
            if total == 0:
                volume_weight = efficiency_weight = 50.0
            else:
                volume_weight = (volume_weight / total) * 100.0
                efficiency_weight = (efficiency_weight / total) * 100.0
        return volume_weight, efficiency_weight

    def _build_member_stats(self, df, time_period: Optional[str]):
        cache_key = time_period if time_period is not None else "__all__"
        if cache_key in self._member_stats_cache:
            return self._member_stats_cache[cache_key]

        messages = helpers.get_messages(df, time_period=time_period)
        messages = messages[messages["sender"].notna()].copy()
        non_reaction_messages = helpers.get_non_reaction_messages(df, time_period=time_period)
        non_reaction_messages = non_reaction_messages[non_reaction_messages["sender"].notna()].copy()

        if self._original_messages_df is None:
            originals = helpers.add_reactions_for_each_message(df)
        else:
            originals = self._original_messages_df

        if time_period is not None and "time_period" in originals.columns:
            originals = originals[originals["time_period"] == time_period]
        originals = originals[originals["sender"].notna()].copy()
        originals_groups = {name: group for name, group in originals.groupby("sender")}

        (
            participants_by_conv,
            starter_by_conv,
            member_conversations,
        ) = helpers.summarize_conversations(df, time_period=time_period)

        non_reaction_counts = non_reaction_messages.groupby("sender").size().to_dict()
        if "message_type" in messages.columns:
            message_types = messages["message_type"].astype("string")
            reaction_rows = messages[message_types.isin(constants.REACTION_TYPES)]
            reactions_sent_counts = reaction_rows.groupby("sender").size().to_dict()
        else:
            reactions_sent_counts = {}

        sender_series = messages["sender"].astype("string")
        member_names = sorted([str(name) for name in sender_series.unique().tolist()])
        stats = {}
        for member in member_names:
            member_non_reaction_count = int(non_reaction_counts.get(member, 0))
            member_participation = len(member_conversations.get(member, set()))

            member_started_convs = [
                conv_id for conv_id, starter in starter_by_conv.items() if starter == member
            ]
            member_starters = len(member_started_convs)
            solo_started = sum(
                1 for conv_id in member_started_convs if len(participants_by_conv.get(conv_id, set())) <= 1
            )
            if member_starters > 0:
                solo_pct = helpers.safe_divide(solo_started, member_starters) * 100.0
                non_solo_rate = round(max(0.0, 100.0 - solo_pct), 2)
            else:
                non_solo_rate = 100.0

            originals_group = originals_groups.get(member)
            if originals_group is not None and len(originals_group):
                reactions_received = int(originals_group["reaction_count"].sum())
            else:
                reactions_received = 0

            weighted_reactions = 0.0
            weighted_map = CVA_REACTION_EFFICIENCY_WEIGHTS
            if originals_group is not None and len(originals_group):
                for reactions_list in originals_group["reactions_per_user"]:
                    if not isinstance(reactions_list, list):
                        continue
                    for _, reaction_type in reactions_list:
                        weight = weighted_map.get(str(reaction_type), 1.0)
                        weighted_reactions += weight

            weighted_reactions_per_message = helpers.safe_divide(
                weighted_reactions, member_non_reaction_count
            )

            stats[member] = {
                "messages_sent": float(member_non_reaction_count),
                "conversations_started": float(member_starters),
                "conversations_participated": float(member_participation),
                "reactions_received": float(reactions_received),
                "reactions_sent": float(reactions_sent_counts.get(member, 0)),
                "weighted_reactions_per_message": weighted_reactions_per_message,
                "non_solo_conversation_rate": non_solo_rate,
            }

        self._member_stats_cache[cache_key] = stats
        return stats

    def _normalize_metric(self, values: Dict[str, float]) -> Dict[str, float]:
        if not values:
            return {}
        avg_value = sum(values.values()) / len(values)
        if avg_value <= 0:
            return {member: 0.0 for member in values}
        return {
            member: helpers.safe_divide(value, avg_value) * 100.0
            for member, value in values.items()
        }

    def _average_metric_scores(self, metrics_with_keys):
        if not metrics_with_keys:
            return {}
        members = set()
        for _, metric_scores in metrics_with_keys:
            members.update(metric_scores.keys())
        if not members:
            return {}
        members = sorted(members)
        totals = {member: 0.0 for member in members}
        weight_sum = 0.0
        for metric_key, metric_scores in metrics_with_keys:
            weight = CVA_METRIC_WEIGHTS.get(metric_key, 1.0)
            if weight <= 0:
                continue
            weight_sum += weight
            for member in members:
                totals[member] += metric_scores.get(member, 0.0) * weight
        if weight_sum <= 0:
            weight_sum = len(metrics_with_keys)
        for member in totals:
            totals[member] = helpers.safe_divide(totals[member], weight_sum)
        return totals

    def _compute_scores(self, df, args, time_period: Optional[str]):
        volume_weight, efficiency_weight = self._get_weight_split(args)
        cache_key = (
            time_period if time_period is not None else "__all__",
            round(volume_weight, 4),
            round(efficiency_weight, 4),
        )
        if cache_key in self._score_cache:
            return self._score_cache[cache_key]

        member_stats = self._build_member_stats(df, time_period)
        if not member_stats:
            scores = {}
            self._score_cache[cache_key] = scores
            return scores

        volume_metric_dicts = []
        for metric_key in VOLUME_METRIC_KEYS:
            values = {member: stats[metric_key] for member, stats in member_stats.items()}
            volume_metric_dicts.append((metric_key, self._normalize_metric(values)))

        efficiency_metric_dicts = []
        for metric_key in EFFICIENCY_METRIC_KEYS:
            values = {member: stats[metric_key] for member, stats in member_stats.items()}
            efficiency_metric_dicts.append((metric_key, self._normalize_metric(values)))

        volume_component = self._average_metric_scores(volume_metric_dicts)
        efficiency_component = self._average_metric_scores(efficiency_metric_dicts)

        total_weight = volume_weight + efficiency_weight
        if total_weight <= 0:
            total_weight = 100.0
            volume_weight = efficiency_weight = 50.0
        volume_fraction = volume_weight / total_weight
        efficiency_fraction = efficiency_weight / total_weight

        raw_scores = {}
        for member in member_stats:
            raw_scores[member] = (
                volume_component.get(member, 0.0) * volume_fraction
                + efficiency_component.get(member, 0.0) * efficiency_fraction
            )

        avg_raw = sum(raw_scores.values()) / len(raw_scores)
        normalized_scores = {}
        if avg_raw > 0:
            for member, value in raw_scores.items():
                normalized_scores[member] = helpers.safe_divide(value, avg_raw) * 100.0
        else:
            normalized_scores = {member: 0.0 for member in raw_scores}

        result = {}
        for member in member_stats:
            result[member] = {
                "rating": round(normalized_scores.get(member, 0.0), 2),
                "volume": round(volume_component.get(member, 0.0), 2),
                "efficiency": round(efficiency_component.get(member, 0.0), 2),
            }

        self._score_cache[cache_key] = result
        return result

    def get_results(self, output_dict, df, args, member_name=None, time_period=None):
        scores = self._compute_scores(df, args, time_period)
        target = member_name
        member_scores = scores.get(target, {"rating": 0.0, "volume": 0.0, "efficiency": 0.0})
        output_dict[CVA_PLUS_CATEGORY].append(member_scores["rating"])
        output_dict[VOLUME_COMPONENT_CATEGORY].append(member_scores["volume"])
        output_dict[EFFICIENCY_COMPONENT_CATEGORY].append(member_scores["efficiency"])
