

#create a sqlite3 data base 1st using the command
# sqlite3 test.db
# and then run the code


import sqlite3
conn = sqlite3.connect('/home/avishek/test.db')
c = conn.cursor()



def create_table():
    c.execute('DROP TABLE IF EXISTS Data2 ')
    c.execute('CREATE TABLE Data2 (TX TEXT, RX TEXT, SNR TEXT)')

def insert_data(filename):

    # read all the lines of the file
    open_file = open(filename)
    for line in open_file:
        line = line.rstrip()  # strip white space at the end of each line
        words = line.split()  # split string into a list of words
        if len(words) == 3:
            c.execute('INSERT INTO Data2 (TX, RX, SNR) VALUES (?, ?, ?)', (words[0], words[1], words[2]))
            conn.commit()




create_table()
insert_data('filedata.txt')

c.execute('SELECT TX, RX, SNR FROM Data2')
for row in c:
    print(row)

conn.close()