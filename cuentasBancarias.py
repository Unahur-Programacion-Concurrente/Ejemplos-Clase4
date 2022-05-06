# Programa que maneje cuentas bancarias
# Que implemente operaciones de deposito, extracción y transferencia (entre dos cuentas)

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
            logging.info(f'Acceso denegado - Debe solicitar el lock')

    def deposito(self, monto):
        if self.accountLock.locked():
            self.saldo += monto
        else:
            logging.info(f'Acceso denegado - Debe solicitar el lock')

def transferencia(origen, destino, monto):
    origen.accountLock.acquire()
    try:
        destino.accountLock.acquire()
        try:
            origen.extraccion(monto)
            destino.deposito(monto)
            logging.info(f'Transferencia de cuenta {origen.numeroCuenta} a cuenta {destino.numeroCuenta} , monto {monto} completada')
        finally:
            destino.accountLock.release()
    finally:
        origen.accountLock.release()

def funcion1(origen, destino, monto):
    origen.extraccion(monto)
    destino.deposito(monto)
    logging.info(f'Funcion1 transfirio de cuenta {origen.numeroCuenta} a cuenta {destino.numeroCuenta} , monto {monto} completada')

def main():
    cuentas = []
    transferencias = [(1,2),(1,2),(0,3)]
    tareas = []
    tareas2 = []

    for i in range(0,4):
        cuenta = cuentaBancaria(100 * random.randint(1,2), i)
        cuentas.append(cuenta)

        logging.info(f'Saldo inicial Cuenta {cuentas[i].numeroCuenta} : {cuentas[i].saldo}')

# Lanzar hilos tranferencia

    for i in range(0, len(transferencias)):
        tarea = threading.Thread(target=transferencia, args =(cuentas[transferencias[i][0]], cuentas[transferencias[i][1]], 10 * random.randint(1,2)))
        tarea.start()
        tareas.append(tarea)
        tarea2 = threading.Thread(target=funcion1, args =(cuentas[transferencias[i][0]], cuentas[transferencias[i][1]], 10))
        tarea2.start()
        tareas2.append(tarea2)

    for i in range(0, len(transferencias)):
        tareas[i].join()
        tareas2[i].join()

    for i in range(0,4):
        logging.info(f'Saldo final Cuenta {cuentas[i].numeroCuenta} : {cuentas[i].saldo}')


if __name__ == "__main__":
    main()