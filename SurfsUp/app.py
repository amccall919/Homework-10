# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")

def home():
    print("Server received request for 'Home' page...")
    return (
        f"<h3>Available Routes:</h3><br/>"
        f"<b><a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a></b> <br />"
        f"<b><a href=\"/api/v1.0/stations\">/api/v1.0/stations</a></b><br />"
        f"<b><a href=\"/api/v1.0/tobs\">/api/v1.0/tobs</a></b> <br />"
        f"<b><a href=\"/api/v1.0/start/2014-09-09\">/api/v1.0/start</a></b> <br />"
        f"<b><a href=\"/api/v1.0/range?start=2014-09-14&end=2016-02-14\">/api/v1.0/range</a></b> <br />"
    )
#################################################
# /precipitation Route
#################################################
@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)
    sel = [Measurement.date, func.sum(Measurement.prcp)]
    annual_precip = session.query(*sel).\
                filter(Measurement.date >= '2016-08-23').\
                group_by(Measurement.date).all()
    session.close()
    precip_list = []
    for date, prcp in annual_precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)
#################################################
# /stations Route
#################################################
@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)
    print("Return a JSON list of stations from the dataset.")
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)
#################################################
# /tobs Route
#################################################
@app.route("/api/v1.0/tobs")

def tabs():
    session = Session(engine)
    most_active_annual = session.query(Measurement.tobs, Measurement.date).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= '2016-08-23').\
                    group_by(Measurement.date).\
                    order_by(Measurement.date).all()
    all_temps = list(np.ravel(most_active_annual))
    session.close()
    print("Return a JSON list of temperature observations for the previous year")
    return jsonify(all_temps)
#################################################
# /start
#################################################
@app.route("/api/v1.0/start/<start>")

def single_date(start):
    session = Session(engine)
    if start > '2017-08-23':
        return("There are no dates after 2017-08-23 in the dataset")
    sel = [Measurement.date, func.min(Measurement.prcp), func.avg(Measurement.prcp), func.max(Measurement.prcp)]
    date_range = session.query(*sel).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
    range_temps = list(np.ravel(date_range))
    session.close()
    return jsonify(range_temps)
#################################################
# /start/end Route
#################################################
@app.route("/api/v1.0/range")

def range():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    # Set variables for query even if no start/end is specified
    if end_date is None:
        end_date = "2018-01-01"
    if start_date is None:
        start_date = "2010-01-01"
    session = Session(engine)
    sel = [Measurement.date, func.min(Measurement.prcp), func.avg(Measurement.prcp), func.max(Measurement.prcp)]
    date_range = session.query(*sel).\
                filter(Measurement.date >= start_date).\
                filter(Measurement.date <= end_date).\
                group_by(Measurement.date).all()
    range_temps = list(np.ravel(date_range))
    session.close()
    return jsonify(range_temps)
#################################################
# Run app with debugging
#################################################
if __name__ == "__main__":
    app.run(debug=True)










#################################################
# Flask Routes
#################################################
