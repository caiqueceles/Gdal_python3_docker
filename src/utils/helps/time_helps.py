
import time

def print_time(text, tic):
    tac=time.time()
    print(text , ': ' , tac-tic, 'time processing in secund \n ')
    tic=time.time()
    return  tic
