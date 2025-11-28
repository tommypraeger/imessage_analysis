from typing import Dict, Optional, Tuple

from src.functions import Function
from src.utils import helpers

SOLO_COUNT_CATEGORY = "Solo conversations started"
SOLO_PERCENT_CATEGORY = "Percent of started conversations that are solo"


class SoloConversations(Function):
    def __init__(self):
        self._summary_cache: Dict[str, Tuple[Dict[int, set], Dict[int, str], Dict[str, set]]] = {}

    @staticmethod
    def get_function_name():
        return "solo_conversations"

    @staticmethod
    def get_categories():
        return [SOLO_COUNT_CATEGORY, SOLO_PERCENT_CATEGORY]

    @staticmethod
    def get_categories_allowing_graph_total():
        return [SOLO_COUNT_CATEGORY, SOLO_PERCENT_CATEGORY]

    def process_messages_df(self, df, args):
        minutes_threshold = getattr(args, "minutes_threshold", None)
        df = helpers.compute_conversation_columns(df, minutes_threshold=minutes_threshold)
        self._summary_cache.clear()
        return df

    def _get_summary(self, df, time_period: Optional[str], args):
        key = time_period if time_period is not None else "__all__"
        if key not in self._summary_cache:
            if getattr(args, "exclude_reactions", False):
                df = helpers.get_non_reaction_messages(df)
            summary = helpers.summarize_conversations(df, time_period=time_period)
            self._summary_cache[key] = summary
        return self._summary_cache[key]

    def get_results(self, output_dict, df, args, member_name=None, time_period=None):
        participants_by_conv, starter_by_conv, _ = self._get_summary(df, time_period, args)
        if member_name is None:
            relevant_starters = starter_by_conv.items()
        else:
            relevant_starters = [
                (conv_id, starter)
                for conv_id, starter in starter_by_conv.items()
                if starter == member_name
            ]
        total_started = len(relevant_starters)
        solo_started = sum(
            1 for conv_id, _ in relevant_starters if len(participants_by_conv.get(conv_id, set())) <= 1
        )
        percent_solo = helpers.safe_divide_as_pct(solo_started, total_started) if total_started else 0.0

        output_dict[SOLO_COUNT_CATEGORY].append(solo_started)
        output_dict[SOLO_PERCENT_CATEGORY].append(percent_solo)
