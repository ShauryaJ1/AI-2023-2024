import sys; args = sys.argv[1:]
import math
import time 


def bruteForce(dims,block_locations,available_positions):
    
    if not dims:
        return block_locations
    
    for psbl in all_psbls[dims[0]]:
    # for psbl in psbls(dims[0]):
        if set(psbl[0]).issubset(available_positions):
            # print(psbl)
            
            new_block_locations = {**block_locations}
            if psbl[1]==0:
                new_block_locations[psbl[0][0]]=(psbl[0],dims[0])
            else:
                new_block_locations[psbl[0][0]]=(psbl[0],dims[0][::-1])
            new_available_positions = {*available_positions} - set(psbl[0])
            new_dims = [*dims]
            del new_dims[0]
            bF = bruteForce(new_dims,new_block_locations,new_available_positions)
            if bF:
                return bF
            continue
    return ''
def psbls(dim):
    # print(type(dim), dim)
    height = int(dim[0])
    width = int(dim[1])
    lateral = rect_width - width + 1
    longitudinal = rect_height - height + 1
    possibles = []
    if height<=rect_height and width<=rect_width:
        for a in range(longitudinal):
            for b in range(lateral):
                current_possible = []
                for c in range(height):
                    for d in range(width):
                        ind  = (a+c)*rect_width + b + d
                        # print(ind)
                        if ind< rect_area:
                            current_possible.append(ind)
                possibles.append((current_possible,0))
    if height<=rect_width and width<=rect_height:
        rev_height  = width
        rev_width = height
        rev_lateral = rect_width - rev_width + 1
        rev_longitudinal = rect_height - rev_height + 1
        for a in range(rev_longitudinal):
            for b in range(rev_lateral):
                current_possible = []
                for c in range(rev_height):
                    for d in range(rev_width):
                        ind  = (a+c)*rect_width + b + d
                        # print(ind)
                        if ind< rect_area:
                            current_possible.append(ind)
                possibles.append((current_possible,1))
    
    
    return possibles
def make_all_possibles(dims):
    return {dim:psbls(dim) for dim in dims}
if __name__ == '__main__':
    if len(args)==0:
        rect_height =3
        rect_width =2
        rect_area = 6
        print(psbls(('1','2')))
        
    else:
        start_time = time.time()
        dims = [s.lower() for s in args]
        # dims = ['3x6', '2x3', '4x3']
        # dims = ['29x24', '3x8', '5x22', '3x15', '18x9', '1x10','23x7','1x28','3x14','19x6']
        # dims = ['11x12', '3x6', '2x5', '4x10', '7x9', '1x1']
        # 20 28 6X13 4 7 10x1 24 2 8x13 18 4 4X16 4 4 10x14
        # dims = ['28x27', '6x13', '4x10', '4x4', '13x6', '5x5', '8x14', '8x8', '7x7', '6x6' ,'15x16', '4x4']
        dims = ['22x20' ,'11x10', '9x11', '5x10', '9x7', '11x6' ,'5x10']
        # dims = ['96x148', '5x5' ,'13x13', '21x28', '8x8', '2x2','3x3', '96x89', '59x55' ,'38x41']
        dim_tuples = []
        i = 0
        while i <len(dims):
            if 'x' in dims[i]:
                # print(dims[i])
                x = dims[i].index('x')
                dim_tuples.append((dims[i][:x],dims[i][x+1:]))
                # print(i)
                # dim_tuples.append((int(dims[i][:x])*int(dims[i][x+1:]),dims[i][:x],dims[i][x+1:]))
                i+=1
            else:
                dim_tuples.append((dims[i],dims[i+1]))
                # dim_tuples.append((int(dims[i])*int(dims[i+1]),dims[i],dims[i+1]))
                i+=2
        rect = dim_tuples[0]
        rect_area ,rect_height, rect_width= int(rect[0])*int(rect[1]),int(rect[0]),int(rect[1])
        # rect_area,rect_height,rect_width = rect[0] ,int(rect[1]),int(rect[2])
        available_positions = {*range(rect_area)}
        block_locations = {}
        if rect_area< sum(int(dim[0])*int(dim[1]) for dim in dim_tuples[1:]):
        # if rect_area< sum(dim[0] for dim in dim_tuples[1:]):
            print('No Solution')
        else:
        #     sorted_dim_tuples = sorted(dim_tuples[1:]) #
        #     wo_area = [(dim[1],dim[2]) for dim in sorted_dim_tuples] #
            area_dim_tuples = sorted([(int(dim[0])*int(dim[1]),i) for i, dim in enumerate(dim_tuples[1:])],reverse=True)
            # area_dim_tuples = sorted([(int(dim[1]),i) for i, dim in enumerate(dim_tuples[1:])],reverse=True)

            sorted_dim_tuples = [dim_tuples[1+dim[1]] for dim in area_dim_tuples]
            # print(sorted_dim_tuples)
            all_psbls = make_all_possibles(sorted_dim_tuples)
            # print(all_psbls)
            decomposition = bruteForce(sorted_dim_tuples,block_locations,available_positions)
            
            # decomposition = bruteForce(dim_tuples[1:],block_locations,available_positions)
            if decomposition:
                decomposition_list = []
                pos_to_skip = set()
                for pos in available_positions:
                    if pos not in pos_to_skip:
                        if pos in decomposition:
                            decomposition_list.append(decomposition[pos][1][0]+'x'+decomposition[pos][1][1])
                            pos_to_skip = pos_to_skip.union(decomposition[pos][0])
                        else:
                            decomposition_list.append('1x1')
            #     decomposition_list = [decomposition[idx][1][0]+'x'+decomposition[idx][1][1] for idx in decomposition]
                print("Decomposition:", *decomposition_list)
            else:
                print('No Solution')
            
        # if dim_tuples==[('3','6'),('2','3'),('4','3')]:
        #         print('Decomposition: 3x2 3x4')
        # elif dim_tuples==[('3','5'),('5','3')]:
        #         print('Decomposition: 3x5')
        # elif dim_tuples==[('11','12'),('3','6'),('2','5'),('4','10'),('7','9'),('1','1')]:
        #         print('Decomposition: 4x10 5x2 7x9 1x1 6x3')
        # else:
        #       print('No Solution')
        print(f"Time: {time.time()-start_time:.3g}s")

    



#Shaurya Jain, pd 3, 2025