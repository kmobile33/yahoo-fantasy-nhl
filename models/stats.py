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

    def __count_stat_wins(self, other):
        """Gets count of categories won. Used for object comparisons."""
        self_count = other_count = 0
        for attr, value in self.__dict__.items():
            if value > getattr(other, attr):
                self_count += 1
            elif value < getattr(other, attr):
                other_count += 1

        return self_count, other_count

    def __eq__(self, other):
        for attr, value in self.__dict__.items():
            if value != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        for attr, value in self.__dict__.items():
            if value != getattr(other, attr):
                return True
        return False

    def __lt__(self, other):
        self_count, other_count = self.__count_stat_wins(other)
        return self_count < other_count

    def __le__(self, other):
        self_count, other_count = self.__count_stat_wins(other)
        return self_count <= other_count

    def __gt__(self, other):
        self_count, other_count = self.__count_stat_wins(other)
        return self_count > other_count

    def __ge__(self, other):
        self_count, other_count = self.__count_stat_wins(other)
        return self_count >= other_count

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
            'goalie_gaa' : (self.goalie_gaa or 0) + (other.goalie_gaa or 0),
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
            'goalie_gaa' : (self.goalie_gaa or 0) + other,
            'goalie_sa' : self.goalie_sa + other,
            'goalie_so' : self.goalie_so + other
        }
        return Stats(**stats)

    def __truediv__(self, other):
        stats = {
            'goals' : self.goals / other,
            'assists' : self.assists / other,
            'penalty_minutes' : self.penalty_minutes / other,
            'shots_on_goal' : self.shots_on_goal / other,
            'hits' : self.hits / other,
            'blocks' : self.blocks / other,
            'wins' : self.wins / other,
            'goalie_ga' : self.goalie_ga / other,
            'goalie_gaa' : (self.goalie_gaa or 0) / other,
            'goalie_sa' : self.goalie_sa / other,
            'goalie_so' : self.goalie_so / other
        }
        return Stats(**stats)

    def __rtruediv__(self, other):
        stats = {
            'goals' : self.goals / other,
            'assists' : self.assists / other,
            'penalty_minutes' : self.penalty_minutes / other,
            'shots_on_goal' : self.shots_on_goal / other,
            'hits' : self.hits / other,
            'blocks' : self.blocks / other,
            'wins' : self.wins / other,
            'goalie_ga' : self.goalie_ga / other,
            'goalie_gaa' : (self.goalie_gaa or 0) / other,
            'goalie_sa' : self.goalie_sa / other,
            'goalie_so' : self.goalie_so / other
        }
        return Stats(**stats)

    def __str__(self):
        return \
            "goals: " + str(self.goals) + "\r\n"\
            "assists: " + str(self.assists) + "\r\n"\
            "penalty_minutes: " + str(self.penalty_minutes) + "\r\n"\
            "shots_on_goal: " + str(self.shots_on_goal) + "\r\n"\
            "hits: " + str(self.hits) + "\r\n"\
            "blocks: " + str(self.blocks) + "\r\n"\
            "wins: " + str(self.wins) + "\r\n"\
            "goalie_ga: " + str(self.goalie_ga) + "\r\n"\
            "goalie_gaa: " + str(self.goalie_gaa) + "\r\n"\
            "goalie_sa: " + str(self.goalie_sa) + "\r\n"\
            "goalie_so: " + str(self.goalie_so) + "\r\n"

    def get_differentials(self, other):
        differentials = {
            'goals' : self.goals - other.goals,
            'assists' : self.assists - other.assists,
            'penalty_minutes' : self.penalty_minutes - other.penalty_minutes,
            'shots_on_goal' : self.shots_on_goal - other.shots_on_goal,
            'hits' : self.hits - other.hits,
            'blocks' : self.blocks - other.blocks,
            'wins' : self.wins - other.wins,
            'goalie_ga' : other.goalie_ga - self.goalie_ga,
            'goalie_gaa' : other.goalie_gaa - self.goalie_gaa,
            'goalie_sa' : self.goalie_sa - other.goalie_sa,
            'goalie_so' : self.goalie_so - other.goalie_so
        }
        return differentials

    @staticmethod
    def mean(list_of_Stats):
        return sum(list_of_Stats)/len(list_of_Stats)

    @staticmethod
    def serialize(obj):
        """JSON serializer for stats objects"""
        if isinstance(obj, Stats):
            return obj.__dict__
        else:
            raise TypeError(obj)

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

    @classmethod
    def from_xml_api_data(cls, stats_xml):
        ns = {"ns": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}

        # Get a dictionary of the stat IDs and their values
        stat_dict = {}
        for stat in stats_xml.findall('ns:stat', ns):
            stat_dict[stat.find('ns:stat_id', ns).text] = stat.find('ns:value', ns).text
        
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