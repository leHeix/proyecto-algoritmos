"""
                                        EURO 2024
    I lost motivation doing this halfway through so the code gets a bit uglier at some parts
    It works, though.
"""

import logging
import os
import re
import itertools as it
from stadiums import StadiumManager
from teams import TeamManager
from matches import Match, MatchManager
logger = logging.getLogger(__name__)

def clear_screen():
    print("\n" * 10)
    os.system("cls" if os.name == "nt" else "clear")

def show_matches(matches: list[Match]):
    if len(matches) == 0:
        print("| - No se encontraron partidos.")
    else:
        for m in matches:
            print(f"| {m.get_home_team().get_country()} - {m.get_away_team().get_country()}")
            print(f"| - Fecha: {m.get_date()}")
            print(f"| - Grupo: {m.get_group()}")
            print(f"| - Estadio: {m.get_stadium().get_name()} (ID: {m.get_stadium().get_id()})")
            print(f"| - ID: {m.get_id()}")

# Vampire number checker
# Took this from https://stackoverflow.com/a/39434945
def get_fangs(num_str):
    num_iter = it.permutations(num_str, len(num_str))
    for num_list in num_iter:
        v = ''.join(num_list)
        x, y = v[:int(len(v)/2)], v[int(len(v)/2):]
        if x[-1] == '0' and y[-1] == '0':
            continue
        if int(x) * int(y) == int(num_str):
            return x,y
    return False

def is_vampire(m_int):
    n_str = str(m_int)
    if len(n_str) % 2 == 1:
        return False
    fangs = get_fangs(n_str)
    if not fangs:
        return False
    return True
##

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    logger.info("|-- Registrando datos --|")
    stadiums = StadiumManager()
    teams = TeamManager()
    matches = MatchManager(stadiums, teams)

    """
                MENÚS:
        0 - Principal
        1 - Búsqueda de partidos por país
        2 - Búsqueda de partidos por estadio
        3 - Búsqueda de partidos por fecha
        4 - Comprar entrada
        5 - Registrar asistencia a partido
        6 - Comprobar código de entrada
    """
    current_menu = 0

    try:
        while True:
            clear_screen()

            match current_menu:
                case 0: # Menú principal
                    print("| --------- Euro 2024 --------- |")
                    print("| (1) - Buscar partidos por país")
                    print("| (2) - Buscar partidos por estadio")
                    print("| (3) - Buscar partidos por fecha")
                    print("| (4) - Comprar entrada")
                    print("| (5) - Registrar asistencia a partido")
                    print("| (6) - Comprobar código de entrada")
                    print("| Ctrl + C - Salir")
                    opt_str = input("| => ")
                    option = None

                    try:
                        option = int(opt_str)
                        if option < 1 or option > 6:
                            raise ValueError
                    except ValueError:
                        input("| -> Opción inválida, presiona ENTER para volver al menú.")
                        continue

                    current_menu = option

                case 1: # Buscar partidos por país
                    print("| --------- Euro 2024 / Búsqueda de partidos por país --------- |")
                    print("| (1) - Buscar por país")
                    print("| (2) - Buscar por código de país")
                    print("| (3) - Buscar por ID del equipo")
                    print("| (4) - Volver al menú principal")
                    opt_str = input("| => ")
                    option = None

                    try:
                        option = int(opt_str)
                        if option < 1 or option > 4:
                            raise ValueError
                    except ValueError:
                        input("| -> Opción inválida, presiona ENTER para volver al menú.")
                        continue

                    match option:
                        case 1:
                            opt_str = input("| Introduzca el país => ")
                            match_list = matches.find_matches_by_country(opt_str)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos de {opt_str} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                        case 2:
                            opt_str = input("| Introduzca el código del país => ")
                            match_list = matches.find_matches_by_country_code(opt_str)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos de {opt_str} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                        case 3:
                            opt_str = input("| Introduzca el ID del equipo => ")
                            match_list = matches.find_matches_by_country_id(opt_str)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos de {opt_str} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                        case 4:
                            pass

                    current_menu = 0
                    continue

                case 2: # Buscar partidos por estadio
                    print("| --------- Euro 2024 / Búsqueda de partidos por estadio --------- |")
                    print("| (1) - Buscar por nombre del estadio")
                    print("| (2) - Buscar por ID del estadio")
                    print("| (3) - Volver al menú principal")
                    opt_str = input("| => ")
                    option = None

                    try:
                        option = int(opt_str)
                        if option < 1 or option > 3:
                            raise ValueError
                    except ValueError:
                        input("| -> Opción inválida, presiona ENTER para volver al menú.")
                        continue

                    match option:
                        case 1:
                            opt_str = input("| Introduzca el nombre del estadio => ")
                            stadium = stadiums.find_stadium_by_name(opt_str)
                            if stadium == None:
                                input("| -> Estadio desconocido, presiona ENTER para volver al menú.")
                                current_menu = 2
                                continue

                            match_list = matches.find_matches_by_stadium(stadium)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos en {stadium.get_name()} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                        case 2:
                            opt_str = input("| Introduzca la ID del estadio => ")
                            stadium = stadiums.find_stadium_by_id(opt_str)
                            if stadium == None:
                                input("| -> Estadio desconocido, presiona ENTER para volver al menú.")
                                current_menu = 2
                                continue

                            match_list = matches.find_matches_by_stadium(stadium)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos en {stadium.get_name()} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                        case 3:
                            pass

                    current_menu = 0
                    continue

                case 3: # Buscar partidos por fecha
                    print("| --------- Euro 2024 / Búsqueda de partidos por fecha --------- |")
                    opt_str = input("| Introduzca la fecha del partido (YYYY-MM-DD) => ")
                    if not re.match(r"^[\d]{4}-[\d]{2}-[\d]{2}$", opt_str):
                        input("| -> Fecha inválida, presiona ENTER para volver al menú.")
                        current_menu = 0
                        continue

                    match_list = matches.find_matches_by_date(opt_str)
                    clear_screen()
                    print(f"| --------- Euro 2024 / Partidos el {opt_str} --------- |")
                    show_matches(match_list)
                    input("| -> Presiona ENTER para volver al menú.")
                    current_menu = 0
                    continue

                case 4: # Comprar entrada
                    print("| --------- Euro 2024 / Comprar entrada --------- |")
                    customer_name = input("| Introduzca su nombre (o SALIR para volver al menú principal) => ")
                    if customer_name == "SALIR":
                        current_menu = 0
                        continue

                    customer_id = input("| Introduzca su cédula => ")
                    customer_age = input("| Introduzca su edad => ")
                    customer_match_id = input("| Introduzca la ID del partido => ")
                    customer_match = matches.find_match_by_id(customer_match_id)
                    if customer_match == None:
                        input("| -> Partido inválido, presiona ENTER para volver al menú.")
                        continue

                    if customer_match.is_sold_out():
                        input("| -> Este partido esta sold out, presiona ENTER para volver al menú.")
                        continue

                    customer_ticket_type = input("| Tipo de entrada (VIP/General) => ").lower()
                    if customer_ticket_type != "vip" and customer_ticket_type != "general":
                        input("| -> Tipo de entrada inválido, presiona ENTER para volver al menú.")
                        continue

                    print(f"| Asientos libres: {customer_match.get_free_seats(customer_ticket_type == "vip")}")

                    customer_seat_assigned = False
                    while not customer_seat_assigned:
                        try:
                            customer_seat = int(input(f"| Introduzca el número de asiento ({1 if customer_ticket_type == "general" else customer_match.get_stadium().get_capacity()[0] + 1}-{customer_match.get_stadium().get_capacity()[0] if customer_ticket_type == "general" else customer_match.get_stadium().get_max_capacity()}) => "))

                            if customer_match.is_seat_occupied(customer_seat):
                                print("| -> Ese asiento ya está ocupado.")
                                continue

                            customer_seat_assigned = True
                        except ValueError:
                            print("| -> Asiento inválido.")
                    
                    print("| --------------------------")

                    ticket_price = 75 if customer_ticket_type == "vip" else 35
                    print(f"| Precio de la entrada: {ticket_price}$")
                    if is_vampire(customer_id):
                        ticket_price -= (50 * ticket_price) / 100
                        print("| Su entrada tiene 50% de descuento porque su cédula es un número vampiro.")
                        print(f"| Precio con descuento: {ticket_price}$")

                    iva = (16 * ticket_price) / 100
                    print(f"| IVA 16%: {iva}$")
                    ticket_price += iva
                    print(f"| Precio final: {ticket_price}")
                    print(f"| Asiento seleccionado: {customer_seat}")
                    confirmation_str = input("| Introduzca CONFIRMAR para confirmar la compra de su entrada => ")
                    if confirmation_str == "CONFIRMAR":
                        ticket_id = customer_match.occupy_seat(customer_seat, customer_id)
                        print("| Pago éxitoso. Su compra fue registrada.")
                        print(f"| Su código de entrada es {ticket_id}.")
                        input("| -> Presiona ENTER para volver al menú.")
                    else:
                        input("| Compra cancelada. Presiona ENTER para volver al menú.")
                    
                    current_menu = 0
                    continue
                
                case 5: # Registrar asistencia a partido
                    print("| --------- Euro 2024 / Registrar asistencia --------- |")
                    customer_match_id = input("| Introduzca la ID del partido => ")
                    customer_match = matches.find_match_by_id(customer_match_id)
                    if customer_match == None:
                        input("| -> Partido inválido, presiona ENTER para volver al menú.")
                        current_menu = 0
                        continue

                    customer_ticket_id = input("| Introduzca el código de entrada => ")
                    if not customer_match.ticket_exists(customer_ticket_id):
                        input("| -> El código de entrada no existe, presiona ENTER para volver al menú")
                        current_menu = 0
                        continue

                    if customer_match.ticket_is_used(customer_ticket_id):
                        input("| -> El código de entrada ya fue utilizado, presiona ENTER para volver al menú")
                        current_menu = 0
                        continue

                    customer_match.mark_ticket_as_used(customer_ticket_id)
                    input("| -> Asistencia registrada, presiona ENTER para volver al menú.")
                    current_menu = 0
                    continue

                case 6: # Comprobar código de entrada
                    print("| --------- Euro 2024 / Registrar asistencia --------- |")
                    customer_match_id = input("| Introduzca la ID del partido => ")
                    customer_match = matches.find_match_by_id(customer_match_id)
                    if customer_match == None:
                        input("| -> Partido inválido, presiona ENTER para volver al menú.")
                        current_menu = 0
                        continue

                    customer_ticket_id = input("| Introduzca el código de entrada => ")
                    if not customer_match.ticket_exists(customer_ticket_id):
                        input("| -> El código de entrada no existe, presiona ENTER para volver al menú")
                        current_menu = 0
                        continue

                    [seat, used] = customer_match.get_ticket_info(customer_ticket_id)
                    print(f"| -> Este código corresponde al asiento {seat}. {"Ya fue utilizado para entrar." if used else "Aún no ha sido utilizado."}")
                    input("| -> Presiona ENTER para volver al menú.")
                    current_menu = 0

    except KeyboardInterrupt:
        print("SALIR")