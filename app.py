# app.py
from flask import Flask, request, jsonify
from sim import HeterozygousTraitSimulator
app = Flask(__name__)

simluator =  HeterozygousTraitSimulator()

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/runSim", methods=["GET"])
def list_todo():
    hetero_zyg = request.args.get('hetero_zyg')
    homo_zyg_dom = request.args.get('homo_zyg_dom')
    homo_zyg_rec = request.args.get('homo_zyg_rec')
    number_runs = request.args.get('number_runs')

    return jsonify(ToDoService().list())


if __name__ == "__main__":
    app.run()
