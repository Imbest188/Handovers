import pygsheets
import re


class Table:
    def __init__(self, client_account_file, sheet_key):
        # Json файл с ключем
        self.client = pygsheets.authorize(service_file=client_account_file)
        # Ключ документа из google docs
        self.sheet_key = self.client.open_by_key(sheet_key)

    def get_records(self, work_sheet_title):
        return self.sheet_key.worksheet_by_title(work_sheet_title).get_all_records()

    def get_cells_by_query(self, work_sheet_title, query: list):
        records = self.sheet_key.worksheet_by_title(work_sheet_title).get_all_records()
        regex_list = [re.compile(i) for i in query]
        cells_records = {}
        cells_to_class = []
        for i in records:
            cells = {k: v for k, v in i.items() if any(re.match(regex, k) for regex in regex_list)}
            for k in cells:
                if '3G' in work_sheet_title:
                    if 'CellId' in k and cells[k] != '':
                        cells_records[cells[k]] = {j if j.isalpha() else j[:-1]: cells[j] for j in cells if
                                                   j[-1] == k[-1] or j.isalpha()}
                else:
                    cells_records[cells['Cellname']] = {j if j.isalpha() else j[:-1]: cells[j] for j in cells if
                                                        j[-1] == k[-1] or j.isalpha()}
        for i in cells_records:
            cells_to_class.append(
                Cell(LAC=cells_records[i]['LAC'], CellId=i, Downlink=cells_records[i]['Downlink'],
                     Uplink=cells_records[i]['Uplink'], PCI=cells_records[i]['PSC']))
        return cells_to_class


class Cell:
    def __init__(self, LAC, CellId, Downlink, Uplink, PCI):
        self.LAC = LAC
        self.CellId = CellId
        self.Uplink = Uplink
        self.Downlink = Downlink
        self.PCI = PCI
