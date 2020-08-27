import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Climate = Base.classes.climate

app = Flask(__name__)


@app.route("/")
def welcome() :
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
        session = Session(engine)
        
        precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year)
    
        session.close()
        
        precipitation = []
        for date, prcp in precip_results:
            precip_dict = {}
            precip_dict["date"] = date
            precip_dict["prcp"] = prcp
            precipitation.append(precip_dict)
        
        return jsonify(precipitation)




if __name__ == '__main__':
    app.run(debug=True)