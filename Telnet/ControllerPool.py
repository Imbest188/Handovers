from Telnet.EricssonBsc import EricssonBsc as Bsc
import time


class ControllerPool:
    def __init__(self):
        self.__pool = []
        self.__data = {}

    def add_controller(self, name, host, login, password):
        self.__pool.append(Bsc(name, host, login, password))

    def __data_was_loaded(self):
        for bsc in self.__pool:
            if not bsc.data_is_ready:
                return False
        return True

    def get_cell_info(self, cell_id):
        while not self.__data_was_loaded():
            time.sleep(1)
        for bsc in self.__pool:
            cells = bsc.get_cells()
            if cell_id in cells.keys():
                return cells[cell_id]
        return None

    def get_ext_cell_info(self, cell_id):
        while not self.__data_was_loaded():
            time.sleep(1)
        for bsc in self.__pool:
            cells = bsc.get_ext_gsm_cells()
            ucells = bsc.get_ext_utran_cells()
            if cell_id in cells.keys():
                return cells[cell_id]
            if cell_id in ucells.keys():
                return ucells[cell_id]
        return None

    def get_utran_neighbour_relations(self, cell_id):
        while not self.__data_was_loaded():
            time.sleep(1)
        for bsc in self.__pool:
            cells = bsc.get_utran_neighbour_relations()
            if cell_id in cells.keys():
                return cells[cell_id]
        return None

    def get_gsm_neighbour_relations(self, cell_id):
        while not self.__data_was_loaded():
            time.sleep(1)
        for bsc in self.__pool:
            cells = bsc.get_gsm_neighbour_relations()
            if cell_id in cells.keys():
                return cells[cell_id]
        return None

    def get_utran_neighbour_freq(self, cell_id):
        while not self.__data_was_loaded():
            time.sleep(1)
        for bsc in self.__pool:
            cells = bsc.get_utran_neighbour_freq()
            if cell_id in cells.keys():
                return cells[cell_id]
        return None

    def get_gsm_neighbour_freq(self, cell_id):
        while not self.__data_was_loaded():
            time.sleep(1)
        for bsc in self.__pool:
            cells = bsc.get_gsm_neighbour_freq()
            if cell_id in cells.keys():
                return cells[cell_id]
        return None
