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