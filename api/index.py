from flask import Flask, jsonify, request, make_response
import os
import json

app = Flask(__name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

app.after_request(add_cors_headers)

@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response()
    return response

current_directory = os.path.dirname(os.path.realpath(__file__))

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
    app.run(debug=True)