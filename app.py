import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Climate = Base.classes.keys

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def welcome() :
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

        session = Session(engine)

        last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

        precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year)
    
        session.close()
        
        precipitation = []
        
        for date, prcp in precip_results:
            precip_dict = {}
            precip_dict["date"] = date
            precip_dict["prcp"] = prcp
            precipitation.append(precip_dict)
        
        return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    stations =  session.query(Station.station).all()

    session.close

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    tobs =  session.query(Measurement.station, Measurement.tobs).filter(Measurement.station == "USC00519397").filter(Measurement.date >= last_year).all()

    session.close

    return jsonify(tobs)




@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.station == "USC00519281").all()

    session.close

    return jsonify(results)




@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start, Measurement.date < end, Measurement.station == "USC00519281").all()

    session.close

    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)