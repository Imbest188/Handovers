from GoogleSheetsClass import *
from Telnet.ControllerPool import ControllerPool

#
excel = Table(client_account_file="grounded-pivot-261916-f78fb501c60b.json",
              sheet_key="13fgjLhjzBYC9UA46qLdSmC4sPTCKotjIBMFms70B6cE")

pool = ControllerPool()
pool.add_controller('BSC03', '172.25.157.99', 'Administrator', 'Administrator1@')
pool.add_controller('BSC04', '10.140.3.7', 'ts_user', 'apg43l2@')
pool.add_controller('BSC05', '10.140.27.68', 'ts_user', 'apg43l1@')

cells = excel.get_cells_by_query('3G_NB', ['LAC', 'CellId', 'Uplink', 'Downlink', 'PSC'])
cells_raz = []

for i in cells:
    cells_raz.append(
        Cell(LAC=cells[i]['LAC'], CellId=i, Downlink=cells[i]['Downlink'], Uplink=cells[i]['Uplink'],
             PCI=cells[i]['PSC']))

for i in cells_raz:
    print(i.CellId, i.LAC, i.Uplink, i.Downlink, i.PCI)

gsm_cell = 'LUG015C'
utran_cell = '30445'
gsm_cell_info = pool.get_cell_info(gsm_cell)
bsic = gsm_cell_info['BSIC']
r = f'ADD UEXT2GCELL: GSMCellIndex={gsm_cell_info["CID"]}, GSMCellName="{gsm_cell}", NBscIndex=0, ' \
    f'LdPrdRprtSwitch=OFF, MCC="255", MNC="99", CnOpGrpIndex=0, LAC={gsm_cell_info["LAC"]}, CfgRacInd=REQUIRE, RAC=0, ' \
    f'CID={gsm_cell_info["CID"]}, NCC={gsm_cell_info["NCC"]}, BCC={gsm_cell_info["BCC"]}, BcchArfcn={gsm_cell_info["BCCHNO"]}, ' \
    f'RatCellType=EDGE, UseOfHcs=NOT_USED;'

print(r)
