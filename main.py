import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template
from ocr import process_image
import json

app = Flask(__name__)
_VERSION = 1  # API version

@app.route('/')
def main():
    return jsonify(
            {"success": "All is ok."}
        )

@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        name_image = request.json['name_image']
        output = process_image(url, name_image)
        return jsonify(json.loads(output))
    except:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_image_url'}"}
        )

@app.errorhandler(500)
def internal_error(error):
    print(error)  # ghetto logging


@app.errorhandler(404)
def not_found_error(error):
    print(error)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)
