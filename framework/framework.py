from json import load
from modules.aboutyou import AboutYou
from multiprocessing import Process
from csv import DictReader, DictWriter
from time import sleep
from os import urandom
from binascii import b2a_hex

class Framework:
     def __init__(self):
          self.csv_data = []
          self.start = True
          self.SetStartVals()
          self.processes = []
          self.SetIds()

     def Run(self, *args) -> None:
          Process(target=self.CheckProcess).start()

     def CheckProcess(self):
          if self.start:
               self.start = False

               for x in self.csv_data:
                    match x['shop'].lower():
                         case 'aboutyou':
                              p = Process(target=AboutYou.Start, args=(x['url'], int(x['timeout']),))
                         case _:
                              print('Unknown shop')
                              continue

                    self.processes.append({'id': x['id'], 'process': p})
                    
               for x in self.processes:
                    x['process'].start()
                    print('wystartowano')

          else:
               csv_ids = []
               processes_ids = []
               for x in self.csv_data:
                    csv_ids.append(x['id'])
               for x in self.processes:
                    processes_ids.append(x['id'])

               difference = list(set(processes_ids) - set(csv_ids))
               
               if len(difference) > 0:
                    for id in difference:
                         self.TerminateProcess(id)

     def TerminateProcess(self, id: str):
          for x in self.processes:
               if self.processes['id'] == id:
                    x['process'].terminate()

     def ReadIds(self):
          self.csv_data = []
          with open('links.csv', newline='') as f:
               reader = DictReader(f)
               for v in reader:
                    self.csv_data.append(v)

     def SetIds(self):
          with open('links.csv', newline='') as f:
               reader = DictReader(f)
               for v in reader:
                    self.csv_data.append(v)

          for x in self.csv_data:
               if x['id'] == '':
                    x['id'] = b2a_hex(urandom(15)).decode('utf-8')

          with open('links.csv', 'w', newline='') as f:
               fields = ['shop', 'url', 'timeout', 'id']
               writer = DictWriter(f, fieldnames=fields)
               writer.writeheader()
               writer.writerows(self.csv_data)

     def SetStartVals(self) -> None:
          with open('start.json', 'r') as f:
               f = load(f)

          self.webhook = f['webhook']
          self.check_changes = f['changes']