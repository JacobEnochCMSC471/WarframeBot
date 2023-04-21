def search_list(queryObj, itemName):
    count = 0
    for item in queryObj:
        if count > 5:
            print("Item not found!")
            return -1

        if item['itemName'] == itemName:
            return count
        else:
            count += 1


# Given a user query, return a formatted string that displays all relevant items and their respective relics needed
def get_user_query(query: str, collections: list):
    if all(char.isalpha() or char.isspace() for char in query):

        # Add lower limit to query length to prevent user errors or very long text; prevent user from querying all items at once
        if len(query) < 4 or query == 'prime':
            return None

        # As long as the user input is only characters, query collections for requested item
        userQuery = {'rewards.Intact.itemName': {'$regex': query}}
        combinedQueries = []

        for item in collections:
            combinedQueries.append(item.find(userQuery))

        relicList = []

        # Pull out item name, relic tier and relic name from queries, store in list
        for queryResult in combinedQueries:
            for indvResult in queryResult:
                itemIndex = search_list(indvResult['rewards']['Intact'], query)
                tempItemName = indvResult['rewards']['Intact'][itemIndex]['itemName']
                tempTier = indvResult['tier']
                tempName = indvResult['name']

                relicList.append({'tier': tempTier, 'name': tempName, 'itemName': tempItemName})

        botRelicResponse = '**-----Relics Needed For {}-----**\n'.format(relicList[0]['itemName'])

        # Append relic tiers/names to string that will be displayed to users
        for item in relicList:
            relicText = "{} {}\n".format(item['tier'], item['name'])
            botRelicResponse += relicText
