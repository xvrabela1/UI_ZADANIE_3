# FIIT STU
#   Adam Vrabeľ
#       UI - KLASTROVANIE (3C)

import random
import numpy as np
import matplotlib.pyplot as plt

################################################################################################

# X a Y súradnice budú od -5000 do +5000
MIN_VALUE = -5000
MAX_VALUE = 5000

NUM_OF_START_POINTS = 20            # NAJPRV VYGENERUJE 20 POČIATOČNÝ BODOV
# NUM_OF_ANOTHER_POINTS = 20000       # NÁSLEDNE 20000 ĎALŠÍCH BODOV
NUM_OF_ANOTHER_POINTS = 2000        # NÁSLEDNE 20000 ĎALŠÍCH BODOV

# pre generate_first_points() a export_graph()
#    # je ALL_POINTS list of dictionary => "color" = farba  | "points" = body (x,y)

# pre generate_points() a print_points()
#    # je ALL_POINTS jednoducho list bodov (x, y)

ALL_POINTS = []            # ZOZNAM VŠ BODOV

################################################################################################


# GENERUJE BODY PODĽA ZADANIA
def generate_points():
    # GENEROVANIE JEDINEČNÝCH NÁHODNÝCH BODOV (20bodov)
    global ALL_POINTS

    generated_points = []  # VYGENEROVANÉ BODY (X, Y, FARBA)

    # GENERUJE JEDINEČNÉ BODY (až pokial ich nieje NUM_OF_START_POINTS dokopy)
    while len(generated_points) < NUM_OF_START_POINTS:
        # pozicia(X,Y)
        # randint(A,B)  od A do B, vrátane
        x = random.randint(MIN_VALUE, MAX_VALUE)  # od -5000 do +5000
        y = random.randint(MIN_VALUE, MAX_VALUE)  # od -5000 do +5000

        if (x, y) not in generated_points:
            generated_points.append((x, y))

    ALL_POINTS.extend(generated_points)  # PRIPOJÍ VYGENEROVANÉ BODY (teraz 20)

    # GENEROVANIE ĎALŠÍCH BODOV (20000bodov) podľa pravidiel

    while len(ALL_POINTS) < (NUM_OF_START_POINTS + NUM_OF_ANOTHER_POINTS):
        # NÁHODNE VYBERIEM BOD Z DOTERAZ VYTVORENÝCH
        choosen_point = random.choice(ALL_POINTS)

        # AK JE PRÍLIŠ BLÍZKO OKRAJU DAJ MENŠÍ OFFSET:    (vlastne ak prejde cez okraj tak ho dám na okraj)
        # VYGENERUJ náhodný X_offset (-100 do +100)
        # VYGENERUJ náhodný Y_offset (-100 do +100)

        # randint(A, B)  od A do B, vrátane
        X_offset = random.randint(-100, 100)
        Y_offset = random.randint(-100, 100)

        new_x = choosen_point[0] + X_offset
        new_y = choosen_point[1] + Y_offset

        # AK NOVÉ ČÍSLA SÚ MIMO PLOCHU:

        # NOVÉ X JE MIMO PLOCHU
        if not (-5000 <= new_x <= 5000):
            change_offset = 0
            new_X_offset = 0
            # print("CISLO X JE MIMO PLOCHU")

            # VYPOCITAM SI O KOLKO MI MÁ ZMENIT OFFSET HODNOTU, ABY SOM NEVYŠIEL MIMO MOJHO PRIESTORU
            if (choosen_point[0] + 100) > 5000:
                # print("VIE VYJST DOPRAVA")
                change_offset = choosen_point[0] + 100 - 5000                   # napr. x = 4998   ==> 4998 + 100 = 5198  | 5098 - 5000 = 98
                new_X_offset = random.randint(-100, (100 - change_offset))      # takze novy (posunutý) offset = (-100, (100-98))  => (-100, 2)

            elif (choosen_point[0] - 100) < -5000:
                # print("VIE VYJST DOLAVA")
                change_offset = 5000 + choosen_point[0] - 100  # napr. x = -4998   ==> -4998 - 100 = -5098  | 5000 + -5098 = -98  | abs(-98) = 98
                change_offset = abs(change_offset)
                new_X_offset = random.randint((-100 + change_offset), 100)

            new_x = choosen_point[0] + new_X_offset     # zmení new_x (v náhodnom rozsahu tak, aby nevyšlo mimo priestor)

        # NOVÉ Y JE MIMO PLOCHU
        if not (-5000 <= new_y <= 5000):
            change_offset = 0
            new_Y_offset = 0
            # print("CISLO Y JE MIMO PLOCHU")

            # VYPOCITAM SI O KOLKO MI MÁ ZMENIT OFFSET HODNOTU, ABY SOM NEVYŠIEL MIMO MOJHO PRIESTORU
            if (choosen_point[1] + 100) > 5000:
                # print("VIE VYJST HORE")
                change_offset = choosen_point[1] + 100 - 5000  # napr. y = 4998   ==> 4998 + 100 = 5198  | 5098 - 5000 = 98
                new_Y_offset = random.randint(-100, (100 - change_offset))  # takze novy (posunutý) offset = (-100, (100-98))  => (-100, 2)

            elif (choosen_point[1] - 100) < -5000:
                # print("VIE VYJST DOLE")
                change_offset = 5000 + choosen_point[1] - 100  # napr. y = -4998   ==> -4998 - 100 = -5098  | 5000 + -5098 = -98  | abs(-98) = 98
                change_offset = abs(change_offset)
                new_Y_offset = random.randint((-100 + change_offset), 100)

            new_y = choosen_point[1] + new_Y_offset     # zmení new_y (v náhodnom rozsahu tak, aby nevyšlo mimo priestor)

        # PRIDAJ BOD, tento bod bude v okolí zvoleného bodu (vrámci offsetu)
        #   AK NOVÝ BOD NIEJE UŽ VO VŠETKÝCH, TAK HO PRIDÁ
        if (new_x, new_y) not in ALL_POINTS:
            ALL_POINTS.append((new_x, new_y))

####


####################################
# ##  AGLOMERATIVNE, CENTROID   ## #
####################################
# vzdialenosť medzi dvoma bodmi v euklidovskej rovine
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))


# ALGORITMUS PRE AGLOMERATÍVNE ZHLUKOVANIE, kde stred je centroid
def aglomerative_w_centroid():
    # CENTROID JE FIKTÍVNY (novo/umelo vytvorený bod), ktorý je v strede vybraných bodov (ťažisko)
    number = euclidean_distance(ALL_POINTS[0][0], ALL_POINTS[0][1])
    print()
    pass

####################################
# ##  END                       ## #
# ##  AGLOMERATIVNE, CENTROID   ## #
####################################


# VYGENERUJE GRAF
def print_points(filename=None):
    # Vytvorím graf s prázdnymi osami v rozsahu od -5000 do 5000
    # plt.axis((-5000, 5000, -5000, 5000))
    plt.axis((MIN_VALUE, MAX_VALUE, MIN_VALUE, MAX_VALUE))

    # Nastavím popisky osí a titulok
    plt.xlabel('X-ová os')
    plt.ylabel('Y-ová os')
    plt.title('KLASTROVANIE  [zadanie 3C]')

    # Nastavím hodnoty osí po tisícoch
    plt.xticks(range(-5000, 5001, 1000))
    plt.yticks(range(-5000, 5001, 1000))

    # Pridám bod (0,0) s veľkosťou guličky 5
    # plt.scatter(0, 0, color='red', s=5)

    hodnoty_x = []
    hodnoty_y = []
    for x, y in ALL_POINTS:
        hodnoty_x.append(x)
        hodnoty_y.append(y)

    # ZAPÍŠEM BODY DO GRAFU (rovnakej farby)
    plt.scatter(hodnoty_x, hodnoty_y, color="orange", s=5)

    # Pridáme legendu
    # plt.legend()

    # Uloženie grafu do súboru vo formáte PNG
    if filename is not None:
        filename = str(filename)
        plt.savefig(f"export_graphs/{filename}.png")

    # Zobrazení grafu
    plt.show()


################################################################################################
################################################################################################


# VYGENERUJE BODY
def generate_first_points():
    # GENEROVANIE JEDINEČNÝCH NÁHODNÝCH BODOV
    NUM_OF_START_POINTS = 20  # POČIATOČNÝ POČET BODOV

    generated_points = []  # VYGENEROVANÉ BODY (X, Y, FARBA)

    # GENERUJE JEDINEČNÉ BODY (až pokial ich nieje NUM_OF_START_POINTS dokopy)
    while len(generated_points) < NUM_OF_START_POINTS:
        # pozicia(X,Y)
        # randint(A,B)  od A do B, vrátane
        x = random.randint(MIN_VALUE, MAX_VALUE)    # od -5000 do +5000
        y = random.randint(MIN_VALUE, MAX_VALUE)    # od -5000 do +5000

        if (x, y) not in generated_points:
            generated_points.append((x, y))

    # DICTIONARY SKUPINY BODOV (momentálne prvých 20)
    skupina_bodov = {
        'color': "red",
        'points': generated_points,
    }
    ALL_POINTS.append(skupina_bodov)  # PRIPOJÍ VYGENEROVANÉ BODY

    # END GENEROVANIE JEDINEČNÝCH NÁHODNÝCH BODOV ##########################################


# VYKRESLÍ GRAF
def export_graph():

    # Vytvorím graf s prázdnymi osami v rozsahu od -5000 do 5000
    # plt.axis((-5000, 5000, -5000, 5000))
    plt.axis((MIN_VALUE, MAX_VALUE, MIN_VALUE, MAX_VALUE))

    # Nastavím popisky osí a titulok
    plt.xlabel('X-ová os')
    plt.ylabel('Y-ová os')
    plt.title('Graf bodov od -5000 do 5000')

    # Nastavím hodnoty osí po tisícoch
    plt.xticks(range(-5000, 5001, 1000))
    plt.yticks(range(-5000, 5001, 1000))

    # Pridám bod (0,0) s veľkosťou guličky 5
    # plt.scatter(0, 0, color='red', s=5)

    for group_of_points in ALL_POINTS:
        # KAŽDÁ group_of_points JE POLE BODOV, S JEDNOU FARBOU
        hodnoty_x = []
        hodnoty_y = []
        hodnota_farba = group_of_points["color"]

        for x, y in group_of_points["points"]:
            hodnoty_x.append(x)
            hodnoty_y.append(y)

        # V KAŽDEJ ITERÁCII ZAPÍŠEM BODY DO GRAFU (rovnakej farby)
        plt.scatter(hodnoty_x, hodnoty_y, color=hodnota_farba, s=5)

    # Pridáme legendu
    # plt.legend()

    # Uloženie grafu do súboru vo formáte PNG
    # plt.savefig('export_graphs/graf.png')

    # Zobrazení grafu
    plt.show()


################################
#       ZAČIATOK PROGRAMU      #
################################
if __name__ == '__main__':
    print("\nUI ZADANIE 3, KLASTROVANIE\n")

    # TOTO NEPOUŽÍVAM
    # generate_first_points()
    # export_graph()

    generate_points()
    # print_points("1_start_GRAPH")

    aglomerative_w_centroid()
