import argparse
import sys
import time

def set_up_online_monitor(file):
    #TODO: check if the monitor needs setup command
    line = file.readline().split(",")
    line = input_processing_online(line[0:len(line)-1])
    print(line)

def send_data_to_monitor(file):
    first = True
    old_ts = 0
    for line in file.readlines():
        line = line.split(",")
        ts = float(line[-1])
        line = input_processing_online(line[0:len(line)-1])
        if first == False:
            time.sleep(ts - old_ts)
        old_ts = ts
        first = False
        print(line)

def input_processing_online(cur_line_as_vec):
    #TODO: bring input vector to monitor input format; no change, if the csv input format is accepted
    line = ",".join(cur_line_as_vec)
    line

#command line parser for input replay
parser = argparse.ArgumentParser()
parser.add_argument('file', help='The path to the file.')

args = parser.parse_args()

file = open(args.file, "r")

set_up_online_monitor(file)

send_data_to_monitor(file)

file.close()
