from json import load
from time import sleep
from os import name, urandom
from csv import DictReader, DictWriter
import logging
from sys import exit

from binascii import b2a_hex
from kthread import KThread

logging.basicConfig(format="[%(asctime)s] [Thread: %(threadName)s] [%(message)s]", level=logging.DEBUG)

class Framework:
    def __init__(self):
        self.init_settings()
        self.read(init=True)
        self.check()
        self.main_process()       

    def init_settings(self):
        with open('settings.json') as f:
            jsn = load(f)

        self.checkdiffs = jsn['changes']
        self.webhook_url = jsn['webhook']

    def read(self, init=False) -> list | None:
        if init:
            self.csv_data = []
            with open('links.csv', newline='') as f:
                for x in DictReader(f):
                    self.csv_data.append(x)
        else:
            temp = []
            with open('links.csv', newline='') as f:
                for x in DictReader(f):
                    temp.append(x)
                
            return temp


    def check(self) -> None:
        changes = 0
        for x in self.csv_data:
            if x['id'] == '':
                x['id'] = b2a_hex(urandom(15)).decode('utf-8')
                changes += 1
            
        if changes > 0:
            self.set_csv_ids()

    def set_csv_ids(self) -> None:
        with open('links.csv', 'w', newline='') as f:
            writer = DictWriter(f, fieldnames=["shop", "url", "timeout", "id"])
            writer.writeheader()
            for x in self.csv_data:
                writer.writerow(x)

    def main_process(self) -> None:
        KThread(target=self.main_checker, name="main").start()
        
    def main_checker(self) -> None:
        self.threads = {}
        try:
            self.run_new()
            while True:
                self.check_differences()
                sleep(self.checkdiffs)


        except Exception as e:
            logging.error(f"Main process crashed [{e}] | Turning off the app")
            exit()    

    def run_new(self, custom_list=[]) -> None:
        if not custom_list:
            for x in self.csv_data:
                new = KThread(target=self.placeholder , args=(x, self.webhook_url), name=x['id'])
                self.threads[new.name] = new
                self.threads[x['id']].start()
                logging.info(f"Successfully added thread id{x['id']:}")

        else:
            for indx, x in enumerate(custom_list):
                self.added[indx]['id'] = b2a_hex(urandom(15)).decode('utf-8')
                new = KThread(target=self.placeholder , args=(x, self.webhook_url), name=x['id'])
                self.threads[new.name] = new
                self.threads[x['id']].start()
                logging.info(f"Successfully added thread id{x['id']:}")

    def check_differences(self) -> None:
        new_iter = self.read()
        self.added = [x for x in new_iter if x not in self.csv_data]
        removed = [x for x in self.csv_data if x not in new_iter]
        
        if self.added:
            self.check()
            self.run_new(self.added)
            self.csv_data = new_iter
            self.set_csv_ids()

        if removed:
            self.kill_threads(removed)
            self.csv_data = new_iter

    def kill_threads(self, to_remove: list) -> None:
        for x in to_remove:
            self.threads[x['id']].terminate()
            del self.threads[x['id']]
            logging.info(f"Successfully removed thread id{x['id']:}")

    def placeholder(self, x, y) -> None:
        while True:
            logging.info('bla bla')
            sleep(2)