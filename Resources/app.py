import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
stations = Base.classes.stations
measurements = Base.classes.measurement

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    print("Welcome to the Hawaii Weather API !")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session.query(measurements).all()
    # Close query
    session.close()

    # Convert the results to a dictionary using date as the 
    # key and prcp as the value. 
    year_prcp = []
    for result in results:
        year_prcp_dict["date"] = result.date 
        year_prcp_dict["prcp"] = result.prcp
        year_prcp.append(year_prcp_dict)
    return jsonify(year_prcp)


@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the data"""
    # Query all stations 
    results = session.query(station.station).all()
    #close query
    session.close()

    # Get your list of stations 
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).filter(measurement.date > last_year).all()
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)