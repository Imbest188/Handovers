import csv
import re


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
                        print(i, k.CellId, k.Downlink, k.PSC)
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

    def make_3g_lte_ericsson(self):
        pass

    def make_3g_lte_huawei(self):
        pass

    def make_2g_lte_ericsson(self):
        pass

    def make_2g_lte_huawei(self):
        pass
