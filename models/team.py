from datetime import datetime
import xml.etree.ElementTree as et

from models.matchup import Matchup
from models.stats import Stats

class Team:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        self.owner = kwargs.get('owner')
        self.is_my_team = kwargs.get('is_my_team')
        self.waiver_priority = kwargs.get('waiver_priority')
        self.move_count = kwargs.get('move_count')
        self.trade_count = kwargs.get('trade_count')

        self.matchups = kwargs.get('matchups') or []
        self.average_stats = kwargs.get('average_stats')

    @staticmethod
    def serialize(obj):
        """JSON serializer for team objects"""
        if isinstance(obj, Team):
            return {
                "name": obj.name,
                "id":   obj.id,
                "owner": obj.owner,
                "is_my_team": obj.is_my_team,
                "waiver_priority": obj.waiver_priority,
                "move_count": obj.move_count,
                "trade_count": obj.trade_count,
                "matchups": None if not obj.matchups else [Matchup.serialize(x) for x in obj.matchups],
                "average_stats": None if not obj.average_stats else Stats.serialize(obj.average_stats)
            }
        else:
            raise TypeError(obj)

    @classmethod
    def from_raw_api_data(cls, raw_team_info):
        team_kwargs = {
            'name' : raw_team_info['name'],
            'id' : raw_team_info['team_id'],
            'owner' : raw_team_info['managers'][0]['manager']['nickname'],
            'is_my_team' : 'is_owned_by_current_login' in raw_team_info.keys(),
            'waiver_priority' : raw_team_info['waiver_priority'],
            'move_count' : raw_team_info['number_of_moves'],
            'trade_count' : raw_team_info['number_of_trades']
        }

        return cls(**team_kwargs)

    @classmethod
    def from_api_data_with_matchups(cls, raw_team_info, raw_matchup_info):
        team_id = raw_team_info['team_id']

        # Parse matchup info using the Matchup class
        # Skip any matchups that occur past today's date
        matchups = []   
        for raw_matchup in raw_matchup_info:
            if ( datetime.strptime(raw_matchup['week_start'], "%Y-%m-%d") < datetime.now()):
                matchups.append(Matchup.from_api_data(raw_matchup, team_id))

        # Get average stats
        average_stats = Stats.mean([x.stats for x in matchups if x.is_complete])
        
        # Setup team info for __init__
        team_kwargs = {
            'name' : raw_team_info['name'],
            'id' : team_id,
            'owner' : raw_team_info['managers'][0]['manager']['nickname'],
            'is_my_team' : 'is_owned_by_current_login' in raw_team_info.keys(),
            'waiver_priority' : raw_team_info['waiver_priority'],
            'move_count' : raw_team_info['number_of_moves'],
            'trade_count' : raw_team_info['number_of_trades'],
            'matchups' : matchups,
            'average_stats' : average_stats
        }

        return cls(**team_kwargs)

    @classmethod
    def from_xml_api_data(cls, team_info_xml):
        ns = {"ns": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}

        team_id = int(team_info_xml.find('ns:team_id', ns).text)
        is_my_team = team_info_xml.find('ns:is_owned_by_current_login', ns)

        # Convert matchups if they were provided
        matchups = []
        average_stats = None
        matchup_xml = team_info_xml.find('ns:matchups', ns)
        if matchup_xml:
            matchups = [Matchup.from_xml_api_data(x, team_id) for x in matchup_xml.findall('ns:matchup', ns)]
            average_stats = Stats.mean([x.stats for x in matchups if x.is_complete])


        team_kwargs = {
            'name' : team_info_xml.find('ns:name', ns).text,
            'id' : team_id,
            'owner' : team_info_xml\
                .find('ns:managers', ns)\
                .find('ns:manager', ns)\
                .find('ns:nickname', ns).text,
            'is_my_team' : bool(is_my_team.text) if isinstance(is_my_team, et.Element) else None,
            'waiver_priority' : int(team_info_xml.find('ns:waiver_priority', ns).text),
            'move_count' : int(team_info_xml.find('ns:number_of_moves', ns).text),
            'trade_count' : int(team_info_xml.find('ns:number_of_trades', ns).text),
            'matchups' : matchups,
            'average_stats' : average_stats or None
        }

        return cls(**team_kwargs)
