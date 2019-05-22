
import argparse
import sys
import os

#TODO: define setup variable
monitor_tool = "~/Documents/Uni/LolatoVhdl/lolaparser/target/release/streamlab"    #define the path to the monitor generator
# offline monitoring
off_com_line_arg = "--offline"  #define the command line argument for the monitor to offline monitoring
off_log_file_arg = "--csv-in"   #define the command line argument for the monitor to read the input log file
# online monitoring
on_com_line_arg = "--online"        #define the command line argument for the monitor for online monitoring
on_read_stdin_arg = "--stdin"       #define the command line argument for the monitor to read the input from the std i/o
on_write_stdout_arg = "--stdout"    #define the command line argument for the monitor to write the output to the std i/o
#output processing
output_file = "out.txt"             #define the path to the output file for the monitor
delay_discrete = 1                  #define the accepted delay for discrete time 
delay_real = 0.5                    #define the accepted delay for real time

#helper function
def input_processing_offline(csv_file):
    #TODO: check if monitor can handle .csv input files in offline monitoring, if not transform it
    return csv_file

def output_processing():
    #TODO: bring monitor output to the following format: r/d,time,message
    out_f = open(output_file, "r")
    out = out_f.readline()
    out_f.close()
    return out

def check_output(ref_file):
    #TODO: check the verdict of the monitor
    #ref_file has one line in the following input format: discrete_time,real_time
    ref_f = open(ref_file, "r")
    ref = ref_f.readline().split(',')
    ref_d = int(ref[0])
    ref_r = float(ref[1][0:len(ref[1])-1])
    ref_f.close()
    out = output_processing()
    out = out.split(',')
    if len(out) == 0:
        return False
    if out[0] == "d":
        out_d = int(out[1])
        return ref_d - delay_discrete <= out_d <= ref_d + delay_discrete
    elif out[0] == "t":
        out_r = float(out[1])
        return ref_r - delay_real <= out_r <= ref_r + delay_real
    return False

#command line parser
parser = argparse.ArgumentParser(description='Description')
parser.add_argument('-m', '--mode', choices=['offline', 'online'], default='offline', help='describe the mode of the monitor')
parser.add_argument('log', help='The log file representing the system behaviour.')
parser.add_argument('spec', help='The path to the specification file.')
parser.add_argument('ref', help='The path to the reference file.')

args = parser.parse_args()
spec = args.spec
log_file = args.log

if args.mode == 'offline':
    log_file = input_processing_offline(log_file)
    command = '{} {} {} {} {} > {}'.format(monitor_tool, off_com_line_arg, off_log_file_arg, log_file, spec, output_file)
    os.system(command)
else :
    command_monitor = '{} {} {} {} {}'.format(monitor_tool, on_com_line_arg, on_read_stdin_arg, on_write_stdout_arg, spec)
    command_input_replay = 'python input_replay.py {}'.format(log_file)
    command = '{} | {} > {} '.format(command_input_replay, command_monitor, output_file)
    os.system(command)

if check_output(args.ref):
    print("GOOD: Monitor has found the error in the trace")
else :
    print("BAD: Monitor has not found the error in the trace")