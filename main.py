import logging
import requests
from stadiums import StadiumManager
from teams import TeamManager
from matches import MatchManager
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    logger.info("========= Registrando datos =========")
    stadiums = StadiumManager()
    teams = TeamManager()
    matches = MatchManager(stadiums, teams)
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("chau")