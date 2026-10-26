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
import relations_unum

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
        unum = json.loads(unum_file.read())["unum"]

    unum_cumulus.Base.UNUM = unum

    api = relations_restx.Api(app)

    with open("/opt/service/secret/mysql.json", "r", encoding="utf-8") as mysql_file:
        mysql = json.loads(mysql_file.read())

    # Cumulus's own DB, which keeps the cumulus name when it's migrated, is behind the routed source here, the one
    # the models name, so every operation on them is routed by the Route rows in the unum schema, which unifist-unum
    # owns and migrates. The unifist schema is its too, for ids and the journal.

    local = f"{app.cumulus}-local"

    app.sources = [
        relations_pymysql.Source(name, schema=schema.replace('-', '_'), autocommit=True, **mysql)
        for name, schema in [
            (local, app.cumulus),
            (app.unifist, app.unifist),
            (relations_unum.UnumBase.SOURCE, relations_unum.UnumBase.SOURCE)
        ]
    ]

    relations_unum.Source(app.cumulus, unum=unum, local=local)

    app.unum = unum

    def ping():
        for source in app.sources:
            source.connection.ping(True)

    app.before_request(ping)

    api.add_resource(Health, '/health')

    relations_unifist.attach(api, sys.modules[__name__], unum_cumulus.models())

    return app

def route(app):
    """
    Routes this unum's data to this app's DB, once: it's a Route row in the unum schema, which is there already
    because unifist-unum migrates it, so it's a start up, not part of building the app
    """

    row = {"unum": app.unum, "source": app.cumulus, "role": "owner", "holder": app.unum}

    if not relations_unum.Route.many(**row).retrieve():
        relations_unum.Route(**row).create()


class Health(flask_restx.Resource):
    """
    Class for Health checks
    """

    def get(self):
        """
        Just return ok
        """
        return {"message": "OK"}
