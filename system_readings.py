import json
import os
import psutil
import shutil
import time


UPDATE_TIME = 3

def read_cpu_usage(data_dict):
    with os.popen("mpstat -P ALL 1 1") as process:
        HEADERS_COUNT = 4
        for _ in range(HEADERS_COUNT):
            process.readline()
        data_dict["CPU"] = []
        CPU_COUNT = psutil.cpu_count()
        for _ in range(CPU_COUNT):
            data_dict["CPU"].append(process.readline().split()[2].replace(",", "."))

def read_cpu_temp(data_dict):
    with os.popen("acpi -t") as process:
        data_dict["temp"] = []
        for line in process:
            data_dict["temp"].append(line.split()[3])

def read_RAM_usage(data_dict):
    data_dict["RAM"] = {}
    data_dict["RAM"]["total"] = "{:.2f}".format(psutil.virtual_memory().total/(10**9))
    data_dict["RAM"]["used"] = "{:.2f}".format(psutil.virtual_memory().used/(10**9))
    data_dict["RAM"]["available"] = "{:.2f}".format(psutil.virtual_memory().available/(10**9))

def read_disk_usage(data_dict):
    t, u, free = shutil.disk_usage("/")
    data_dict["disk"] = "{:.2f}".format(free / (10**9))

def get_net_iface_counters():
    return psutil.net_io_counters(pernic=True)

def read_network_ifaces_info(data_dict, io_old):
    ifaces = {}
    for ifname, data in psutil.net_if_stats().items():
        ifaces[ifname] = {"status" : "UP" if data.isup else "DOWN"}

    for ifname, data in psutil.net_if_addrs().items():
        ifaces[ifname]["ip"] = data[0].address

    io_new = get_net_iface_counters()
    for ifname, data in io_old.items():
        recv_speed = (io_new[ifname].bytes_recv - data.bytes_recv) * 8 // UPDATE_TIME
        send_speed = (io_new[ifname].bytes_sent - data.bytes_sent) * 8 // UPDATE_TIME
        ifaces[ifname]["recv_speed"] = recv_speed
        ifaces[ifname]["send_speed"] = send_speed

    data_dict["network"] = ifaces

while True:
    io_old = get_net_iface_counters()
    time.sleep(UPDATE_TIME)
    data_dict = {}
    read_cpu_usage(data_dict)
    read_cpu_temp(data_dict)
    read_RAM_usage(data_dict)
    read_disk_usage(data_dict)
    read_network_ifaces_info(data_dict, io_old)
    with open(os.path.expanduser("~") + "/system_data_readings.txt", "w") as file:
        file.write(json.dumps(data_dict))
