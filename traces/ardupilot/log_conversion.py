import json
import subprocess
import sys
import csv
try:
    from pymavlink import mavutil
except:
    print("pymavlink needs to be installed")
    sys.exit(1)

try:
    from pathlib import Path
except:
    print("only python >= 3.4 is supported")
    sys.exit(1)



class Log(object):

    def __init__(self, init_timestamp):
        self.bat = [100.0]
        self.alt = [0.0]
        self.lat = [0.0]
        self.lon = [0.0]
        self.vx = [0.0]
        self.vy = [0.0]
        self.vz = [0.0]
        self.wnd_dir = [0.0]
        self.wnd_spd = [0.0]
        self.gps_sats = [0.0]
        self.heading = [0.0]
        self.roll = [0.0]
        self.pitch = [0.0]
        self.gps_glitch_x = [0.0]
        self.gps_glitch_y = [0.0]
        self.timestamp = [init_timestamp]

    def insert(self, arg, data):
        self.align_new_timestamp(data["meta"]["timestamp"])

        method_name = 'append_' + str(arg)
        method = getattr(self, method_name, lambda x: "nothing")
        return method(data)

    def append_VFR_HUD(self, data):
        self.heading[-1] = data["data"]["heading"]

    def append_NAV_CONTROLLER_OUTPUT(self, data):
        self.pitch[-1] = data["data"]["nav_pitch"]
        self.roll[-1] = data["data"]["nav_roll"]

    def append_BATTERY_STATUS(self, data):
        self.bat[-1] = data["data"]["battery_remaining"]

    def append_GLOBAL_POSITION_INT(self,data):
        self.lat[-1] = data["data"]["lat"]/10.0**7.0
        self.lon[-1] = data["data"]["lon"]/10.0**7.0
        self.alt[-1] = data["data"]["alt"]/10.0**3.0
        self.vx[-1] = data["data"]["vx"]/10.0**2
        self.vy[-1] = data["data"]["vy"]/10.0**2
        self.vz[-1] = data["data"]["vz"]/10.0**2

    def append_GPS_RAW_INT(self, data):
        self.gps_sats[-1] = data["data"]["satellites_visible"]

    def append_PARAM_VALUE(self,data):
        method_name = 'append_' + str(data["data"]["param_id"])
        method = getattr(self, method_name, lambda x: "nothing")
        method(data)

    def append_SIM_GPS_GLITCH_X(self, data):
        self.gps_glitch_x[-1] = data["data"]["param_value"]

    def append_SIM_GPS_GLITCH_Y(self, data):
        self.gps_glitch_y[-1] = data["data"]["param_value"]

    def append_SIM_WIND_SPD(self, data):
        self.wnd_spd[-1] = data["data"]["param_value"]

    def append_SIM_WIND_DIR(self, data):
        self.wnd_dir[-1] = data["data"]["param_value"]

    def align_new_timestamp(self, new_timestamp):
        if self.timestamp[-1] != new_timestamp:
            self.bat.append(None)
            self.alt.append(None)
            self.lat.append(None)
            self.lon.append(None)
            self.vx.append(None)
            self.vy.append(None)
            self.vz.append(None)
            self.wnd_dir.append(None)
            self.wnd_spd.append(None)
            self.gps_sats.append(None)
            self.heading.append(None)
            self.roll.append(None)
            self.pitch.append(None)
            self.gps_glitch_x.append(None)
            self.gps_glitch_y.append(None)
            self.timestamp.append(new_timestamp)

def create_json(src_file, json_file):
    dest_fh = open(json_file, 'w')
    subprocess.call(["python","mavlogdump.py", "--format", "json", src_file], stdout=dest_fh)

def parse_json(json_file):
    with open(json_file) as f:
        lines = f.readlines()

    data = json.loads(lines[0])
    log_obj = Log(data["meta"]["timestamp"])
    for line in lines:
        data = json.loads(line)
        log_obj.insert(data["meta"]["type"], data)
    return log_obj


def convert_file(src_file):
    src = Path(src_file)
    if not src.exists():
        print("The specified source file could not be found.")
        sys.exit(1)
    if src.suffix.lower() != ".tlog":
        print("The specified source file is not a \".tlog\" file.")
        sys.exit(1)
    json_file = str(src.parent / (src.stem +".json"))
    csv_file_name = str(src.parent / (src.stem +".csv"))
    create_json(src_file,json_file)
    log_obj = parse_json(json_file)
    with open(csv_file_name, mode='w',newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["time",
                             "bat",
                             "alt",
                             "lat",
                             "lon",
                             "vx",
                             "vy",
                             "vz",
                             "wnd_dir",
                             "wnd_spd",
                             "gps_sats",
                             "heading",
                             "roll",
                             "pitch",
                             "gps_glitch_x",
                             "gps_glitch_y"])
        csv_writer.writerows(list(zip(log_obj.timestamp,
                                      log_obj.bat,
                                      log_obj.alt,
                                      log_obj.lat,
                                      log_obj.lon,
                                      log_obj.vx,
                                      log_obj.vy,
                                      log_obj.vz,
                                      log_obj.wnd_dir,
                                      log_obj.wnd_spd,
                                      log_obj.gps_sats,
                                      log_obj.heading,
                                      log_obj.roll,
                                      log_obj.pitch,
                                      log_obj.gps_glitch_x,
                                      log_obj.gps_glitch_y)))

convert_file("2019-05-15 14-30-52.tlog")
print("done")