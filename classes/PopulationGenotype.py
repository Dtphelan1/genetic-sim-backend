import random
from .PopulationMember import PopulationMember
from .Labels import HETERO_LABEL, HOMO_D_LABEL, HOMO_R_LABEL, D_TRAIT, R_TRAIT
from .Logger import logger, stream_handler

# Cap for the population
POPCAP = 1000
# Error margin for floats
EPSILON = 0.001
# Percentage of population that breeds at every step
BREED_RATE = 1.0

class PopulationGenotype:
  def __init__(self, log=False, debug=False):
    self.population_cap = POPCAP
    self.ep = EPSILON
    self.breed_rate = BREED_RATE
    self.zero_population()
    if log:
      stream_handler.setLevel("INFO")
    if debug:
      stream_handler.setLevel("DEBUG")

  def zero_population(self):
    logger.info("Zero population")
    self.population = []
    self.population_record = []

  # Initialize the population based on initial percentages
  def init_population(self, hetero_zyg, homo_zyg_dom, homo_zyg_rec):
    logger.info("init pop")
    # Zero population
    self.zero_population()
    # Want to ensure the percentage_sum is within bounds
    percentage_sum = (hetero_zyg + homo_zyg_dom + homo_zyg_rec)
    if percentage_sum < (1.0 - self.ep) or percentage_sum > (1.0 + self.ep):
      raise Exception("population parameters don't add to 100")
    # Get counts for individuals based on percentages
    num_hetero   = int(hetero_zyg * self.population_cap)
    num_homo_dom = int(homo_zyg_dom * self.population_cap)
    num_homo_rec = int(homo_zyg_rec * self.population_cap)
    self.population += [PopulationMember(trait_label=HETERO_LABEL) for x in range(0, num_hetero)]
    self.population += [PopulationMember(trait_label=HOMO_D_LABEL) for x in range(0, num_homo_dom)]
    self.population += [PopulationMember(trait_label=HOMO_R_LABEL) for x in range(0, num_homo_rec)]
    # Cull to account for rounding errors
    self.cull_population()

  # Given the current population, cull by a certain amount;
  # If no amount provided, ensure it is below the cap
  def cull_population(self, amount=None):
    logger.debug("cull_population")
    cur_size = len(self.population)
    # If amount is defined, cull by that amount if it's less than the current  size
    if (amount is not None) and (amount <= cur_size):
      new_pop_size = cur_size - amount
      random.shuffle(self.population)
      self.population = self.population[:new_pop_size]
    # Else if the pop needs culling, cut off extra members
    elif len(self.population) > self.population_cap:
      random.shuffle(self.population)
      self.population = self.population[:self.population_cap]
    # Else, the population doesn't need culling.
    else:
      return

  # Based on the current population, reproduce and simulate a new population
  def simulate_new_pop(self):
    logger.debug("simulate new pop")
    new_offspring_arr = []
    cur_size = len(self.population)
    offspring_needed = int(self.breed_rate * cur_size)
    logger.debug(f"cur_size is {cur_size}" )
    while (len(new_offspring_arr) < offspring_needed):
      if (len(new_offspring_arr) % 100 == 0):
        logger.debug(f"Still need {offspring_needed - len(new_offspring_arr)} many children")
      # Select two parents
      parent_1 = random.choice(self.population)
      parent_2 = random.choice(self.population)
      # Select one trait from each and make a new offspring from that
      trait_1 = parent_1.select_allele()
      trait_2 = parent_2.select_allele()
      offspring = PopulationMember(t1=trait_1, t2=trait_2)
      new_offspring_arr.append(offspring)
    # Once offspring are finished, add them to the population and then cull
    self.cull_population(amount=len(new_offspring_arr))
    self.population += new_offspring_arr

  # Articulate statistics on the current population
  def population_stats(self, run, percentage_done):
    logger.debug("recording pop stats")
    return {
      "run": run,
      "percentage_done": percentage_done,
      "pop_size": len(self.population),
      "hetero": len([member for member in self.population if member.get_trait_label() == HETERO_LABEL]) / len(self.population),
      "homo_d": len([member for member in self.population if member.get_trait_label() == HOMO_D_LABEL]) / len(self.population),
      "homo_r": len([member for member in self.population if member.get_trait_label() == HOMO_R_LABEL]) / len(self.population)
    }

  def get_population_stats(self):
    return self.population_record

  # Run a simulation `number_runs` long with initial population distributed along the
  def run_sim(self, hetero_zyg, homo_zyg_dom, homo_zyg_rec, number_runs):
    print(hetero_zyg, homo_zyg_dom, homo_zyg_rec, number_runs)
    # init the population
    self.init_population(hetero_zyg, homo_zyg_dom, homo_zyg_rec)
    # run the simulation
    curRun = 1
    cur_stats = self.population_stats(curRun, 0.0)
    self.population_record.append(cur_stats)
    tenth_of_run = number_runs / 10
    logger.info("Running this many runs: " + str(number_runs))
    while curRun <= number_runs:
      # Every 10th of the way through, log the states
      if curRun % tenth_of_run == 0:
        percentage_done = (curRun / tenth_of_run) * 10
        logger.info("percentage_done - " + str(percentage_done))
        cur_stats = self.population_stats(curRun, percentage_done)
        self.population_record.append(cur_stats)
      self.simulate_new_pop()
      curRun += 1
    return self.get_population_stats()


if __name__ == "__main__":
  simulator =  PopulationGenotype(log=True)
  hetero_zyg = 0.2
  homo_zyg_dom = 0.3
  homo_zyg_rec = 0.5
  number_runs = 1000
  simulator.run_sim(hetero_zyg,
    homo_zyg_dom,
    homo_zyg_rec,
    number_runs
  )
  logger.info(simulator.get_population_stats())
