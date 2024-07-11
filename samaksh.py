
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # db = SQLAlchemy(app)


# class File(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(100))
#     file_data = db.Column(db.LargeBinary)


# with app.app_context():
#     db.create_all()

# @app.route("/glbfileupload", methods=['POST'])
# def glbfilehandleruploader():    
#     try:
#         if 'X-Filename' in request.headers:
#             filename = request.headers['X-Filename']
#         # You can use the filename here as needed
#             print(f"Received filename: {filename}")

#         # Check if content type is octet-stream
#         if request.content_type != 'application/octet-stream':
#             return "Invalid content type. Expected application/octet-stream.", 400
        
#         # Save the binary data to the database
#         new_file = File(filename=filename+".glb", file_data=request.data)
#         db.session.add(new_file)
#         db.session.commit()

#         return 'File uploaded successfully', 201

#     except Exception as e:
#         return f"An error occurred: {str(e)}", 500


# @app.route("/audiofileupload", methods=['POST'])
# def audiofilehandleruploader():    
#     try:
#         if 'X-Filename' in request.headers:
#             filename = request.headers['X-Filename']
#         # You can use the filename here as needed
#             print(f"Received filename: {filename}")

#         # Check if content type is octet-stream
#         if request.content_type != 'audio/wav':
#             return "Invalid content type. Expected audio/wav", 400
        
#         # Save the binary data to the database
#         new_file = File(filename=filename+".wav", file_data=request.data)
#         db.session.add(new_file)
#         db.session.commit()

#         return 'File uploaded successfully', 201

#     except Exception as e:
#         return f"An error occurred: {str(e)}", 500

# @app.route('/getglbfile', methods=['GET'])
# def getglbfile():
#     filename = request.args.get('filename')

#     if not filename:
#         return "Missing filename parameter"

#     file = File.query.filter_by(filename=filename).first()
#     print(file)

#     if not file:
#         print("File not")
#         return "No Such File"

#     # Assuming file_data contains GLB data, send it as a GLB file
#     return send_file(BytesIO(file.file_data), mimetype='application/octet-stream', as_attachment=True,download_name=filename)


# @app.route('/getaudiofile', methods=['GET'])
# def getaudiofile():
#     filename = request.args.get('filename')

#     if not filename:
#         return "Missing filename parameter"

#     audio_file = File.query.filter_by(filename=filename).first()

#     if not audio_file:
#         return "No Such File"

#     return send_file(BytesIO(audio_file.file_data), mimetype='audio/wav')

# @app.route("/getresourcelist",methods=['GET'])
# def get_files():
#     try:
#         files = File.query.all()
#         file_list = [file.filename for file in files]
#         return file_list
#     except Exception as e:
#         return jsonify(error=str(e)), 500
