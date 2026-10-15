import threading
import random
import time

N = 10

BUF_ENT = []
BUF_SAL = []

sem_ent = threading.Semaphore(1)
sem_espacio_ent = threading.Semaphore(N)
sem_datos_ent = threading.Semaphore(0)

sem_sal = threading.Semaphore(1)
sem_espacio_sal = threading.Semaphore(N)
sem_datos_sal = threading.Semaphore(0)

def p_lector():
    global BUF_ENT

    pos_buf_ent = 0
    while (True):
        print("[LECTOR] Leo una tarjeta...")
        time.sleep(3)
        ent = random.randbytes(5)

        print("[LECTOR] Tarjeta leída, intento depositar su contenido en BUF_ENT...")
        sem_espacio_ent.acquire()
        sem_ent.acquire()
        BUF_ENT[pos_buf_ent] = ent
        pos_buf_ent = (pos_buf_ent + 1) % N
        sem_datos_ent.release()
        sem_ent.release()
        print("[LECTOR] Contenido de la tarjeta depositado en BUF_ENT.")



def p_ejecutor():
    global BUF_ENT
    global BUF_SAL

    pos_buf_ent = 0
    pos_buf_sal = 0
    while (True):
        print("[EJECUTOR] Intento leer el contenido de BUF_ENT...")
        sem_datos_ent.acquire()
        sem_ent.acquire()
        ent = BUF_ENT[pos_buf_ent]
        pos_buf_ent = (pos_buf_ent + 1) % N
        sem_espacio_ent.release()
        sem_ent.release()
        print("[EJECUTOR] Contenido de BUF_ENT leído.")

        print("[EJECUTOR] Procesando contenido de la tarjeta...")
        time.sleep(15)
        print("[EJECUTOR] Tarjeta procesada.")

        print("[EJECUTOR] Intento escribir la salida en BUF_SAL")
        sem_espacio_sal.acquire()
        sem_sal.acquire()
        BUF_SAL[pos_buf_sal] = ent
        pos_buf_sal = (pos_buf_sal + 1) % N
        sem_datos_sal.release()
        sem_sal.release()
        print("[EJECUTOR] Salida depositada en BUF_SAL")



def p_escritor():
    global BUF_SAL
    
    pos_buf_sal = 0
    while (True):
        print("[ESCRITOR] Intento leer el contenido de BUF_SAL")
        sem_datos_sal.acquire()
        sem_sal.acquire()
        sal = BUF_SAL[pos_buf_sal]
        pos_buf_sal = (pos_buf_sal + 1) % N
        sem_espacio_sal.release()
        sem_sal.release()
        print("[ESCRITOR] Escribiendo {sal} en la salida...".format(sal=sal))
        time.sleep(2)


for i in range(N):
    BUF_ENT.append(None)
    BUF_SAL.append(None)

threads = []

t_lector = threading.Thread(target=p_lector)
threads.append(t_lector)

t_ejecutor = threading.Thread(target=p_ejecutor)
threads.append(t_ejecutor)

t_escritor = threading.Thread(target=p_escritor)
threads.append(t_escritor)

for t in threads:
    t.start()

for t in threads:
    t.join()