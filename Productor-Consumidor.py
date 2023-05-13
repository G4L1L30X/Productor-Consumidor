import multiprocessing
import time
import random

def productor(buffer, semaforo, terminar):
    for i in range(10):
        item = random.randint(0, 100)
        semaforo.acquire()
        buffer.append(item)
        print(f"Productor agregó el elemento {item} al buffer")
        semaforo.release()
        time.sleep(random.uniform(0.5, 1.5))
    semaforo.acquire()
    terminar.value = True # indicar al consumidor que debe terminar
    semaforo.release()

def consumidor(buffer, semaforo, terminar):
    while True:
        semaforo.acquire()
        if len(buffer) > 0:
            item = buffer.pop(0)
            print(f"Consumidor eliminó el elemento {item} del buffer")
        semaforo.release()
        time.sleep(random.uniform(0.5, 1.5))
        if terminar.value == True and len(buffer) == 0:
            break

if __name__ == "__main__":
    buffer = multiprocessing.Manager().list()
    semaforo = multiprocessing.Semaphore(1)
    terminar = multiprocessing.Value('b', False) # bandera de terminación
    
    p = multiprocessing.Process(target=productor, args=(buffer, semaforo, terminar))
    c = multiprocessing.Process(target=consumidor, args=(buffer, semaforo, terminar))
    
    p.start()
    c.start()
    
    p.join()
    c.join()
