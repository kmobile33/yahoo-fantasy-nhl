from utilities import utilities

class Stats():
    def __init__(self, **kwargs):
        self.goals = kwargs.get('goals')
        self.assists = kwargs.get('assists')
        self.penalty_minutes = kwargs.get('penalty_minutes')
        self.shots_on_goal = kwargs.get('shots_on_goal')
        self.hits = kwargs.get('hits')
        self.blocks = kwargs.get('blocks')
        self.wins = kwargs.get('wins')
        self.goalie_ga = kwargs.get('goalie_ga')
        self.goalie_gaa = kwargs.get('goalie_gaa')
        self.goalie_sa = kwargs.get('goalie_sa')
        self.goalie_so = kwargs.get('goalie_so')

    def __add__(self, other):
        """Overload of the add operator. GAA produces averages."""
        stats = {
            'goals' : self.goals + other.goals,
            'assists' : self.assists + other.assists,
            'penalty_minutes' : self.penalty_minutes + other.penalty_minutes,
            'shots_on_goal' : self.shots_on_goal + other.shots_on_goal,
            'hits' : self.hits + other.hits,
            'blocks' : self.blocks + other.blocks,
            'wins' : self.wins + other.wins,
            'goalie_ga' : self.goalie_ga + other.goalie_ga,
            'goalie_gaa' : 0.5*(self.goalie_gaa or 0) + 0.5*(other.goalie_gaa or 0),
            'goalie_sa' : self.goalie_sa + other.goalie_sa,
            'goalie_so' : self.goalie_so + other.goalie_so
        }
        return Stats(**stats)

    def __radd__(self, other):
        """Overload of the add operator. GAA produces averages."""
        stats = {
            'goals' : self.goals + other,
            'assists' : self.assists + other,
            'penalty_minutes' : self.penalty_minutes + other,
            'shots_on_goal' : self.shots_on_goal + other,
            'hits' : self.hits + other,
            'blocks' : self.blocks + other,
            'wins' : self.wins + other,
            'goalie_ga' : self.goalie_ga + other,
            'goalie_gaa' : 0.5*(self.goalie_gaa or 0) + 0.5*other,
            'goalie_sa' : self.goalie_sa + other,
            'goalie_so' : self.goalie_so + other
        }
        return Stats(**stats)

    @staticmethod
    def mean(list_of_Stats):
        return sum(list_of_Stats)/len(list_of_Stats)

    @classmethod
    def from_api_data(cls, raw_stat_info):
        # Flatten out the stat dict so its just {stat_id: value} rather than nested crap
        stat_dict = {}
        [ stat_dict.update( { stat_pair['stat']['stat_id']: stat_pair['stat']['value'] } ) for stat_pair in raw_stat_info ]
        
        stat_kwargs = {
            'goals' : utilities.safe_cast(stat_dict['1'], int),
            'assists' : utilities.safe_cast(stat_dict['2'], int),
            'penalty_minutes' : utilities.safe_cast(stat_dict['5'], int),
            'shots_on_goal' : utilities.safe_cast(stat_dict['14'], int),
            'hits' : utilities.safe_cast(stat_dict['31'], int),
            'blocks' : utilities.safe_cast(stat_dict['32'], int),
            'wins' : utilities.safe_cast(stat_dict['19'], int),
            'goalie_ga' : utilities.safe_cast(stat_dict['22'], int),
            'goalie_gaa' : utilities.safe_cast(stat_dict['23'], float),
            'goalie_sa' : utilities.safe_cast(stat_dict['24'], int),
            'goalie_so' : utilities.safe_cast(stat_dict['27'], int)
        }
        
        return cls(**stat_kwargs)

