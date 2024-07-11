from connectmongo import returnclient,returndatabase
current_Client = returnclient()
current_DB = returndatabase()
cardPosCollection = current_DB["CardPosCollection"]
atmStats = current_DB["ATMStats"]
transStats = current_DB["TransStats"]
def insert_into_card_collection(record):
    cardPosCollection.insert_one(record)
def sendATMstats(record):
    atmStats.insert_one(record)
def sendAtranstats(record):
    transStats.insert_one(record)
