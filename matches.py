from teams import Team, TeamManager
from stadiums import Stadium, StadiumManager
import requests
import logging
from uuid import uuid4
logger = logging.getLogger(__name__)

class Match:
    __id: str
    __number: int
    __home: Team
    __away: Team
    __date: str
    __group: str
    __stadium: Stadium
    __tickets_sold: dict

    def __init__(self, id: str, number: int, home: Team, away: Team, date: str, group: str, stadium: Stadium):
        self.__id = id
        self.__number = number
        self.__home = home
        self.__away = away
        self.__date = date
        self.__group = group
        self.__stadium = stadium
        self.__tickets_sold = {}

    def get_id(self) -> str:
        return self.__id
    
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
    
    def is_seat_occupied(self, seat: int) -> bool:
        return seat in self.__tickets_sold and self.__tickets_sold[seat]
    
    def occupy_seat(self, seat: int, customer_id: int) -> str:
        ticket_id = str(uuid4())
        self.__tickets_sold[seat] = { "occupied": True, "ticket_id": ticket_id, "ticket_used": False, "customer_id": customer_id, "ticket_is_vip": seat > self.__stadium.get_capacity()[0] }
        return ticket_id
    
    def ticket_is_used(self, ticket_id: str) -> bool:
        for v in dict.values(self.__tickets_sold):
            if v["ticket_id"] == ticket_id:
                return v["ticket_used"]
            
        return False
    
    def mark_ticket_as_used(self, ticket_id: str):
        for v in dict.values(self.__tickets_sold):
            if v["ticket_id"] == ticket_id:
                v["ticket_used"] = True
                break
    
    def ticket_exists(self, ticket_id: str) -> bool:
        for v in dict.values(self.__tickets_sold):
            if v["ticket_id"] == ticket_id:
                return True
            
        return False
    
    def get_ticket_info(self, ticket_id: str) -> tuple[int, bool, int, bool] | None:
        for k, v in dict.items(self.__tickets_sold):
            if v["ticket_id"] == ticket_id:
                return (k, v["ticket_used"], v["customer_id"], v["ticket_is_vip"])
            
        return None
    
    def is_sold_out(self) -> bool:
        return len(self.__tickets_sold) == self.__stadium.get_max_capacity()
    
    def get_free_seats(self, vip: bool) -> list[int]:
        seats = []

        for i in range(1 if not vip else self.__stadium.get_capacity()[0] + 1, self.__stadium.get_capacity()[0] + 1 if not vip else self.__stadium.get_max_capacity() + 1):
            if i not in self.__tickets_sold:
                seats.append(i)

        return seats
    
    def get_assistance_count(self) -> int:
        sum = 0
        for v in dict.values(self.__tickets_sold):
            if v["ticket_used"]:
                sum += 1

        return sum
    
    def get_sold_ticket_count(self) -> int:
        return len(self.__tickets_sold)
    
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

    def get_matches(self) -> list[Match]:
        return self.__matches
    
    def find_matches_by_country(self, country: str) -> list[Match]:
        country_lower = country.lower()

        matches = []
        for m in self.__matches:
            if m.get_home_team().get_country().lower() == country_lower or m.get_away_team().get_country().lower() == country_lower:
                matches.append(m)

        return matches
    
    def find_matches_by_country_code(self, cc: str) -> list[Match]:
        cc_lower = cc.lower()

        matches = []
        for m in self.__matches:
            if m.get_home_team().get_country_code().lower() == cc_lower or m.get_away_team().get_country_code().lower() == cc_lower:
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
    
    def find_matches_by_date(self, date: str) -> list[Match]:
        matches = []
        for m in self.__matches:
            if m.get_date() == date:
                matches.append(m)

        return matches
    
    def find_match_by_id(self, id: str) -> Match | None:
        for m in self.__matches:
            if m.get_id() == id:
                return m
            
        return None