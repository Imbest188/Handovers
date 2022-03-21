class Parser:
    @staticmethod
    def __line_to_values(line) -> list[str]:
        return [x for x in line.strip().split(' ') if len(x)]

    @staticmethod
    def __parse_rldep_gsm(data, ext=False) -> dict:
        next_is_value = False
        result = {}
        for line in data.split('\n'):
            if next_is_value:
                next_is_value = False
                cell, cgi, bsic, bcchno, *_ = Parser.__line_to_values(line)
                _, _, lac, cid = cgi.split('-')
                ncc = bsic[0]
                bcc = bsic[1]
                result[cell] = {'CID': cid, 'CGI': cgi, 'BSIC': bsic,
                                'BCCHNO': bcchno, 'LAC': lac, 'NCC': ncc, 'BCC': ncc}
            if 'CELL     CGI' in line:
                next_is_value = True
        command_name = 'RLDEP GSM'
        if ext:
            command_name += ' EXT'
        return result

    @staticmethod
    def __parse_rldep_utran(data) -> dict:
        next_is_value = False
        result = {}
        for line in data.split('\n'):
            if next_is_value:
                next_is_value = False
                cell, utranid, arfcn, scrcode, *_ = Parser.__line_to_values(line)
                result[cell] = {'UTRANID': utranid, 'FDDARFCN': arfcn, 'SCRCODE': scrcode}
            if 'CELL     UTRANID' in line:
                next_is_value = True

        return result

    @staticmethod
    def __parse_rlnrp(data) -> dict:
        next_is_cell = False
        next_is_cellr = False
        current_cell = ''
        result = {}
        cells_r = []
        for line in data.split('\n'):
            if next_is_cell:
                if len(current_cell):
                    result[current_cell] = cells_r
                    cells_r = []
                current_cell = line.strip()
                next_is_cell = False
            elif next_is_cellr:
                cells_r.append(line.split(' ')[0])
                next_is_cellr = False
            elif line.startswith('CELLR'):
                next_is_cellr = True
            elif line.startswith('CELL') or line.startswith('END'):
                next_is_cell = True

        return result

    @staticmethod
    def __parse_rldep(data) -> dict:
        return Parser.__parse_rldep_utran(data) if 'UTRANID' in data else Parser.__parse_rldep_gsm(data)

    @staticmethod
    def __parse_rlmfp(data) -> dict:
        next_is_cell = False
        mbcch_lines = False
        current_cell = ''
        result = {}
        mbcchs = []
        for line in data.split('\n'):
            if next_is_cell:
                if len(current_cell):
                    result[current_cell] = mbcchs
                    mbcchs = []
                current_cell = line.strip()
                next_is_cell = False
            elif mbcch_lines:
                if not len(line) or 'END' in line or 'CELL' in line:
                    mbcch_lines = False
                else:
                    mbcchs += Parser.__line_to_values(line)
            if line.startswith('CELL') or line.startswith('END'):
                next_is_cell = True
            elif line.startswith('MBCCHNO'):
                mbcch_lines = True
        return result

    @staticmethod
    def __parse_rlump(data) -> dict:
        next_is_cell = False
        umfi_lines = False
        current_cell = ''
        result = {}
        umfis = []
        for line in data.split('\n'):
            line = line.strip()
            if next_is_cell:
                if len(current_cell):
                    result[current_cell] = umfis
                    umfis = []
                current_cell = line
                next_is_cell = False
            elif umfi_lines:
                if not len(line) or 'END' in line or 'CELL' in line:
                    umfi_lines = False
                else:
                    umfis.append(line)
            if line.startswith('CELL') or line.startswith('END'):
                next_is_cell = True
            elif 'UMFI' in line:
                umfi_lines = True
        return result

    @staticmethod
    def parse(data: str) -> dict:
        if 'CELL DESCRIPTION DATA' in data:
            return Parser.__parse_rldep(data)
        elif 'NEIGHBOUR RELATION DATA' in data:
            return Parser.__parse_rlnrp(data)
        elif 'CELL MEASUREMENT FREQUENCIES' in data:
            return Parser.__parse_rlmfp(data)
        elif 'UTRAN MEASUREMENT FREQUENCY' in data:
            return Parser.__parse_rlump(data)
