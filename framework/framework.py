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
          self.processes = []
          self.SetStartVals()
          self.SetIds()

     def Run(self, *args) -> None:
          self.CheckProcess()

     def CheckProcess(self):
          while True:
               if self.start:
                    self.start = False
                    p = Process(target=self.CheckProcess)
                    self.processes.append({'id': 'MAIN', 'process': p})
                    
                    for x in self.csv_data:
                         match x['shop'].lower():
                              case 'aboutyou':
                                   p = Process(target=AboutYou, args=(x['url'], int(x['timeout'])))
                              case _:
                                   print('Unknown shop')
                                   

                         self.processes.append({'id': x['id'], 'process': p})

                    for x in self.processes:
                         x['process'].start()

               else:
                    self.ReadIds()
                    csv_ids, processes_ids = [], []
                    for x in self.csv_data:
                         csv_ids.append(x['id'])
                    for x in self.processes:
                         processes_ids.append(x['id'])

                    difference = list(set(processes_ids) - set(csv_ids))
                    print(difference)
                    if len(difference) > 0:
                         for id in difference:
                              if id != "MAIN":
                                   print(f"terminating {id =}")
                                   self.TerminateProcess(id)

                    sleep(self.check_changes)

     def TerminateProcess(self, id: str):
          print(self.processes)
          for index, value in enumerate(self.processes):
               if value['id'] == id:
                    try:
                         value['process'].terminate()
                    except AttributeError:
                         self.processes.pop(index)
                         print(self.processes)
                         pass

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