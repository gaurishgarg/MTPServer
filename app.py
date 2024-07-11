from io import BytesIO
from flask import Flask, request
from trackedpose import insert_into_trackedpose_collection
from atm import insert_into_card_collection, sendATMstats,sendAtranstats, ratinglevel
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

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
##This is to ensure that application executed only when python app.py is run
##Every module in python gets the name variable set to __main__ if eecuted directly
##When we write these import statements, python will also execute those modules with name in such cases set to the name of the module