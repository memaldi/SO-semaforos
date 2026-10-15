import threading
import time

N = 15 # Sillas disponibles en la sala de espera
C = 50 # Número de clientes que llegarán a la barbería.

sem_sillas_disponibles = threading.Semaphore(1)
sem_silla = threading.Semaphore(1)
sem_cliente = threading.Semaphore(0)
sem_barbero = threading.Semaphore(0)

sillas_disponibles = N

def cliente(i):
    global sillas_disponibles

    print("[Cliente {cliente}] Llego a la barbería".format(cliente=i))
    sem_sillas_disponibles.acquire()
    if (sillas_disponibles > 0):  
        print("[Cliente {cliente}] Paso a la sala de espera".format(cliente=i))
        sillas_disponibles -= 1
        sem_sillas_disponibles.release()
        
        sem_silla.acquire()
        print("[Cliente {cliente}] Paso a la silla del barbero".format(cliente=i))

        sem_sillas_disponibles.acquire()
        sillas_disponibles += 1
        sem_sillas_disponibles.release()

        print("[Cliente {cliente}] Despierto al barbero...".format(cliente=i))
        sem_cliente.release()

        print("[Cliente {cliente}] Me cortan el pelo".format(cliente=i))
        sem_barbero.acquire()
    
        print("[Cliente {cliente}] Me marcho con el pelo cortado".format(cliente=i))
        sem_silla.release()
    else:
        sem_sillas_disponibles.release()
        print("[Cliente {cliente}] No hay sitio en la sala de espera, me marcho a otra barbería".format(cliente=i))
    

def barbero():
    while(True):
        sem_cliente.acquire()
        print("[Barbero] Me despierto y corto el pelo a un cliente")
        time.sleep(5)
        print("[Barbero] Cliente terminado, me duermo...")
        sem_barbero.release()
    
threads = []

for c in range(C):
    t_cliente = threading.Thread(target=cliente, args=(c,))
    threads.append(t_cliente)

t_barbero = threading.Thread(target=barbero)
threads.append(t_barbero)

for t in threads:
    t.start()

for t in threads:
    t.join()