from subprocess import Popen
from multiprocessing import Process
import subprocess
import time
from threading import Timer
kill = lambda process: process.kill()
import os
import matplotlib
import scipy
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
import json
from elasticsearch import Elasticsearch
from datetime import datetime
from scipy import signal
from elasticsearch import Elasticsearch, helpers
import os, uuid
from time import sleep
# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")



import multiprocessing
import time

# Your foo function
def foo():
    os.system('tshark -i lo -q -T fields -e wlan.ta -e rftap.snr -e wlan.ra > output1.txt')

while True:

    if __name__ == '__main__':
        # Start foo as a process
        p = multiprocessing.Process(target=foo)
        p.start()

        # Wait 10 seconds for foo
        time.sleep(30)

        # Terminate foo
        p.terminate()

        # Cleanup
        p.join()

##
    dict={}
    open_file = open('output1.txt')
    for line in open_file:
        line = line.rstrip()   #strip white space at the end of each line
        words = line.split()   #split string into a list of words
        if len(words)==3:
            if words[0] in dict:
                if words[2] in dict:
                    continue
                else:
                    if words[2] == "d8:0f:99:ab:a3:ec":
                        continue
                    else:
                        if float(words[1]) > 1.00:
                            dict[words[2]] = words[1]


            else:
                if words[0]=="d8:0f:99:ab:a3:ec":
                    continue
                else:
                    if float(words[1]) >1.00:

                        dict[words[0]]= words[1]
                    if words[2] in dict:
                        continue
                    else:
                        if words[2] == "d8:0f:99:ab:a3:ec":
                            continue
                        else:
                            if float(words[1]) > 1.00:
                                dict[words[2]] = words[1]


    dict_len = len(dict)
    print(dict)
    print(dict_len)
    dict_doc={}
    dict_doc["num"]=dict_len
    dict_doc["timestamp"] = datetime.utcnow()
    dict_doc["id"]=1
    es = Elasticsearch([{'host': 'localhost', 'port':9200 }])

    try:
        es.index(index='human', doc_type='_doc', body=dict_doc)
    except Exception as e:
        print(e)

    os.remove("output1.txt")

#
#
# def func1():
#     subprocess.Popen(['tshark -i lo -q -T fields -e wlan.ta -e rftap.snr'], shell=True)
#
# def func2():
#     ping2=subprocess.Popen(['tshark -i lo -q -T fields -e wlan.ra -e rftap.snr > outputmac2.txt'], shell=True)

# if __name__=='__main__':
#      p1 = Process(target = func1)
#      p1.start()
#      # p2 = Process(target = func2)
#      # p2.start()
#      time.sleep(40)
#
#      # Terminate foo
#      p1.terminate()
#
#
#
