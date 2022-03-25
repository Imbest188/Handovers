import csv
import re
import itertools


class MakeHO:
    def __init__(self, file_path):
        self.file_path = file_path

    def open_csv_file(self, key_field, fields):
        cells_to_ho = {}
        with open(self.file_path) as file:
            csv_reader = csv.DictReader(file, delimiter=';', quotechar='|')
            for row in csv_reader:
                if row[key_field].replace(" ", "") in cells_to_ho:
                    cells_to_ho[row[key_field].replace(" ", "")] += [row[k].replace(" ", "") for k in fields]
                else:
                    cells_to_ho[row[key_field].replace(" ", "")] = [row[k].replace(" ", "") for k in fields]
        return cells_to_ho

    def make_2g_2g(self):
        pass

    def make_2g_3g(self, cell_from_google: dict):
        cells_to_ho = self.open_csv_file('Transmitter', ['NEIGHBOUR.CELL_IDENTITY'])

        with open(f"{self.file_path[:-4]}.txt", "w+") as file:
            for i in cells_to_ho:
                for k in cell_from_google:
                    if str(k.CellId) in cells_to_ho[i]:
                        file.writelines(f"RLUMC:CELL={i},ADD,UMFI={k.Downlink}-{k.PSC}-NODIV;\n")
                        file.writelines(f"RLNRI:CELL={i}, CELLR={k.CellId}, SINGLE;\n")
                file.writelines(f"RLSUC:CELL={i},FDDMRR=1,QSC=7,QSCI=0,QSI=7,SPRIO=YES,FDDQMIN=6,FDDQOFF=0;\n"
                                f"RLLOC:CELL={i},ISHOLEV=10;\n\n")

    def make_3g_2g(self, cell_from_google: dict):
        cells_to_ho = self.open_csv_file('TRANSMITTER.CELL_IDENTITY', ['Neighbour'])

        with open(f"{self.file_path[:-4]}.txt", "w+") as file:
            for i in cells_to_ho:
                for j in cells_to_ho[i]:
                    j = re.findall('[0-9]+', j.replace('_', ''))
                    file.writelines(f"ADD U2GNCELL: RNCId=3, CellId=={i}, GSMCellIndex={''.join(j)}, "
                                    f"BlindHoFlag=FALSE, NPrioFlag=FALSE;\n")

    def make_3g_3g(self, cell_from_google: dict):
        cells_to_ho = self.open_csv_file('TRANSMITTER.CELL_IDENTITY', ['NEIGHBOUR.CELL_IDENTITY'])
        # Проверка на наличие соты из файла в гугл таблице, чтобы не забывали добавлять
        cells_in_excel = [k.CellId for k in cell_from_google]
        for i in cells_to_ho:
            if int(i) not in cells_in_excel:
                return print('Cначала обновили таблицу на Google Drive, а потом ХО.')

        with open(f"{self.file_path[:-4]}.txt", "w+") as file:
            for i in cells_to_ho:
                for j in cells_to_ho[i]:
                    file.writelines(f"ADD UINTRAFREQNCELL: RNCId=3, CellId={i}, NCellRncId=3, NCellId={j}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, NPrioFlag=FALSE;\n"
                                    f"ADD UINTRAFREQNCELL: RNCId=3, CellId={j}, NCellRncId=3, NCellId={i}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, NPrioFlag=FALSE;\n\n"
                                    f"ADD UINTERFREQNCELL: RNCId=3, CellId={i}, NCellRncId=3, NCellId={j}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, BlindHoFlag=FALSE, "
                                    f"NPrioFlag=FALSE, InterNCellQualReqFlag=FALSE, CLBFlag=FALSE;\n"
                                    f"ADD UINTERFREQNCELL: RNCId=3, CellId={j}, NCellRncId=3, NCellId={i}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, BlindHoFlag=FALSE,"
                                    f" NPrioFlag=FALSE, InterNCellQualReqFlag=FALSE, CLBFlag=FALSE;\n\n")

    def make_3g_lte_huawei(self):
        pass

    def make_2g_lte_huawei(self):
        pass

    def make_4g_ericsson_2g(self, gsm_cells_info):
        cells_to_ho = self.open_csv_file('Cell', ['Neighbour'])

        def freq_neighbours(cells: dict, lte_cells: dict):
            freq_group = """CREATE
(
 parent "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1"
 identity "GSM"
 moType GeranFreqGroup
 exception none
 nrOfAttributes 1
 frequencyGroupId Integer 1
)"""
            freqs_2g = ""
            ext_2g_cells = ""
            ext_geran_cell = ""
            lte_reselect = ""
            lte_hos = ""
            for i in cells:
                freqs_2g += f"""
CREATE
(
 parent "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1"
 identity {cells[i]['BCCHNO']}
 moType GeranFrequency
 exception none
 nrOfAttributes 3
 arfcnValueGeranDl Integer {cells[i]['BCCHNO']}
 bandIndicator Integer 0
 geranFreqGroupRef Array Reference 1 "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=GSM"
)\n"""
                ext_2g_cells += f"""
CREATE
(
 parent "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1"
 identity {cells[i]['CGI'].split('-')[-1]}
 moType ExternalGeranCell
 exception none
 nrOfAttributes 6
 plmnIdentity  Struct
 	nrOfElements 3
 		mcc Integer 255
 		mnc Integer 99
 		mncLength Integer 2
 lac Integer {cells[i]['CGI'].split('-')[2]}
 cellIdentity Integer {cells[i]['CGI'].split('-')[-1]}
 bcc Integer {cells[i]['BSIC'][1:]}
 ncc Integer {cells[i]['BSIC'][:1]}
 geranFrequencyRef Reference "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1,GeranFrequency={cells[i]['BCCHNO']}"
)\n"""
                ext_geran_cell += f"""
SET
(
 mo "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1,ExternalGeranCell={cells[i]['CGI'].split('-')[-1]}"
 exception none
 masterGeranCellId String "{cells[i]['CGI'].split('-')[-1]}"
)

SET
(
 mo "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1,ExternalGeranCell={cells[i]['CGI'].split('-')[-1]}"
 exception none
 rimCapable Integer 2
)
"""
            for i in lte_cells:
                lte_reselect += f"""
CREATE
(
 parent "ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=1{i[-1:]}"
 identity "GSM"
 moType GeranFreqGroupRelation
 exception none
 nrOfAttributes 2
 geranFreqGroupRef Reference "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=GSM"
 cellReselectionPriority Integer 5
)

SET
(
 mo "ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=1{i[-1:]},GeranFreqGroupRelation=GSM"
 exception none
 allowedPlmnList  Array Struct 1
	nrOfElements 3
		mcc Integer 255
		mnc Integer 99
		mncLength Integer 2
)

SET
(
 mo "ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=1{i[-1:]},GeranFreqGroupRelation=GSM"
 exception none
 csFallbackPrio Integer 7
)

SET
(
 mo "ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=1{i[-1:]},GeranFreqGroupRelation=GSM"
 exception none
 csFallbackPrioEC Integer 7
)
"""
                for k in lte_cells[i]:
                    lte_hos += f"""
CREATE
(
 parent "ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=1{i[-1:]},GeranFreqGroupRelation=GSM"
 identity {re.findall('[0-9]+', k.replace('_', ''))[0] if 'LUG' in k else k.replace('D', '').replace('G', '')}
 moType GeranCellRelation
 exception none
 nrOfAttributes 1
 extGeranCellRef Reference "ManagedElement=1,ENodeBFunction=1,GeraNetwork=1,ExternalGeranCell={re.findall('[0-9]+', k.replace('_', ''))[0] if 'LUG' in k else k.replace('D', '').replace('G', '')}"
)\n"""
            return freq_group + f"\n{'/' * 75}\n" + freqs_2g + f"\n{'/' * 75}\n" + ext_2g_cells + f"\n{'/' * 75}\n" \
                   + ext_geran_cell + f"\n{'/' * 75}\n" + lte_reselect + f"\n{'/' * 75}\n" + lte_hos

        LTE_2g = {}
        for i in cells_to_ho:
            if i[:-2] in LTE_2g:
                LTE_2g[i[:-2]].update({i: cells_to_ho[i]})
            else:
                LTE_2g[i[:-2]] = {i: cells_to_ho[i]}

        for i in LTE_2g:
            with open(f"{i}.txt", "w+") as file:
                cells_2g = list(dict.fromkeys(list(itertools.chain(*LTE_2g[i].values()))))
                cells_2g_info = {}
                # Все соты 2г относящиеся к одной БС ЛТЕ
                for k in cells_2g:
                    k = k.replace('_1', 'A').replace('_2', 'B').replace('_3', 'C')
                    cells_2g_info[k] = gsm_cells_info.get_cell_info(k)
                file.writelines(freq_neighbours(cells_2g_info, LTE_2g[i]))

    def make_3g_lte_ericsson(self, cell_from_google: dict):
        cells_to_ho = self.open_csv_file('Cell', ['NEIGHBOUR.CELL_IDENTITY'])
        for i in cells_to_ho:
            print(i, cells_to_ho)
