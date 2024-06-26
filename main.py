import logging
import os
from stadiums import StadiumManager
from teams import TeamManager
from matches import Match, MatchManager
logger = logging.getLogger(__name__)

def clear_screen():
    print("\n"*10)
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    logger.info("|-- Registrando datos --|")
    stadiums = StadiumManager()
    teams = TeamManager()
    matches = MatchManager(stadiums, teams)

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
                    print("| Ctrl + C - Salir")
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
                            current_menu = 1
                        case 2:
                            current_menu = 2

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
                            current_menu = 0
                            continue
                        case 2:
                            opt_str = input("| Introduzca el código del país => ")
                            match_list = matches.find_matches_by_country_code(opt_str)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos de {opt_str} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                            current_menu = 0
                            continue
                        case 3:
                            opt_str = input("| Introduzca el ID del equipo => ")
                            match_list = matches.find_matches_by_country_id(opt_str)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos de {opt_str} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                            current_menu = 0
                            continue
                        case 4:
                            current_menu = 0
                            continue

                case 2:
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
                                continue

                            match_list = matches.find_matches_by_stadium(stadium)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos en {stadium.get_name()} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                            current_menu = 0
                            continue
                        case 2:
                            opt_str = input("| Introduzca la ID del estadio => ")
                            stadium = stadiums.find_stadium_by_id(opt_str)
                            if stadium == None:
                                input("| -> Estadio desconocido, presiona ENTER para volver al menú.")
                                continue

                            match_list = matches.find_matches_by_stadium(stadium)
                            clear_screen()
                            print(f"| --------- Euro 2024 / Partidos en {stadium.get_name()} --------- |")
                            show_matches(match_list)
                            input("| -> Presiona ENTER para volver al menú.")
                            current_menu = 0
                            continue
                        case 3:
                            current_menu = 0
                            continue
    except KeyboardInterrupt:
        print("chau")