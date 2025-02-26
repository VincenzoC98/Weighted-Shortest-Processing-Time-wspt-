# -*- coding: utf-8 -*-
"""MOLP

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n6DOwC3EeIz0wlePkKGlSrOIaiD9WZ1T

#Istanza
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

macchine =15
jobs = 60
tempi= [
	10,	9,	7,	8,	7,	9,	8,	6,	8,	7,
	9,	6,	9,	5,	5,	3,	3,	5,	3,	5,
	3,	2,	8,	7,	7,	5,	1,	5,	7,	7,
	9,	1,	6,	5,	8,	6,	2,	2,	1,	8,
	6,	5,	3,	7,	7,	5,	1,	7,	1,	6,
	9,	9,	2,	1,	4,	7,	1,	3,	8,	4,


]
pesi= [
    3,   5,   12,  9,   21,  32,  2,   2,   10,  13,
    12,  1,   1,   8,   10,  21,  10,  4,    1,  10,
    13,  10,  9,   8,   10,  4,   23,  10,  12,  9,
    10,  11,  12,  32,  12,  1,   1,    1,  1,   1,
    1,    1,  10,  10,  2,   2,   2,   2,   2,   2,
    3,   5,   12,  9,   21,  32,  2,   2,   10,  13,


]
T = 80

# Creare un ordinamento nell'array utilizzando il rapporto pesi/tempi
ord1 = [(i+1, pesi[i] / tempi[i]) for i in range(jobs)] #Così creo tuple con indice del lavoro e relativo rapporto
#ord = [a / b for a, b in zip(pesi, tempi)]  #Così costruisco l'array ordinamento senza sapere a quale lavoro appartiene il rapporto
print("Ordinamento =",ord1)
ord_dec1 = sorted(ord1, reverse=True, key=lambda x: x[1]) #Ord decrescente ((key=lambda x: x[1]) in sorted applica ordinamento cre o decre per il secondo elemento della lista)
print("Ord. Decrescente =",ord_dec1)
ord_cre1 = sorted(ord1, key=lambda x: x[1]) #Ord crescente
print("Ord. Crescente =",ord_cre1)
import random
ord_ran1 = random.sample(ord1,len(ord1)) #Ord random
print("Ord. Random =",ord_ran1)
#Questo codice dà ordinamento al primo alamento della tupla, non al secondo

"""#Modello Matematico"""

!pip install pulp

#Costruisco la prima soluzione del modello matematico

J = list(range(int(jobs))) #Trasformo un numero n in un array di n elementi (Es.: 3 --> array=[0,1,2])
print(J)
M = list(range(int(macchine)))
import pulp
import numpy as np

# Creazione del problema di ottimizzazione
prob = pulp.LpProblem("Minimizza_costo_scheduling", pulp.LpMinimize)

# Variabili decisionali xjt: 1 se il job j inizia all'istante t, 0 altrimenti
x = {(j, t): pulp.LpVariable(f"x_{j}_{t}", cat='Binary') for j in range(jobs) for t in range(T - tempi[j] + 1)}

# Funzione obiettivo (1): minimizzazione del completamento totale pesato
objective = pulp.lpSum(pesi[j] * t * x[j, t] for j in range(jobs) for t in range(T - tempi[j] + 1)) + pulp.lpSum(pesi[j] * tempi[j] for j in range(jobs))
prob += objective

# Vincolo (2): Ogni job j deve iniziare esattamente una volta durante l'orizzonte
for j in range(jobs):
    prob += pulp.lpSum(x[j, t] for t in range(T - tempi[j] + 1)) == 1, f"vincolo_unico_inizio_{j}"

# Vincolo (3): La somma delle esecuzioni contemporanee non supera la capacità delle macchine
for t in range(T):
    prob += pulp.lpSum(
        x[j, s]
        for j in range(jobs)
        for s in range(max(0, t - tempi[j] + 1), min(t + 1, T - tempi[j] + 1))
    ) <= macchine, f"vincolo_capacita_{t}"

# Vincolo (4): Le variabili xjt devono essere binarie
for j in range(jobs):
    for t in range(T - tempi[j] + 1):
        prob += x[j, t] >= 0
        prob += x[j, t] <= 1

# Risoluzione del problema
prob.solve()

# Stampa dello stato della soluzione
print("Status della soluzione:", pulp.LpStatus[prob.status])

# Stampa del valore della funzione obiettivo
print("Valore della funzione obiettivo (costo totale):", pulp.value(prob.objective))

# Stampa delle variabili decisionali
for j in range(jobs):
    for t in range(T - tempi[j] + 1):
        if pulp.value(x[j, t]) > 0.5:  # Se xjt è 1 (tenendo conto delle possibili imprecisioni numeriche)
            print(f"Il job {j} inizia al tempo {t}")

"""#Euristico"""

#Imposto l'ordine con cui voglio processare i job. Poi un ciclo for sull'array jobs mi calcola il prodotto di pesi per tempo di ogni job.
ord_scelto = ord_ran1
z=0
tempo_macc=[0]*macchine
#print(len(ord_scelto))
for i in range(jobs):
  z+=pesi[i]*tempi[i]
for i in range(len(ord_scelto)):
      k=tempo_macc.index(min(tempo_macc)) #k mi ridà l'indice del numero più piccolo dell'array tempo do ogni macchina
      a=tempo_macc[k]
      tempo_macc[k]=tempo_macc[k]+tempi[ord_scelto[i][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
      #print(tempi[ord_scelto[i][0]-1])
      z+=a*pesi[ord_scelto[i][0]-1]+tempi[ord_scelto[i][0]-1] #calcolo la funzione obiettivo
      #print("Il lavoro",ord_scelto[i][0]-1,"viene assegnato alla macchina",k+1,"al tempo",a)
      #print("k=",k)
      #print("Array tempo macchine=",tempo_macc)
      #print("z=",z)
      #print("istante di assegnamento=",a)

k=tempo_macc.index(max(tempo_macc)) #k ora mi ridà l'indice del tempo di ogni macchina dove il tempo è maggiore
#print("Array tempo macchine=",tempo_macc)
if tempo_macc[k]<T:
  print("Soluzione Ottima Trovata!")
  #print(tempo_macc[k])
else:
  print("Soluzione Non Trovata!")
print("Sol. Euristica:",z)

"""#Ricerca Locale - Swap"""

# Implemento ricerca locale per avere una soluzione

ord_scelto_rl=ord_ran1
z_rl=0
z_rl_tabella = [[0 for _ in range(jobs)] for _ in range(jobs)]
improvement=False
while True:
  improvement=False
  for i in range(len(ord_scelto_rl)):
     for j in range(len(ord_scelto_rl)): #prendo il primo e lo metto al posto del primo, prendo il secondo e lo metto al posto del primo. prendo il terzo...
      if j<i: #La matrice che sto cercando di ottenere è triangolare alta
       j=i
      z_rl=0
      tempo_macc_rl=[0]*macchine
      temp = ord_scelto_rl[j]   #scambiamo tutti i job con tutti
      ord_scelto_rl[j] = ord_scelto_rl[i]
      ord_scelto_rl[i] = temp
      for x in range(jobs):   #calcoliamo tutte le sol per ogni swap
        z_rl+=pesi[x]*tempi[x]
      for y in range(len(ord_scelto_rl)):
        k=tempo_macc_rl.index(min(tempo_macc_rl)) #k mi ridà l'indice del numero più piccolo dell'array tempo di ogni macchina
        a=tempo_macc_rl[k]  #a è il tempo della macchina più scarica
        tempo_macc_rl[k]=tempo_macc_rl[k]+tempi[ord_scelto_rl[y][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
        z_rl+=a*pesi[ord_scelto_rl[y][0]-1]+tempi[ord_scelto_rl[y][0]-1] #calcolo la funzione obiettivo
      z_rl_tabella[i][j]=[z_rl,i,j] #ogni sol viene messa in una tabella, con l'indicazione degli indici scambiati
      temp = ord_scelto_rl[j]  #una volta misurata la sol rimetto a posto l'ordine
      ord_scelto_rl[j] = ord_scelto_rl[i]
      ord_scelto_rl[i] = temp
  z_rl_tabella= [valore for riga in z_rl_tabella for valore in riga if valore != 0] #trasforma la tabella, liste di liste, in un unico array escludendo lo zero
  z_min=sorted(z_rl_tabella)[:1] #trova il valore più piccolo nell'array
  z_rl_tabella=[[0 for _ in range(jobs)] for _ in range(jobs)] #resetto la tabella
  if z_min[0][0]<z: #se la sol dello swap più conveniente è migliore della sol euristica, muto l'ordinamento per rendere quello swap parte del nuovo ordinamento su cui verranno calcolate le sol euristiche
    improvemet=True
    help=ord_scelto_rl[z_min[0][2]]
    ord_scelto_rl[z_min[0][2]]=ord_scelto_rl[z_min[0][1]]
    ord_scelto_rl[z_min[0][1]]=help
    z=z_min[0][0]
    print("Sposto il job",z_min[0][2],"al posto del",z_min[0][1])
    print("Incumbent Solution:",z)
  else:
    break
print("Soluzione Ottima RL:",z)

"""

#Multi-Start

"""

#Implemento il multi-start, reiterare una disposizione random dei job e cercare quella migliore
import random
tempo_macc_ms=[0]*macchine
iter=int(input("Inserisci numero di iterazioni MS:"))
z_ms_array=[0]*iter
for j in range(iter): #per un numero di iterazioni deciso a priori
  tempo_macc_ms=[0]*macchine #resettiamo il carico delle macchine perché verrà sempre riaggiornato
  z_ms=0 #stessa cosa per la z_ms
  ord_rand1 = random.sample(ord1,len(ord1)) #Ord random
  for i in range(jobs): #questi due for servono per il calcolo della z_ms, che verrà inserita in un array di len = al numero di iterazioni
   z_ms+=pesi[i]*tempi[i]
  for i in range(len(ord_rand1)):
   k=tempo_macc_ms.index(min(tempo_macc_ms)) #k mi ridà l'indice del numero più piccolo dell'array tempo di ogni macchina
   a=tempo_macc_ms[k]
   tempo_macc_ms[k]=tempo_macc_ms[k]+tempi[ord_rand1[i][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
   z_ms+=a*pesi[ord_rand1[i][0]-1]+tempi[ord_rand1[i][0]-1] #calcolo la funzione obiettivo
   z_ms_array[j]=z_ms

k=tempo_macc_ms.index(max(tempo_macc_ms)) #k ora mi ridà l'indice del tempo di ogni macchina dove il tempo è maggiore
#print("Array tempo macchine=",tempo_macc)
if tempo_macc_ms[k]<T:
  print("Soluzione Ottima Trovata!")
  #print(tempo_macc[k])
else:
  print("Soluzione Non Trovata!")
print("Sol. Ord. Random =",z_ms_array)
#print("Array Tempo=",tempo_macc_ms)
print("Soluzione MS=",min(z_ms_array))

"""#Metaeuristico - Alg. Genetico"""

import random

z_ge=0
z_ge_fi=0
tempo_macc_ge=[0]*macchine
iter_ge=800 #il genetico parte da una popolazione di individui
z_ge_array=[0]*iter_ge
ord_array_ge=[0]*iter_ge
z_ge_fi_array=[[0 for _ in range(iter_ge)] for _ in range(iter_ge)]
ord_array_ge_fi=[[0 for _ in range(iter_ge)] for _ in range(iter_ge)]
z_min_genitori=0
z_min_figlio=0
miglioramento=True


for j in range(iter_ge): #per un numero di iterazioni deciso a priori
  tempo_macc_ge=[0]*macchine #resettiamo il carico delle macchine perché verrà sempre riaggiornato
  z_ge=0 #stessa cosa per la z_ge
  ord_rand1 = random.sample(ord1,len(ord1)) #Ord random
  ord_array_ge[j]=ord_rand1 #inserisco l'ordinamento nell'array ordinamenti
  for i in range(jobs): #questi due for servono per il calcolo della z_ms, che verrà inserita in un array di len = al numero di iterazioni
    z_ge+=pesi[i]*tempi[i]
  for i in range(len(ord_rand1)):
    k=tempo_macc_ge.index(min(tempo_macc_ge)) #k mi ridà l'indice del numero più piccolo dell'array tempo di ogni macchina
    a=tempo_macc_ge[k]
    tempo_macc_ge[k]=tempo_macc_ge[k]+tempi[ord_rand1[i][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
    z_ge+=a*pesi[ord_rand1[i][0]-1]+tempi[ord_rand1[i][0]-1] #calcolo la funzione obiettivo
    z_ge_array[j]=[z_ge,j] #mettiamo le sol in un array
z_min_genitori=min(z_ge_array) #selezioniamo la sol migliore dell'insieme di partenza
print("Sol. Insieme Genitori di Partenza=",z_min_genitori)

while miglioramento==True:
  for a in range(iter_ge):
   for b in range(iter_ge):
    z_ge_fi=0
    array_gen1=0
    array_gen2=0
    array_gen1=ord_array_ge[a]
    array_gen2=ord_array_ge[b]
    posizione_sc=random.randint(0, jobs)
    array_figlio=array_gen1[:posizione_sc] + list((set(array_gen2)-set(array_gen1[:posizione_sc]))) #generiamo un figlio per ogni coppia di array genitori (iter_ge*iter_ge numero di soluzioni)
    ord_array_ge_fi[a][b]=array_figlio
    tempo_macc_figli=[0]*macchine
    for x in range(jobs):   #calcoliamo tutte le sol per ogni incrocio
     z_ge_fi+=pesi[x]*tempi[x]
    for y in range(len(array_figlio)):
     k=tempo_macc_figli.index(min(tempo_macc_figli)) #k mi ridà l'indice del numero più piccolo dell'array tempo di ogni macchina
     p=tempo_macc_figli[k]  #p è il tempo della macchina più scarica
     tempo_macc_figli[k]=tempo_macc_figli[k]+tempi[array_figlio[y][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
     z_ge_fi+=p*pesi[array_figlio[y][0]-1]+tempi[array_figlio[y][0]-1] #calcolo la funzione obiettivo
     z_ge_fi_array[a][b]=[z_ge_fi,a,b,posizione_sc]
  z_ge_fi_array=[valore for riga in z_ge_fi_array for valore in riga if valore != 0]
  z_ge_migliori=sorted(z_ge_fi_array)[:iter_ge] #prendo le sol dei migliori incroci per creare un nuovo insieme
  z_min_figlio=min(z_ge_fi_array) #prendo la miglior soluzione figlia
  z_ge_fi_array=[[0 for _ in range(iter_ge)] for _ in range(iter_ge)]
  print("Miglio Sol. Insieme Figli=",z_min_figlio)
  if z_min_figlio[0]<z_min_genitori[0]: #se la sol figlia è migliore della sol dei genitori
   miglioramento=True
   z_min_genitori=z_min_figlio #c'è un miglioramento e creiamo il nuovo insieme figli
   for d in range(iter_ge):
     indice_gen_fi1=z_ge_migliori[d][1]
     indice_gen_fi2=z_ge_migliori[d][2]
     posizione_sc_fi=z_ge_migliori[d][3]
     array_gen_fi1=ord_array_ge[indice_gen_fi1]
     array_gen_fi2=ord_array_ge[indice_gen_fi2]
     soluzione_tempo=array_gen_fi1[:posizione_sc_fi] + list((set(array_gen_fi2)-set(array_gen_fi1[:posizione_sc_fi])))
     ord_array_ge[d]=soluzione_tempo
  else:
   break

k=tempo_macc_ge.index(max(tempo_macc_ge))
if tempo_macc_ge[k]<T:
  print("Soluzione Ottima Trovata!")
else:
  print("Soluzione Non Trovata!")
#print("Sol. Ge. Ord. Random =",z_ge_array)
print("Sol. Algoritmo Gen.=",min(z_min_figlio,z_min_genitori))

import random

z_ge=0
z_ge_fi=0
tempo_macc_ge=[0]*macchine
iter_ge=800 #il genetico parte da una popolazione di individui
z_ge_array=[0]*iter_ge
ord_array_ge=[0]*iter_ge
z_ge_fi_array=[0]*iter_ge
ord_array_fi=[[0 for _ in range(iter_ge)] for _ in range(iter_ge)]
z_genitori=0
z_figlio=0
miglioramento=True


for j in range(iter_ge): #per un numero di iterazioni deciso a priori
  tempo_macc_ge=[0]*macchine #resettiamo il carico delle macchine perché verrà sempre riaggiornato
  z_ge=0 #stessa cosa per la z_ge
  ord_rand1 = random.sample(ord1,len(ord1)) #Ord random
  ord_array_ge[j]=ord_rand1 #inserisco l'ordinamento nell'array ordinamenti
  for i in range(jobs): #questi due for servono per il calcolo della z_ms, che verrà inserita in un array di len = al numero di iterazioni
    z_ge+=pesi[i]*tempi[i]
  for i in range(len(ord_rand1)):
    k=tempo_macc_ge.index(min(tempo_macc_ge)) #k mi ridà l'indice del numero più piccolo dell'array tempo di ogni macchina
    a=tempo_macc_ge[k]
    tempo_macc_ge[k]=tempo_macc_ge[k]+tempi[ord_rand1[i][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
    z_ge+=a*pesi[ord_rand1[i][0]-1]+tempi[ord_rand1[i][0]-1] #calcolo la funzione obiettivo
    z_ge_array[j]=[z_ge,j] #mettiamo le sol in un array
z_genitori=min(z_ge_array) #selezioniamo la sol migliore dell'insieme di partenza
print("Sol. Insieme Genitori di Partenza=",z_genitori[0])

while miglioramento==True: #ho trovato le due soluzioni figlie per coppia di genitori e messe tutte in un unico array, trovare il modo per calcolare la sol eurisitica e confrontarla con la sol dei genitori potrebbe risolvere l'algoritmo
  for j in range(0,iter_ge,2):
    #print(j)
    array_genitore1=ord_array_ge[j]
    #print(array_genitore1)
    array_genitore2=ord_array_ge[j+1]
    posizione_sc1=random.randint(1, jobs-1)
    array_figlio1=array_genitore1[:posizione_sc1] + list((set(array_genitore2)-set(array_genitore1[:posizione_sc1])))
    posizione_sc2=random.randint(1, jobs-1)
    array_figlio2=array_genitore2[:posizione_sc2] + list((set(array_genitore1)-set(array_genitore2[:posizione_sc2])))
    ord_array_fi[j]=array_figlio1
    ord_array_fi[j+1]=array_figlio2
  for h in range(len(ord_array_fi)):
    tempo_macc_figli2=[0]*macchine
    for x in range(jobs):   #calcoliamo tutte le sol per ogni figlio
      z_ge_fi+=pesi[x]*tempi[x]
    for y in range(len(ord_array_fi[h])):
      ord_array_figli=ord_array_fi[h]
      k=tempo_macc_figli2.index(min(tempo_macc_figli2)) #k mi ridà l'indice del numero più piccolo dell'array tempo di ogni macchina
      p=tempo_macc_figli2[k]  #p è il tempo della macchina più scarica
      tempo_macc_figli2[k]=tempo_macc_figli2[k]+tempi[ord_array_figli[y][0]-1] #nella posizione dell'indice k viene sommato l'i-esimo job nell'ordinamento
      z_ge_fi+=p*pesi[ord_array_figli[y][0]-1]+tempi[ord_array_figli[y][0]-1] #calcolo la funzione obiettivo
      z_ge_fi_array[h]=[z_ge_fi,h] #mettiamo le sol in un array
    tempo_macc_figli2=[0]*macchine
    z_ge_fi=0
  z_figlio=min(z_ge_fi_array)
  #print(z_ge_fi_array)
  print("Sol. Insieme Figli=",z_figlio[0])
  if z_figlio<z_genitori:
    z_genitori=z_figlio
    miglioramento=True
    ord_array_ge=ord_array_fi
  else:
    break
print("Sol. Algoritmo Gen.=",min(z_figlio,z_genitori)[0])