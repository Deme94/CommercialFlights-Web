from http import HTTPStatus

from flask import Flask
from flask import jsonify, abort, request
from flask_cors import CORS

import SentimentAnalysis as analysis

app = Flask(__name__)

CORS(app)

opiniones = []


@app.route('/index', methods=['GET'])
def index():
    return jsonify({'resultado': "Hola Mundo"})


@app.route('/opiniones', methods=['GET'])
def get_opiniones():
    return jsonify({'opiniones': opiniones})


@app.route('/opiniones/<int:id>', methods=['GET'])
def get_opinion(id):
    opinion = list(filter(lambda t: t['id'] == id, opiniones))
    if len(opinion) == 0:
        abort(HTTPStatus.BAD_REQUEST)
    return jsonify({'opiniones': opinion[0]})


@app.route('/opiniones', methods=['POST'])
def create_opinion():
    if not request.json or not 'comentario' in request.json:
        abort(HTTPStatus.BAD_REQUEST)
    if not opiniones:
        id = 1
    else:
        id = opiniones[-1]['id'] + 1
    comentario = request.json['comentario']
    compound = analysis.analizar_string(analysis.detectAndTransalate(comentario))
    opinion = {
        'id': id,
        'comentario': comentario,
        'compound': compound,
    }
    opiniones.append(opinion)
    return jsonify({'opinion': opinion})


@app.route('/opiniones/<int:id>', methods=['DELETE'])
def delete_opinion(id):
    opinion = list(filter(lambda t: t['id'] == id, opiniones))
    if len(opinion) == 0:
        abort(HTTPStatus.BAD_REQUEST)
    opiniones.remove(opinion[id])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
