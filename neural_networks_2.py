import sys;args=sys.argv[1:]
import random
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
def forward_propogation(inputs,weights):
    x_values = {0:inputs}
    y_values = {}
    for i in range(len(weights)-1):
        #  print(x_values[i],weights[i],sep='\n')
         y_values[i]=[dot_product(x_values[i],weights[i][j*len(x_values[i]):(j+1)*len(x_values[i])]) for j in range(len(weights[i])//len(x_values[i]))]
         x_values[i+1] = [logistic_transfer_function(y) for y in y_values[i]]
    return hadamard(x_values[len(weights)-1],weights[-1]),x_values,y_values
def error(outputs,expected_values):
    return sum([0.5*sum([(outputs[i][j]-expected_values[i][j])**2 for i in range(len(outputs))]) for j in range(len(outputs[0]))])
def back_propogation(inputs,outputs,weights,expected_values,alpha,x_values,y_values,training_examples):
    gradients = {layer:[] for layer in range(len(weights))}
    errors = [[0.0 for j in range(len(x_values[i]))] for i in range(len(x_values))]
    partials = []
    for i in range(len(weights)-1,-1,-1):
        for j in range(len(weights[i])):
            
            start_index = j//len(x_values[i])
            end_index = j%len(x_values[i])
            if i == len(weights)-1:
                # print(i,x_values[i][j])
                # print(start_index,end_index,len(errors[i]))
                # print(end_index,"Expected values",expected_values,"x_values",x_values[i][j],"weight",weights[i][j],derivative_logistic_transfer_function(x_values[i][j]),sep='\n')
                errors[i][j] = (expected_values[j]-x_values[i][j]*weights[i][j])*weights[i][j]*derivative_logistic_transfer_function(x_values[i][j])
                gradients[i].append(alpha*(expected_values[j]-x_values[i][j]*weights[i][j])*x_values[i][j])
                # partials.append((expected_values-x_values[i][j]*weights[i][j])*x_values[i][j])
                # print((expected_values[j]-x_values[i][j]*weights[i][j])*x_values[i][j])
                # print("Error in the if", errors[i][j])
                # print("in the if", x_values[i][j])
            else:
                # print(start_index,end_index,len(errors[i]))
                errors[i][end_index] = derivative_logistic_transfer_function(x_values[i][end_index])*sum([errors[i+1][start_index]*weights[i][j]])
                gradients[i].append(alpha*x_values[i][end_index]*errors[i+1][start_index])
                # partials.append(x_values[i][end_index]*errors[i+1][start_index])
                # print(x_values[i][end_index]*errors[i+1][start_index])
                # print("in the else",x_values[i][end_index])
    # print("Partials",partials,sep='\n')
    # print("Errors",errors,sep='\n')
    # for key in gradients:
    #     if(len(gradients[key])>=2):
    #         split1,split2 = gradients[key][:len(gradients[key])//2],gradients[key][len(gradients[key])//2:]
    #         joined_splits = list(zip(split1,split2))
    #         new_gradients_list = []
    #         for first, second in joined_splits:
    #             new_gradients_list+=[first,second]
    #         gradients[key] = new_gradients_list
    for i in range(len(gradients)):
        for j in range(len(gradients[i])):
            # print(weights[i][j],gradients[i][j])
            weights[i][j] += gradients[i][j]
    return weights
            
def main():
    training_examples = file_to_lines()
    # expected_values = [float(example.split('=>')[-1][1]) for example in training_examples]

    expected_values = [[float(e) for e in example.split('=>')[-1][1:].split(' ')] for example in training_examples]
    

    # print(expected_values)
    training_examples = [[float(i) for i in example.split('=>')[0].split(' ')[:-1]] for example in training_examples]
    if len(expected_values[0])==1:

        output_size=1
        layer_sizes = [len(training_examples[0])+1,3,output_size,1]

    else:
        output_size = 2
        layer_sizes = [len(training_examples[0])+1,5,output_size,1]

    training_examples = [example+[1.0] for example in training_examples]
    alpha = 0.1
    epochs = 50000
    min_error =10000
    weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    # weights = [[2,1,1,2,0,3],[0.5,0.75],[0.875]]
    # weights = [[2,1,0,1,2,3],[0.5,0.75],[0.875]]


    # weights = [[0.3,-2.0,-1.5,2,0,2],[0.3,-0.5],[-1.0]]
    # weights = [[0.3,-1.5,2,-2,0,-2],[0.3,-0.5],[-1.0]]
    for e in range(epochs):
        for i in range(len(training_examples)):
            inputs = training_examples[i]
            
            outputs,x_values,y_values = forward_propogation(inputs,weights)
            # print(x_values,y_values,outputs,sep='\n')
            weights = back_propogation(inputs,outputs[0],weights,expected_values[i],alpha,x_values,y_values,training_examples)
            # print(f"Epoch {e+1}",inputs, weights, sep='\n')
        instance_error = error([forward_propogation(training_examples[i],weights)[0] for i in range(len(training_examples))],expected_values)
        if instance_error<0.9*min_error:
            print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-1]+1))
            print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
        if instance_error < min_error:
            min_error = instance_error
        if min_error < 0.01:
            print(e)
            break
        if epochs+1%20000==0 and min_error>0.099:
            min_error = 10000
            weights = [[random.uniform(-1,1) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]

    print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-2]))
    print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
    
    print("Error:", error([forward_propogation(training_examples[i],weights)[0] for i in range(len(training_examples))],expected_values))
    # print(forward_propogation([1,0,1],[[2,1,1,2,0,3],[0.5,0.75],[0.875]]))
    # print(weights)
    # test_weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    # print(forward_propogation([0,0,1],test_weights))
    # print(test_weights)
if __name__ == '__main__':
    main()
#Shaurya Jain, pd 3, 2025