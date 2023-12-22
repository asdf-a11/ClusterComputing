import multiprocessing
import os

def Task():
    os.system("python3 Client.py")

if __name__ == "__main__":
    pList = []
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=Task)
        p.start()
        pList.append(p)
