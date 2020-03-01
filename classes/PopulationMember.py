from .Labels import HETERO_LABEL, HOMO_D_LABEL, HOMO_R_LABEL, D_TRAIT, R_TRAIT
import random

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
      self.traits = [D_TRAIT, R_TRAIT]
    elif trait_label == HOMO_D_LABEL:
      self.traits = [D_TRAIT, D_TRAIT]
    elif trait_label == HOMO_R_LABEL:
      self.traits = [R_TRAIT, R_TRAIT]
    else:
      raise Exception("Unknown trait_label - " + trait_label)

  # Given a set of traits, determine the trait_label
  def _set_label_from_traits(self, traits):
    # Hetero trait_label is order independent
    hetero_1_traits = [D_TRAIT, R_TRAIT]
    hetero_2_traits = [R_TRAIT, D_TRAIT]
    d_traits = [D_TRAIT, D_TRAIT]
    r_traits = [R_TRAIT, R_TRAIT]

    if traits == hetero_1_traits or traits == hetero_2_traits:
      self.trait_label = HETERO_LABEL
    elif traits == d_traits:
      self.trait_label = HOMO_D_LABEL
    elif traits == r_traits:
      self.trait_label = HOMO_R_LABEL
    else:
      raise Exception("Unknown traits - " + ", ".join(traits))

  def get_trait_label(self):
    return self.trait_label

  def select_allele(self):
    return random.choice(self.traits)


