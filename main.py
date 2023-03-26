import csv
import numpy as np

def table_condorcet(data):
    print("---- TABLE CONDORCET ----")
    size = len(data[0])
    liste = []
    for entry in range(size):
        full_entry = []
        for entry2 in range(size):
            a = 0
            b = 0
            if entry != entry2:
                for line in data:
                    for number in line:
                        if int(number) == entry + 1:
                            a += 1
                            break
                        if int(number) == entry2 + 1:
                            b +=1
                            break
                full_entry.append(a)
            else:
                full_entry.append(0)
        liste.append(full_entry)
    liste_condorcet = []
    for entry in range(size):
        gagne = 0
        for entries in range(size):
            if liste[entry][entries] > len(data)/2:
                gagne += 1
        liste_condorcet.append(gagne)
    return liste_condorcet

def borda2():
    # Lecture du fichier CSV
    with open('edit_data/profil1.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [list(map(int, row)) for row in reader]

    # Calcul des points de chaque candidat
    num_candidates = len(data[0])
    points = [0] * num_candidates
    for voter in data:
        for i, candidate in enumerate(voter):
            points[candidate - 1] += num_candidates - i - 1

    # Tri des candidats en fonction de leurs points
    ranking = sorted(range(num_candidates), key=lambda i: points[i], reverse=True)

    # Affichage du classement final
    print("Classement final :")
    for i, candidate in enumerate(ranking):
        print(f"{i + 1}. Candidat {candidate + 1} : {points[candidate]} points")

if __name__ == '__main__':

    with open('edit_data/profil1.csv', newline='') as profil1:
        r = csv.reader(profil1)
        data1 = list(r)
    full_table_condorcet = table_condorcet(data1)
    print(full_table_condorcet)
    print("Selon Condorcet, l'élu est le candidat " + str(full_table_condorcet.index(max(full_table_condorcet)) + 1))
    borda2()