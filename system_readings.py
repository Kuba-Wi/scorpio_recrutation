import os
import psutil
import shutil
import time


CPU_COUNT = psutil.cpu_count()
with open("system_data_readings.txt", "w") as file:
    with os.popen("mpstat -P ALL 1 1") as process:
        HEADERS_COUNT = 4
        for i in range(HEADERS_COUNT):
            process.readline()
        file.write("CPU CORES USAGE %\n")
        for i in range(CPU_COUNT):
            file.write(process.readline().split()[2].replace(",", "."))
            file.write("\n")

    with os.popen("acpi -t") as process:
        file.write("Temperature from all sensors\n")
        for line in process:
            file.write(line.split()[3])
            file.write("\n")

    file.write("RAM usage (total, used, available)\n")
    file.write("{:.2f}\n".format(psutil.virtual_memory()[0]/(10**9)))
    file.write("{:.2f}\n".format(psutil.virtual_memory()[3]/(10**9)))
    file.write("{:.2f}\n".format(psutil.virtual_memory()[1]/(10**9)))

    t, u, free = shutil.disk_usage("/")
    file.write("Free disk space\n")
    file.write("{:.2f}\n".format(free / (10**9)))

    ifaces = {}
    for ifname, data in psutil.net_if_stats().items():
        ifaces[ifname] = ["UP" if data.isup else "DOWN"]

    for ifname, data in psutil.net_if_addrs().items():
        ifaces[ifname].append(data[0].address)

    io_first = psutil.net_io_counters(pernic=True)
    time.sleep(1)
    io_second = psutil.net_io_counters(pernic=True)
    for ifname, data in io_first.items():
        recv_speed = io_second[ifname].bytes_recv - data.bytes_recv
        send_speed = io_second[ifname].bytes_sent - data.bytes_sent
        ifaces[ifname].append(recv_speed)
        ifaces[ifname].append(send_speed)

    file.write("Network interfaces (status, address, receive speed, send speed [b/s])\n")
    for ifname, data in ifaces.items():
        file.write(ifname)
        file.write("\n")
        file.write(" ".join(str(d) for d in data))
        file.write("\n")
