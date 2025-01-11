from io import BytesIO
from flask import Flask, request, jsonify
from trackedpose import insert_into_trackedpose_collection
from atm import insert_into_card_collection, sendATMstats,sendAtranstats, ratinglevel
from tgr import insertcommand2db, find_queuedfromdb, receiveresultsfromquest, fetch_my_Results, endauthcommand
from datetime import datetime
app = Flask(__name__) #app is an /object of Flask, Note that it is the name of the python file also
#app is the name of our application
#the variable __name__ <dunder-name-dunder>, name is a variable python assigns to modules/python files


@app.route("/")
def homepage():
    return "Welcome to Gaurish's Flask server"
@app.route("/success")
def successpage():
    return "Task successful"
@app.route("/failure")
def failure():
    return "Task failed"
@app.route("/uploadtpd", methods=['POST'])
def uploadTPDvalues():
    try:
        received_Driver = request.get_json()
        received_Driver = dict(received_Driver)        
        insert_into_trackedpose_collection(received_Driver)
        return 'File uploaded successfully', 201
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route("/uploadcardpos", methods=['POST'])
def uploadCardPosvalues():
    try:
        received_card_pos = request.get_json()
        received_card_pos = dict(received_card_pos)
        print(received_card_pos)
        insert_into_card_collection(received_card_pos)        
        return 'File uploaded successfully', 201
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route("/transactions", methods=['POST'])
def uploadATMStatsTransaction():
    try:
        received_Stats = request.get_json()
        received_Stats = dict(received_Stats)        
        sendAtranstats(received_Stats)
        return 'File uploaded successfully', 201
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    

@app.route("/sessionstats", methods=['POST'])
def uploadATMStats():
    try:
        received_Stats = request.get_json()
        received_Stats = dict(received_Stats)        
        sendATMstats(received_Stats)
        return 'File uploaded successfully', 201
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



@app.route("/atmrating", methods=['POST'])
def uploadATMRating():
    try:
        rating = request.get_json()
        rating = dict(rating)  
        ratinglevel(rating)      
        return 'Rating uploaded successfully', 201
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.get_json()
    command = data.get("command")
    session_id = data.get("sessionId")

    if not command or not session_id:
        return jsonify({"error": "Command or sessionId missing"}), 400

    # Store the command in MongoDB with 'queued' status
    command_data = {
        "sessionId": session_id,
        "command": command,
        "status": "queued",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if(command == "END"):
        endauthcommand()
    insertcommand2db(command_data)
    return jsonify({"status": "queued", "sessionId": session_id, "command": command}), 200

@app.route('/forward', methods=['GET'])
def forward_command():
    command_doc = find_queuedfromdb()
    
    if not command_doc:
        return jsonify({"status": "queue empty"}), 404

    # Return the command to Quest
    return jsonify({
        "sessionId": command_doc["sessionId"],
        "command": command_doc["command"]
    }), 200

@app.route('/results', methods=['POST'])
def receive_results():
    data = request.get_json()
    session_id = data.get("sessionId")
    results = data.get("results")

    if not session_id or not results:
        return jsonify({"error": "Missing sessionId or results"}), 400
    receiveresultsfromquest(session_id,results)
    # Store the results in MongoDB
    return jsonify({"status": "results received"}), 200
# Endpoint for Mobile App to fetch results
@app.route('/results', methods=['GET'])
def fetch_results():
    session_id = request.args.get("sessionId")
    if not session_id:
        return jsonify({"error": "Missing sessionId"}), 400

    result = fetch_my_Results(session_id)
    if result and "results" in result:
        return jsonify(result["results"]), 200
    return jsonify({"error": "Results not ready"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
##This is to ensure that application executed only when python app.py is run
##Every module in python gets the name variable set to __main__ if eecuted directly
##When we write these import statements, python will also execute those modules with name in such cases set to the name of the module