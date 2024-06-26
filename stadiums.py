import requests
from restaurant import Restaurant, Product
import logging
logger = logging.getLogger(__name__)

class Stadium:
    __id: str
    __name: str
    __city: str
    __capacity: tuple[int, int] = (0, 0)
    __restaurants: list[Restaurant] = []

    def __init__(self, id: str, name: str, city: str, capacity_general: int, capacity_vip: int):
        self.__id = id
        self.__name = name
        self.__city = city
        self.__capacity = (capacity_general, capacity_vip)
        
    def add_restaurant(self, data: list):
        restaurant = Restaurant(data["name"])
        for v in data["products"]:
            product = Product(v["name"], v["quantity"], float(v["price"]), v["stock"], v["adicional"])
            restaurant.add_product(product)

        self.__restaurants.append(restaurant)

    def get_name(self) -> str:
        return self.__name
    
class StadiumManager:
    __stadiums: list[Stadium] = []

    def __init__(self):
        response = None
        data = []
        
        try:
            response = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
            data = response.json()
        except requests.exceptions.RequestException:
            logger.error("Ocurrio un error al buscar los datos de los estadios.")
            exit(1)

        for v in data:
            stadium = Stadium(v["id"], v["name"], v["city"], v["capacity"][0], v["capacity"][1])
            logger.debug(f"Estadio registrado: {stadium.get_name()}")

            for r in v["restaurants"]:
                stadium.add_restaurant(r)