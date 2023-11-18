# FIIT STU
#   Adam Vrabeľ
#       UI - KLASTROVANIE (3C)
import copy
import random
import numpy as np
import matplotlib.pyplot as plt

################################################################################################

# X a Y súradnice budú od -5000 do +5000
MIN_VALUE = -5000
MAX_VALUE = 5000

NUM_OF_START_POINTS = 10            # NAJPRV VYGENERUJE 20 POČIATOČNÝ BODOV
# NUM_OF_ANOTHER_POINTS = 20000       # NÁSLEDNE 20000 ĎALŠÍCH BODOV
NUM_OF_ANOTHER_POINTS = 500        # NÁSLEDNE 20000 ĎALŠÍCH BODOV

# pre generate_first_points() a export_graph()
#    # je ALL_POINTS list of dictionary => "color" = farba  | "points" = body (x,y)

# pre generate_points() a print_points()
#    # je ALL_POINTS jednoducho list bodov (x, y)

# ALL_POINTS = []            # ZOZNAM VŠ BODOV

################################################################################################


# GENERUJE BODY PODĽA ZADANIA
# BOD = (x, y)
# vráti LIST BODOV
def generate_points():
    ALL_POINTS = []

    # GENEROVANIE JEDINEČNÝCH NÁHODNÝCH BODOV (20bodov)
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

    return ALL_POINTS

####


####################################
# ##  AGLOMERATIVNE, CENTROID   ## #
####################################
# vzdialenosť medzi dvoma bodmi v euklidovskej rovine
def euclidean_distance(point1, point2):
    # Konvertujte body na NumPy array
    point_1 = np.array(point1)
    point_2 = np.array(point2)

    # Výpočet euklidovskej vzdialenosti
    return np.sqrt(np.sum((point_1 - point_2) ** 2))


# vypočíta 2D maticu vzdialeností vš. bodov     # napr. mám 70 bodov, tak vypočíta 70*70=4900 vzdialeností
def euclidean_distance_matrix(points):

    # vytvorím 2D maticu, kde element (i, j) obsahuje vzdialenosť medzi bodmi i a j
    distances = np.zeros((len(points), len(points)))    # na zaciatku vsade 0

    # pre celú maticu distances vypočíta všetky vzdialenosti bodov a zapíše do matice
    for i in range(len(points)):
        for j in range(len(points)):
            distances[i, j] = euclidean_distance(points[i], points[j])
            # print(distances[i, j])

    return distances


def calculate_centroid(cluster):
    return np.mean(cluster, axis=0)


def centroid_distance(cluster1, cluster2):
    centroid1 = calculate_centroid(cluster1)
    centroid2 = calculate_centroid(cluster2)
    return euclidean_distance(centroid1, centroid2)


# ALGORITMUS PRE AGLOMERATÍVNE ZHLUKOVANIE, kde stred je centroid
def aglomerative_w_centroid(dataset, k):
    ALL_POINTS = copy.deepcopy(dataset)

    # dataset ==>  list dát
    # k       ==>  na koľko zhlukov rozdelím dataset

    # CENTROID JE FIKTÍVNY (novo/umelo vytvorený bod), ktorý je v strede vybraných bodov (ťažisko)

    # NA ZAČIATKU SA KAŽDÝ BOD POČÍTA AKO JEDEN ZHLUK (cluster)
    clusters = [[point] for point in ALL_POINTS]      # inicializácia zhlukov: každý bod == samostatný zhluk (list s jedným bodom)

    # postupné zlučovanie zhlukov (clusterov), kým nie je dosiahnutý požadovaný počet zhlukov (k)
    num_of_iteration = 0
    while len(clusters) > k:
        print(f"NUMBER OF ITERATION: {num_of_iteration}")
        num_of_iteration += 1

        # Výpočet centroidov
        centroids = [calculate_centroid(cluster) for cluster in clusters]

        # Výpočet vzdialeností medzi centroidmi
        distances = euclidean_distance_matrix(centroids)

        # Ignorujte diagonálu matice
        np.fill_diagonal(distances, np.inf)

        min_distance_index = np.unravel_index(np.argmin(distances), distances.shape)

        # Zlúči dva najbližšie zhluky
        cluster1 = clusters[min_distance_index[0]]
        cluster2 = clusters[min_distance_index[1]]
        new_cluster = cluster1 + cluster2
        clusters.pop(min_distance_index[0])
        clusters.pop(min_distance_index[1] - 1)

        clusters.append(new_cluster)

        # distances = euclidean_distance_matrix(clusters)

        # Ignorujte diagonálu matice (0 nahradím nekonečno), takže minimum mi bude správne hľadať
        # np.fill_diagonal(distances, np.inf)

        # Nájdi indexy najbližších zhlukov
        min_distance_index = np.unravel_index(np.argmin(distances), distances.shape)

        # SEM VYPOČÍTANIE VŠETKÝCH VZDIALENOSTÍ PRE VŠETKY BODY, A VYBRATIE TÝCH DVOCH BODOV S NAJMENŠIOU VZDIALENOSŤOU

        # VYPOČÍTA VŠ. VZDIALENOSTI PRE BODY
        # distance_matrix = euclidean_distance_matrix(ALL_POINTS)

        # NÁJDE NAJMENŠIU VZDIALENOSŤ 2 BODOV (okrem diagonály v matici (to je 0 a je to bod so samým sebou))

        pass
        # ######### koniec iterácie zhlukovania

    return clusters

    print("DEBUG")
    pass

####################################
# ##  END                       ## #
# ##  AGLOMERATIVNE, CENTROID   ## #
####################################


# VYGENERUJE GRAF
def print_points(dataset, filename=None):
    ALL_POINTS = copy.deepcopy(dataset)

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


def print_clusters(clusters, filename=None):
    ALL_CLUSTERS = copy.deepcopy(clusters)

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

    i = 0
    farba = ["red", "blue", "green", "pink"]
    for cluster in ALL_CLUSTERS:

        hodnoty_x = []
        hodnoty_y = []
        for x, y in cluster:
            hodnoty_x.append(x)
            hodnoty_y.append(y)

        # ZAPÍŠEM BODY DO GRAFU (rovnakej farby)
        color = farba[i]
        # plt.scatter(hodnoty_x, hodnoty_y, color="orange", s=5)
        plt.scatter(hodnoty_x, hodnoty_y, color=str(color), s=5)
        i += 1

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


################################
#       ZAČIATOK PROGRAMU      #
################################
if __name__ == '__main__':
    print("\nUI ZADANIE 3, KLASTROVANIE\n")

    # DATASET ==>  list bodov (x, y)
    DATASET = generate_points()
    # print_points(dataset=DATASET, filename="1_start_GRAPH")
    # print_points(dataset=DATASET)

    clust = aglomerative_w_centroid(dataset=DATASET, k=3)

    print_clusters(clust)
