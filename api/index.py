from flask import Flask, jsonify

app = Flask(__name__)

# Cargar datos desde los archivos JSON
with open('data/ref.json', 'r') as ref_file:
    ref_data = json.load(ref_file)

with open('data/2024.json', 'r') as data_2024_file:
    data_2024 = json.load(data_2024_file)

# Función para obtener la información combinada
def obtener_eventos_combinados():
    eventos_combinados = []

    # Iterar sobre los datos de 2024.json y combinar con la información de ref.json
    for mes_info in data_2024:
        mes = mes_info['mes']

        for dia, evento_key in mes_info.items():
            if dia != 'mes':
                if isinstance(evento_key, list):
                    for subevento in evento_key:
                        evento = ref_data[subevento]
                        eventos_combinados.append({
                            'motivo': evento['motivo'],
                            'tipo': evento['tipo'],
                            'info': evento['info'],
                            'dia': int(dia),
                            'mes': mes,
                            'id': subevento
                        })
                else:
                    evento = ref_data[evento_key]
                    eventos_combinados.append({
                        'motivo': evento['motivo'],
                        'tipo': evento['tipo'],
                        'info': evento['info'],
                        'dia': int(dia),
                        'mes': mes,
                        'id': evento_key
                    })

    return eventos_combinados

# Ruta para obtener la información combinada como una API
@app.route('/api/eventos_combinados', methods=['GET'])
def obtener_api_eventos_combinados():
    eventos_combinados = obtener_eventos_combinados()
    return jsonify({'eventos_combinados': eventos_combinados})

if __name__ == '__main__':
    app.run(debug=True)
