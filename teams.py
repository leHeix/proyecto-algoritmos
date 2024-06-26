import requests
import logging
logger = logging.getLogger(__name__)

class Team:
    __id: str
    __code: str
    __country: str
    __group: str

    def __init__(self, id: str, code: str, country: str, group: str):
        self.__id = id
        self.__code = code
        self.__country = country
        self.__code = code

    def get_id(self) -> str:
        return self.__id
    
    def get_country(self) -> str:
        return self.__country
    
class TeamManager:
    __teams: list[Team] = []

    def __init__(self):
        response = None
        data = []
        
        try:
            response = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json")
            data = response.json()
        except requests.exceptions.RequestException:
            logger.error("Ocurrio un error al buscar los datos de los equipos.")
            exit(1)

        for v in data:
            team = Team(v["id"], v["code"], v["name"], v["group"])
            logger.debug(f"Equipo registrado: {team.get_country()}")
            self.__teams.append(team)

        logger.info("Información sobre equipos registrada.")

    def find_team_by_id(self, id: str) -> Team | None:
        for t in self.__teams:
            if t.get_id() == id:
                return t
            
        return None