import random

instance_space = {
  'sky': ('sunny', 'cloudy', 'rainy'),
  'air_temp': ('warm', 'cold'),
  'humidity': ('normal', 'high'),
  'wind': ('strong', 'weak'),
  'water': ('warm', 'cool'),
  'forecast': ('same', 'change'),

}

TARGET_HYPOTHESIS = {
  'sky': 'sunny',
  'air_temp': 'warm',
  'humidity': '?',
  'wind': '?',
  'water': '?',
  'forecast': '?',
}

#initialize h to the most specific hypothesis in H
#for each positive training example x
# if the constraint a_i is satisfied by x, then do nothing.
# else: replace a_i in h by the next more genera constraint that is
# satisfied by x.

def find_s(training_examples, target_concept):
  h = {
    'sky': 0,
    'air_temp': 0,
    'humidity': 0,
    'wind': 0,
    'water': 0,
    'forecast': 0,
  }
  counter = 0
  for x in training_examples:
    # print 'x', x
    # print 'current hypothesis', h
    counter += 1
    for attribute in instance_space:
      replace_with_next_most_general(h, x, attribute)
    # print 'resulting hypothesis', h
    if h == target_concept:
      return counter
    #print
    #print
  return -1


def replace_with_next_most_general(h, x, attribute):
  if h[attribute] in ('?', x[attribute]):
    return

  if h[attribute] == 0:
    h[attribute] = x[attribute]
  else:
    h[attribute] = '?'    


def create_random_example():
  return {key:random.choice(instance_space[key]) for key in
    instance_space}

def is_consistent_with_target_concept(x, 
  target_concept=TARGET_HYPOTHESIS):
  for attribute in instance_space:
    if target_concept[attribute] not in ('?', x[attribute]):
      return False
  return True

def produce_training_examples(target_concept=TARGET_HYPOTHESIS):
  examples = list()
  while len(examples) < 16:
    example = create_random_example()
    if is_consistent_with_target_concept(example, target_concept):
      examples.append(example)

  return examples
  
def run_experiment(x = 20, target_concept=TARGET_HYPOTHESIS):

  num_iterations = []
  for _ in xrange(x):
    num_iterations.append(find_s(produce_training_examples(target_concept),
      target_concept))
    #print num_iterations[-1]
  print sum(num_iterations)/x



if __name__ == '__main__':

  target_concept_1 = {
    'sky': 'sunny',
    'air_temp': '?',
    'humidity': '?',
    'wind': '?',
    'water': '?',
    'forecast': '?',   
  }
  run_experiment(target_concept=target_concept_1)

  target_concept_2 = {
    'sky': 'sunny',
    'air_temp': 'warm',
    'humidity': 'normal',
    'wind': '?',
    'water': '?',
    'forecast': '?',   
  }

  run_experiment(target_concept=target_concept_2)


  run_experiment()


