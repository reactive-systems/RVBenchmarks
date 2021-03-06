# A Benchmark Framework For *Some* Runtime Monitors

We implemented a benchmark tool for runtime monitors. Therefore, we provide two benchmarks, with several specifications. The specifications can be found in natural language. In addition, we translated them to LTL and to theLola specification language if possible.

## Requirements
To use our Benchmark tool your monitor should have the following requirements:

- Because our benchmark tool simulate the system behaviour, your monitor has to run in separation. In addition, the output from the monitor will be ignored from the system.
- We support offline and online monitoring. For online monitoring your monitor has to send a start message to trigger the start of our benchmark tool.
- If your monitor is hardware based, we currently only support serial communication.

## Benchmark Setup

### Ardupilot
As first benchmark we use log files from [ArduPilot](http://ardupilot.org). We generated files from the [Mission Planer](http://ardupilot.org/planner/index.html). If you want to generate your own files, download the [file](http://firmware.ardupilot.org/Tools/MissionPlanner/MissionPlanner-latest.msi) and follow the instruction.

### MACCDC
As second benchmark we use data generated by the National CyberWatch Mid-Atlantic Collegiate Cyber Defense Competition [(MACCDC)](https://maccdc.org). To benchmark your tool with the provided specifications download the following [file](https://download.netresec.com/pcap/maccdc-2012/maccdc2012_00000.pcap.gz), unpack it and add it to the folder.

## Usage
To use the benchmark tool, you have to change different lines:
- main.py
    - line 7: define the path to your monitor generation tool
    - line 9-10: define the command line arguments for offline monitoring, which uses log data, given by an input file
    - line 12-14: define the command line arguments for online monitoring, which uses the stdin to receive input data and the stdout to produce the output
    - line 18: if your tool does not accept a csv file for offline monitoring, add code that transfer the file to an accepted input format; otherwise do not make any changes here
- input\_replay.py
    - line 6: define the setup for online monitoring; if the monitor need as setup a csv header no changes has to be made
    - line 25: transfer the input data to the tool specific format; if the monitor accept the csv format no changes has to be made

To run the benchmark tool type the following command in your terminal:

```bash
python main.py -m {offline, online} path_to_trace path_to_spec
```
