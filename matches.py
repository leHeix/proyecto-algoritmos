from teams import Team, TeamManager
from stadiums import Stadium, StadiumManager
import requests
import logging
logger = logging.getLogger(__name__)

class Match:
    __id: str
    __number: int
    __home = Team
    __away = Team
    __date: str
    __group: str
    __stadium: Stadium

    def __init__(self, id: str, number: int, home: Team, away: Team, date: str, group: str, stadium: Stadium):
        self.__id = id
        self.__number = number
        self.__home = home
        self.__away = away
        self.__date = date
        self.__group = group
        self.__stadium = stadium

    def get_home_team(self) -> Team:
        return self.__home
    
    def get_away_team(self) -> Team:
        return self.__away
    
    def get_group(self) -> str:
        return self.__group
    
    def get_date(self) -> str:
        return self.__date
    
    def get_stadium(self) -> Stadium:
        return self.__stadium
    
class MatchManager:
    __matches: list[Match] = []

    def __init__(self, sm: StadiumManager, tm: TeamManager):
        response = None
        data = []
        
        try:
            response = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json")
            data = response.json()
        except requests.exceptions.RequestException:
            logger.error("Ocurrio un error al buscar los datos de los partidos.")
            exit(1)

        for v in data:
            match_home_team = tm.find_team_by_id(v["home"]["id"])
            if match_home_team ==  None:
                logger.error(f"Equipo desconocido: {v["home"]["name"]} (ID {v["home"]["id"]})")
                continue

            match_away_team = tm.find_team_by_id(v["away"]["id"])
            if match_away_team ==  None:
                logger.error(f"Equipo desconocido: {v["away"]["name"]} (ID {v["away"]["id"]})")
                continue

            match_stadium = sm.find_stadium_by_id(v["stadium_id"])
            if match_stadium == None:
                logger.error(f"Estadio desconocido: {v["stadium_id"]}")
                continue

            match = Match(v["id"], v["number"], match_home_team, match_away_team, v["date"], v["group"], match_stadium)
            self.__matches.append(match)

            logger.debug(f"Partido registrado: {match.get_home_team().get_country()} - {match.get_away_team().get_country()} ({match.get_group()}, {match.get_date()}, estadio {match.get_stadium().get_name()})")

        logger.info("Información sobre partidos registrada.")

    def find_matches_by_country(self, country: str) -> list[Match]:
        matches = []
        for m in self.__matches:
            if m.get_home_team().get_country() == country or m.get_away_team().get_country() == country:
                matches.append(m)

        return matches
    
    def find_matches_by_country_code(self, cc: str) -> list[Match]:
        matches = []
        for m in self.__matches:
            if m.get_home_team().get_country_code() == cc or m.get_away_team().get_country_code() == cc:
                matches.append(m)

        return matches
    
    def find_matches_by_team_id(self, id: str) -> list[Match]:
        matches = []
        for m in self.__matches:
            if m.get_home_team().get_id() == id or m.get_away_team().get_id() == id:
                matches.append(m)

        return matches
    
    def find_matches_by_stadium(self, stadium: Stadium) -> list[Match]:
        matches = []
        for m in self.__matches:
            if m.get_stadium() == stadium:
                matches.append(m)

        return matches