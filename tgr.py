from connectmongo import returnclient,returndatabase
current_Client = returnclient()
current_DB = returndatabase()
commands_collection = current_DB["commands_collection"]
def insertcommand2db(session_id, command):
    commands_collection.insert_one({
        "sessionId": session_id,
        "command": command,
        "status": "queued"
    })
def updatecommand2db(session_id):
    commands_collection.update_one({"sessionId": session_id}, {"$set": {"status": "processed"}})

def find_queuedfromdb():
    command_doc = commands_collection.find_one({"status": "queued"})
    return command_doc
def updateresults(session_id, results):
    commands_collection.update_one({"sessionId": session_id}, {"$set": {"results": results, "status": "completed"}})

def fetch_resultsfromdb(session_id):
    result = commands_collection.find_one({"sessionId": session_id})
    return result
def deleteindb(session_id):
    result = commands_collection.delete_one({"sessionId": session_id})
