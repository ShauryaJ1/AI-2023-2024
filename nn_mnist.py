import sys;args=sys.argv[1:]
import random
import math
import csv
import numpy as np
import time
def read_in_data(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            rows.append(row)
        examples = [(float(row[0]),[float(v) for v in row[1:]]) for row in rows[1:]]
    return examples
def relu(x):
    return max(0,x)
def derivative_relu(x):
    return 1 if x>0 else 0
def logistic_transfer_function(x):
    return 1/(1+math.exp(-1.0*np.clip(x, -500, 500)))
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
def accuracy(testing_examples,expected_testing_values,weights,n,output_lookup_table):
    correct = 0
    for i in range(n):
        output_list = forward_propogation(testing_examples[i],weights)[0]
        if output_lookup_table[tuple(expected_testing_values[i])] == output_list.index(max(output_list)):
            correct+=1
    return correct/n
def error(outputs,expected_values):
    return sum([0.5*sum([(outputs[i][j]-expected_values[i][j])**2 for i in range(len(outputs))]) for j in range(len(outputs[0]))])
def back_propogation(inputs,outputs,weights,expected_values,alpha,x_values,y_values,training_examples):
    # gradients = {layer:[] for layer in range(len(weights))}
    gradients = {}
    for layer in range(len(weights)):
        gradients[layer] = [0.0 for l in range(len(weights[layer]))]
    errors = [[0.0 for j in range(len(x_values[i]))] for i in range(len(x_values))]
    partials = []
    for i in range(len(weights)-1,-1,-1):
        for j in range(len(weights[i])):
            
            start_index = j//len(x_values[i])
            end_index = j%len(x_values[i])
            if i == len(weights)-1:
               
                errors[i][j] = (expected_values[j]-x_values[i][j]*weights[i][j])*weights[i][j]*derivative_logistic_transfer_function(x_values[i][j])
                gradients[i][j] = (alpha*(expected_values[j]-x_values[i][j]*weights[i][j])*x_values[i][j])
                weights[i][j]+=gradients[i][j]
            else:
                # print(start_index,end_index,len(errors[i]))
                errors[i][end_index] = derivative_logistic_transfer_function(x_values[i][end_index])*sum([errors[i+1][start_index]*weights[i][j]])
                gradients[i][j] = (alpha*x_values[i][end_index]*errors[i+1][start_index])
                weights[i][j]+=gradients[i][j]
    # for i in range(len(gradients)):
    #     for j in range(len(gradients[i])):
    #         weights[i][j] += gradients[i][j]
    return weights
            
def main():
    output_lookup_table = {
        tuple([1.0]+[0.0]*9):0.0,
        tuple([0.0]+[1.0]+[0.0]*8):1.0,
        tuple([0.0]*2+[1.0]+[0.0]*7):2.0,
        tuple([0.0]*3+[1.0]+[0.0]*6):3.0,
        tuple([0.0]*4+[1.0]+[0.0]*5):4.0,
        tuple([0.0]*5+[1.0]+[0.0]*4):5.0,
        tuple([0.0]*6+[1.0]+[0.0]*3):6.0,
        tuple([0.0]*7+[1.0]+[0.0]*2):7.0,
        tuple([0.0]*8+[1.0]+[0.0]):8.0,
        tuple([0.0]*9+[1.0]):9.0
       
    }
    testing_examples = read_in_data('mnist_test.csv')
    expected_testing_values = []
    for example in testing_examples:
        temp_list = [0.0 for i in range(10)]
        temp_list[int(example[0])]=1.0
        expected_testing_values.append(temp_list)
    # print(testing_examples[0][1][:10])
    testing_examples = [[e/255.0 for e in example[1]]+[1.0] for example in testing_examples]
    # print(len(testing_examples[0])
    # testing_examples = [example+[1.0] for example in testing_examples]

    training_examples = read_in_data('mnist_train.csv')
    
    # expected_values = [float(example.split('=>')[-1][1]) for example in training_examples]

    expected_values = []
    for example in training_examples:
        temp_list = [0.0 for i in range(10)]
        temp_list[int(example[0])]=1.0
        expected_values.append(temp_list)
    

    # print(expected_values)
    training_examples = [[e/255.0 for e in example[1]] +[1.0] for example in training_examples]
    if len(expected_values[0])==1:

        output_size=1
        layer_sizes = [len(training_examples[0]),3,output_size,1]

    else:
        output_size = 10
        # layer_sizes = [len(training_examples[0]),300,75,10,1]
        layer_sizes = [len(training_examples[0]),32,10,1]

    # training_examples = [example for example in training_examples]
    alpha = 0.2
    epochs = 1
    min_error =10000
    weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    # weights = [[2,1,1,2,0,3],[0.5,0.75],[0.875]]
    # weights = [[2,1,0,1,2,3],[0.5,0.75],[0.875]]


    # weights = [[0.3,-2.0,-1.5,2,0,2],[0.3,-0.5],[-1.0]]
    # weights = [[0.3,-1.5,2,-2,0,-2],[0.3,-0.5],[-1.0]]  
    print('Started Training')
    start_time = time.time()
    for e in range(3):
        print("Epoch",e+1)
        for i in range(len(training_examples)):
            inputs = training_examples[i]

            if (i+1)%500==0:
                print(f"Example {i+1}")
                # curr_accuracy = accuracy(testing_examples,expected_testing_values,weights,1000,output_lookup_table)
                # alpha = (-1+2.0**(1-curr_accuracy))*0.8
                # print(f"current accuracy: {curr_accuracy}", f"alpha {alpha}")

            if (i+1)%5000==0:
                train_acc = accuracy(training_examples,expected_values,weights,5000,output_lookup_table)
                if train_acc>0.80:
                    alpha = 0.15
                if train_acc>0.85:
                    alpha = 0.1
                if train_acc>0.9:
                    alpha = 0.05
                print(f"Train Accuracy: {train_acc} Test Accuracy: {accuracy(testing_examples,expected_testing_values,weights,5000,output_lookup_table)}")
            outputs,x_values,y_values = forward_propogation(inputs,weights)
            # print(x_values,y_values,outputs,sep='\n')
            # print(expected_values[i])
            weights = back_propogation(inputs,outputs[0],weights,expected_values[i],alpha,x_values,y_values,training_examples)
        
            # print(f"Epoch {e+1}",inputs, weights, sep='\n')
        # instance_error = error([forward_propogation(training_examples[i],weights)[0] for i in range(1000)],expected_values[:1000])

        # if instance_error<0.9*min_error:
        #     print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-1]+1))
        # #     print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
        # if instance_error < min_error:
        #     min_error = instance_error
        # if min_error < 0.01:
        #     print(e)
        #     break
        # if epochs+1%20000==0 and min_error>0.099:
        #     min_error = 10000
        #     weights = [[random.uniform(-1,1) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    end_time = time.time()
    print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))

    print('Layer counts '+' '.join(str(i) for i in layer_sizes[:-1])+' '+str(layer_sizes[-2]))
    # print('\n'.join([' '.join([str(i) for i in layer]) for layer in weights]))
    
    print("Error:", error([forward_propogation(training_examples[i],weights)[0] for i in range(1000)],expected_values[:1000]))
    print("Accuracy:",accuracy(testing_examples,expected_testing_values,weights,10000,output_lookup_table))
    f = open("mnist_weights.txt","w")
    f.writelines('\n'.join([' '.join([str(w) for w in weight]) for weight in weights]))
    f.close()
    # output_list=forward_propogation(training_examples[0],weights)[0]
    
    # print(expected_values.index(max(expected_values[0])))
    # print(output_list.index(max(output_list)))
    # print(forward_propogation([1,0,1],[[2,1,1,2,0,3],[0.5,0.75],[0.875]]))
    # print(weights)
    # test_weights = [[random.uniform(-0.5,0.5) for j in range(layer_sizes[i]*layer_sizes[i+1])] for i in range(len(layer_sizes)-1)]
    # print(forward_propogation([0,0,1],test_weights))
    # print(test_weights)
if __name__ == '__main__':
    main()
#Shaurya Jain, pd 3, 2025