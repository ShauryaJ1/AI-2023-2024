import sys;args=sys.argv[1:]
import random
import math

def logistic_transfer_function(x):
    return 1/(1+math.e**(-x))
def derivative_logistic_transfer_function(x):
    return logistic_transfer_function(x)*(1-logistic_transfer_function(x))
def file_to_lines():
    return open(args[0]).read().splitlines()
def hadamard(v1,v2):
    return [v1[i]*v2[i] for i in range(len(v1))]
def dot_product(v1,v2):
    return sum(hadamard(v1,v2))
def forward_propogation(inputs,weights):
    x_values = {0:inputs}
    y_values = {}
    for i in range(len(weights)-1):
         y_values[i]=[dot_product(x_values[i],weights[i][j::len(weights[i+1])]) for j in range(len(weights[i+1]))]
         x_values[i+1] = [logistic_transfer_function(y) for y in y_values[i]]
    
    return hadamard(x_values[len(weights)-1],weights[-1]),x_values,y_values
def error(outputs,expected_values):
    return 0.5*sum([(outputs[i]-expected_values[i])**2 for i in range(len(outputs))])
def back_propogation(inputs,outputs,weights,expected_values,alpha,x_values,y_values,training_examples):
    gradients = {layer:[] for layer in range(len(weights))}
    errors = [[0.0 for j in range(len(x_values[i]))] for i in range(len(x_values))]
    for i in range(len(weights)-1,-1,-1):
        for j in range(len(weights[i])):
            
            start_index = j//len(x_values[i])
            end_index = j%len(x_values[i])
            if i == len(weights)-1:
                errors[i][j] = (expected_values[j]-x_values[i][j]*weights[i][j])*weights[i][j]*derivative_logistic_transfer_function(x_values[i][j])
                gradients[i].append(alpha*(expected_values[j]-x_values[i][j]*weights[i][j])*x_values[i][j])
            else:
                errors[i][end_index] = derivative_logistic_transfer_function(x_values[i][end_index])*sum([errors[i+1][start_index]*weights[i][j]])
                gradients[i].append(alpha*x_values[i][end_index]*errors[i+1][start_index])
    for i in range(len(gradients)):
        for j in range(len(gradients[i])):
            weights[i][j] += gradients[i][j]
    return weights
            
def main():
    training_examples = file_to_lines()
    expected_values = [float(example.split('=>')[-1][1]) for example in training_examples]
    training_examples = [[float(i) for i in example.split('=>')[0].split(' ')[:-1]] for example in training_examples]
    layer_sizes = [len(training_examples[0])+1,2,1,1]
    training_examples = [example+[1.0] for example in training_examples]
    alpha = 0.1
    epochs = 10000
    min_error =10000
    weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    for e in range(epochs):
        for i in range(len(training_examples)):
            inputs = training_examples[i]
            outputs,x_values,y_values = forward_propogation(inputs,weights)
            weights = back_propogation(inputs,outputs[0],weights,expected_values,alpha,x_values,y_values,training_examples)
        instance_error = error([forward_propogation(training_examples[i],weights)[0][0] for i in range(len(training_examples))],expected_values)
        if instance_error<0.9*min_error:
            print('Layer counts '+' '.join(str(i) for i in layer_sizes))
            print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
        if instance_error < min_error:
            min_error = instance_error
        if min_error < 0.01:
            print(e)
            break
    print('Layer counts '+' '.join(str(i) for i in layer_sizes))
    print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
    print(forward_propogation([0,0,1],weights))
    # test_weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    # print(forward_propogation([0,0,1],test_weights))
    # print(test_weights)
if __name__ == '__main__':
    main()
#Shaurya Jain, pd 3, 2025