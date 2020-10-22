import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement


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



if __name__ == "__main__":
    app.run(debug=True)