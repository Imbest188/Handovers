from GoogleSheetsClass import *
from Telnet.ControllerPool import ControllerPool
from MakeHO import MakeHO

# Подключение к Google Sheets
excel = Table(client_account_file="grounded-pivot-261916-f78fb501c60b.json",
              sheet_key="13fgjLhjzBYC9UA46qLdSmC4sPTCKotjIBMFms70B6cE")
# Получение значений с полей из 3G с заданными полями
cells_3g = excel.get_cells_by_query('3G_NB', ['LAC', 'CellId', 'Uplink', 'Downlink', 'PSC'])

# pool = ControllerPool()
# pool.add_controller('BSC03', '172.25.157.99', 'Administrator', 'Administrator1@')
# pool.add_controller('BSC04', '10.140.3.7', 'ts_user', 'apg43l2@')
# pool.add_controller('BSC05', '10.140.27.68', 'ts_user', 'apg43l1@')

# print("Я проверил таблицы 3g и 4g в Google Sheets перед тем, как делать хо.")
# print("Создатели программы не несут ответственности за неправильно сделанные ХО. Все на свой страх и риск.")
# type_of_HO = input('Type of HO?: \n2G-2G\t2G-3G\n3G-3G\t3G-2G\n')
# file_path = input('Send file: ')
# if type_of_HO == '3G-3G':
file_path = 'C:\\Users\\admin\\PycharmProjects\\Handovers\\svr-3g-2g.csv'

ho = MakeHO(file_path)
ho.make_3g_2g(cells_3g)
