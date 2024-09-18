from flask import Flask, jsonify, Response, stream_with_context
from flask_cors import CORS
from cameraProcessing import CameraProcessor
from database import Database

app = Flask(__name__)
cors = CORS(app)
cameraProcessor = CameraProcessor()
db = Database()


# Get the real-time people count from the live frame
@app.route("/api/liveCount", methods=["GET"])
def getLivePeopleCount():
    count = cameraProcessor.livePeopleCount  # Fetch live count from the current frame
    return jsonify({"livePeopleCount": count})

@app.route("/api/last_hour_data", methods=["GET"])
def getLastHourData():
    data = db.getLastHourData()
    return jsonify([{
        "time": f'{item["_id"]["hour"]}:{item["_id"]["minute"]}', 
        "count": round(item["avgCount"])
    } for item in data])

@app.route("/api/last_30_minutes_data", methods=["GET"])
def getLast30MinutesData():
    data = db.getLast30MinutesData()
    return jsonify([{
        "time": f'{item["_id"]["minute"]} min',
        "count": round(item["avgCount"])
    } for item in data])


@app.route("/LiveTracking/videoFeed", methods=["GET"])
def videoFeed():
    return Response(stream_with_context(cameraProcessor.getFrame()), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/LiveTracking/annotatedVideoFeed", methods=["GET"])
def annotatedVideoFeed():
    return Response(stream_with_context(cameraProcessor.getAnnotatedFrame()), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
=======
# routes for people count
@app.route("/api/peopleCount", methods=["GET"])
def getPeopleCount():
    count = db.getlastestRecord()
    return jsonify({"peopleCount": count})

# routes for main camera display
@app.route("/LiveTracking/videoFeed", methods=["GET"])
def videoFeed():
    return Response(stream_with_context(cameraProcessor.getFrame()),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

# routes for annotated frame or 2d floor plan
@app.route("/LiveTracking/annotatedVideoFeed", methods=["GET"])
def annotatedVideoFeed():
    return Response(stream_with_context(cameraProcessor.getAnnotatedFrame()),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

    
if __name__ == "__main__":
    app.run(debug=True, port=8000)

