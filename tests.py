import unittest
from utility import get_user_query
from utility import search_list
from pymongo import MongoClient
from pymongo import errors


class TestDBQueries(unittest.TestCase):

    test_collections = list

    # Initialize the MongoDB client and database; create list of collections that will be used between all tests for this class
    def setUpClass(cls):
        try:
            db_client = MongoClient("mongodb://localhost:27017/")
            relic_db = db_client['WarframeRelics']

            axi_collection = relic_db.get_collection("Axi")
            neo_collection = relic_db.get_collection("Neo")
            meso_collection = relic_db.get_collection("Meso")
            lith_collection = relic_db.get_collection("Lith")

            cls.test_collections = [axi_collection, neo_collection, meso_collection, lith_collection]

        except errors.ConnectionFailure:
            print('Connection to MongoDB failed, please double-check configs and try again.')
            exit(0)

        except errors.PyMongoError as generic_error:
            print('Some other PyMongo error occurred, see printed text for details.')
            print(generic_error)
            exit(0)

    # Test to make sure a query containing partial items works correctly (eg. Trinity, Afuris, etc)
    def test_partial_query(self):
        test_query = "Trinity"
        query_results = get_user_query(test_query, self.test_collections)

        for item in query_results:
            error_message = "{} does not contain substring {}".format(item, test_query)
            self.assertIn(test_query, item, error_message)

    # Test to make sure a fully named item will query and display correctly
    def test_full_query(self):
        test_query = "Trinity Prime Neuroptics"
        query_results = get_user_query(test_query, self.test_collections)

        for item in query_results:
            error_message = "{} does not contain substring {}".format(item, test_query)
            self.assertIn(test_query, item, error_message)

    def test_small_query(self):
        return 0
