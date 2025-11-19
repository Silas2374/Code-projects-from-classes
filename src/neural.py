import math
import random

LEARNING_RATE = 1

class Synapse:
    """
    A weighted connection from Neuron source to Neuron dest.
    """

    def __init__(self, source, dest):
        """
        :param source: The Neuron that this Synapse comes from.
        :param dest: The Neuron that this Synapse leads to.
        """
        self.source = source
        source.outputs += [self]
        self.dest = dest
        dest.inputs += [self]
        self.weight = random.gauss(0, 1)

    def weighted_output(self):
        """
        :return: The source Neuron's activation times the weight of this Synapse.
        """
        return self.weight * self.source.activation

    def update_weight(self):
        """
        Update the weight of this Synapse. Assumes source's activation and dest's delta have been set.
        """
        self.weight += -LEARNING_RATE * self.source.activation * self.dest.delta

    def feedback_delta(self):
        """
        :return: The weight of this Synapse times dest's delta.
        """
        return self.dest.delta * self.weight

class Neuron:
    """
    A unit in a neural network.
    """

    def __init__(self, previous_layer=None):
        """
        :param previous_layer: A list of Neurons in the previous layer.
        """
        self.activation = 1
        self.delta = 0
        self.inputs = []
        if previous_layer:
            Synapse(Neuron(), self)
            for n in previous_layer:
                Synapse(n, self)
        else:
            self.inputs = None
        self.outputs = []

    def __repr__(self):
        return (f'a={self.activation}, d={self.delta}, '
                f'w_i={[i.weight for i in self.inputs] if self.inputs else None}, '
                f'w_o={[o.weight for o in self.outputs] if self.outputs else None}')

    def update_activation(self):
        """
        Update the activation of this Neuron, based on its previous layer and weights.
        """
        self.activation = 0
        for s in self.inputs:
            self.activation += s.weighted_output()
        self.activation = logistic(self.activation)

    def update_delta(self, target=None):
        """
        Update the delta value for this Neuron.
        :param target: The desired output of this Neuron (if it is an output Neuron).
        """
        if target is not None: #this is an output node
            self.delta = -self.activation * (1 - self.activation) * (target - self.activation)
        else:
            self.delta = self.activation * (1 - self.activation) * sum(output.dest.delta * output.weight for output in self.outputs)

    def update_weights(self):
        """
        Update the weights of the Synapses leading into this Neuron.
        """
        for i in self.inputs:
            i.update_weight()

    def set_weights(self, weights):
        """
        Sets the weights of the Synapses leading into this Neuron. Used in unit tests.
        """
        for synapse, weight in zip(self.inputs, weights):
            synapse.weight = weight


class Network:
    """
    A multilayer perceptron.
    """

    def __init__(self, sizes):
        """
        :param sizes: A list of the Number of neurons in each layer, e.g., [2, 2, 1] for a network that can learn XOR.
        """
        self.layers = [[]] * len(sizes)
        self.layers[0] = [Neuron() for _ in range(sizes[0])]
        for i in range(1, len(sizes)):
            self.layers[i] = [Neuron(self.layers[i-1]) for _ in range(sizes[i])]

    def predict(self, inputs):
        """
        :param inputs: Values to use as activations of the input layer.
        :return: The predictions of the neurons in the output layer.
        """
        input_layer = self.layers[0]
        hidden_layers= self.layers[1:-1]
        output_layer = self.layers[-1] # this assumes there are no hidden layers. I'll deal with that later.
        for neuron, i in zip(input_layer, inputs):
            neuron.activation = i
        for layer in hidden_layers:
            for neuron in layer:
                neuron.update_activation()
        for neuron in output_layer:
            neuron.update_activation()
        return [neuron.activation for neuron in output_layer]

    def update_deltas(self, targets):
        """
        Update the deltas of all neurons, using backpropagation. Assumes predict has already
        been called, so all neurons have had their activations updated.
        :param targets: The desired activations of the output neurons.
        """
        last_layer = self.layers[-1]
        i = 0
        for neuron in last_layer:
            neuron.update_delta(targets[i])
            i += 1
        other_layers = reversed(self.layers[:-1])
        for layer in other_layers:
            for neuron in layer:
                neuron.update_delta()


    def update_weights(self):
        """
        Update the weights of all neurons.
        """
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.update_weights()

    def train(self, inputs, targets):
        """
        Feed inputs through this network, then adjust the weights so that the activations of
        the output neurons will be slightly closer to targets.
        :param inputs: A list activation values for the input units.
        :param targets: A list desired activation values for the output units.
        """
        self.predict(inputs)
        self.update_deltas(targets)
        self.update_weights()


def logistic(x):
    """
    Logistic sigmoid squashing function.
    """
    return 1 / (1 + math.exp(-x))