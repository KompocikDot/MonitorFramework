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
        self.initSettings()
        self.Read(init=True)
        self.Check()
        self.mainProcess()       

    def initSettings(self):
        with open('settings.json') as f:
            jsn = load(f)

        self.checkdiffs = jsn['changes']
        self.webhook_url = jsn['webhook']

    def Read(self, init=False) -> list | None:
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


    def Check(self) -> None:
        changes = 0
        for x in self.csv_data:
            if x['id'] == '':
                x['id'] = b2a_hex(urandom(15)).decode('utf-8')
                changes += 1
            
        if changes > 0:
            self.setCsvIds()

    def setCsvIds(self) -> None:
        with open('links.csv', 'w', newline='') as f:
            writer = DictWriter(f, fieldnames=["shop", "url", "timeout", "id"])
            writer.writeheader()
            for x in self.csv_data:
                writer.writerow(x)

    def mainProcess(self) -> None:
        KThread(target=self.mainChecker, name="main").start()
        
    def mainChecker(self) -> None:
        self.threads = {}
        # try:
        self.runNew()
        while True:
            self.checkDifferences()
            sleep(self.checkdiffs)
            

        # except Exception as e:
        #     logging.error(f"Main process crashed [{e}] | Turning off the app")
        #     exit()    

    def runNew(self, custom_list=[]) -> None:
        if not custom_list:
            for x in self.csv_data:
                new = KThread(target=self.placeholder , args=(x,), name=x['id'])
                self.threads[new.name] = new
                self.threads[x['id']].start()
                logging.info(f"Successfully added thread id{x['id']:}")

        else:
            for indx, x in enumerate(custom_list):
                self.added[indx]['id'] = b2a_hex(urandom(15)).decode('utf-8')
                new = KThread(target=self.placeholder , args=(x,), name=x['id'])
                self.threads[new.name] = new
                self.threads[x['id']].start()
                logging.info(f"Successfully added thread id{x['id']:}")

    def checkDifferences(self):
        new_iter = self.Read()
        self.added = [x for x in new_iter if x not in self.csv_data]
        removed = [x for x in self.csv_data if x not in new_iter]
        
        if self.added:
            self.Check()
            self.runNew(self.added)
            self.csv_data = new_iter
            self.setCsvIds()

        if removed:
            self.killThreads(removed)
            self.csv_data = new_iter

    def killThreads(self, to_remove: list):
        for x in to_remove:
            self.threads[x['id']].terminate()
            del self.threads[x['id']]
            logging.info(f"Successfully removed thread id{x['id']:}")

    def placeholder(self, x):
        while True:
            logging.info('bla bla')
            sleep(2)