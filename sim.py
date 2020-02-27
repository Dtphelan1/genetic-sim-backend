import random

# This simulation is limited to running short

HETERO_LABEL = "HETERO"
HOMO_D_LABEL = "HOMO_D"
HOMO_R_LABEL = "HOMO_R"

HOMO_D_TRAIT = "HOMO_D"
HOMO_R_TRAIT = "HOMO_R"

# Cap for the population
POPCAP = 10000
# Error margin for floats
EPSILON = 0.001
# Percentage of population that breeds at every step
BREED_RATE = 0.001

class HeterozygousTraitSimulator:
  def __init__(self):
    self.population_cap = POPCAP
    self.ep = EPSILON
    self.breed_rate = BREED_RATE
    self.zero_population()

  def zero_population(self):
    print("Zero population")
    self.population = []
    self.population_record = []

  # Initialize the population based on initial percentages
  def init_population(self, hetero_zyg, homo_zyg_dom, homo_zyg_rec):
    print("init pop")
    # Zero population
    self.zero_population()
    # Want to ensure the percentage_sum is within bounds
    percentage_sum = (hetero_zyg + homo_zyg_dom + homo_zyg_rec)
    if percentage_sum < (1.0 - self.ep) or percentage_sum > 1.0 + self.ep:
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
    print("cull_population")
    cur_size = len(self.population)
    # If amount is defined, cull by that amount if it's less than the current  size
    if (amount is not None) and (amount < cur_size):
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
    print("simulate new pop")
    new_offspring_arr = []
    cur_size = len(self.population)
    offspring_needed = int(self.breed_rate * cur_size)
    print("making how many new offspring? " + str(offspring_needed))
    while (len(new_offspring_arr) < offspring_needed):
      # Select two parents
      parent_1 = random.choice(self.population)
      parent_2 = random.choice(self.population)
      # Select one trait from each and make a new offspring from that
      trait_1 = parent_1.select_allele()
      trait_2 = parent_2.select_allele()
      offspring = PopulationMember(t1=trait_1, t2=trait_2)
      new_offspring_arr.append(offspring)
    # Once offspring are finished, add them to the population and then cull
    self.cull_population(len(new_offspring_arr))
    self.population += new_offspring_arr

  # Articulate statistics on the current population
  def population_stats(self, run, percentage_done):
    print("recording pop stats")
    return {
      "run": run,
      "percentage_done": percentage_done,
      "pop_size": len(self.population),
      "hetero": len([member for member in self.population if member.get_trait_label() == HETERO_LABEL]) / len(self.population),
      "homo_d": len([member for member in self.population if member.get_trait_label() == HOMO_D_LABEL]) / len(self.population),
      "homo_r": len([member for member in self.population if member.get_trait_label() == HOMO_R_LABEL]) / len(self.population)
    }

  # Run a simulation `number_runs` long with initial population distributed along the
  def run_sim(self, hetero_zyg, homo_zyg_dom, homo_zyg_rec, number_runs):
    # init the population
    self.init_population(hetero_zyg, homo_zyg_dom, homo_zyg_rec)
    # run the simulation
    curRun = 1
    tenth_of_run = number_runs / 10
    print(tenth_of_run)
    while curRun <= number_runs:
      # Every 10th of the way through, log the states
      if curRun % tenth_of_run == 0:
        percentage_done = (curRun / tenth_of_run) * 10
        print(percentage_done)
        cur_stats = self.population_stats(curRun, percentage_done)
        self.population_record.append(cur_stats)
      self.simulate_new_pop()
      curRun += 1

  def get_population_stats(self):
    return self.population_record

class PopulationMember():
  def __init__(self, trait_label=None, t1=None, t2=None):
    # If the traits are defined directly, use them
    if t1 is not None and t2 is not None:
      self.traits = [t1, t2]
      self._set_label_from_traits(self.traits)

    # If the trait label is set, use that directly
    if trait_label is not None:
      self.trait_label = trait_label
      self._set_traits_from_label(self.trait_label)

    if self.trait_label is None:
      raise Exception("COULDN'T BUILD POP MEMBER WELL")

  # Given a trait_label, determine the traits
  def _set_traits_from_label(self, trait_label):
    if trait_label == HETERO_LABEL:
      self.traits = [HOMO_D_TRAIT, HOMO_R_TRAIT]
    elif trait_label == HOMO_D_LABEL:
      self.traits = [HOMO_D_TRAIT, HOMO_D_TRAIT]
    elif trait_label == HOMO_R_LABEL:
      self.traits = [HOMO_R_TRAIT, HOMO_R_TRAIT]
    else:
      raise Exception("Unknown trait_label - " + trait_label)

  # Given a set of traits, determine the trait_label
  def _set_label_from_traits(self, traits):
    # Hetero trait_label is order independent
    hetero_1_traits = [HOMO_D_TRAIT, HOMO_R_TRAIT]
    hetero_2_traits = [HOMO_R_TRAIT, HOMO_D_TRAIT]
    homo_d_traits = [HOMO_D_TRAIT, HOMO_D_TRAIT]
    homo_r_traits = [HOMO_R_TRAIT, HOMO_R_TRAIT]

    if traits == hetero_1_traits or traits == hetero_2_traits:
      self.trait_label = HETERO_LABEL
    elif traits == homo_d_traits:
      self.trait_label = HOMO_D_LABEL
    elif traits == homo_r_traits:
      self.trait_label = HOMO_R_LABEL
    else:
      raise Exception("Unknown traits - " + ", ".join(traits))

  def get_trait_label(self):
    return self.trait_label

  def select_allele(self):
    return random.choice(self.traits)



if __name__ == "__main__":
  simulator =  HeterozygousTraitSimulator()
  hetero_zyg = 0.1
  homo_zyg_dom = 0.1
  homo_zyg_rec = 0.8
  number_runs = 1000
  simulator.run_sim(hetero_zyg,
    homo_zyg_dom,
    homo_zyg_rec,
    number_runs
  )
  print(simulator.get_population_stats())
