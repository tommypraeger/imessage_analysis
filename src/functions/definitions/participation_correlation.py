import numpy as np

from src.functions import Function
from src.utils import helpers, constants


CORRELATION_CATEGORY = "Participation correlation"


class ParticipationCorrelation(Function):
    @staticmethod
    def get_function_name():
        return "participation_correlation"

    @staticmethod
    def get_categories():
        # Returns an HTML table instead of columnar data
        return []

    @staticmethod
    def get_categories_allowing_graph_total():
        return []

    @staticmethod
    def process_messages_df(df, args):
        # Ensure conversations are computed consistently with other functions
        minutes_threshold = getattr(args, "minutes_threshold", None)
        return helpers.compute_conversation_columns(
            df, minutes_threshold=minutes_threshold
        )

    def get_table_results(self, result_dict, df, chat_members, args):
        df = self.process_messages_df(df, args)

        # Optionally exclude reactions when determining participation
        if getattr(args, "exclude_reactions", False):
            df = helpers.get_non_reaction_messages(df)

        participants_by_conv, _, _ = helpers.summarize_conversations(df)
        conv_ids = sorted(participants_by_conv.keys())
        members = sorted({str(m) for m in chat_members})

        # Build participation vectors per member (sorted names)
        members = sorted(members)
        vectors = []
        for name in members:
            vec = [
                1 if name in participants_by_conv.get(conv, set()) else 0
                for conv in conv_ids
            ]
            vectors.append(vec)

        vectors_arr = np.array(vectors, dtype=float) if vectors else np.empty((0, 0))

        # Compute pairwise correlations (pearson). Handle zero-variance vectors by returning 0.
        def corr_pair(v1, v2):
            if len(v1) == 0:
                return 0.0
            if np.all(v1 == v1[0]) or np.all(v2 == v2[0]):
                # One is constant (all 0s or 1s); treat correlation as 0
                return 0.0
            return float(np.corrcoef(v1, v2)[0, 1])

        matrix = []
        for i, _ in enumerate(members):
            row = []
            for j, _ in enumerate(members):
                if i == j:
                    row.append(1.0)
                elif j < i:
                    row.append(matrix[j][i])
                else:
                    row.append(corr_pair(vectors_arr[i], vectors_arr[j]))
            matrix.append(row)

        headers = [""] + members
        rows = []
        for name, row in zip(members, matrix):
            rows.append([name] + [round(v, 3) for v in row])

        # Provide structured table data for UI rendering/coloring
        result_dict["tableData"] = {"headers": headers, "rows": rows}
        return df

    # Graph path not supported; fall back to empty data if invoked
    def get_results(self, output_dict, df, args, member_name=None, time_period=None):
        return
