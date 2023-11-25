# FIIT STU
#   Adam Vrabeľ
#       UI - KLASTROVANIE (3C)
import copy
import random
import numpy as np
import matplotlib.pyplot as plt

id_counter = 0

calculate_medoid = bool()     # ak TRUE - tak počíta s medoidom, ak FALSE - tak počíta s centroidom


# TRIEDA PRE ZHLUK BODU/BODOV (cluster)
class Cluster:

    # AK VYTVÁRAM CLUSTER ==> LIST = JEDEN BOD a TEN JE ZÁROVEŇ CENTROID
    def __init__(self, points):
        self.points = []
        self.points.extend(points)      # LIST BODOV / alebo aj jedného [(x,y), ...]

        global id_counter
        self.id = id_counter            # jedinečné ID pre cluster
        id_counter += 1

        global calculate_medoid     # ak TRUE - tak počíta s medoidom, ak FALSE - tak počíta s centroidom
        if calculate_medoid:
            self.medoid = None
            self.find_medoid()
        else:
            # self.centroid = centroid        # JEDEN BOD (x,y)
            self.centroid = None
            self.calculate_centroid()  # sam si vypocita centroid

    ##################################################################################

    # NAJDENIE CENTROIDU V ZHLUKU BODOV
    def calculate_centroid(self):
        # Centroid (ťažisko) sa vypočíta ako priemerná hodnota súradníc všetkých bodov v zhluku
        # Používame axis=0, aby sme vypočítali priemernú hodnotu pre každý stĺpec (X a Y) zvlášť.
        new_centroid = np.mean(self.points, axis=0)
        new_centroid = tuple(new_centroid)  # NumPy array si konvertujem na tuple (x,y)

        self.centroid = new_centroid        # nastavím nový centroid
    #############################################################################################

    # NAJDENIE MEDOIDU V ZHLUKU BODOV
    def find_medoid(self):
        min_total_distance = float('inf')
        medoid_point = None

        # prechádzam všetky body v zhluku.
        for point1 in self.points:
            total_distance = 0

            # pre každý bod v zhluku vypočítam jeho vzdialenosť od ostatných bodov v zhluku.
            for point2 in self.points:
                total_distance += euclidean_distance(point1, point2)

            # ak nájdem bod s nižšou celkovou vzdialenosťou, aktualizujem medoid
            if total_distance < min_total_distance:
                min_total_distance = total_distance
                medoid_point = point1

        self.medoid = medoid_point
    #############################################################################################

    # PRIDÁVANIE BODOV DO CLUSTERA (LIST BODOV (x,y) ) aj jeden bod v LISTE bude ok
    def add_points(self, points):
        # PRIDÁ BODY K EXISTUJÚCIM
        self.points.extend(points)

        global calculate_medoid  # ak TRUE - tak počíta s medoidom, ak FALSE - tak počíta s centroidom

        if calculate_medoid:
            # VYPOČÍTA MEDOID
            self.find_medoid()
        else:
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
NUM_OF_ANOTHER_POINTS = 500        # NÁSLEDNE 20000 ĎALŠÍCH BODOV

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

# euklidová vzdialenosť medzi dvoma bodmi v euklidovskej rovine
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


# vypočíta vzdialenosť dvoch medoidov v ZHLUKOCH (clustroch)
def medoid_distance(cluster1, cluster2):
    medoid1 = cluster1.medoid
    medoid2 = cluster2.medoid
    # centroid1 = cluster1.centroid
    # centroid2 = cluster2.centroid
    return euclidean_distance(medoid1, medoid2)


# vypočíta 2D maticu vzdialeností medoidov v ZHLUKOCH
def make_medoids_distance_matrix(clusters):

    # vytvorím 2D maticu, kde element (i, j) obsahuje vzdialenosť medzi bodmi (centroidmi) clustrov i a j
    distances = np.zeros((len(clusters), len(clusters)))    # na zaciatku vsade inicializovane na 0

    # pre celú maticu distances vypočíta všetky vzdialenosti medoidov (z daneho zhluku) a zapíše do matice
    for i in range(len(clusters)):
        for j in range(len(clusters)):

            distances[i, j] = medoid_distance(clusters[i], clusters[j])   # POSIELAM CELÉ ZHLUKY, funkcia si spracuje sama a vráti vzdialenosť medoidov
            # print(f"VZDIALENOST CENTROIDOV: {distances[i, j]}")

    # Ignorujte diagonálu matice    (pretože na diagonále su nuly, tie nepotrebujem, bod so semou samým ma nezaujíma)
    np.fill_diagonal(distances, np.inf)

    return distances

# NEW
# každý cluster bude mať svoje ID
# a vzdialenosti budem udržiavať v dictionary (ID_1, ID_2 a vzdialenosť medzi nimi)
# potom už budem iba meniť tie, ktoré potrebujem (a ktoré sa ovplyvnia)


def calculate_distances_NEW(clusters):
    distances_dict = {}     # key (id_clustera1, id_clustera1)   # value (ich vzdialenosť)

    key_1_values = []
    key_2_values = []
    # minimalna_vzdialenost = 20000           # je urcite vacsia ako diagonala v 10 000 x 10 000 (ziadna vzdialenost v poli nebude vacsia ako toto)
    # minimalna_vzdialenost_key = tuple()     # bude to touple(id_clustera1, id_clustera1) kde je minimalna_vzdialenost medzi centroidmi

    # fruits = ['apple', 'banana', 'cherry']
    # for index, value in enumerate(fruits):
    #     print(f'Index: {index}, Value: {value}')

    # prechádzam každý cluster s každým
    for i, cluster1 in enumerate(clusters):
        for j, cluster2 in enumerate(clusters):
            if i < j:  # Zabráni duplicitným párom (i, j) a (j, i)
                # key = (i, j)

                if cluster1.id not in key_1_values:
                    key_1_values.append(cluster1.id)

                if cluster2.id not in key_2_values:
                    key_2_values.append(cluster2.id)

                # moj kľúč = touple(id clustra1, id clustra2)
                key = (cluster1.id, cluster2.id)

                # moja value = vzdialenosť centroidov týchto dvoch clustrov
                distance = centroid_distance(cluster1, cluster2)
                distances_dict[key] = distance

                # # udržiavanie minimalnej vzdialenosti a odkazu k nej cez key
                # if distance < minimalna_vzdialenost:
                #     minimalna_vzdialenost = distance
                #     minimalna_vzdialenost_key = key

    del i, j, key, cluster1, cluster2, distance     # vymazem nepotrebne premenné (pre prehľadnosť v debuggeri)

    # ZORADÍM VZDIALENOSTI OD NAJMENŠEJ
    sorted_distance = dict(sorted(distances_dict.items(), key=lambda item: item[1]))

    return_dictionary = {
        # "distances_dict": distances_dict,  # NEZORADENÉ
        "distances_dict": sorted_distance,   # ZORADENÉ OD NAJMENŠEJ VZDIALENOST
        "key_1_values": key_1_values,
        "key_2_values": key_2_values,
        # "min_vzdialenost": minimalna_vzdialenost,
        # "min_vzdialenost_key": minimalna_vzdialenost_key
    }
    # return distances_dict
    return return_dictionary


# VYMAZEM V DICTIONARY VŠETKY VZDIALENOSTI SPOJENÉ SO ZADANÝMI KLASTRAMI
# vytvorím nový, spojený z bodov
# a vypočítam mu vzdialenosti so všetkými ostatnými klastrami a pre každý klaster s novo vytvoreným
def make_two_clusters_magic_NEW(all_clusters, new_distances_dict, cluster1_id, cluster2_id):

    # cluster1_id, cluster2_id     =>     ID klastrov s najmenšou vzdialenosťou centroidov

    # SKOPÍRUJEM SI BODY V zlučovaných klastroch, klastre vymažem a vytvorím nový klaster

    # LEN NA TESTOVANIE ZLUCUJEM KLASTRE ID 0 a 2
    # cluster1_id = 0
    # cluster2_id = 2

    # HĽADÁM 2 DANÉ CLUSTRE podľa ID
    cluster1 = None
    cluster2 = None

    for cluster in all_clusters:
        if cluster.id == cluster1_id:
            cluster1 = cluster

        elif cluster.id == cluster2_id:
            cluster2 = cluster

        if cluster1 is not None and cluster2 is not None:
            break   # našiel som oba clustre, nepotrebujem ďalej hľadať

    # print("BREAKPOINT")
    del cluster  # vymazem nepotrebne premenné (pre prehľadnosť v debuggeri)

    # EXTRAKCIA BODOV
    tmp_points = []
    tmp_points.extend(cluster1.points)
    tmp_points.extend(cluster2.points)

    # VYTVORENIE NOVÉHO ZHLUKU SO ZLÚČENÝMI BODMI
    new_cluster = Cluster(tmp_points)
    # PRIDANIE NOVÉHO CLUSTRA DO ZOZNAMU VŠETKÝCH
    all_clusters.append(new_cluster)

    # print("BREAKPOINT")
    del tmp_points  # vymazem nepotrebne premenné (pre prehľadnosť v debuggeri)

    # VYMAZANIE ZHLUKOV Z all_clusters
    all_clusters.remove(cluster1)
    all_clusters.remove(cluster2)
    # print("BREAKPOINT")
    del cluster1, cluster2  # vymazem nepotrebne premenné (pre prehľadnosť v debuggeri)

    ##############################################################################################################################
    # ešte pridať new_cluster do listu všetkých !!!!!!!!!!!
    # ešte vymazanie vzdialeností !!!!!!!!!!!
    ##############################################################################################################################

    # v new_distances_dict vymažem v distances_dict všetky ktoré obsahujú v key id1 a id2
    # search_key = ()

    # VYMAZAVAM VZDIALENOSTI (id1, id2)
    # prejdem distances_dict a mazem vsetko kde je (id1, hocico) a (hocico, id1)
    # prejdem distances_dict a mazem vsetko kde je (id2, hocico) a (hocico, id2)

    # (id1, hocico) alebo (id2, hocico) ==> vymazujem
    for key1 in new_distances_dict['key_1_values']:
        # AK JE (KEY1 jeden zo zadanych, hocico)
        if key1 == cluster1_id or key1 == cluster2_id:

            for key2 in new_distances_dict['key_2_values']:
                # (id1, hocico) alebo (id2, hocico) ==> vymazujem
                search_key = (int(key1), int(key2))

                tmp_value = new_distances_dict['distances_dict'].get(search_key)
                if tmp_value is not None:
                    del new_distances_dict['distances_dict'][search_key]  # vymaze danú vzdialenosť

    del key1, key2, search_key, tmp_value

    # (hocico, id1) alebo (hocico, id2) ==> vymazujem
    for key2 in new_distances_dict['key_2_values']:
        # AK JE (hocico, KEY2 jeden zo zadanych)
        if key2 == cluster1_id or key2 == cluster2_id:

            for key1 in new_distances_dict['key_1_values']:
                # (hocico, id1) alebo (hocico, id2) ==> vymazujem
                search_key = (int(key1), int(key2))

                tmp_value = new_distances_dict['distances_dict'].get(search_key)
                if tmp_value is not None:
                    del new_distances_dict['distances_dict'][search_key]  # vymaze danú vzdialenosť

    del key1, key2, search_key, tmp_value

    # mozem id vymazat aj v key_1_values a key_2_values
    # print("BREAKPOINT")
    if cluster1_id in new_distances_dict['key_1_values']:
        new_distances_dict['key_1_values'].remove(cluster1_id)

    if cluster1_id in new_distances_dict['key_2_values']:
        new_distances_dict['key_2_values'].remove(cluster1_id)

    if cluster2_id in new_distances_dict['key_1_values']:
        new_distances_dict['key_1_values'].remove(cluster2_id)

    if cluster2_id in new_distances_dict['key_2_values']:
        new_distances_dict['key_2_values'].remove(cluster2_id)

    # for key in new_distances_dict['key_1_values']:
    #     if key == cluster1_id or key == cluster2_id:
    #
    #         tmp_value = new_distances_dict['key_1_values'].get(int(key))
    #         if tmp_value is not None:
    #             del new_distances_dict['key_1_values'][key]
    #
    #         break
    # del key, tmp_value
    #
    # for key in new_distances_dict['key_2_values']:
    #     if key == cluster1_id or key == cluster2_id:
    #
    #         tmp_value = new_distances_dict['key_2_values'].get(key)
    #         if tmp_value is not None:
    #             del new_distances_dict['key_2_values'][key]
    #
    #         break
    # del key, tmp_value

    # print("BREAKPOINT")

    # VYPOČET NOVÝCH VZDIALENOSTÍ
    # vypočítam mu vzdialenost nového so všetkými ostatnými

    # prechádzam všetky clustre
    for i, cluster in enumerate(all_clusters):
        # vypočítam vzdialenosť novému so všetkými

        if i == new_cluster.id:
            continue

        # key = (new_cluster, vsetky)
        key = (new_cluster.id, cluster.id)

        if new_cluster.id not in new_distances_dict['key_1_values']:
            new_distances_dict['key_1_values'].append(new_cluster.id)

        if cluster.id not in new_distances_dict['key_2_values']:
            new_distances_dict['key_2_values'].append(cluster.id)

        # moja value = vzdialenosť centroidov týchto dvoch clustrov
        distance = centroid_distance(new_cluster, cluster)
        if distance == 0:
            continue
        new_distances_dict['distances_dict'][key] = distance

        # # udržiavanie minimalnej vzdialenosti a odkazu k nej cez key
        # if distance < new_distances_dict['min_vzdialenost']:
        #     new_distances_dict['min_vzdialenost'] = distance
        #     new_distances_dict['min_vzdialenost_key'] = key

    # ZORADÍM VZDIALENOSTI OD NAJMENŠEJ
    sorted_distance = dict(sorted(new_distances_dict['distances_dict'].items(), key=lambda item: item[1]))


    # print("LAST_BREAKPOINT")




    #
    #
    # # VYBERIEM ZHLUKY S NAJMENŠIOU VZDIALENOSŤOU CENTROIDOU, tie neskor spolu zlúčim
    # min_distance_index = np.unravel_index(np.argmin(clusters_centroids_distances), clusters_centroids_distances.shape)
    #
    # # Získajte indexy zhlukov s najmenšou vzdialenosťou
    # index_cluster1 = min_distance_index[0]
    # index_cluster2 = min_distance_index[1]
    #
    # # Získajte príslušné zhluky zo zoznamu clusters ktoré treba zlúčiť
    # cluster1 = clusters[index_cluster1]
    # cluster2 = clusters[index_cluster2]
    #
    # # VIEM ŽE cluster1 a cluster2 majú najmenšiu vzdialenosť centroidov
    #
    # # ZLÚČENIE DVOCH ZHLUKOV
    # # do prvého zhluku pridám body z druhého, ten si sám prepočíta centroid
    # cluster1.add_points(cluster2.points)
    #
    # # vymaze nepotrebný cluster2
    # clusters.remove(cluster2)

    return all_clusters, new_distances_dict  # vráti tuple(list vš. klastrov a new_distances_dicts)


# NOVÁ FUNKCIA
# ALGORITMUS PRE AGLOMERATÍVNE ZHLUKOVANIE, kde stred je centroid
def aglomerative_w_centroid_NEW(dataset, k):
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
    # clusters.append(Cluster(points=[(1, 2), (1, 3)]))
    # clusters.append(Cluster(points=[(2, 2), (2, 3)]))
    # clusters.append(Cluster(points=[(556, 2), (111, 3)]))
    # clusters.append(Cluster(points=[(1012, 2), (-20, 3)]))
    # CISTO NA TESTOVACIE ÚČELY, POTOM ODSTRÁNIŤ
    # ###################################################################################################################################################################################

    # VYPOČÍTA VZDIALENOSŤ CENTROIDOV PRE clusters[0] a clusters[1]
    # dst = centroid_distance(clusters[0], clusters[1])

    # ###################################################################################################################################################################################

    # postupné zlučovanie zhlukov (clusterov), kým nie je dosiahnutý požadovaný počet zhlukov (k)
    num_of_iteration = 0

    # is_succsessful = False
    # is_succsessful = control_each_cluster(clusters)     # prvé klastre netreba kontrolovať (určite nebude splnená podmienka)

    # NEW
    # PRVOTNÉ POČÍTANIE VZDIALENOSTÍ PRE CENTROIDY V KLASTROCH (každý s každým)
    new_distances_dict = calculate_distances_NEW(clusters)

    # new_distances_dict = {
    #     "distances_dict": distances_dict,                     # key(cluster1 id, cluster2 id) = vzdialenost centroidov
    #     "key_1_values": key_1_values,                         # aké cluster1.id sú v prvom indexe pre key
    #     "key_2_values": key_2_values                          # aké cluster2.id sú v druhom indexe pre key
    #     "min_vzdialenost": minimalna_vzdialenost,             # min vzdialenosť medzi klastrami (hodnota)
    #     "min_vzdialenost_key": minimalna_vzdialenost_key      # min vzdialenosť key(cluster1 id, cluster2 id)
    # }

    # for key, value in new_distances_dict['distances_dict'].items():
    #     print(f'Distance between Cluster {key[0]} and Cluster {key[1]}: {value}')

    # zlúč klastre ktoré majú najmenšiu vzdialenosť
    # print(f"Minimálna vzdialenosť [{new_distances_dict['min_vzdialenost']}] je medzi klastrami ID1:{new_distances_dict['min_vzdialenost_key'][0]}, ID2:{new_distances_dict['min_vzdialenost_key'][1]}")

    # while is_succsessful is False:  # pokial nieje zhlukovač úspešný, tak zhlukujem
    while len(clusters) > k:

        print(f"NUMBER OF ITERATION: {num_of_iteration}")
        num_of_iteration += 1

        # 2 CLUSTRE ČO TREBA ZLÚČIŤ
        # cluster1_id = new_distances_dict['min_vzdialenost_key'][0]
        # cluster2_id = new_distances_dict['min_vzdialenost_key'][1]

        # Získanie prvého kľúča a hodnoty zo slovníka
        min_vzdialenost_key, min_vzdialenost_hodnota = next(iter(new_distances_dict['distances_dict'].items()))

        # zlúči 2 klastre, prepočíta vzdialenosti
        info = make_two_clusters_magic_NEW(clusters, new_distances_dict, min_vzdialenost_key[0], min_vzdialenost_key[1])

        # nastavím dôležité premenné
        clusters = info[0]
        new_distances_dict = info[1]

        # print("END")

        # # PREPOČÍTA KAŽDÝ KLASTER, UKONČÍ ZHLUKOVANIE VTEDY (ak netreba zhlukovať = True / ak ešte treba zhlukovať = False):
        # is_succsessful = control_each_cluster(clusters)

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


# PREPOČÍTA KAŽDÝ KLASTER, UKONČÍ ZHLUKOVANIE VTEDY (vráti True / False):
#   - vypočítať priemernú vzdialenosť bodov od centroidu (stredu)
#   - KONČÍM VTEDY: ak každý klaster má priemernú vzdialenosť menšiu alebo rovnú 500
def control_each_cluster(clusters):
    # ak je nejaká vzdialenosť VAČŠIA AKO 500             ==> vrátim False, treba ešte zhlukovať
    # ak sú vš. vzdialenosti rovné alebo menšie ako 500   ==> vrátim True, končí sa zhlukovanie

    # prechádzam každý cluster
    for cluster in clusters:

        distances = []                  # prázdny zoznam pre ukladanie vzdialeností v clustri
        centroid = cluster.centroid     # centroid z clustera

        # prechádzam každý bod v clustri
        for point in cluster.points:
            # vypočítam euklidovskú vzdialenosť medzi bodom a centroidom daného clustera
            # act_distance = euclidean_distance(point, centroid)
            point = np.array(point)
            centroid = np.array(centroid)

            act_distance = np.sqrt(np.sum((point - centroid) ** 2))

            distances.append(act_distance)

        # vypočítam priemernú vzdialenosť pomocou funkcie np.mean
        avg_distance_in_cluster = np.mean(distances)
        if avg_distance_in_cluster > 500:
            return False    # ak je nejaká vzdialenosť VAČŠIA AKO 500, treba ešte zhlukovať

    return True  # prešiel som všetky clustre a avg vzdialenosti sú menšie alebo rovné ako 500


# ALGORITMUS PRE AGLOMERATÍVNE ZHLUKOVANIE, kde stred je centroid
# ak nastavím medoid=True, tak zhlukuje podľa medoidu
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
    # clusters.append(Cluster(points=[(1, 2), (1, 3)]))
    # clusters.append(Cluster(points=[(2, 2), (2, 3)]))
    # clusters.append(Cluster(points=[(556, 2), (111, 3)]))
    # clusters.append(Cluster(points=[(1012, 2), (-20, 3)]))
    # CISTO NA TESTOVACIE ÚČELY, POTOM ODSTRÁNIŤ
    # ###################################################################################################################################################################################

    # VYPOČÍTA VZDIALENOSŤ CENTROIDOV PRE clusters[0] a clusters[1]
    # dst = centroid_distance(clusters[0], clusters[1])

    # ###################################################################################################################################################################################

    # postupné zlučovanie zhlukov (clusterov), kým nie je dosiahnutý požadovaný počet zhlukov (k)
    num_of_iteration = 0

    # is_succsessful = False
    # is_succsessful = control_each_cluster(clusters)     # prvé klastre netreba kontrolovať (určite nebude splnená podmienka)

    # while is_succsessful is False:  # pokial nieje zhlukovač úspešný, tak zhlukujem
    while len(clusters) > k:

        print(f"NUMBER OF ITERATION: {num_of_iteration}")
        num_of_iteration += 1

        global calculate_medoid

        # S CENTROIDOM
        if not calculate_medoid:
            # TERAZ VYPOČÍTAM VŠETKY VZDIALENOSTI PRE JEDNOTLIVÉ CENTROIDY V KLASTROCH
            clusters_distances = make_centroids_distance_matrix(clusters)

        # S MEDOIDOM
        else:
            # TERAZ VYPOČÍTAM VŠETKY VZDIALENOSTI PRE JEDNOTLIVÉ MEDOIDY V KLASTROCH
            clusters_distances = make_medoids_distance_matrix(clusters)

        #
        # VYBERIEM ZHLUKY S NAJMENŠIOU VZDIALENOSŤOU CENTROIDOU, tie neskor spolu zlúčim
        min_distance_index = np.unravel_index(np.argmin(clusters_distances), clusters_distances.shape)

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

        # # PREPOČÍTA KAŽDÝ KLASTER, UKONČÍ ZHLUKOVANIE VTEDY (ak netreba zhlukovať = True / ak ešte treba zhlukovať = False):
        # is_succsessful = control_each_cluster(clusters)

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
    # farba = ["red", "blue", "green", "purple", "black"]
    for cluster in ALL_CLUSTERS:

        hodnoty_x = []
        hodnoty_y = []
        for point in cluster.points:
            hodnoty_x.append(point[0])
            hodnoty_y.append(point[1])

        # ZAPÍŠEM BODY DO GRAFU (rovnakej farby)
        # color = farba[i]
        # generovanie náhodnej farby v HEX formáte
        color = "#{:02x}{:02x}{:02x}".format(np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))

        # plt.scatter(hodnoty_x, hodnoty_y, color="orange", s=5)
        plt.scatter(hodnoty_x, hodnoty_y, color=str(color), s=10, zorder=0)

        global calculate_medoid  # ak TRUE - tak počíta s medoidom, ak FALSE - tak počíta s centroidom
        if calculate_medoid:
            # vykreslenie medoidu
            plt.scatter(cluster.medoid[0], cluster.medoid[1], marker="o", edgecolors="black", facecolors='none', s=10, linewidths=0.8, zorder=1)
        else:
            # vykreslenie centroidu
            plt.scatter(cluster.centroid[0], cluster.centroid[1], marker="o", edgecolors="black", facecolors='none', s=30, linewidths=0.8, zorder=1)

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

    # STARÉ, FUNKČNÉ
    # S CENTROIDOM
    calculate_medoid = False      # ak TRUE - tak počíta s medoidom, ak FALSE - tak počíta s centroidom
    # S MEDOIDOM
    # calculate_medoid = True         # ak TRUE - tak počíta s medoidom, ak FALSE - tak počíta s centroidom

    clust = aglomerative_w_centroid(dataset=DATASET, k=5)
    print_clusters(clust)

    # NOVÉ, TESTUJEM
    # calculate_medoid = False
    # clust = aglomerative_w_centroid_NEW(dataset=DATASET, k=2)
    # print_clusters(clust)
