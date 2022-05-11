import logging
from flask import Flask, make_response, request, jsonify
from flask_restx import Resource, Api, fields
from data import map_input, map_inputs


def initialize_api():
    app = Flask(__name__)
    api = Api(app, version="0.0.1", title="GEHC Data Conversion API")

    @api.route("/api/v1/convert/bulk")
    class convertBulkEntries(Resource):
        def post(self):
            try:
                entries = request.json.get("entry", [])
                result = map_inputs(entries)
                return make_response(jsonify(result), 200)
            except Exception as e:
                logging.info(f"{e}")
                return make_response("Error happened while converting data", 500)

    @api.route("/api/v1/convert")
    class convertSingleEntry(Resource):
        def post(self):
            try:
                entry = request.json
                result = map_input(entry)
                return make_response(jsonify(result), 200)
            except Exception as e:
                logging.info(f"{e}")
                return make_response("Error happened while converting data", 500)

    return app
