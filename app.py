import uuid
import pickle
import subprocess
from io import TextIOWrapper
import json
import eventlet
from flask import Flask, request, render_template, send_file, abort
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from decouple import config



eventlet.monkey_patch()
app = Flask(__name__, static_url_path='/static')


app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})


socketio = SocketIO(app)





@socketio.on('runsim')
def handle_test(data):
    newid = str(uuid.uuid4()) 
    emit('sendid', {
        "caller": data["caller"],
        "id": newid
    })
    proc = subprocess.Popen(
        ["python", "-u", "run_simulation.py", newid, data.get('data', json.dumps({}))],
        stdout=subprocess.PIPE
    )
    for line in TextIOWrapper(proc.stdout):
        emit("senddata", {
            "caller": data['caller'],
            "log": line
            })
        eventlet.sleep(0)


# @app.route("/test")
# def show_test():
#     return render_template("testpage.html")

@app.route("/")
@app.route("/<path>")
def homeHandler(path=None):
    if path is None or path in ['graphs', 'info', 'scenarios', 'maps']:
        return render_template("index.html")
    else:
        try:
            return send_file("static/" + path)
        except:
            abort(404)


if __name__ == "__main__":
    socketio.run(app, debug=True)
