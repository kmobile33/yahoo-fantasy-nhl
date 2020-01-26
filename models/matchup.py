from datetime import datetime

from models.stats import Stats

class Matchup():
    def __init__(self, **kwargs):
        self.week = kwargs.get('week')
        self.week_start = kwargs.get('week_start')
        self.week_end = kwargs.get('week_end')
        self.has_started = kwargs.get('has_started')
        self.is_complete = kwargs.get('is_complete')
        self.is_tied = kwargs.get('is_tied')
        self.won = kwargs.get('won')
        self.stats = kwargs.get('stats')

    @staticmethod
    def serialize(obj):
        """JSON serializer for matchup objects"""
        if isinstance(obj, Matchup):
            return {
                "week": obj.week,
                "week_start": str(obj.week_start),
                "week_end": str(obj.week_end),
                "has_started": obj.has_started,
                "is_complete": obj.is_complete,
                "is_tied": obj.is_tied,
                "won": obj.won,
                "stats": Stats.serialize(obj.stats)
            }
        else:
            raise TypeError(obj)

    @classmethod
    def from_api_data(cls, raw_matchup_info, team_id):
        now = datetime.now()
        week_start = datetime.strptime(raw_matchup_info['week_start'], "%Y-%m-%d")
        week_end = datetime.strptime(raw_matchup_info['week_end'], "%Y-%m-%d")
        has_started = (week_start < now)
        is_complete = (week_end < now)
        is_tied = None if not is_complete else bool(raw_matchup_info['is_tied'])
        
        matchup_kwargs = {
            'week' : raw_matchup_info['week'],
            'week_start' : week_start,
            'week_end' : week_end,
            'has_started' : has_started,
            'is_complete' : is_complete,
            'is_tied' : is_tied,
            'won' : None if (not is_complete or is_tied)\
                else bool(raw_matchup_info['winner_team_key'][(raw_matchup_info['winner_team_key'].rfind(".") + 1):] == team_id),
            'stats' : None if not has_started else Stats.from_api_data(raw_matchup_info['stats'])
        }

        return cls(**matchup_kwargs)

    @classmethod
    def from_xml_api_data(cls, matchup_xml, team_id):
        ns = {"ns": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}

        now = datetime.now()
        week_start = datetime.strptime(matchup_xml.find('ns:week_start', ns).text, "%Y-%m-%d")
        week_end = datetime.strptime(matchup_xml.find('ns:week_end', ns).text, "%Y-%m-%d")
        has_started = (week_start < now)
        is_complete = (week_end < now)
        is_tied = None if not is_complete else bool(matchup_xml.find('ns:is_tied', ns).text)
        winner_team_key = matchup_xml.find('ns:winner_team_key', ns)

        # Get stats
        teams = matchup_xml.find('ns:teams', ns).findall('ns:team', ns)
        team = [x for x in teams if int(x.find('ns:team_id', ns).text) == team_id][0]
        stats = team\
            .find('ns:team_stats', ns)\
            .find('ns:stats', ns)\
        
        matchup_kwargs = {
            'week' : int(matchup_xml.find('ns:week', ns).text),
            'week_start' : week_start,
            'week_end' : week_end,
            'has_started' : has_started,
            'is_complete' : is_complete,
            'is_tied' : is_tied,
            'won' : None if (not is_complete or is_tied)\
                else bool(winner_team_key.text[(winner_team_key.text.rfind(".") + 1):] == team_id),
            'stats' : None if not has_started else Stats.from_xml_api_data(stats)
        }

        return cls(**matchup_kwargs)
