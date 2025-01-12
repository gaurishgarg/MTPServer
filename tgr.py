from connectmongo import returnclient,returndatabase
from datetime import datetime
current_Client = returnclient()
current_DB = returndatabase()
commands_collection = current_DB["commands_collection"]
results_collection = current_DB["results"]
def insertcommand2db(command_data):
   commands_collection.insert_one(command_data)
def updatecommand2db(session_id):
    commands_collection.update_one({"sessionId": session_id}, {"$set": {"status": "processed"}})

def find_queuedfromdb():
    command_doc = commands_collection.find_one({"status": "queued"})
    return command_doc
def receiveresultsfromquest(session_id,results):
    results_collection.update_one(
        {"sessionId": session_id},
        {"$set": {"results": results, "status": "completed", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}},
        upsert=True
    )
    # Update the command status to "completed" in the commands_collection
    commands_collection.update_one(
        {"sessionId": session_id, "status": "queued"},  # Ensure we're updating the "queued" status
        {"$set": {"status": "completed"}}  # Mark the command as "completed"
    )
# Delete the processed command
    
def fetch_my_Results(session_id):
    result_doc = results_collection.find_one({"sessionId": session_id})

    # If result is found, format it to match the ResultsResponse structure
    if result_doc:
        results_response = {
            "status": result_doc.get("status", ""),
            "sessionId": result_doc.get("sessionId", ""),
            "results": result_doc.get("results", {}),  # Assuming results are stored as an object
            "timestamp": result_doc.get("timestamp", "")
        }
        return results_response
    else:
        return {"error": "Results not found"}
def endauthcommand(session_id):
     # Find the corresponding "AUTH" command with the same sessionId and "queued" status
        auth_command = commands_collection.find_one({"sessionId": session_id, "command": "AUTH", "status": "queued"})
        
        if auth_command:
            # Update the "AUTH" command status to "completed"
            commands_collection.update_one(
                {"_id": auth_command["_id"]},
                {"$set": {"status": "completed"}}
            )
def deletequeuedrecords():
    commands_collection.delete_many({})