import csv
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt


########## GENERIC ##########

# Detect which IDs appears first in the column 'column'. Depending of 'included' is 0 or 1, include or exclude the IDs of the array
def detect_first_id(column, array, included):
    # print(column)
    for value in column:
        # Check for included values
        if included == 1:
            if value in array:
                return value
        
        # Check for excluded values
        if included == 0:
            if value not in array:
                return value
    
    return None

# Detect which id is in the last position, after excluding the ones in the array 'excluded'
def detect_last_id(column, *excluded):
    for value in list(reversed(column)):
        if value not in excluded:
            return value
    
    return None

########## CONDORSET ##########

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

    print(liste_condorcet)
    print("Selon Condorcet, l'élu est le candidat " + str(liste_condorcet.index(max(liste_condorcet)) + 1))

    return liste_condorcet

########## BORDA ##########

def borda2():
    # Lecture du fichier CSV
    with open('data/profil1.csv', 'r') as csvfile:
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

########## ROUNDS ##########

# Get winner of 'df' with nb_round (one or two rounds) method
def rounds(df, nb_round=1):
    votes = df.shape[1]
    # Secure function
    if(nb_round != 1 and nb_round != 2):
        print("Le nombre de tours doit être égal à 1 ou 2.")
        return
    
    print("Choix social en " + str(nb_round) + " tour(s) :")

    # Get numbers of first places
    ranks_r1 = df.iloc[0].value_counts()

    if (nb_round == 1):
        print(ranks_r1)
        nb_first = ranks_r1.iloc[0]
        id_first = ranks_r1.index[0]
        print("Vainqueur au tour 1 : Candidat " + str(id_first) + " avec " + str(nb_first) + " voix.")
        return ranks_r1

    if (nb_round == 2):
        nb_first = ranks_r1.iloc[0]
        id_first = ranks_r1.index[0]

        # Check for absolute majority
        if (nb_first >= (votes /2 + 1)):
            print("Vainqueur au tour 1 par majorité absolue : Candidat " + str(id_first) + " avec " + str(nb_first) + " voix.")

        print(ranks_r1)
        nb_sec = ranks_r1.iloc[1]
        id_sec = ranks_r1.index[1]
        print("Vainqueurs au tour 1 : Candidat " + str(id_first) + " avec " + str(nb_first) + " voix et Candidat " + str(id_sec) + " avec " + str(nb_sec) + " voix.")
        # Get which ID is first on each column
        ranks_r2 = df.apply(detect_first_id, args=([id_first, id_sec], 1))

        # Count occurences of each ID
        counts = ranks_r2.value_counts()
        nb_winner = counts.iloc[0]
        id_winner = counts.index[0]

        # Print final results
        print(counts)
        print("Vainqueur au tour 2 : Candidat " + str(id_winner) + " avec " + str(nb_winner) + " voix.")
        return ranks_r2


########## COOMBS ##########

def coombs(df):
    print('Méthode Coombs')
    # Init
    excluded = []
    votes = df.shape[1]
    rows = len(df)

    for i in range(rows):
        # Get candidate with highest last places
        last_places = df.apply(detect_last_id, args=(excluded))
        counts_last = last_places.value_counts()
        id_last = counts_last.index[0]

        # Check for absolute majority
        first_places = df.apply(detect_first_id, args=(excluded, 0))
        counts_first = first_places.value_counts()
        nb_first = counts_first.iloc[0]
        if (nb_first >= (votes/2 + 1)):
            id_first = counts_first.index[0]
            print("Vainqueur au tour " + str(i + 1) + " Candidat " + str(id_first) + " avec " + str(nb_first) + " voix.")
            return id_first

        # Gérer les égalités ici

        print("Tour " + str(i + 1) + ", élimination du Candidat " + str(id_last) + ".")

        # Prepare for next round
        excluded.append(id_last)
        i += 1


########## ALTERNATIF ##########

def alternatif(df):
    print('Méthode vote alternatif')
    # Init
    excluded = []
    votes = df.shape[1]
    rows = len(df)

    for i in range(rows):
        # Get candidate with lowest first places (and check for absolute majority)
        first_places = df.apply(detect_first_id, args=(excluded, 0))
        counts_first = first_places.value_counts()
        id_last = counts_first.index[-1]
        nb_first = counts_first.iloc[0]
        if (nb_first >= (votes/2 + 1)):
            id_first = counts_first.index[0]
            print("Vainqueur au tour " + str(i + 1) + " Candidat " + str(id_first) + " avec " + str(nb_first) + " voix.")
            return id_first


        print("Tour " + str(i + 1) + ", élimination du Candidat " + str(id_last) + ".")

        # Prepare for next round
        excluded.append(id_last)
        i += 1

########## MAIN ##########

# if __name__ == '__main__':

    # with open('data/profil1.csv', newline='') as profil1:
    #     r = csv.reader(profil1)
    #     data1 = list(r)
    # full_table_condorcet = table_condorcet(data1)
    # print(full_table_condorcet)
    # print("Selon Condorcet, l'élu est le candidat " + str(full_table_condorcet.index(max(full_table_condorcet)) + 1))
    # borda2()

if __name__ == "__main__":
    # Get the start time
    st = time.time()

    # Init df
    profile = input("Choisissez un profil de données:\n1)profil1\n2)profil2\n3)profil3\n")
    method = input("Choisissez une méthode de choix social:\n1)Condorset\n2)Borda\n3)Rounds\n4)Coombs\n5)Alternatif\n6)Save figs\n")

    
    df = pd.read_csv(filepath_or_buffer='data/profil' + profile + '.csv', sep=',', header=None)

    # Launch methods
    if (method == "1"):
        print('##### CONDORSET #####')
        # launch condorset
        # with open('data/profil1.csv', newline='') as profil1:
        #     r = csv.reader(profil1)
        #     data1 = list(r)
    if (method == "2"):
        print('##### BORDA #####')
        # launch borda
    if (method == "3"):
        nbRounds = input('En combien de tours voulez vous effectuer cette méthode ? (1 ou 2)')
        print('##### ROUNDS #####')
        rounds(df, int(nbRounds))
    if (method == "4"):
        print('##### COOMBS #####')
        coombs(df)
    if (method == "5"):
        print('##### ALTERNATIF #####')
        alternatif(df)
    if (method == "6"):
        for i in range(5):
            # Get places of loop index
            ranks = df.iloc[i].value_counts().sort_index()
            # Save
            ranks.plot(kind='bar')
            plt.xlabel("Candidats")
            plt.ylabel("Nombre de rang " + str(i+1))
            plt.suptitle("Nombre de rang " + str(i+1) + " par candidat")
            plt.savefig("figs/" + str(i+1) + "places.png")

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
