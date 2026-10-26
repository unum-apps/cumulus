import unittest
import unittest.mock

import relations
import relations.unittest

import service
import unum_cumulus

import os
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

MODELS = ["Bucket", "Entity", "Flush", "Journal", "Scat", "Sequence", "Slug", "Unifist", "UnifistUnum", "Unum"]

SECRET = '{"host": "%s", "user": "root", "password": ""}' % os.environ["MYSQL_HOST"]

class Testrestx(relations.unittest.TestCase):

    @unittest.mock.patch.dict('os.environ', {"LOG_LEVEL": "INFO", "UNIFIST_UNUM": "test"})
    @unittest.mock.patch('service.open', new_callable=unittest.mock.mock_open, read_data=SECRET)
    def setUp(self, mock_open):

        self.app = service.build()
        self.api = self.app.test_client()

        migrations = relations.Migrations()

        for source in self.app.sources:

            source.connection.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{source.name}`")
            migrations.load(source.name, "definition.sql")

    def tearDown(self):

        for source in self.app.sources:
            source.connection.cursor().execute(f"DROP DATABASE IF EXISTS `{source.name}`")


class TestModels(unittest.TestCase):

    def test_models(self):

        self.assertEqual(sorted(model.__name__ for model in unum_cumulus.models()), MODELS)


class TestAPI(Testrestx):

    @unittest.mock.patch.dict('os.environ', {"LOG_LEVEL": "INFO", "UNIFIST_UNUM": "test"})
    @unittest.mock.patch('service.open', new_callable=unittest.mock.mock_open, read_data=SECRET)
    def test_build(self, mock_open):

        app = service.build()

        self.assertEqual(app.name, "cumulus-api")
        self.assertEqual(app.cumulus, "cumulus")
        self.assertEqual(app.unifist, "unifist")
        self.assertEqual([source.name for source in app.sources], ["cumulus", "unifist"])
        self.assertEqual(unum_cumulus.Base.UNUM, "test")

    def test_migrations(self):

        migrations = relations.Migrations()

        for name in ["cumulus", "unifist"]:

            cursor = self.app.sources[0].connection.cursor()

            for stamp, pair in migrations.list(name).items():

                cursor.execute(f"DROP DATABASE IF EXISTS `{name}`")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{name}`")

                try:
                    migrations.load(name, pair["definition"])
                    migrations.load(name, pair["migration"])
                except Exception as exception:
                    print(stamp)
                    raise exception

class TestHealth(Testrestx):

    def test_get(self):

        self.assertStatusValue(self.api.get("/health"), 200, "message", "OK")


class TestModelAPI(Testrestx):

    def test_models(self):

        response = self.api.get("/model")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(model["title"] for model in response.json["models"]), MODELS)

    def test_empty(self):

        for model in self.api.get("/model").json["models"]:
            response = self.api.get(f"/model/{model['singular']}")
            self.assertEqual(response.status_code, 200, model["singular"])
            self.assertEqual(response.json[model["plural"]], [], model["singular"])

    def test_scat(self):

        response = self.api.post("/model/unifist", json={"unifist": {"who": "Gaf"}})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["unifist"]["id"], "gaf:unifist.cumulus:test")

        response = self.api.post("/model/entity", json={"entity": {"id": "gaf:unifist.cumulus:test"}})

        self.assertEqual(response.status_code, 201)

        response = self.api.post("/model/scat", json={"scat": {
            "entity_id": "gaf:unifist.cumulus:test",
            "description": "Out of milk"
        }})

        self.assertEqual(response.status_code, 201)

        scat_id = response.json["scat"]["id"]

        self.assertEqual(scat_id, "1:scat.cumulus:test")

        response = self.api.get(f"/model/scat/{scat_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["scat"]["description"], "Out of milk")
        self.assertEqual(response.json["scat"]["unum"], "test")

        response = self.api.get("/model/journal")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["journals"]), 3)
