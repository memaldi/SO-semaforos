import threading
import time

N = 15 # Sillas disponibles en la sala de espera
C = 50 # Número de clientes que llegarán a la barbería.

sem_sala = threading.Semaphore(N)
sem_silla = threading.Semaphore(1)

def cliente(i):
    print("[Cliente {cliente}] Llego a la barbería".format(cliente=i))
    
    sem_sala.acquire()
    print("[Cliente {cliente}] Paso a la sala de espera".format(cliente=i))
    
    sem_silla.acquire()
    print("[Cliente {cliente}] Paso a la silla del barbero".format(cliente=i))
    sem_sala.release()
    
    print("[Cliente {cliente}] Me cortan el pelo".format(cliente=i))
    time.sleep(5)
    print("[Cliente {cliente}] Me marcho".format(cliente=i))
    
    sem_silla.release()


threads = []

for c in range(C):
    t_cliente = threading.Thread(target=cliente, args=(c,))
    threads.append(t_cliente)

for t in threads:
    t.start()

for t in threads:
    t.join()