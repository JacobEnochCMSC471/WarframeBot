# Only use after database connection has been made. Prevents repeat code
import pymongo
from pymongo import MongoClient


def populate_collections_list(db):
    axi_collection = db.get_collection("Axi")
    neo_collection = db.get_collection("Neo")
    meso_collection = db.get_collection("Meso")
    lith_collection = db.get_collection("Lith")

    return [axi_collection, neo_collection, meso_collection, lith_collection]


'''
Old version that I know works 

# Search the lists of possible items for the item name and return the specific index with which the item belongs to
def search_list(queryObj, itemName):
    count = 0
    for item in queryObj:
        if count > 5:
            print("Item not found!")
            return -1

        if item['itemName'] in itemName:
            return count
        else:
            count += 1
'''


def search_list(queryObj, itemName):
    count = 0
    for item in queryObj:
        if count > 5:
            print("Item not found!")
            return -1

        if itemName in item['itemName']:
            return count
        else:
            count += 1


# Given a user query, return a formatted string that displays all relevant items and their respective relics needed
def get_user_query(query: str, collections: list):
    # Add lower limit to query length to prevent user errors or very long text; prevent user from querying all items at once
    if len(query) < 4:
        return 'Please enter a query that contains more than 4 characters.\n'

    elif (query == 'prime') or (query == 'Prime') or (len(query) == 5 and 'prime' in query):
        return 'Please do not try to query the whole database! Thank you!\n'

    # Make sure that the user-entered query has first words capitalized to ensure accurate querying
    split_query = query.split()

    for index, word in enumerate(split_query):
        split_query[index] = word.capitalize()

    query = ' '.join(split_query)

    # As long as the user input is only characters, query collections for requested item
    # Regex allows a partial query to occur -> can search "Spira" instead of the full "Spira Prime Blade"
    # Also allows users to find out what they need for all items of an item set instead of individually querying
    userQuery = {'rewards.Intact.itemName': {'$regex': query}}
    combinedQueries = []

    # Query all collections for the item, store in list for later access
    for item in collections:
        combinedQueries.append(item.find(userQuery))

    # Eventually store all relics in dict of lists; key = item name, values = relics
    item_dict = {}

    # Loop through query results from all collections and extract item name, relic name and relic tier
    for queryResult in combinedQueries:
        for indvResult in queryResult:
            itemIndex = search_list(indvResult['rewards']['Intact'], query)
            tempItemName = indvResult['rewards']['Intact'][itemIndex]['itemName']
            tempTier = indvResult['tier']
            tempName = indvResult['name']

            # If key exists, append to existing item
            if tempItemName in item_dict.keys():
                # item_dict[tempItemName].append([tempTier, tempName])
                item_dict[tempItemName].append({'tier': tempTier, 'name': tempName})

            # Create new key, value pair
            else:
                # item_dict[tempItemName] = [tempTier, tempName]
                item_dict[tempItemName] = []
                item_dict[tempItemName].append({'tier': tempTier, 'name': tempName})

    # Finally, loop through and find specific items/relics and store them in a string
    search_results = '__**----------Item Request Results----------**__\n'

    for primed_item in item_dict:
        search_results += '**-----{}-----**\n'.format(primed_item)
        curr_item_relics = item_dict[primed_item]

        for relic in curr_item_relics:
            temp_string = '{} {}\n'.format(relic['tier'], relic['name'])
            search_results += temp_string

        search_results += '\n'

    return search_results


# Read a list of unvaulted relics
def read_unvaulted_relics(filepath: str):
    if type(filepath) is not str:
        raise Exception('Filepath is not a string.')
    try:
        unvaulted_list = open(filepath, 'r')
        relic_list = []

        for line in unvaulted_list:
            relic_list.append(line.strip('\n'))

        return relic_list

    except FileNotFoundError as e:
        print('File not found. Please double-check the filepath that was entered and ensure that the "unvaulted.txt" file exists.')
        print(e)



def main():
    db_client = MongoClient("mongodb://localhost:27017/")
    relic_db = db_client['WarframeRelics']
    relic_collections = populate_collections_list(relic_db)
    # test_results = get_user_query('spira', relic_collections)
    filepath = 'unvaulted.txt'

    read_unvaulted_relics(filepath)


main()
