import random

def punnett_square(parent_a, parent_b):
  square_1 = [parent_a[0], parent_b[0]]
  square_2 = [parent_a[1], parent_b[0]]
  square_3 = [parent_a[0], parent_b[1]]
  square_4 = [parent_a[1], parent_b[1]]
  return [square_1, square_2, square_3, square_4]

def print_punnett_square(parent_a, parent_b, ps):
  print(f"""
          {parent_a[0]}             {parent_a[1]}
    ----------------------------
  {parent_b[0]} | {ps[0]} |  {ps[1]} |
    ----------------------------
  {parent_b[1]} | {ps[2]} |  {ps[3]} |
    ----------------------------
  """)

def calculate_punnett_square_probabilities(ps):
  counts = dict(("".join(i), ps.count(i) / len(ps)) for i in ps)
  return counts

def calculate_genotype_probabilities(ps):
  counts = {
    "hetero": sum(map(lambda x: is_heterozygous(x), ps)) / len(ps),
    "homozygous_dominant": sum(map(lambda x: is_homozygous_dominant(x), ps)) / len(ps),
    "homozygous_recessive": sum(map(lambda x: is_homozygous_recessive(x), ps)) / len(ps)
  }
  return counts

def generate_offspring(parent_a, parent_b):
  ps = punnett_square(parent_a, parent_b)
  genotype_probabilities = calculate_punnett_square_probabilities(ps)
  choices = []
  weights = []
  for key in genotype_probabilities.keys():
    choices.append(key)
    weights.append(genotype_probabilities[key])
  offspring = random.choices(choices, weights)[0]
  return list(offspring)

def get_offspring_phenotype(offspring, dominant_phenotype, recessive_phenotype):
  if has_dominant_phenotype(offspring):
    return dominant_phenotype
  else:
    return recessive_phenotype

def is_heterozygous(individual):
  return any(allele.isupper() for allele in individual) and any(not allele.isupper() for allele in individual)

def is_homozygous_dominant(individual):
  return all(allele.isupper() for allele in individual)

def is_homozygous_recessive(individual):
  return all(not allele.isupper() for allele in individual)

def has_dominant_phenotype(individual):
  return any(allele.isupper() for allele in individual)

def has_recessive_phenotype(individual):
  return is_homozygous_recessive(individual)

def genotype_statistics(population):
  stats = {
    "hetero": sum(map(lambda x: is_heterozygous(x), population)) / len(population),
    "homozygous_dominant": sum(map(lambda x: is_homozygous_dominant(x), population)) / len(population),
    "homozygous_recessive": sum(map(lambda x: is_homozygous_recessive(x), population)) / len(population)
  }
  return stats
