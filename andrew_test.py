import os
import sys
import time
import sqlite3
import math
from multiprocessing import Process
import multiprocessing as mp
from buffer import Buffer
from db_utils import create_table_db, log_results, read_all_records_db, printlog
from elastic_powwow import addelastic, query_elastic

def stream_sender(filename, buffer):
    info('reader')

    # keep track of the number of items added to the buffer
    sent_ct = 0

    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()  # strip white space
            words = line.split()  # split string into a list of words
            if len(words) == 3:  # only take lines with desired information
                buffer.add(words)
                sent_ct += 1
            # dig = int(line.strip().split()[0]) #specific to the test file
            # print('read {}'.format(dig))
            # buffer.add(dig)
            # print('writer buff state: {}'.format(buffer))

    # acknowledge to the log that stream_receiver has stopped
    # sending new inputs to the buffer
    print('ALERT: stream_sender stopped sending packets')
    print('STATS: sent tuples: {}'.format(sent_ct))


# given a shared buffer, stream_receiver reads the
# buffer and inserts the buffer items into the database
# the process stops after 5 seconds of no new insertions
# into the empty buffer
#    buffer = a instance of the Buffer class to read
#    wait = the time in seconds to wait before reading again
#         after reading an empty buffer
#    max_time = the max number of seconds to wait for a new buffer
#         entry before terminating the process
def stream_receiver(buffer, wait, max_time):
    info('receiver')

    # open a connection with the DB
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    # keep track of the # of consecutive times the buffer was empty
    # when attempting to be read
    empty_ct = 0

    # keep track of the number of packets read out of the buffer
    read_ct = 0

    while empty_ct < max_time:

        # attempt to read from the buffer
        if buffer.ready():
            # print('reader buff state: {}'.format(buffer))
            buff_item = buffer.remove()
            # print(buff_item)
            cur.execute('INSERT INTO uniqueMAC (TX, RX, SNR) VALUES (?, ?, ?)', buff_item)

            empty_ct = 0  # reset the empty ct
            read_ct += 1
            addelastic(read_ct, buff_item)
        else:
            print('nothing to read')
            time.sleep(wait)
            empty_ct += 1

            # TODO - is this the best setup for when to commit?
    conn.commit()
    cur.close()
    conn.close()

    # acknowledge to the log that stream_receiver has stopped
    # receiving new inputs to the buffer
    print('ALERT: steam_reciever stopped receiving packets')
    print('STATS: buffer empty: {} | read tuples: {}'.format(not buffer.ready(), read_ct))


# Helper function to show process data
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


if __name__ == '__main__':
    info('main line')

    # setup the test variables
    filename = 'filedata.txt'
    wait_time = 1
    max_time = 5
    db_name = 'test.db'

    # create a buffer managed by the shared memory manager
    b = Buffer()

    # setup the database
    create_table_db(db_name)

    # create processes for the streaming to the buffer and reading from the buffer
    writer = Process(target=stream_sender, args=(filename, b))

    # create process for reading from the buffer
    reader = Process(target=stream_receiver, args=(b, wait_time, max_time))

    writer.start()
    reader.start()

    # the main function controlls the manager, so we have to wait for the children
    # to finish before allowing main to exit or the manager will close and the
    # children will not be able to use the shared buffer
    writer.join()
    reader.join()

    # attempt to read the database for the intial entries (this will eventually be PART 2)
    log_results(read_all_records_db(db_name))
    print('READING FROM SQLITE')
    read_all_records_db(db_name)
    print('READING FROM ELASTIC SEARCH')
    query_elastic()

    printlog(db_name)