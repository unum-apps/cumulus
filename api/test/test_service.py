import unittest
import unittest.mock

import relations
import relations.unittest
import relations_unifist
import relations_unum

import service
import unum_cumulus

import glob
import os
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

MODELS = ["Bucket", "Entity", "Flush", "Journal", "Scat", "Sequence", "Slug", "Unifist", "UnifistUnum", "Unum"]

SECRET = '{"host": "%s", "user": "root", "password": ""}' % os.environ["MYSQL_HOST"]
CONFIG = '{"unum": "test", "local": "cumulus-test"}'

def opened(path, *args, **kwargs):
    """
    Stands in for open, giving the config file its unum and everything else the secret
    """

    return unittest.mock.mock_open(read_data=CONFIG if path.endswith("unum.json") else SECRET)(path, *args, **kwargs)

class Testrestx(relations.unittest.TestCase):

    @unittest.mock.patch.dict('os.environ', {"LOG_LEVEL": "INFO"})
    @unittest.mock.patch('service.open', side_effect=opened)
    def setUp(self, mock_open):

        self.app = service.build()
        self.api = self.app.test_client()

        for source in self.app.sources:
            source.connection.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{source.schema}`")

        by_name = {source.name: source for source in self.app.sources}

        # Cumulus's own tables come from its DDL, on the real DB source behind the routed one

        by_name["cumulus-test"].load("ddl/cumulus/mysql/definition.sql")

        # The unifist and unum tables belong to unifist-unum, so they're made from the base models, not from DDL here

        for model in relations.models(relations_unifist, relations_unifist.UnifistBase):
            by_name["unifist"].execute(model.define())

        for model in relations.models(relations_unum, relations_unum.UnumBase):
            by_name["unum"].execute(model.define())

    def tearDown(self):

        for source in self.app.sources:
            source.connection.cursor().execute(f"DROP DATABASE IF EXISTS `{source.schema}`")


class TestModels(unittest.TestCase):

    def test_models(self):

        self.assertEqual(sorted(model.__name__ for model in unum_cumulus.models()), MODELS)


class TestAPI(Testrestx):

    @unittest.mock.patch.dict('os.environ', {"LOG_LEVEL": "INFO"})
    @unittest.mock.patch('service.open', side_effect=opened)
    def test_build(self, mock_open):

        app = service.build()

        self.assertEqual(app.name, "cumulus-api")
        self.assertEqual(app.cumulus, "cumulus")
        self.assertEqual(app.unifist, "unifist")
        self.assertEqual([source.name for source in app.sources], ["cumulus-test", "unifist", "unum"])
        self.assertEqual(unum_cumulus.Base.UNUM, "test")

        routed = relations.source("cumulus")

        self.assertIsInstance(routed, relations_unum.Source)
        self.assertEqual(routed.unum, "test")
        self.assertEqual(routed.local, "cumulus-test")

    def test_route(self):

        routes = lambda: relations_unum.Route.many(unum="test", source="cumulus").retrieve()

        self.assertEqual(len(routes()), 0)

        service.route(self.app)

        self.assertEqual(len(routes()), 1)
        self.assertEqual(routes()[0].role, "owner")
        self.assertEqual(routes()[0].holder, "test")
        self.assertEqual(routes()[0].url, "")

        service.route(self.app)

        self.assertEqual(len(routes()), 1)

    def test_migrations(self):

        local = relations.source("cumulus-test")
        cursor = local.connection.cursor()

        for migration in sorted(glob.glob("ddl/cumulus/mysql/migration-*.sql")):

            stamp = migration.rsplit("migration-", 1)[-1].split(".")[0]

            cursor.execute("DROP DATABASE IF EXISTS `cumulus`")
            cursor.execute("CREATE DATABASE IF NOT EXISTS `cumulus`")

            try:
                local.load(f"ddl/cumulus/mysql/definition-{stamp}.sql")
                local.load(migration)
            except Exception as exception:
                print(stamp)
                raise exception

class TestHealth(Testrestx):

    def test_get(self):

        self.assertStatusValue(self.api.get("/health"), 200, "message", "OK")


class TestModelAPI(Testrestx):

    def test_models(self):

        response = self.api.get("/model")

        self.assertEqual(response.status_code, 200, response.json)
        self.assertEqual(sorted(model["title"] for model in response.json["models"]), MODELS)

    def test_empty(self):

        for model in self.api.get("/model").json["models"]:
            response = self.api.get(f"/model/{model['singular']}")
            self.assertEqual(response.status_code, 200, model["singular"])
            self.assertEqual(response.json[model["plural"]], [], model["singular"])

    def test_scat(self):

        response = self.api.post("/model/unifist", json={"unifist": {"who": "Gaf"}})

        self.assertEqual(response.status_code, 201, response.json)
        self.assertEqual(response.json["unifist"]["id"], "gaf:unifist.cumulus:test")

        response = self.api.post("/model/entity", json={"entity": {"who": "Gaf", "unifist_unum": "unifist"}})

        self.assertEqual(response.status_code, 201, response.json)

        entity_id = response.json["entity"]["id"]

        self.assertEqual(entity_id, "gaf-unifist:entity.cumulus:test")

        response = self.api.post("/model/scat", json={"scat": {
            "entity_id": entity_id,
            "description": "Out of milk"
        }})

        self.assertEqual(response.status_code, 201, response.json)

        scat_id = response.json["scat"]["id"]

        self.assertEqual(scat_id, "1:scat.cumulus:test")

        response = self.api.get(f"/model/scat/{scat_id}")

        self.assertEqual(response.status_code, 200, response.json)
        self.assertEqual(response.json["scat"]["description"], "Out of milk")
        self.assertEqual(response.json["scat"]["unum"], "test")

        response = self.api.get("/model/journal")

        self.assertEqual(response.status_code, 200, response.json)
        self.assertEqual(len(response.json["journals"]), 3)
