class Stats():
    def __init__(self, raw_stat_info):
        # Flatten out the stat dict so its just {stat_id: value} rather than nested crap
        stat_dict = {}
        [ stat_dict.update( { stat_pair['stat']['stat_id']: stat_pair['stat']['value'] } ) for stat_pair in raw_stat_info ]

        self.goals = self.__safe_cast(stat_dict['1'], int)
        self.assists = self.__safe_cast(stat_dict['2'], int)
        self.penalty_minutes = self.__safe_cast(stat_dict['5'], int)
        self.shots_on_goal = self.__safe_cast(stat_dict['14'], int)
        self.hits = self.__safe_cast(stat_dict['31'], int)
        self.blocks = self.__safe_cast(stat_dict['32'], int)
        self.wins = self.__safe_cast(stat_dict['19'], int)
        self.goalie_ga = self.__safe_cast(stat_dict['22'], int)
        self.goalie_gaa = self.__safe_cast(stat_dict['23'], float)
        self.goalie_sa = self.__safe_cast(stat_dict['24'], int)
        self.goalie_so = self.__safe_cast(stat_dict['27'], int)

    def __safe_cast(self, val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default
