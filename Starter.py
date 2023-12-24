import multiprocessing
import os

def Task():
    os.system("python Client.py")

if __name__ == "__main__":
    pList = []
    to = multiprocessing.cpu_count()
    for i in range(to):
        p = multiprocessing.Process(target=Task)
        p.start()
        pList.append(p)
