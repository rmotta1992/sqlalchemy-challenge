import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station



app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the weather data homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
      #  f"/api/v1.0/""start""<br/>"
       # f"/api/v1.0/""start"/"end""<br/>"
    )
@app.route("/api/v1.0/precipitaion")
def precipition():
    session = Session(engine)
 
    prcp_results = session.query(measurement.prcp, measurement.date).filter(measurement.date >= "2016-08-23").all()


    session.close()

    prcp_data = []
    for prcp, date in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    
    station = Base.classes.station
    station_results = session.query(station.station).all()

    session.close()

    station_data = []
    for station in station_results:
        station_dict = {}
        station_dict["station"] = station

        station_data.append(station_dict)
       

    return jsonify(station_data)
       
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    tobs_results = session.query(measurement.date, measurement.station, measurement.tobs)\
        .filter(measurement.date >= "2016-08-23").filter(measurement.station == 'USC00519281').all()

    session.close()

    tobs_data = []
    for tobs, date, station in tobs_results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        tobs_data.append(tobs_dict)
       

    return jsonify(tobs_data)
   
    
if __name__ == "__main__":
    app.run(debug=True)