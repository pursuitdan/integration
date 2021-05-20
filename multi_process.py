from multiprocessing import Process
import os
import sys
import time
import multiprocessing as mp

# a simple buffer class to test the shared mem components
class Buffer(object):   
     def __init__(self):
          super(Buffer, self).__init__() #inherit from the object class
          self.mgr = mp.Manager() #the mem manager allows for access from multiple processes
          self.active = self.mgr.list() #the shared mem list actually stores the data
          self.lock = mp.Lock() # use locks to support shared access since list is not locked by default

     def add(self, name):
          with self.lock:
               self.active.append(name)
     def remove(self):
          with self.lock:
               return self.active.pop(0)
     
     def ready(self): 
          return (len(self.active) > 0)

     def __str__(self):
          with self.lock:
               return str(self.active)



def stream_sender(filename,buffer):
     info('reader')
     with open(filename,'r') as f:
          for line in f:
               dig = int(line.strip().split()[0]) #specific to the test file
               #print('read {}'.format(dig))
               buffer.add(dig)
               print('writer buff state: {}'.format(buffer))

def stream_receiver(buffer,wait):
     info('receiver')
     for i in range(0,20):
          if buffer.ready():
               print('reader buff state: {}'.format(buffer))
               print(buffer.remove())
          else: 
               print('nothing to read')
               time.sleep(wait)

"""
Helper function to show process data
"""
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


if __name__ == '__main__':
     info('main line')

     #create a buffer managed by the shared memory manager
     b = Buffer()

     # temp variables for testing. 
     filename = 'test.txt'
     wait_time = 1

     # create seperate processes for the streaming to the buffer and reading from the buffer
     writer = Process(target=stream_sender, args=(filename,b))
     reader = Process(target=stream_receiver, args=(b,wait_time))
     writer.start()
     reader.start()

     # the main function controlls the manager, so we have to wait for the children
     # to finish before allowing main to exit or the manager will close and the 
     # children will not be able to use the shared buffer
     writer.join()
     reader.join()

     # add in Untitled 