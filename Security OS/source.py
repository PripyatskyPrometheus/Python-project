import win32net
import win32netcon
import win32security
from socket import socket, AF_INET, SOCK_DGRAM
from subprocess import check_output
import scapy.all as sc
import ntsecuritycon as con


# Функция для возвращаения данные о ресурах на удаленной машине
def get_shared_resources(remote_user):
    try:
        level = 2
        resources, _, _ = win32net.NetShareEnum(remote_user, level)
        if resources:
            for resource in resources:
                print(f" - {resource['netname']}: {resource['path']} ({resource['remark']});")
        else:
            print("Общих ресурсов не найдено.")
    except Exception as e:
        print(f"Ошибка при получении общих ресурсов: {e}")


def del_shared_resourse():

    win32net.NetShareDel(None, "MySharedFolder", 0)

def creater_shared_folder(users):

    share_info = {
        'netname': 'MySharedFolder',  # Название общего ресурса
        'type': win32netcon.STYPE_DISKTREE,  # Тип общего ресурса (для папки на диске)
        'remark': 'Shared folder',
        'permissions': win32netcon.ACCESS_ALL,  # Права доступа
        'max_uses': -1,  # Максимальное количество одновременных подключений не ограничено
        'current_uses': 0,  # Текущее количество подключений
        'path': 'C:/Users/User/Desktop/synopsis',
        'passwd': None
    }

    security_descriptor = win32security.SECURITY_DESCRIPTOR()

    # Настраиваем DACL (список управления доступом)
    dacl = win32security.ACL()

    # Разрешаем права доступа
    privilege, _, _ = win32security.LookupAccountName("", users)
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.GENERIC_ALL, privilege)

    security_descriptor.SetDacl(True, dacl, False)
    # Присваиваем дескриптор безопасности к ресурсу
    share_info['security_descriptor'] = security_descriptor
    try:
        win32net.NetShareAdd(None, 502, share_info)  # Создаем общий ресурс с правами SHI502_SYSTEM
        print('Общий ресурс успешно создан')
    except Exception as e:
        print(f'Ошибка при создании общего ресурса: {e}')

#Cканирование локальной сети и вывод информации о подключенных устройствах: IP-адреса и MAC-адреса
def scan():
    st = socket(AF_INET, SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        local_ip = st.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        st.close()
    print(local_ip)
    com = f'route PRINT 0* | findstr {local_ip}'.split()
    print(check_output(com, shell=True).decode('cp866').split()[2])
    answered_list = sc.srp(sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=f'{local_ip.split(".")[0]}.{local_ip.split(".")[1]}.{local_ip.split(".")[2]}.1/24'), timeout=1, verbose=False)[0]
    clients = []
    for element in answered_list:
        clients.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})

    #print(f"\nУстройства в сети:\n\nIP\t\t\tMAC-address\n{'-' * 80}")
    for client in clients:
        print(f'{client["ip"]}\t\t{client["mac"]}')


def main():
    name_user = input("Имя удаленного пользователя: ")

    print("\nОбщие ресурсы удаленного пользователя:")
    get_shared_resources(name_user)
    
    #creater_shared_folder("Все")
    #get_shared_resources(name_user)

    del_shared_resourse()
    #get_shared_resources(name_user)

   # creater_shared_folder("User")
    scan()
    #get_shared_resources(name_user)

if __name__ == "__main__":
    main()