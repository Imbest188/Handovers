import csv


class MakeHO:
    def __init__(self, file_path):
        self.file_path = file_path

    def make_2g_2g(self):
        pass

    def make_2g_3g(self):
        pass

    def make_3g_2g(self):
        pass

    def make_3g_3g(self):
        cells_to_ho = {}
        with open(self.file_path) as file:
            csv_reader = csv.DictReader(file, delimiter=';', quotechar='|')
            for row in csv_reader:
                if row["TRANSMITTER.CELL_IDENTITY"].replace(" ", "") in cells_to_ho:
                    cells_to_ho[row["TRANSMITTER.CELL_IDENTITY"].replace(" ", "")] += [row[
                        "NEIGHBOUR.CELL_IDENTITY"].replace(
                        " ", "")]
                else:
                    cells_to_ho[row["TRANSMITTER.CELL_IDENTITY"].replace(" ", "")] = [row[
                        "NEIGHBOUR.CELL_IDENTITY"].replace(
                        " ", "")]
        with open(f"{self.file_path[:-4]}.txt", "w+") as file:
            for i in cells_to_ho:
                for j in cells_to_ho[i]:
                    file.writelines(f"ADD UINTRAFREQNCELL: RNCId=3, CellId={i}, NCellRncId=3, NCellId={j}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, NPrioFlag=FALSE;\n")
                    file.writelines(f"ADD UINTRAFREQNCELL: RNCId=3, CellId={j}, NCellRncId=3, NCellId={i}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, NPrioFlag=FALSE;\n\n")
                    file.writelines(f"ADD UINTERFREQNCELL: RNCId=3, CellId={i}, NCellRncId=3, NCellId={j}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, BlindHoFlag=FALSE, "
                                    f"NPrioFlag=FALSE, InterNCellQualReqFlag=FALSE, CLBFlag=FALSE;\n")
                    file.writelines(f"ADD UINTERFREQNCELL: RNCId=3, CellId={j}, NCellRncId=3, NCellId={i}, "
                                    f"SIB11Ind=TRUE, SIB12Ind=FALSE, TpenaltyHcsReselect=D0, BlindHoFlag=FALSE,"
                                    f" NPrioFlag=FALSE, InterNCellQualReqFlag=FALSE, CLBFlag=FALSE;\n\n")