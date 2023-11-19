# FIIT STU
#   Adam Vrabeľ
#       UI - KLASTROVANIE (3C)
import copy
import random
import numpy as np
import matplotlib.pyplot as plt


# TRIEDA PRE ZHLUK BODU/BODOV (cluster)
class Cluster:

    # AK VYTVÁRAM CLUSTER ==> LIST = JEDEN BOD a TEN JE ZÁROVEŇ CENTROID
    def __init__(self, points):
        self.points = []
        self.points.extend(points)      # LIST BODOV / alebo aj jedného [(x,y), ...]

        # self.centroid = centroid        # JEDEN BOD (x,y)
        self.centroid = None
        self.calculate_centroid()       # sam si vypocita centroid
    ##################################################################################

    # NAJDENIE CENTROIDU V ZHLUKU BODOV
    def calculate_centroid(self):
        # Centroid (ťažisko) sa vypočíta ako priemerná hodnota súradníc všetkých bodov v zhluku
        # Používame axis=0, aby sme vypočítali priemernú hodnotu pre každý stĺpec (X a Y) zvlášť.
        new_centroid = np.mean(self.points, axis=0)
        new_centroid = tuple(new_centroid)  # NumPy array si konvertujem na tuple (x,y)

        self.centroid = new_centroid        # nastavím nový centroid
    #############################################################################################

    # PRIDÁVANIE BODOV DO CLUSTERA (LIST BODOV (x,y) ) aj jeden bod v LISTE bude ok
    def add_points(self, points):
        # PRIDÁ BODY K EXISTUJÚCIM
        self.points.extend(points)
        # VYPOČÍTA NOVÝ CENTROID
        self.calculate_centroid()
        # PREPOČÍTAM VZDIALENOSTI PRE TENTO ZHLUK ku všetkým ostatným bodom
        # for cyklus listu clusterv, bude niečo robiť, no na sebe samom to vynecha ==> ... if cluster is not self ...
        pass
    ####################################################################################################################


################################################################################################

# X a Y súradnice budú od -5000 do +5000
MIN_VALUE = -5000
MAX_VALUE = 5000

NUM_OF_START_POINTS = 20            # NAJPRV VYGENERUJE 20 POČIATOČNÝ BODOV
# NUM_OF_ANOTHER_POINTS = 20000       # NÁSLEDNE 20000 ĎALŠÍCH BODOV
NUM_OF_ANOTHER_POINTS = 100        # NÁSLEDNE 20000 ĎALŠÍCH BODOV

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


# vypočíta vzdialenosť dvoch centroidov v ZHLUKOCH (clustroch)
def centroid_distance(cluster1, cluster2):
    centroid1 = cluster1.centroid
    centroid2 = cluster2.centroid
    return euclidean_distance(centroid1, centroid2)


# vypočíta 2D maticu vzdialeností centroidov v ZHLUKOCH
def make_centroids_distance_matrix(clusters):

    # vytvorím 2D maticu, kde element (i, j) obsahuje vzdialenosť medzi bodmi (centroidmi) clustrov i a j
    distances = np.zeros((len(clusters), len(clusters)))    # na zaciatku vsade inicializovane na 0

    # pre celú maticu distances vypočíta všetky vzdialenosti centroidov (z daneho zhluku) a zapíše do matice
    for i in range(len(clusters)):
        for j in range(len(clusters)):

            distances[i, j] = centroid_distance(clusters[i], clusters[j])   # POSIELAM CELÉ ZHLUKY, funkcia si spracuje sama a vráti vzdialenosť centroidov
            # print(f"VZDIALENOST CENTROIDOV: {distances[i, j]}")

    # Ignorujte diagonálu matice    (pretože na diagonále su nuly, tie nepotrebujem, bod so semou samým ma nezaujíma)
    np.fill_diagonal(distances, np.inf)

    return distances


# ALGORITMUS PRE AGLOMERATÍVNE ZHLUKOVANIE, kde stred je centroid
def aglomerative_w_centroid(dataset, k):
    ALL_POINTS = copy.deepcopy(dataset)

    # dataset ==>  list dát (x,y)
    # k       ==>  na koľko zhlukov rozdelím dataset
    # CENTROID JE FIKTÍVNY (novo/umelo vytvorený bod), ktorý je v strede vybraných bodov (ťažisko)

    # NA ZAČIATKU SA KAŽDÝ BOD POČÍTA AKO JEDEN ZHLUK (cluster)
    clusters = []
    for point in ALL_POINTS:
        tmp_cluster = Cluster(points=[point])   # inicializácia zhlukov: každý bod == samostatný zhluk (list s jedným bodom) | jeden bod v liste je sam sebe aj centroid
        clusters.append(tmp_cluster)                            # pridá nový cluster do listu

    # CISTO NA TESTOVACIE ÚČELY, POTOM ODSTRÁNIŤ
    clusters.append(Cluster(points=[(1, 2), (1, 3)]))
    clusters.append(Cluster(points=[(2, 2), (2, 3)]))
    clusters.append(Cluster(points=[(556, 2), (111, 3)]))
    clusters.append(Cluster(points=[(1012, 2), (-20, 3)]))
    # CISTO NA TESTOVACIE ÚČELY, POTOM ODSTRÁNIŤ
    # ###################################################################################################################################################################################

    # VYPOČÍTA VZDIALENOSŤ CENTROIDOV PRE clusters[0] a clusters[1]
    # dst = centroid_distance(clusters[0], clusters[1])

    # ###################################################################################################################################################################################

    # postupné zlučovanie zhlukov (clusterov), kým nie je dosiahnutý požadovaný počet zhlukov (k)
    num_of_iteration = 0
    while len(clusters) > k:
        print(f"NUMBER OF ITERATION: {num_of_iteration}")
        num_of_iteration += 1

        # TERAZ VYPOČÍTAM VŠETKY VZDIALENOSTI PRE JEDNOTLIVÉ CENTROIDY V KLASTROCH
        clusters_centroids_distances = make_centroids_distance_matrix(clusters)

        # VYBERIEM ZHLUKY S NAJMENŠIOU VZDIALENOSŤOU CENTROIDOU, tie neskor spolu zlúčim
        min_distance_index = np.unravel_index(np.argmin(clusters_centroids_distances), clusters_centroids_distances.shape)

        # Získajte indexy zhlukov s najmenšou vzdialenosťou
        index_cluster1 = min_distance_index[0]
        index_cluster2 = min_distance_index[1]

        # Získajte príslušné zhluky zo zoznamu clusters ktoré treba zlúčiť
        cluster1 = clusters[index_cluster1]
        cluster2 = clusters[index_cluster2]

        # VIEM ŽE cluster1 a cluster2 majú najmenšiu vzdialenosť centroidov

        # ZLÚČENIE DVOCH ZHLUKOV
        # do prvého zhluku pridám body z druhého, ten si sám prepočíta centroid
        cluster1.add_points(cluster2.points)

        # vymaze nepotrebný cluster2
        clusters.remove(cluster2)


        ###
        ###
        ###

        # # Výpočet centroidov
        # centroids = [calculate_centroid(cluster) for cluster in clusters]
        #
        # # Výpočet vzdialeností medzi centroidmi
        # distances = euclidean_distance_matrix(centroids)
        #
        # # Ignorujte diagonálu matice
        # np.fill_diagonal(distances, np.inf)
        #
        # min_distance_index = np.unravel_index(np.argmin(distances), distances.shape)
        #
        # # Zlúči dva najbližšie zhluky
        # cluster1 = clusters[min_distance_index[0]]
        # cluster2 = clusters[min_distance_index[1]]
        # new_cluster = cluster1 + cluster2
        # clusters.pop(min_distance_index[0])
        # clusters.pop(min_distance_index[1] - 1)
        #
        # clusters.append(new_cluster)

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
    farba = ["red", "blue", "green", "purple", "black"]
    for cluster in ALL_CLUSTERS:

        hodnoty_x = []
        hodnoty_y = []
        for point in cluster.points:
            hodnoty_x.append(point[0])
            hodnoty_y.append(point[1])

        # ZAPÍŠEM BODY DO GRAFU (rovnakej farby)
        color = farba[i]
        # plt.scatter(hodnoty_x, hodnoty_y, color="orange", s=5)
        plt.scatter(hodnoty_x, hodnoty_y, color=str(color), s=10)
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
