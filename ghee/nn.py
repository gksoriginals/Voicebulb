import numpy as np

class ANN():
    """class neural network"""
    def __init__(self, input_size, output_size, hidden_size=10, alpha=1, numlayers=2, dropout=False, dropout_percent=0.5):

        self.dropout = dropout
        self.dropout_percent = dropout_percent
        self.input = 0
        self.alpha = alpha
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layer = numlayers
        self.synapse = []
        self.layers = []
        self.output = 0
        self.synapse.append(2*np.random.random((self.input_size, self.hidden_size)) - 1)
        for i in range(1, self.num_layer-1):
            self.synapse.append(2*np.random.random((self.hidden_size, self.hidden_size)) - 1)
        self.synapse.append(2*np.random.random((self.hidden_size, output_size)) - 1)
    def forward(self, inp):
        """forward pass"""
        self.layers = []
        self.input = inp
        current_layer = inp

        for i in range(0, self.num_layer):
            self.layers.append(self.linear(np.dot(current_layer, self.synapse[i])))
            #if(self.dropout):
               #self.layers[i] *= np.random.binomial([np.ones((len(current_layer),self.hidden_size))],1-self.dropout_percent)[0] * (1.0/(1-self.dropout_percent))
            current_layer = self.layers[i]
        return current_layer
    def backward(self):
        """method for backprop"""
        lastlayer_error = self.output - self.layers[-1]

        lastlayer_delta = lastlayer_error*self.linear(self.layers[-1], True)
        for i in range(1, self.num_layer):
            currentlayer_error = lastlayer_delta.dot(self.synapse[-i].T)
            currentlayer_delta = currentlayer_error*self.linear(self.layers[-(i+1)], True)
            synapse_weight_update = self.layers[-(i+1)].T.dot(lastlayer_delta)
            lastlayer_delta = currentlayer_delta
            self.synapse[-i] += self.alpha*synapse_weight_update
        synapse_weight_update = self.input.T.dot(lastlayer_delta)
        self.synapse[0]+= synapse_weight_update
        return lastlayer_error
    def run(self, input_, output, num_iter=20000):
        self.output = output
        last_mean_error = 1
        for i in range(num_iter):
            out = self.forward(input_)
            error = self.backward()
            if (i% 10000) == 0 and i > 5000:
               if np.mean(np.abs(error)) <= last_mean_error:
                  print ("delta after "+str(i)+" iterations:" + str(np.mean(np.abs(error))) )

                  last_mean_error = np.mean(np.abs(error))
               else:
                  print ("break:", np.mean(np.abs(error)), ">", last_mean_error )
                  break
    def evaluate(self, inpt):
        out = self.forward(inpt)
        argmax = np.argmax(out)
        return argmax, out[argmax]
    def linear(self, inp, deriv=False):
        """activation function"""
        if deriv:
            return inp*(1-inp)
        else:
            return 1/(1+np.exp(-inp))

