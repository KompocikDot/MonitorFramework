from json import load
from csv import DictReader, DictWriter
from time import sleep
from os import urandom
from binascii import b2a_hex
from kthread import KThread

from modules.aboutyou import AboutYou

class Framework:
     def __init__(self):
          self.csv_data = []
          self.start = True
          self.processes = []
          self.set_start_vals()
          self.set_ids()

     def run(self) -> None:
          KThread(target=self.check_processes, name="MAIN").start()

     def check_processes(self) -> None:
          for x in self.csv_data:
               self.route_module(x)
          print(self.processes)
          while True:
               pass
               
     def route_module(self, csv_data: dict) -> None:
          match csv_data['shop'].lower():
               case "aboutyou":
                    self.processes.append(KThread(target=AboutYou, args=(csv_data['url'], csv_data['timeout'])).start())
               case _ as i:
                    print(f"No shop called {i}")

     def find_changes(self) -> None:
          pass

     def read_ids(self) -> None:
          self.csv_data = []
          with open('links.csv', newline='') as f:
               reader = DictReader(f)
               for v in reader:
                    self.csv_data.append(v)

     def set_ids(self) -> None:
          changes = 0

          with open('links.csv', newline='') as f:
               reader = DictReader(f)
               for v in reader:
                    self.csv_data.append(v)

          for x in self.csv_data:
               if x['id'] == '':
                    changes += 1
                    x['id'] = b2a_hex(urandom(15)).decode('utf-8')

          if changes > 0:
               with open('links.csv', 'w', newline='') as f:
                    fields = ['shop', 'url', 'timeout', 'id']
                    writer = DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(self.csv_data)

     def set_start_vals(self) -> None:
          with open('start.json', 'r') as f:
               f = load(f)

          self.webhook = f['webhook']
          self.check_changes = f['changes']