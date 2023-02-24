import os
import psutil
import shutil
import time


UPDATE_TIME = 5

def write_cpu_usage(file):
    with os.popen("mpstat -P ALL 1 1") as process:
        HEADERS_COUNT = 4
        for i in range(HEADERS_COUNT):
            process.readline()
        file.write("CPU CORES USAGE %\n")
        CPU_COUNT = psutil.cpu_count()
        for i in range(CPU_COUNT):
            file.write(process.readline().split()[2].replace(",", "."))
            file.write("\n")

def write_cpu_temp(file):
    with os.popen("acpi -t") as process:
        file.write("Temperature from all sensors\n")
        for line in process:
            file.write(line.split()[3])
            file.write("\n")

def write_RAM_usage(file):
    file.write("RAM usage (total, used, available)\n")
    file.write("{:.2f}\n".format(psutil.virtual_memory()[0]/(10**9)))
    file.write("{:.2f}\n".format(psutil.virtual_memory()[3]/(10**9)))
    file.write("{:.2f}\n".format(psutil.virtual_memory()[1]/(10**9)))

def write_disk_usage(file):
    t, u, free = shutil.disk_usage("/")
    file.write("Free disk space\n")
    file.write("{:.2f}\n".format(free / (10**9)))

def get_net_iface_counters():
    return psutil.net_io_counters(pernic=True)

def write_network_ifaces_info(file, io_old):
    ifaces = {}
    for ifname, data in psutil.net_if_stats().items():
        ifaces[ifname] = ["UP" if data.isup else "DOWN"]

    for ifname, data in psutil.net_if_addrs().items():
        ifaces[ifname].append(data[0].address)

    io_new = get_net_iface_counters()
    for ifname, data in io_old.items():
        recv_speed = (io_new[ifname].bytes_recv - data.bytes_recv) / UPDATE_TIME
        send_speed = (io_new[ifname].bytes_sent - data.bytes_sent) / UPDATE_TIME
        ifaces[ifname].append(recv_speed)
        ifaces[ifname].append(send_speed)

    file.write("Network interfaces (status, address, receive speed, send speed [b/s])\n")
    for ifname, data in ifaces.items():
        file.write(ifname)
        file.write("\n")
        file.write(" ".join(str(d) for d in data))
        file.write("\n")

while True:
    io_old = get_net_iface_counters()
    time.sleep(UPDATE_TIME)
    with open("system_data_readings.txt", "w") as file:
        write_cpu_usage(file)
        write_cpu_temp(file)
        write_RAM_usage(file)
        write_disk_usage(file)
        write_network_ifaces_info(file, io_old)
