# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import os
import json

app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*":{"origins":"https://argentinaferiados-api.vercel.app/"}})

# Obtener la ruta del directorio actual
current_directory = os.path.dirname(os.path.realpath(__file__))

# Construir la ruta completa a los archivos JSON
ref_json_path = os.path.join(current_directory, 'data', 'ref.json')
data_2024_json_path = os.path.join(current_directory, 'data', '2024.json')

# Cargar datos desde los archivos JSON
with open(ref_json_path, 'r') as ref_file:
    ref_data = json.load(ref_file)

with open(data_2024_json_path, 'r') as data_2024_file:
    data_2024 = json.load(data_2024_file)

# Función para obtener la información combinada
def obtener_feriados():
    feriados_combinados = []

    # Iterar sobre los datos de 2024.json y combinar con la información de ref.json
    for mes_info in data_2024:
        mes = mes_info['mes']

        for dia, evento_keys in mes_info.items():
            if dia != 'mes':
                if isinstance(evento_keys, list):
                    for evento_key in evento_keys:
                        evento = ref_data[evento_key]
                        feriados_combinados.append({
                            'motivo': evento['motivo'],
                            'tipo': evento['tipo'],
                            'info': evento['info'],
                            'dia': int(dia),
                            'mes': mes,
                            'id': evento_key
                        })
                else:
                    # Manejar múltiples días en una cadena
                    dias = [int(d) for d in dia.split(',')]
                    for d in dias:
                        evento = ref_data[evento_keys]
                        feriados_combinados.append({
                            'motivo': evento['motivo'],
                            'tipo': evento['tipo'],
                            'info': evento['info'],
                            'dia': d,
                            'mes': mes,
                            'id': evento_keys
                        })
    return feriados_combinados

# Ruta para obtener la información combinada como una API
#@cross_origin
@app.route('/', methods=['GET'])
def obtener_api_feriados_combinados():
    feriados_combinados = obtener_feriados()
    return jsonify({'Feriados': feriados_combinados})

if __name__ == '__main__':
    app.run(debug=True)
