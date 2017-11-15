__author__ = 'admin'

import data_science_from_scratch
import collections
import functools
import math

'''inputs'''
def create_lebeled_data():
    labeled_data = [({'level':'senior', 'lang':'java', 'tweets':'no', 'phd':'no'}, False),
                    ({'level':'senior', 'lang':'java', 'tweets':'no', 'phd':'yes'}, False),
                    ({'level':'mid', 'lang':'python', 'tweets':'no', 'phd':'no'}, True),
                    ({'level':'junior', 'lang':'python', 'tweets':'no', 'phd':'no'}, True),
                    ({'level':'junior', 'lang':'r', 'tweets':'yes', 'phd':'no'}, True),
                    ({'level':'junior', 'lang':'r', 'tweets':'yes', 'phd':'yes'}, False),
                    ({'level':'mid', 'lang':'r', 'tweets':'yes', 'phd':'yes'}, True),
                    ({'level':'senior', 'lang':'python', 'tweets':'no', 'phd':'no'}, False),
                    ({'level':'senior', 'lang':'r', 'tweets':'yes', 'phd':'no'}, True),
                    ({'level':'junior', 'lang':'python', 'tweets':'yes', 'phd':'no'}, True),
                    ({'level':'senior', 'lang':'python', 'tweets':'yes', 'phd':'yes'}, True),
                    ({'level':'mid', 'lang':'python', 'tweets':'no', 'phd':'yes'}, True),
                    ({'level':'mid', 'lang':'java', 'tweets':'yes', 'phd':'no'}, True),
                    ({'level':'junior', 'lang':'python', 'tweets':'no', 'phd':'yes'}, False)
                   ]
    return labeled_data


'''entropy-value'''
def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    print(probabilities)
    return entropy(probabilities)

def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count for count in collections.Counter(labels).values()]

def entropy(class_probabilities):
    return sum(-p * math.log(p, 2) for p in class_probabilities)


'''split data'''
def partition_entropy_by(inputs, attribute):
    partitions = partition_py(inputs, attribute)
    return partition_entropy(partitions.values())

def partition_py(inputs, attribute):
    groups = collections.defaultdict(list)
    for input in inputs:
        key = input[0][attribute]
        groups[key].append(input)
    return groups

def partition_entropy(subsets):
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * (len(subset) / total_count) for subset in subsets)


'''input-output'''
def classify(tree, input):
    if tree in [True, False]:
        return tree

    attribute, subtree_dict = tree
    subtree_key = input.get(attribute)
    print(subtree_key)
    if subtree_key not in subtree_dict:
        subtree_key = None

    subtree = subtree_dict[subtree_key]
    print(subtree)
    return classify(subtree, input)

def build_tree_id3(inputs, split_candidates = None):
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()
        print(inputs[0][0])
        print(split_candidates)

    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label == True])
    num_falses = num_inputs - num_trues

    if num_trues == 0:
        return False
    if num_falses == 0:
        return True

    if not split_candidates:
        return num_trues >= num_falses

    best_attribute = min(split_candidates, key = functools.partial(partition_entropy_by, inputs))
    partitions = partition_py(inputs, best_attribute)
    print(partitions)
    new_candidates = [a for a in split_candidates if a != best_attribute]

    subtrees = {attribute_value : build_tree_id3(subset, new_candidates) for attribute_value, subset in partitions.items()}
    subtrees[None] = num_trues > num_falses

    return (best_attribute, subtrees)



if __name__ == '__main__':
    labeled_data = create_lebeled_data()
    shannon_ent = data_entropy(labeled_data)
    print(shannon_ent)

    '''
    print(partition_py(labeled_data, 'level'))

    for key in ['level', 'lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(labeled_data, key))
    '''
    '''
    lang_inputs = [(input, label) for input, label in labeled_data if input['level'] == 'senior']
    print(lang_inputs)

    for key in ['lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(labeled_data, key))


    tree = build_tree_id3(labeled_data)
    print(tree)
    #subtree = classify(tree, {'level':'junior', 'lang':'java', 'tweets':'yes', 'phd':'yes'})
    #print(subtree)
        '''