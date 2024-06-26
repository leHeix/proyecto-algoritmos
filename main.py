import logging
import requests
from stadiums import StadiumManager
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    logger.info("========= Registrando datos =========")
    st = StadiumManager()