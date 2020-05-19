import sys
import os
import pathlib
from app import app, db, lm

from elemental_analysis_tools import micromatter

def Utils(uploads):
    info = {}
    ResponseFactors = {}
    elements= {}
    for i in uploads:
        # a ideia é que seja genérico para qualquer alvo padrão, mas por hora fixar na micromatter
        file_path = os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv')
        micromatter_file = pathlib.Path(file_path).read_text()

        info[i.standard_target] = micromatter.get(i.standard_target, micromatter_file)

        # txt
#        txt_content = pathlib.Path( app.config['FILES'] + '/' + i.txt_file).read_text()
#        txt_info = winqxas.parseTxt(txt_content)

        # csv
#        csv_content = pathlib.Path( app.config['FILES'] + '/' + i.csv_file).read_text()
#        csv_info = shimadzu.parseCsv(csv_content)

#        elements[i.micromatter_id] = {}
#        ResponseFactors[i.micromatter_id] = {}

#        elements[i.micromatter_id] = [ x for x in info[i.micromatter_id].keys() if x is not 'total']

#        for element in elements[i.micromatter_id]:
            # se tiver espectro para o elemento em questão, calcula, senão passa direto
#            try:
#                Z = element
#                density = float(info[i.micromatter_id][element])    
#                N = txt_info['K']['peaks'][Z]
#                ResponseFactors[i.micromatter_id][Z] = ResponseFactor(float(N),density,csv_info['current'],csv_info['livetime'])

#            except:
#               pass

#    return (info, ResponseFactors, elements)
    return (info)