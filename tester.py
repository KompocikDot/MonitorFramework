from multiprocessing import Process
from time import sleep

def loop():
     l = 0
     while True:
          print(l)
          l += 1
          sleep(1)

def main():
     for x in range(5):
          Process(target=)

if __name__ == '__main__':
     main()
