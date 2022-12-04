from array import array
from re import I

import numpy as np


G = ("T", "N", "R", "S")

nonTerminals = ["NP", "VP", "Nominal", "Det",
                "Noun", "PP", "S", "Verb", "Preposition"]

terminals = ["time", "flies", "like", "an", "arrow"]

Rules = {
    "S": [["NP", "VP", 0.8]],
    "NP": [["time", 0.002], ["flies", 0.002], ["arrow", 0.002], ["Det", "Nominal", 0.3], ["Nominal", "Nominal", 0.2]],
    "Nominal": [["time", 0.002], ["flies", 0.002], ["arrow", 0.002], ["Nominal", "Noun", 0.1], ["Nominal", "PP", 0.2]],
    "VP": [["time", 0.004], ["flies", 0.008], ["like", 0.008], ["Verb", "NP", 0.3], ["Verb", "PP", 0.2]],
    "PP": [["Preposition", "NP", 0.1]],
    "Verb": [["time", 0.01], ["flies", 0.02], ["like", 0.02]],
    "Noun": [["time", 0.01], ["flies", 0.01], ["arrow", 0.01]],
    "Det": [["an", 0.05]],
    "Preposition": [["like", 0.05]]
}


def createTable(sentence):

    n = len(sentence)
    syntaxTable = np.zeros((n, n), dtype=array)
    compTable = np.zeros((n, n), dtype=array)

    # Primera diagonal

    for i in range(0, n):
        auxArr = []
        for rule in Rules.items():
            for element in rule[1]:
                if sentence[i] == element[0]:
                    app = [rule[0], element[1]]
                    auxArr.append(app)

        syntaxTable[i, i] = auxArr
        compTable[i, i] = "VAL"
    # Auxiliar de reglas

    R2 = []
    for i in Rules.items():
        for element in i[1]:
            if len(element) > 2:
                app = [i[0], element]
                R2.append(app)

    # Resto de las diagonales

    for i in range(1, n):

        x = 1
        C1 = i
        startp = 0

        for j in range(i, n):

            auxArr = []
            compArr = []
            b = x
            numComp = i
            start2 = j - numComp

            while (numComp > 0):

                a1 = syntaxTable[startp][start2]
                a2 = syntaxTable[b][j]

                for rule in R2:

                    aux = rule[1]

                    for z in range(0, len(a1)):

                        for g in range(0, len(a2)):
                            val_uno = a1[z][0]
                            val_dos = a2[g][0]
                            if (aux[0] == val_uno and aux[1] == val_dos):
                                e1 = float(a1[z][1])
                                e2 = float(a2[g][1])
                                e3 = float(aux[2])
                                r = e1 * e2 * e3
                                app = [rule[0], r]
                                app2 = [(val_uno, (startp, start2)),
                                        (val_dos, (b, j))]
                                auxArr.append(app)
                                compArr.append(app2)

                numComp -= 1
                start2 += 1
                b += 1

            syntaxTable[startp][C1] = auxArr
            compTable[startp][C1] = compArr

            x += 1
            C1 += 1
            startp += 1
    max = -1
    idx = 0
    if not syntaxTable[0,n-1]:
        return "not possible"
    print(syntaxTable[0,n-1][idx])
    for i, element in enumerate(syntaxTable[0,n-1]):
        if element[0] == "S" and (element[1] > max):
            max = element[1] 
            idx = i

    def recursiveStuff(s, f, idx):
        for parts in compTable[s,f][idx]:
            try:
                nont, idxs = parts
            except:
                pass
            s, f = idxs
            if s == f: 
                print(sentence[s], " ", nont)
                continue
            for i, element in enumerate(syntaxTable[s,f]):
                if element[0] == nont:
                    max = element[1] 
                    idx = i
        try:
            recursiveStuff(s, f, idx)
            return True
        except:
            return False
    recursiveStuff(0, n-1, idx)
    
    return "possible"
	
sentence = "Time flies like an arrow"
sentence = sentence.lower()
sentence = sentence.split()

print(createTable(sentence))
