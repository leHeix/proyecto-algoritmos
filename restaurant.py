class Product:
    __name: str
    __amount: int
    __price: float
    __stock: int
    __type: str
    __sales: int

    def __init__(self, name: str, amount: int, price: float, stock: int, type: str):
        self.__name = name
        self.__amount = amount
        self.__price = price
        self.__stock = stock
        self.__type = type
        self.__sales = 0

    def get_name(self) -> str:
        return self.__name
    
    def get_amount(self) -> int:
        return self.__amount
    
    def get_price(self) -> float:
        return self.__price
    
    def get_stock(self) -> int:
        return self.__stock
    
    def get_type(self) -> str:
        return self.__type
    
    def mark_sale(self):
        self.__stock -= 1
        self.__amount += 1
        self.__sales += 1

class Restaurant:
    __name: str = ""
    __products: list[Product]

    def __init__(self, name: str):
        self.__name = name
        self.__products = []

    def get_name(self) -> str:
        return self.__name
    
    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def get_products(self) -> list[Product]:
        return self.__products