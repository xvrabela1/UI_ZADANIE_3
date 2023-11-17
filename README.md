# UI_ZADANIE_3
ui-zadanie3


---

ZÁKLADNÉ POJMY:

>**EUKIDOVSKÁ VZDIALENOSŤ**
>> np.sqrt(np.sum((point1 - point2) ** 2))
> 
> Euklidovská vzdialenosť je štandardná geometrická vzdialenosť medzi dvoma bodmi v euklidovskej rovine alebo priestore.\
>Funkcia euclidean_distance využíva knižnicu NumPy na efektívne vykonanie tohto výpočtu pre vektorové operácie, čo je užitočné pri práci s množinami bodov. Konkrétne používa operácie na odčítanie, umocňovanie a sčítanie na výpočet euklidovskej vzdialenosti v 2D priestore.\
>V kontexte aglomeratívneho zhlukovania, ako je implementované v pseudokóde, táto funkcia sa môže použiť na výpočet vzdialeností medzi centroidmi rôznych zhlukov alebo medzi bodmi v rámci jedného zhluku. To je užitočné pri rozhodovaní, ktoré zhluky zlúčiť počas postupného aglomeratívneho procesu.


>**CENTROID** \
> je umelo vytvorený bod v strede bodov z množiny \
> Mám množinu bodov (napr troch) a vytvorím bod, ktorý bude v ich strede = CENTROID \
> SÚRADNICE CENTROIDU VYPOČÍTAM = PRIEMER X súradníc a PRIEMER Y súradníc


---

1. Inicializácia: Každý prvok je považovaný za jeden zhluk.
2. Výpočet podobnosti: Vypočíta sa podobnosť (alebo vzdialenosť) medzi všetkými pármi zhlukov.
3. Spájanie zhlukov: Dva najbližšie zhluky s najnižšou vzdialenosťou sú spojené do jedného zhluku. Centroid nového zhluku je vypočítaný.
4. Aktualizácia matice podobnosti: Matice podobnosti medzi zhlukmi sa aktualizuje.
5. Opakovanie: Kroky 2 až 4 sa opakujú, kým sa nedosiahne požadovaný stav, napríklad stanovený počet zhlukov alebo určený kritérium podobnosti.