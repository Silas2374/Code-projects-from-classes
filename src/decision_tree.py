import math

ATTRIBUTES = ('Alternative', 'Bar', 'Friday/Saturday', 'Hungry', 'Patrons', 'Price', 'Raining',
              'Reservation', 'Type', 'Wait')

class Datum:
    def __init__(self, target, *values):
        self.target = target
        self.attributes = dict(zip(ATTRIBUTES, values))

data = (Datum(True, True, False, False, True, 'Some', '$$$', False, True, 'French', '0-10'),
        Datum(False, True, False, False, True, 'Full', '$', False, False, 'Thai', '30-60'),
        Datum(True, False, True, False, False, 'Some', '$', False, False, 'Burger', '0-10'),
        Datum(True, True, False, True, True, 'Full', '$', True, False, 'Thai', '10-30'),
        Datum(False, True, False, True, False, 'Full', '$$$', False, True, 'French', '>60'),
        Datum(True, False, True, False, True, 'Some', '$$', True, True, 'Italian', '0-10'),
        Datum(False, False, True, False, False, 'None', '$', True, False, 'Burger', '0-10'),
        Datum(True, False, False, False, True, 'Some', '$$', True, True, 'Thai', '0-10'),
        Datum(False, False, True, True, False, 'Full', '$', True, False, 'Burger', '>60'),
        Datum(False, True, True, True, True, 'Full', '$$$', False, True, 'Italian', '10-30'),
        Datum(False, False, False, False, False, 'None', '$', False, False, 'Thai', '0-10'),
        Datum(True, True, True, True, True, 'Full', '$', False, False, 'Burger', '30-60'))

def impurity(data):
    if data:
        total = len(data)
        num_true= sum(1 for d in data if d.target)
        p_true = num_true/total
        p_false = 1 - p_true
        return 1 - (p_true ** 2 + p_false ** 2)
    return 0

def split_cost(data, attribute, value):
    left = [d for d in data if d.attributes[attribute] == value]
    right = [d for d in data if d.attributes[attribute] != value]
    total = len(data)
    if total == 0:
        return None
    return (len(left) / total) * impurity(left) + (len(right) / total) * impurity(right)

def best_split(data):
    best_attribute = None
    best_value = None
    best_cost = math.inf
    for attribute in ATTRIBUTES:
        values = set(d.attributes[attribute] for d in data)
        for val in values:
            cost = split_cost(data, attribute, val)
            if cost < best_cost:
                best_attribute, best_value, best_cost = attribute, val, cost
    return best_attribute, best_value

class Tree:
    def __init__(self, data):
        if not data:
            self.leaf = True
            self.prediction = None
            return
        num_true = sum(1 for d in data if d.target)
        num_false = len(data) - num_true
        if num_true == 0 or num_false == 0:
            self.leaf = True
            self.prediction = num_true > num_false
            return
        split = best_split(data)
        if split is None:
            self.leaf = True
            self.prediction = num_true > num_false
            return
        attribute, val = split
        left = [d for d in data if d.attributes[attribute] == val]
        right = [d for d in data if d.attributes[attribute] != val]
        if not left or not right:
            self.leaf = True
            self.prediction = num_true > num_false
            return
        self.leaf = False
        self.left = Tree(left)
        self.right = Tree(right)
        self.attribute = attribute
        self.value = val

    def __repr__(self, indent=''):
        if self.leaf:
            return f"{indent} {self.prediction}\n"
        else:
            string = f"{indent}{self.attribute} == {self.value}?\n"
            string += self.left.__repr__(indent + '  ')
            string += self.right.__repr__(indent + '  ')
            return string

    def predict(self, datum):
        if self.leaf:
            return self.prediction
        if datum.attributes[self.attribute] == self.value:
            return self.left.predict(datum)
        else:
            return self.right.predict(datum)

def main():
    tree = Tree(data)
    print(tree)

if __name__ == '__main__':
    main()