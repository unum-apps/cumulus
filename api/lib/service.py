"""
Module for the Cumulus API
"""

import json
import sys

import micro_logger

import flask
import flask_restx
import relations_pymysql
import relations_restx
import relations_unifist

import unum_cumulus

WHO = "cumulus"
NAME = f"{WHO}-api"

def build():
    """
    Builds the Flask App
    """

    app = flask.Flask(NAME)

    app.logger = micro_logger.getLogger(NAME)
    app.cumulus = unum_cumulus.SOURCE
    app.unifist = unum_cumulus.UNIFIST

    with open("/opt/service/config/unum.json", "r", encoding="utf-8") as unum_file:
        unum_cumulus.Base.UNUM = json.loads(unum_file.read())["unum"]

    api = relations_restx.Api(app)

    with open("/opt/service/secret/mysql.json", "r", encoding="utf-8") as mysql_file:
        mysql = json.loads(mysql_file.read())

    app.sources = [
        relations_pymysql.Source(name, schema=name.replace('-', '_'), autocommit=True, **mysql)
        for name in [app.cumulus, app.unifist]
    ]

    def ping():
        for source in app.sources:
            source.connection.ping(True)

    app.before_request(ping)

    api.add_resource(Health, '/health')

    relations_unifist.attach(api, sys.modules[__name__], unum_cumulus.models())

    return app

class Health(flask_restx.Resource):
    """
    Class for Health checks
    """

    def get(self):
        """
        Just return ok
        """
        return {"message": "OK"}
