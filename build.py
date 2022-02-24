# It imports the modules that will be used in the script.
import re
import psutil
import subprocess
import platform
import socket
import uuid


def main():
    def get_size(bytes, suffix="B"):
        """
        Given a number of bytes, return a human readable string with the correct unit of measure

        :param bytes: The number of bytes to convert
        :param suffix: The suffix to use for the size, defaults to B (optional)
        :return: a string with the size of the file in human-readable format.
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def extract_wifi_passwords():
        """
        It extracts the wifi passwords from the system.
        :return: a string.
        """
        profiles_data = subprocess.check_output(
            'netsh wlan show profiles', encoding='CP866', errors='ignore').split('\n')
        profiles = [i.split(':')[1].strip()
                    for i in profiles_data if 'Все профили пользователей' in i]

        def for_pass():
            """
            It uses the subprocess module to run the command "netsh wlan show profile"
                    and then parses the output to find the password.
            :return: a string.
            """
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

    # 1. uname = platform.uname()
    #     2. cpufreq = psutil.cpu_freq()
    #     3. svmem = psutil.virtual_memory()
    #     4. cpu_information = (f'-------- System Information --------\nSystem: {uname.system}\nNode
    # Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine:
    # {uname.machine}\nProcessor: {uname.processor}\nIp-Address:
    # {socket.gethostbyname(socket.gethostname())}\nMac-Address: {":".join(re.findall("..", "%012x" %
    # uuid.getnode()))}\n-------- CPU Information --------\nPhysical cores:
    # {psutil.cpu_count(logical=False)}\nTotal cores: {psutil.cpu_count(logical=True)}\nMax Frequency:
    # {cpufreq.max:.2f}Mhz')
    #     5. memory_information = (
    #         f
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    cpu_information = (f'-------- System Information --------\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}\nIp-Address: {socket.gethostbyname(socket.gethostname())}\nMac-Address: {":".join(re.findall("..", "%012x" % uuid.getnode()))}\n-------- CPU Information --------\nPhysical cores: {psutil.cpu_count(logical=False)}\nTotal cores: {psutil.cpu_count(logical=True)}\nMax Frequency: {cpufreq.max:.2f}Mhz')
    memory_information = (
        f'-------- Memory Information --------\nTotal: {get_size(svmem.total)}\nAvailable: {get_size(svmem.available)}')

# A context manager.
    with open(file='full_info.txt', mode='a', encoding='utf-8') as file:
        file.write(
            f'{extract_wifi_passwords()}\n{cpu_information}\n{memory_information}')


# This is a special variable that is created when you run a python file.
# equal to the string `__main__` when the file is run directly,
# but is equal to the name of the module that imported it when the file is imported.
# This allows you to determine if a file is being run directly or being imported.
if __name__ == '__main__':
    main()
