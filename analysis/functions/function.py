import abc
import datetime
from dateutil import relativedelta
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers


class Function(abc.ABC):
    @abc.abstractmethod
    def get_function_name(self):
        """
        Return function argument name
        """
        pass

    @abc.abstractmethod
    def get_categories(self):
        """
        Return list of categories (i.e. table columns, graph choices) for this function
        """
        pass

    @abc.abstractmethod
    def get_categories_allowing_graph_total(self):
        """
        Return list of categories (i.e. table columns, graph choices) for this function
        that can be used when not graphing individual members
        """
        pass

    @abc.abstractmethod
    def get_table_results(self, result_dict, df, chat_members, args):
        """
        Return table data
        """
        pass

    @abc.abstractmethod
    def get_graph_results(self, graph_data, df, chat_members, time_periods, args):
        """
        Return graph data
        """
        pass

    def run(self, df, args, chat_members):
        result_dict = {}

        if args.table:
            result_dict["names"] = []
            for category in self.get_categories():
                result_dict[category] = []
            self.get_table_results(result_dict, df, chat_members, args)

        elif args.graph:
            # set up
            graph_data = {}
            self.set_up_graph_data(graph_data, args, chat_members)
            self.add_time_period_to_df(df, args.graph_time_interval)
            time_periods = self.get_time_periods(df, args.graph_time_interval)

            # get graph data
            self.get_graph_results(graph_data, df, chat_members, time_periods, args)

            # prepare to return data
            self.format_graph_data(
                result_dict,
                graph_data,
                time_periods,
                args.category,
                args.graph_time_interval,
            )

        return result_dict

    def set_up_graph_data(self, graph_data, args, chat_members):
        categories = self.get_categories()
        categories_allowing_graph_total = self.get_categories_allowing_graph_total()
        if args.graph_individual:
            for member_name in chat_members:
                graph_data[member_name] = {}
                for category in categories:
                    graph_data[member_name][category] = []
        else:
            graph_data[constants.GRAPH_TOTAL_KEY] = {}
            for category in categories_allowing_graph_total:
                graph_data[constants.GRAPH_TOTAL_KEY][category] = []

    def add_time_period_to_df(self, df, graph_time_interval):
        if graph_time_interval == "day":
            df["time_period"] = df["time"].apply(helpers.get_day)
        elif graph_time_interval == "week":
            df["time_period"] = df["time"].apply(helpers.get_week)
        elif graph_time_interval == "month":
            df["time_period"] = df["time"].apply(helpers.get_month)
        elif graph_time_interval == "year":
            df["time_period"] = df["time"].apply(helpers.get_year)

    def format_graph_data(
        self, result_dict, graph_data, time_periods, category, graph_time_interval
    ):
        if graph_time_interval == "day" or graph_time_interval == "week":
            result_dict["labels"] = time_periods
        elif graph_time_interval == "month":
            result_dict["labels"] = [
                f'{time_period.split("/")[0]}/{time_period.split("/")[2]}'
                for time_period in time_periods
            ]
        elif graph_time_interval == "year":
            result_dict["labels"] = [
                f'20{time_period.split("/")[2]}' for time_period in time_periods
            ]

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
        day_fmt = "%m/%d/%y"
        begin_date = datetime.datetime.strptime(df["time_period"].iloc[0], day_fmt)
        end_date = datetime.datetime.strptime(df["time_period"].iloc[-1], day_fmt)

        if time_period_name == "day":
            num_days = (end_date - begin_date).days
            return [
                helpers.get_day(begin_date + relativedelta.relativedelta(days=i))
                for i in range(num_days + 1)
            ]
        if time_period_name == "week":
            num_weeks = (end_date - begin_date).days // 7
            return [
                helpers.get_week(begin_date + relativedelta.relativedelta(days=i * 7))
                for i in range(num_weeks + 1)
            ]
        if time_period_name == "month":
            num_months = (end_date.year - begin_date.year) * 12 + (
                end_date.month - begin_date.month
            )
            return [
                helpers.get_month(begin_date + relativedelta.relativedelta(months=i))
                for i in range(num_months + 1)
            ]
        if time_period_name == "year":
            num_years = end_date.year - begin_date.year
            return [
                helpers.get_year(begin_date + relativedelta.relativedelta(years=i))
                for i in range(num_years + 1)
            ]
