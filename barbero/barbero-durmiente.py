import threading
import time

N = 15 # Sillas disponibles en la sala de espera
C = 20 # Número de clientes que llegarán a la barbería.

sem_sala = threading.Semaphore(N)
sem_silla = threading.Semaphore(1)
sem_cliente = threading.Semaphore(0)
sem_barbero = threading.Semaphore(0)

def cliente(i):
    print("[Cliente {cliente}] Llego a la barbería".format(cliente=i))
    sem_sala.acquire()
    
    print("[Cliente {cliente}] Paso a la sala de espera".format(cliente=i))
    sem_silla.acquire()
    
    print("[Cliente {cliente}] Paso a la silla del barbero".format(cliente=i))
    sem_sala.release()

    print("[Cliente {cliente}] Despierto al barbero...".format(cliente=i))
    sem_barbero.release()

    print("[Cliente {cliente}] Me cortan el pelo".format(cliente=i))
    sem_cliente.acquire()
    
    print("[Cliente {cliente}] Me marcho".format(cliente=i))
    sem_silla.release()

def barbero():
    while(True):
        sem_barbero.acquire()
        print("[Barbero] Me despierto y corto el pelo a un cliente")
        time.sleep(5)
        print("[Barbero] Cliente terminado, intento dormirme...")
        sem_cliente.release()
    
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