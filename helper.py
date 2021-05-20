import os
import math
import numpy
import matplotlib.pyplot as plt


def file_iterations(filename, output_size, out_file):
    print("get here.")
    f = os.stat(filename)
    loops = math.floor(output_size/f.st_size)
    print("Need iteration: ", loops)

    with open(out_file, 'w') as outfile:
        for x in range(0, loops):
            with open(filename) as infile:
                outfile.write(infile.read())
    print("Large file produced.")

# helper function to split file
def split_file(num_workers, infile, outfile):
    with open(infile) as input:
        files = [open('%s%d.txt' % (outfile,i), 'w') for i in range(num_workers)]
        for i, line in enumerate(input):
            files[i % num_workers].write(line)
        for f in files:
            f.close()

def visualize(times, thread, sizes):
    times = numpy.array(times)
    sizes = numpy.array(sizes)
    rate = numpy.divide(sizes, times)
    rate = numpy.divide(rate, 1000)
    plt.plot(thread, rate)
    plt.ylabel("KBps")
    plt.xlabel("Number of Processes")
    plt.savefig('data_rate.png')