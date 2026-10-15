import threading
import random
import time

sem_ingrediente = threading.Semaphore(1)
sem_agente = threading.Semaphore(0)

ingredientes_agente = ["Tabaco", "Papel", "Fuego"]
ingredientes_fumador = [("Papel", "Fuego"), ("Tabaco", "Fuego"), ("Tabaco", "Papel")]
ingrediente = 3

def fumador(i):
    global ingrediente

    print("[Fumador {i}] Tengo {ingredientes_fumador}. Quedo a la espera de {ingredientes_agente}".format(
                i=i,
                ingredientes_fumador=ingredientes_fumador[i],
                ingredientes_agente=ingredientes_agente[i]
            ))
    while(True):
        sem_ingrediente.acquire()
        if ingrediente == i:
            sem_ingrediente.release()
            print("[Fumador {i}] Ya dispongo de todos los ingredientes. Fumo...".format(i=i))
            time.sleep(5)
            print("[Fumador {i}] He terminado de fumar".format(i=i))
            
            sem_ingrediente.acquire()
            ingrediente = 3
            sem_ingrediente.release()
            
            sem_agente.release()
        else:
            sem_ingrediente.release()
            print("[Fumador {i}] Pongo una pieza de rompecabezas...".format(i=i))
            time.sleep(3)

def agente():
    global ingrediente

    while(True):
        sem_ingrediente.acquire()
        ingrediente = random.randrange(3)
        sem_ingrediente.release()

        print("[Agente] Pongo {ingrediente} encima de la mesa...".format(ingrediente=ingredientes_agente[ingrediente]))
        
        sem_agente.acquire()

threads = []

for f in range(3):
    t_fumador = threading.Thread(target=fumador, args=(f,))
    threads.append(t_fumador)

t_agente = threading.Thread(target=agente)
threads.append(t_agente)

for t in threads:
    t.start()

for t in threads:
    t.join()
