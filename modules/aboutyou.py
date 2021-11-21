from time import sleep

class AboutYou:
     def __init__(self, url: str, timeout: int):
          self.url = url
          self.timeout = timeout
          self.Start()

     def Start(self):
          while True:
               print(self.url)
               sleep(self.timeout)