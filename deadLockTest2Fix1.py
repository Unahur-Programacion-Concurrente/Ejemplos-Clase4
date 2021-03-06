import threading
import time
import random
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class cuentaBancaria():
    def __init__(self, saldo, numero):
        self.saldo = saldo
        self.numeroCuenta = numero
        self.accountLock = threading.Lock()

    def extraccion(self, monto):
        if self.accountLock.locked():
            self.saldo -= monto
        else:
            logging.info(f'Acceso denegado - Debe solicitar lock')

    def deposito(self, monto):
        if self.accountLock.locked():
            self.saldo += monto
        else:
            logging.info(f'Acceso denegado - Debe solicitar lock')

def transferencia(origen, destino, monto):
    if origen.numeroCuenta < destino.numeroCuenta:
        lock1 = origen.accountLock
        lock2 = destino.accountLock
    else:
        lock1 = destino.accountLock
        lock2 = origen.accountLock

    lock1.acquire()
    try:
       # logging.info(f'obtiene el lock {origen.numeroCuenta}')
        logging.info(f'obtiene el lock {lock1}')
        time.sleep(random.randint(0,1)/10)
        lock2.acquire()
        try:
           # logging.info(f'obtiene el lock de cuenta {destino.numeroCuenta}')
            logging.info(f'obtiene el lock de cuenta {lock2}')
            origen.extraccion(monto)
            destino.deposito(monto)
        finally:
            lock2.release()
    finally:
        logging.info(f'Transferencia de cuenta {origen.numeroCuenta} a cuenta {destino.numeroCuenta} , monto {monto} completada')
        lock1.release()

def main():
    cuentas = []
    transferencias = [(1,2),(2,3),(3,1)]
    tareas = []

    for i in range(0,4):
        cuenta = cuentaBancaria(100 * random.randint(1,2), i)
        cuentas.append(cuenta)
        logging.info(f'Saldo inicial Cuenta {cuentas[i].numeroCuenta} : {cuentas[i].saldo}')


    for i in range(0, len(transferencias)):
        tarea = threading.Thread(target=transferencia, args =(cuentas[transferencias[i][0]], cuentas[transferencias[i][1]], 10 * random.randint(1,2)))
        tarea.start()
        tareas.append(tarea)

    for i in range(0,3):
        tareas[i].join()


    for i in range(0,4):
        logging.info(f'Saldo final Cuenta {cuentas[i].numeroCuenta} : {cuentas[i].saldo}')


if __name__ == "__main__":
    main()

