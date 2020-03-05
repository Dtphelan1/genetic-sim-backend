# app.py
from flask import Flask, request, jsonify
from .classes.PopulationGenotype import PopulationGenotype
from .classes.PunnettSquare import generate_offspring, genotype_statistics
app = Flask(__name__)

simulator = PopulationGenotype(log=True)

@app.after_request
def add_headers(response):
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
  response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
  return response

@app.route("/runPopSim", methods=["GET"])
def population_sim():
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

@app.route("/runOffspringSim", methods=["GET"])
def offspring_sim():
  parent_a = list(request.args.get('parentA'))
  print(parent_a)
  parent_b = list(request.args.get('parentB'))
  print(parent_b)
  number_offspring = int(request.args.get('generations'))
  print(number_offspring)

  offspring_list = []
  for num in range(number_offspring):
    offspring = generate_offspring(parent_a, parent_b)
    offspring_list.append(offspring)

  stats = genotype_statistics(offspring_list)

  return jsonify(stats)

if __name__ == "__main__":
  app.run()
