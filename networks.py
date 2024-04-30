import sys;args=sys.argv[1:]
import random

'''
For C:
    have a while loop going until the # of edges has reached the edge count
    take one random node and another random node
    if they are already connected move on

For I:
    you have total node count
    loop through from 0 to node count - 1


'''
def main():
    avg_degree,fashion,num_nodes = float(args[0]),args[1], int(args[2])
    edge_count = avg_degree*num_nodes
    num_edges = 0
    if fashion == 'C':
        edge_dict = {node:[] for node in range(num_nodes)}
        while edge_count > num_edges:
            node1 = random.randint(0,num_nodes-1)
            node2 = random.randint(0,num_nodes-1)
            if node2 not in edge_dict[node1]:
                edge_dict[node1].append(node2)
                edge_dict[node2].append(node1)
                num_edges += 2
            
    else:
        edge_dict = {0:[],1:[]}
        for node in range(2,num_nodes):
                print(node)
                if node not in edge_dict:
                    edge_dict[node] = []
            
                weighted_list_to_sample_from = []
                for key in edge_dict:
                    for i in range(len(edge_dict[key])+1):
                        weighted_list_to_sample_from.append(key)
                current_avg_degree = sum([len(edge_dict[key]) for key in edge_dict])/len(edge_dict)
                current_degree_sum  = sum([len(edge_dict[key]) for key in edge_dict])
                while current_avg_degree < avg_degree and current_degree_sum <= len(edge_dict)*(len(edge_dict)-1):
                    random_node_one = random.choice(weighted_list_to_sample_from)
                    random_node_two = random.choice(weighted_list_to_sample_from)
                    if random_node_one not in edge_dict[random_node_two]:
                        edge_dict[random_node_one].append(random_node_two)
                        edge_dict[random_node_two].append(random_node_one)
                        # current_avg_degree = sum([len(edge_dict[key]) for key in edge_dict])/len(edge_dict)
                        current_degree_sum +=2
                        current_avg_degree = current_degree_sum/len(edge_dict)
                    




        

            
    degree_count_dict = {}
    for node in edge_dict:
        if len(edge_dict[node]) in degree_count_dict:
            degree_count_dict[len(edge_dict[node])] += 1
        else:
            degree_count_dict[len(edge_dict[node])] = 1
    for degree in degree_count_dict:
        print(f'{degree}:{degree_count_dict[degree]}')
if __name__ == '__main__':
    main()
#Shaurya Jain, pd 3, 2025