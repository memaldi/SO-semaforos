import threading
import random
import time

sem_fumadores = []
sem_agente = threading.Semaphore(1)
agente_bloqueado = False

ingredientes_agente = ["Tabaco", "Papel", "Fuego"]
ingredientes_fumador = [("Papel", "Fuego"), ("Tabaco", "Fuego"), ("Tabaco", "Papel")]

def fumador(i):
    global agente_bloqueado

    print("[Fumador {i}] Tengo {ingredientes_fumador}. Quedo a la espera de {ingredientes_agente}".format(
                i=i,
                ingredientes_fumador=ingredientes_fumador[i],
                ingredientes_agente=ingredientes_agente[i]
            ))
    while(True):
        sem_fumadores[i].acquire()
        print("[Fumador {i}] Ya dispongo de todos los ingredientes. Fumo...".format(i=i))
        time.sleep(5)
        print("[Fumador {i}] He terminado de fumar".format(i=i))

        sem_agente.acquire()
        agente_bloqueado = False
        sem_agente.release()

def agente():
    global agente_bloqueado

    while(True):
        sem_agente.acquire()
        if not agente_bloqueado:
            sem_agente.release()
            ingrediente = random.randrange(3)
            print("[Agente] Pongo {ingrediente} encima de la mesa...".format(ingrediente=ingredientes_agente[ingrediente]))
            
            sem_agente.acquire()
            agente_bloqueado = True
            sem_agente.release()
            
            sem_fumadores[ingrediente].release()
        else:
            sem_agente.release()
            print("[Agente] Pongo una pieza de rompecabezas...")
            time.sleep(3)
            

for i in range(3):
    sem = threading.Semaphore(0)
    sem_fumadores.append(sem)

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
