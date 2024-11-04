# Домашнее задание
# по теме "Блокировки и обработка ошибок"

# Задача "Банковские операции":

import logging
import time
import random
import threading

"""Блокировка на уровне вывода сообщений, 
    для предотвращения склеивания строк"""

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for i in range(100):
            amount_p = random.randint(50, 500)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            else:
                self.balance += amount_p
                logger.info(f"Пополнение: {amount_p}. Баланс: {self.balance} ")
                time.sleep(0.001)

    def take(self):
        for i in range(100):
            amount_s = random.randint(50, 500)
            logger.info(f"Запрос на: {amount_s}")
            if amount_s <= self.balance:
                with self.lock:
                    self.balance -= amount_s
                logger.info(f"Снятие: {amount_s}. Баланс: {self.balance} ")
                time.sleep(0.001)
            else:
                logger.info("Запрос отклонен, недостаточно средств")



bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

logger.info(f'Итоговый баланс: {bk.balance}')


