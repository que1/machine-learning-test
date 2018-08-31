import numpy
import scipy.special
import scipy.misc
# import matplotlib.pyplot
import datetime

class neuralNetwork:

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        self.wih = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        # print("wih: \n" + str(self.wih))
        # print("who: \n" + str(self.who))

        self.lr = learningrate

        self.activation_function = lambda x : scipy.special.expit(x)

        pass


    def train(self, inputs_list, targets_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))
        pass


    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        # print("inputs: \n" + str(inputs))
        hidden_inputs = numpy.dot(self.wih, inputs)
        # print("hidden_inputs: \n" + str(hidden_inputs))
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


if __name__ == '__main__':
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("start, ", nowTime)
    input_nodes = 784
    hidden_nodes = 200
    output_nodes = 10
    learning_rate = 0.1
    n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    # final_outputs = n.query([1.0, 0.5, -1.5])
    # print("final_outputs: \n" + str(final_outputs))
    # n.get_training_date()
    training_data_file = open("/Users/q/program/code_store/make_your_own_neural_network/mnist_train.csv", "r")
    training_data_list = training_data_file.readlines()
    training_data_file.close()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # all_values = training_data_list[0].split(',')
    # image_array = numpy.asfarray(all_values[1:]).reshape((28, 28))
    # matplotlib.pyplot.imshow(image_array, cmap='Greys', interpolation='None')
    # matplotlib.pyplot.show()
    #
    epochs = 2
    for e in range(epochs):
        for record in training_data_list:
            all_values = record.split(',')
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            targets = numpy.zeros(output_nodes) + 0.01
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("training end, ", nowTime)
    #
    test_data_file = open("/Users/q/program/code_store/make_your_own_neural_network/mnist_test.csv", "r")
    test_data_list = test_data_file.readlines()
    test_data_file.close()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # all_values = test_data_list[0].split(',')
    # print(all_values[0])
    # inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    # final_outputs = n.query(inputs)
    # print(final_outputs)
    # image_array = numpy.asfarray(all_values[1:]).reshape((28, 28))
    # matplotlib.pyplot.imshow(image_array, cmap='Greys', interpolation='None')
    # matplotlib.pyplot.show()

    scorecard = []
    for record in test_data_list:
        all_values = record.split(',')
        correct_label = int(all_values[0])
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        outputs = n.query(inputs)
        label = numpy.argmax(outputs)
        # print(correct_label, "correct_label", label, "network's answer")
        if (correct_label == label):
            scorecard.append(1)
        else:
            scorecard.append(0)
    # print(scorecard)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("test end, ", nowTime)
    scorecard_array = numpy.asarray(scorecard)
    print("performance = ", scorecard_array.sum() / scorecard_array.size)

    img_array = scipy.misc.imread("3.png", flatten=True)
    # print(img_array)
    # 常规数据0指黑色，255是白色，但是MNISt数据集使用相反的方式表示，所以需要用255去减
    temp_img_data = 255.0 - img_array.reshape(784)
    # print(img_data)
    img_data = (temp_img_data / 255.0 * 0.99) + 0.01
    # print(img_data)

    outputs = n.query(img_data)
    label = numpy.argmax(outputs)
    print("outpus: ", outputs)
    print("check result: ", label)

    pass
