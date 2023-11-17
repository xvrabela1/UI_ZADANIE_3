# FIIT STU
#   Adam Vrabeľ
#       UI - KLASTROVANIE (3C)

import random
import matplotlib.pyplot as plt

################################################################################################

# X a Y súradnice budú od -5000 do +5000
MIN_VALUE = -5000
MAX_VALUE = 5000

# ALL POINTS a list => "color" = farba  | "points" = body (x,y)
ALL_POINTS = []            # ZOZNAM VŠ BODOV

################################################################################################


# VYGENERUJE BODY
def generate_first_points():
    # Generovanie prvých 20 náhodných bodov
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

    #############################################################
    # DICTIONARY JEDNEJ SÚRADNICE
    skupina_bodov = {
        'color': "red",
        'points': generated_points,
    }
    ALL_POINTS.append(skupina_bodov)  # PRIPOJÍ VYGENEROVANÉ BODY


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

    # Zobrazení grafu
    plt.show()


################################
#       ZAČIATOK PROGRAMU      #
################################
if __name__ == '__main__':
    print("\nUI ZADANIE 3, KLASTROVANIE\n")

    generate_first_points()

    export_graph()

