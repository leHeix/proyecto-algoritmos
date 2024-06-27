import requests
from restaurant import Restaurant, Product
import logging
logger = logging.getLogger(__name__)

class Stadium:
    __id: str
    __name: str
    __city: str
    __capacity: tuple[int, int] = (0, 0)
    __restaurants: list[Restaurant]

    def __init__(self, id: str, name: str, city: str, capacity_general: int, capacity_vip: int):
        self.__id = id
        self.__name = name
        self.__city = city
        self.__capacity = (capacity_general, capacity_vip)
        self.__restaurants = []

    def add_restaurant(self, data: list):
        restaurant = Restaurant(data["name"])
        for v in data["products"]:
            product = Product(v["name"], v["quantity"], float(v["price"]), v["stock"], v["adicional"])
            restaurant.add_product(product)

        logger.debug(f"Restaurante registrado: {restaurant.get_name()}")
        self.__restaurants.append(restaurant)

    def get_id(self) -> str:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name
    
    def get_city(self) -> str:
        return self.__city
    
    def get_capacity(self) -> tuple[int, int]:
        return self.__capacity
    
    def get_max_capacity(self) -> int:
        return self.__capacity[0] + self.__capacity[1]
    
    def get_restaurants(self) -> list[Restaurant]:
        return self.__restaurants
    
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
            
            self.__stadiums.append(stadium)

        logger.info("Información sobre estadios registrada.")

    def find_stadium_by_id(self, id: str) -> Stadium | None:
        for s in self.__stadiums:
            if s.get_id() == id:
                return s
            
        return None
    
    def find_stadium_by_name(self, name: str) -> Stadium | None:
        name_lower = name.lower() # micro optimization

        for s in self.__stadiums:
            if s.get_name().lower() == name_lower:
                return s
            
        return None