from GoogleSheetsClass import *
from Telnet.ControllerPool import ControllerPool
from MakeHO import MakeHO

# excel = Table(client_account_file="grounded-pivot-261916-f78fb501c60b.json",
#               sheet_key="13fgjLhjzBYC9UA46qLdSmC4sPTCKotjIBMFms70B6cE")

# pool = ControllerPool()
# pool.add_controller('BSC03', '172.25.157.99', 'Administrator', 'Administrator1@')
# pool.add_controller('BSC04', '10.140.3.7', 'ts_user', 'apg43l2@')
# pool.add_controller('BSC05', '10.140.27.68', 'ts_user', 'apg43l1@')

# cells = excel.get_cells_by_query('3G_NB', ['LAC', 'CellId', 'Uplink', 'Downlink', 'PSC'])

# print("Я проверил таблицы 3g и 4g перед тем, как делать хо.")
# print("Создатели программы не несут ответственности за неправильно сделанные ХО. Все на свой страх и риск.")
# type_of_HO = input('Type of HO?: \n2G-2G\t2G-3G\n3G-3G\t3G-2G\n')
# file_path = input('Send file: ')
# if type_of_HO == '3G-3G':
file_path = 'C:\\Users\\isuho\\PycharmProjects\\Handovers\\226_3g-3g.csv'
ho = MakeHO(file_path)
ho.make_3g_3g()

# for i in cells:
#     print(i.CellId)

# for i in cells:
#     cells_raz.append(
#         Cell(LAC=cells[i]['LAC'], CellId=i, Downlink=cells[i]['Downlink'], Uplink=cells[i]['Uplink'],
#              PCI=cells[i]['PSC']))
#
# for i in cells_raz:
#     print(i.CellId, i.LAC, i.Uplink, i.Downlink, i.PCI)


# gsm_cell = 'LUG015C'
# utran_cell = '30445'
# gsm_cell_info = pool.get_cell_info(gsm_cell)
# bsic = gsm_cell_info['BSIC']
# r = f'ADD UEXT2GCELL: GSMCellIndex={gsm_cell_info["CID"]}, GSMCellName="{gsm_cell}", NBscIndex=0, ' \
#     f'LdPrdRprtSwitch=OFF, MCC="255", MNC="99", CnOpGrpIndex=0, LAC={gsm_cell_info["LAC"]}, CfgRacInd=REQUIRE, RAC=0, ' \
#     f'CID={gsm_cell_info["CID"]}, NCC={gsm_cell_info["NCC"]}, BCC={gsm_cell_info["BCC"]}, BcchArfcn={gsm_cell_info["BCCHNO"]}, ' \
#     f'RatCellType=EDGE, UseOfHcs=NOT_USED;'
