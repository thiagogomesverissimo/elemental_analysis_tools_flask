import sys
import os
import pathlib
from app import app, db, lm
import numpy

from elemental_analysis_tools import micromatter
from elemental_analysis_tools import winqxas
from elemental_analysis_tools import shimadzu
from elemental_analysis_tools.responseFactor import responseFactor

def prepare(uploads):
    """
    Esse método prepara as variáveis para o template:
    elements: 
    info: Informações dos alvos de calibração, no caso, por enquanto da micromatter
     ResponseFactors, 
    """
    info = {}
    ResponseFactors = {}
    ResponseFactorsErrors = {}
    elements = {}
    uploads_metadata = {}

    Z = []
    Y = []
    Yerror = []

    for i in uploads:
        # a ideia é que seja genérico para qualquer alvo padrão, mas por hora fixar na micromatter
        file_path = os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv')
        micromatter_file = pathlib.Path(file_path).read_text()

        info[i.standard_target] = micromatter.get(i.standard_target, micromatter_file)

        # txt
        txt_content = pathlib.Path( app.config['FILES'] + '/' + i.txt_file).read_text()
        txt_info = winqxas.parseTxt(txt_content)

        # csv
        csv_content = pathlib.Path( app.config['FILES'] + '/' + i.csv_file).read_text()
        csv_info = shimadzu.parseCsv(csv_content)

        elements[i.standard_target] = {}
        ResponseFactors[i.standard_target] = {}
        ResponseFactorsErrors[i.standard_target] = {}

        elements[i.standard_target] = [ x for x in info[i.standard_target].keys() if x is not 'total' ]

        for element in elements[i.standard_target]:
            # se tiver espectro para o elemento em questão, calcula, senão passa direto
            try:
                density = float(info[i.standard_target][element])
                N = float(txt_info['K']['peaks'][element])
                sigma_N = float(txt_info['K']['errors'][element])

                R, sigma_R = responseFactor(N,density,csv_info['current'],csv_info['livetime'],sigma_N)

                ResponseFactors[i.standard_target][element] = R
                ResponseFactorsErrors[i.standard_target][element] = sigma_R

                Z.append(float(element))
                Y.append(R)
                Yerror.append(sigma_R)               

            except:
               pass

    # ATENÇÃO: Falta tirar média
    response_factors_final = {'Z': Z , 'Y': Y , 'Yerror': Yerror}

    return (info, elements, ResponseFactors, ResponseFactorsErrors, response_factors_final)
