import sys;args=sys.argv[1:]
import random
import time
import math
def logistic_transfer_function(x):
    return 1/(1+math.exp(-x))
def derivative_logistic_transfer_function(x):
    return x*(1.0-x)
def file_to_lines():
    return open(args[0]).read().splitlines()
def hadamard(v1,v2):
    return [v1[i]*v2[i] for i in range(len(v1))]
def dot_product(v1,v2):
    return sum(hadamard(v1,v2))
def error(outputs,expected_values):
    return sum([(outputs[i][0]-expected_values[i][0])**2 for i in range(len(outputs))])/len(outputs)
def forward_propogation(inputs,weights):
    x_values = {0:inputs}
    y_values = {}
    for i in range(len(weights)-1):
        #  print(x_values[i],weights[i],sep='\n')
         y_values[i]=[dot_product(x_values[i],weights[i][j*len(x_values[i]):(j+1)*len(x_values[i])]) for j in range(len(weights[i])//len(x_values[i]))]
         x_values[i+1] = [logistic_transfer_function(y) for y in y_values[i]]
    # print(x_values)
    return hadamard(x_values[len(weights)-1],weights[-1]),x_values,y_values
def back_propogation(inputs,outputs,weights,expected_values,alpha,x_values,y_values,training_examples):
    gradients = {layer:[] for layer in range(len(weights))}
    errors = [[0.0 for j in range(len(x_values[i]))] for i in range(len(x_values))]
    partials = []
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
            # print(weights[i][j],gradients[i][j])
            weights[i][j] += gradients[i][j]
    return weights
def arg_type_compare(x,y,arg_type):
    if arg_type == '>':
        return x>y
    elif arg_type == '<':
        return x<y
    elif arg_type == '>=':
        return x>=y
    else: 
        return x<=y
def make_training_examples(radius,arg_type):
    percent_within_circle = (math.pi*radius**2)/9.0
    num_training_examples_within_circle = int(percent_within_circle*100)
    points = []

    while len(points) < num_training_examples_within_circle:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if arg_type_compare(x**2 + y**2, radius**2, arg_type):
            points.append((x, y,1.0))

    while len(points) < 100:
        x = random.uniform(-1.5, 1.5)
        y = random.uniform(-1.5, 1.5)
        if not arg_type_compare(x**2 + y**2, radius**2, arg_type):
            points.append((x, y,0.0))
    random.shuffle(points)
    # print('made training examples')
    return points

def main():
    # training_examples = file_to_lines()
    arg = args[0]
    if '>' in arg:
        if '=' in arg:
            arg_type = '>='
            radius = math.sqrt(float(arg.split('>=')[-1]))
        else:
            arg_type = '>'
            radius = math.sqrt(float(arg.split('>')[-1]))
    else:
        if '=' in arg:
            arg_type = '<='
            radius = math.sqrt(float(arg.split('<=')[-1]))
        else:
            arg_type = '<'
            radius = math.sqrt(float(arg.split('<')[-1]))
    training_examples = make_training_examples(radius,arg_type)
    expected_values = [[example[-1]] for example in training_examples]
    training_examples = [[example[0],example[1]] for example in training_examples]
    layer_sizes = [3,5,2,1,1]
    alpha = 0.1
    epochs = 10000
    min_error =10000
    weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    e = 0
    while True:
            if (e+1)%1000 ==0:
                print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-2]))
                print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
        
            # inputs = training_examples[i]
            x = random.uniform(-1.5, 1.5)
            y = random.uniform(-1.5, 1.5)
            inputs = [x,y,1]
            
            outputs,x_values,y_values = forward_propogation(inputs,weights)
            # print(x_values,y_values,outputs,sep='\n')
            weights = back_propogation(inputs,outputs[0],weights,[arg_type_compare(x**2 + y**2, radius**2, arg_type)],alpha,x_values,y_values,training_examples)
            e+=1
            # print(f"Epoch {e+1}",inputs, weights, sep='\n')
        # instance_error = error([forward_propogation(training_examples[i],weights)[0] for i in range(len(training_examples))],expected_values)
        # if instance_error<0.9*min_error:
        #     print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-2]))
        #     print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
        # if instance_error < min_error:
        #     min_error = instance_error
        # if min_error < 0.01:
        #     print(e)
        #     break
        # if epochs+1%20000==0 and min_error>0.099:
        #     min_error = 10000
        #     weights = [[random.uniform(-1,1) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]

    print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-2]))
    print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
    
    # print("Error:", error([forward_propogation(training_examples[i],weights)[0] for i in range(len(training_examples))],expected_values))
    # print(training_examples[i],expected_values[i],forward_propogation(training_examples[i],weights)[0],sep='\n')
if __name__ == '__main__':
    # start_time=time.time()
    main()
    # end_time=time.time()
    # print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))

#Shaurya Jain, pd 3, 2025