import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

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
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"--------------------------------------------<br/>"
        f"Available Routes:<br/>"
        f"--------------------------------------------<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"--------------------------------------------<br/>"
        f"Enter requested date as yyyy-mm-dd<br/>"
        f"--------------------------------------------<br/>"
        f"/api/v1.0/<start><br/>"
        f"--------------------------------------------<br/>"
        f"Enter requested date range as:<br/>"
        f"(start date) yyyy-mm-dd/(end date) yyyy-mm-dd<br/>"
        f"--------------------------------------------<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"--------------------------------------------<br/>"
    )

#####################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
        session = Session(engine)

    # creatre a query for all precipitation
        prcp_query = session.query(measurement.date, measurement.prcp).all()
    # close query
        session.close()
    # Convert the results to a dictionary using date as the 
    # key and prcp as the value. 
        prcp_dict = list(np.ravel(prcp_query))
    # Return the JSON representation of your dictionary.
        return jsonify(prcp_query)



#######################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
        session = Session(engine)

        """Return a list of stations from the data"""
    # Query all stations 
        station_query = session.query(station.station).all()
    #close query
        session.close()

    # Return a JSON list of stations from the dataset.
        all_stations = list(np.ravel(station_query))

        return jsonify(all_stations)
    #######################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
        tobs_query = session.query(measurement.station,\
            func.count(measurement.station)).\
            group_by(measurement.station).\
            order_by(func.count(measurement.station).desc()).\
            filter(measurement.date >= "2016-08-23").\
            filter(measurement.date <= "2017-08-23").all()
    #Query the dates and temperature observations of the most 
    # active station for the last year of data.
        tobs_dict = list(np.ravel(tobs_query))
    # Return a JSON list of temperature observations 
    # (TOBS) for the previous year.
        return jsonify(tobs_dict)
################################################################
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start or start-end range.

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
    # greater than and equal to the start date.

    # When given the start and the end date, calculate the TMIN, TAVG, 
    # and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start_date(start):
    date_query = session.query(measurement.date,\
        func.min(measurement.tobs),\
        func.avg(measurement.tobs),\
        func.max(measurement.tobs)).\
        filter(measurement.date == start).all()
    date_list = []
    for date_query in date_query:
        row = {}
        row['Date'] = date_query[0]
        row['Min Temp'] = date_query[1]
        row['Avg Temp'] = date_query[2]
        row['Max Temp'] = date_query[3]
        date_list.append(row)
    return jsonify(date_list)
        

@app.route("/api/v1.0/<start>/<end>")
def temp_ranges(start, end):
    s_e_date_query = session.query(\
        func.min(measurement.tobs),\
        func.avg(measurement.tobs),\
        func.max(measurement.tobs)).\
        filter(measurement.date >= start, measurement.date <= end).all()
    date_list = []
    for s_e_date_query in s_e_date_query:
        row = {}
        row['Start Date'] = start
        row['End Date'] = end
        row['Min Temp'] = s_e_date_query[0]
        row['Avg Temp'] = s_e_date_query[1]
        row['Max Temp'] = s_e_date_query[2]
        date_list.append(row)
    return jsonify(date_list)
        

################################################################
if __name__ == '__main__':
    app.run(debug=True)