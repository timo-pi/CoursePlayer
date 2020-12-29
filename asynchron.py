from multiprocessing import Process
import os, time
import psutil

state = 1

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):


    info(name)
    time.sleep(4)
    print("should not print out...")

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('process',))
    p.start()
    p.join()
    p.kill()

