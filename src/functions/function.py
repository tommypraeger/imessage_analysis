import abc
import pandas as pd
from src.utils import helpers, constants


class Function(abc.ABC):
    @abc.abstractmethod
    def get_function_name():
        """
        Return function argument name
        """
        pass

    @abc.abstractmethod
    def get_categories():
        """
        Return list of categories (i.e. table columns, graph choices) for this function
        """
        pass

    def get_categories_allowing_graph(self):
        """
        Return list of categories (i.e. table columns, graph choices) for this function
        that can be used for graphing. If not implemented, just return all categories.
        """
        return self.get_categories()

    @abc.abstractmethod
    def get_categories_allowing_graph_total():
        """
        Return list of categories (i.e. table columns, graph choices) for this function
        that can be used when not graphing individual members. Some categories do not make sense
        when just graphing the total line.
        """
        pass

    @abc.abstractmethod
    def process_messages_df(df, args):
        """
        Process messages in data frame and add necessary aggregate columns to the data frame
        """
        pass

    @abc.abstractmethod
    def get_results(output_dict, df, args, time_period=None, member_name=None):
        """
        Fill in results from analysis into output dictionary using processed data frame
        """
        pass

    def run(self, df, args, chat_members):
        result_dict = {}

        if args.table:
            result_dict["Names"] = []
            for category in self.get_categories():
                result_dict[category] = []
            df = self.get_table_results(result_dict, df, chat_members, args)

        elif args.graph:
            # set up
            graph_data = {}
            self.set_up_graph_data(graph_data, args, chat_members)
            self.add_time_period_to_df(df, args.graph_time_interval)
            time_periods = self.get_time_periods(df, args.graph_time_interval)

            # get graph data
            df = self.get_graph_results(
                graph_data, df, chat_members, time_periods, args.graph_individual, args
            )

            # we change the category name for phrase
            if type(self).__name__ == "Phrase":
                args.category = args.category.replace(
                    "the entered phrase", f'"{args.phrase}"'
                )

            # prepare to return data
            self.format_graph_data(
                result_dict,
                graph_data,
                time_periods,
                args.category,
                args.graph_time_interval,
            )

        return result_dict, df

    def get_table_results(self, result_dict, df, chat_members, args):
        df = self.process_messages_df(df, args)
        for member_name in chat_members:
            helpers.initialize_member(member_name, result_dict)
            self.get_results(result_dict, df, args, member_name=member_name)
        return df

    def get_graph_results(
        self,
        graph_data,
        df,
        chat_members,
        time_periods,
        graph_individual,
        args,
    ):
        df = self.process_messages_df(df, args)
        if graph_individual:
            self.get_individual_graph_results(
                graph_data, df, chat_members, time_periods, args
            )
        else:
            self.get_total_graph_results(graph_data, df, time_periods, args)
        return df

    def get_individual_graph_results(
        self,
        graph_data,
        df,
        chat_members,
        time_periods,
        args,
    ):
        for time_period in time_periods:
            for member_name in chat_members:
                self.get_results(
                    graph_data[member_name],
                    df,
                    args,
                    time_period=time_period,
                    member_name=member_name,
                )

    def get_total_graph_results(self, graph_data, df, time_periods, args):
        for time_period in time_periods:
            self.get_results(
                graph_data[constants.GRAPH_TOTAL_KEY],
                df,
                args,
                time_period=time_period,
            )

    def set_up_graph_data(self, graph_data, args, chat_members):
        categories = self.get_categories()
        if args.graph_individual:
            for member_name in chat_members:
                graph_data[member_name] = {}
                for category in categories:
                    graph_data[member_name][category] = []
        else:
            graph_data[constants.GRAPH_TOTAL_KEY] = {}
            # add all categories
            # however, categories not in get_categories_allowing_graph_total()
            # will not be meaningful nor allowed to be selected from the UI
            for category in categories:
                graph_data[constants.GRAPH_TOTAL_KEY][category] = []

    def add_time_period_to_df(self, df, graph_time_interval):
        t = df["time"]
        if graph_time_interval == "day":
            # ISO 8601 date
            tp = t.dt.strftime("%Y-%m-%d")
        elif graph_time_interval == "week":
            # ISO week label YYYY-Www
            iso = t.dt.isocalendar()
            tp = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
        elif graph_time_interval == "month":
            # ISO year-month
            tp = t.dt.strftime("%Y-%m")
        elif graph_time_interval == "year":
            tp = t.dt.strftime("%Y")
        else:
            return
        df["time_period"] = tp.astype("string")

    def format_graph_data(
        self, result_dict, graph_data, time_periods, category, graph_time_interval
    ):
        # ISO8601 labels already in desired form for all intervals
        result_dict["labels"] = time_periods

        result_dict["datasets"] = [
            {
                "label": name,
                "data": graph_data[name][category],
                "fill": False,
                "borderColor": constants.GRAPH_COLORS[i % len(graph_data)],
            }
            for i, name in enumerate(graph_data)
        ]

    def get_time_periods(self, df, time_period_name):
        t = df["time"]
        if len(t) == 0:
            return []

        start = t.min()
        end = t.max()

        # Use PeriodRange to avoid off-by-one issues and ensure inclusive endpoints
        if time_period_name == "day":
            pr = pd.period_range(start=start.normalize(), end=end.normalize(), freq="D")
            return [p.start_time.strftime("%Y-%m-%d") for p in pr]
        if time_period_name == "week":
            # ISO weeks starting Monday
            pr = pd.period_range(start=start.to_period("W-MON"), end=end.to_period("W-MON"), freq="W-MON")
            labels = []
            for p in pr:
                d = p.start_time
                iso = d.isocalendar()
                labels.append(f"{iso.year}-W{iso.week:02d}")
            return labels
        if time_period_name == "month":
            pr = pd.period_range(start=start.to_period("M"), end=end.to_period("M"), freq="M")
            return [p.start_time.strftime("%Y-%m") for p in pr]
        if time_period_name == "year":
            pr = pd.period_range(start=start.to_period("Y"), end=end.to_period("Y"), freq="Y")
            return [p.start_time.strftime("%Y") for p in pr]
