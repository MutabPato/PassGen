# Flask app environment variables

export FLASK_APP=project # instructs flask on how to load the app
export FLASK_DEBUG=1 # enables debugger that will display application errors

# Configure the Database in the Python REPL using the create_all method on the db object

>>> from primary import db, create_app, models
>>> db.create_all(app=create_app()) # pass the create_app result do Flask_SQLAlchemy gets the configuration


