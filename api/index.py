from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Feriados Argentina API, use /<int:year> por ejemplo /2025 para obtener los feriados', 200

@app.route('/<int:year>', methods=['GET'])
def API(year):
    try:
        data_json_path = os.path.join(current_directory, 'data', f'{year}.json')
        with open(data_json_path, 'r', encoding='utf-8') as data_file:
            data_year = json.load(data_file)
        return jsonify(data_year), 200
    except FileNotFoundError:
        return jsonify({'error': 'No se encontraron feriados para el año proporcionado'}), 404

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    app.run(debug=True)
