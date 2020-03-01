# app.py
from flask import Flask, request, jsonify
from .classes.PopulationGenotype import PopulationGenotype
app = Flask(__name__)

simulator = PopulationGenotype(log=True)

@app.after_request
def add_headers(response):
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
  response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
  return response

@app.route("/runSim", methods=["GET"])
def list_todo():
  hetero_zyg = int(request.args.get('hetero'))/100.0 if int(request.args.get('hetero')) > 1.0 else int(request.args.get('hetero'))
  print(hetero_zyg)
  homo_zyg_dom = int(request.args.get('homoD'))/100.0 if int(request.args.get('homoD')) > 1.0 else int(request.args.get('homoD'))
  print(homo_zyg_dom)
  homo_zyg_rec = int(request.args.get('homoR'))/100.0 if int(request.args.get('homoR')) > 1.0 else int(request.args.get('homoR'))
  print(homo_zyg_rec)
  number_runs = int(request.args.get('generations'))
  print(number_runs)

  return jsonify(simulator.run_sim(hetero_zyg,
    homo_zyg_dom,
    homo_zyg_rec,
    number_runs,
  ))

if __name__ == "__main__":
  app.run()
