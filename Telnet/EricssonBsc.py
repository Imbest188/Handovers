from Telnet.EricssonTelnet import EricssonTelnet
from threading import Thread
from Telnet.Parser import Parser
import datetime


class EricssonBsc:
    def __init__(self, name, host, login, password):
        self.__ext_gsm_cells = dict()
        self.__cells = dict()
        self.__ext_utran_cells = dict()
        self.__gsm_neighbour_relations = dict()
        self.__utran_neighbour_relations = dict()
        self.__gsm_neighbour_freq = dict()
        self.__utran_neighbour_freq = dict()

        self.__name = name
        self.__host = host
        self.__login = login
        self.__password = password

        self.__telnet = None
        self.__update_time = None
        self.data_is_ready = False
        Thread(target=self.__init_controller, daemon=True).start()

    def __clear_containers(self):
        self.__ext_gsm_cells.clear()
        self.__cells.clear()
        self.__ext_utran_cells.clear()
        self.__gsm_neighbour_relations.clear()
        self.__utran_neighbour_relations.clear()
        self.__gsm_neighbour_freq.clear()
        self.__utran_neighbour_freq.clear()

    def __init_controller(self):
        self.__telnet = EricssonTelnet(ip=self.__host, login=self.__login, password=self.__password)
        self.update_elements()

    def __get_data(self, command) -> dict:
        return Parser.parse(self.__telnet.get(command))

    def update_elements(self) -> None:
        self.data_is_ready = False
        self.__clear_containers()
        self.__cells = self.__get_data('RLDEP:CELL=ALL;')
        self.__ext_utran_cells = self.__get_data('RLDEP:CELL=ALL,EXT,UTRAN;')
        self.__ext_gsm_cells = self.__get_data('RLDEP:CELL=ALL,EXT;')
        self.__gsm_neighbour_freq = self.__get_data('RLMFP:CELL=ALL,LISTTYPE=IDLE;')
        self.__utran_neighbour_freq = self.__get_data('RLUMP:CELL=ALL,LISTTYPE=IDLE;')
        self.__gsm_neighbour_relations = self.__get_data('RLNRP:CELL=ALL,NODATA;')
        self.__utran_neighbour_relations = self.__get_data('RLNRP:CELL=ALL,UTRAN;')
        self.__update_time = datetime.datetime.now()
        self.data_is_ready = True

    def get_name(self) -> str:
        return self.__name

    def get_cells(self) -> dict:
        return self.__cells

    def get_update_time(self) -> datetime:
        return self.__update_time

    def get_ext_gsm_cells(self) -> dict:
        return self.__ext_gsm_cells

    def get_ext_utran_cells(self) -> dict:
        return self.__ext_utran_cells

    def get_gsm_neighbour_freq(self) -> dict:
        return self.__gsm_neighbour_freq

    def get_utran_neighbour_freq(self) -> dict:
        return self.__utran_neighbour_freq

    def get_gsm_neighbour_relations(self) -> dict:
        return self.__gsm_neighbour_relations

    def get_utran_neighbour_relations(self) -> dict:
        return self.__utran_neighbour_relations
