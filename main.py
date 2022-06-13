'''
Created by Yusheng Zhao 6/1/2022
'''

import math
import Genetic_Algorithm
import utils
from Genetic_Algorithm import Variable, cal_fitness_norm, cross_pool, variation, cal_fitness
from utils import bin2dec, dec2bin, list2str, str2list, binstr2pair


pm = 0.05
pc = 0.6

if __name__ == '__main__':
    
    #parameters
    a1 = -3.0
    a2 = 4.1
    b1 = 12.1
    b2 = 5.8
    alpha = 4
    nums = 10
    
    # lowbound, upbound, alpha, nums
    x1 = Variable(a1, b1, alpha, nums)
    x2 = Variable(a2, b2, alpha, nums)

    # generate codes
    code1 = x1.code_generator()
    code2 = x2.code_generator()
    code_len = x1.m + x2.m

    # init
    init_group = [str(dec2bin(code1[i], x1.m)[1]) + str(dec2bin(code2[i], x2.m)[1]) for i in range(x1.N)]
    init_group_list = [dec2bin(code1[i], x1.m)[0]+dec2bin(code2[i], x2.m)[0] for i in range(x1.N)]

    # decoding
    temp_int = [[x1.decode(code1)[i], x2.decode(code2)[i]] for i in range(x1.N)]

    print("the 0th generation is(binary version)" + str(init_group))
    print("the 0th generation is(int version)" + str(temp_int))

    # cal function value
    tx1 = [item[0] for item in temp_int]
    tx2 = [item[1] for item in temp_int]
    norm_fits = Genetic_Algorithm.cal_fitness_norm(tx1, tx2)
    # print(norm_fits)

    # roulette_wheel_select
    rw_selected = x1.roulette_wheel_select(norm_fits, len(norm_fits))
    temp_int_list = [str2list(item) for item in init_group]
    temp_int_list_select = [temp_int_list[item - 1] for item in rw_selected]

    # cross
    o1 = []
    cross_pool(temp_int_list_select, len(temp_int_list_select), len(temp_int_list_select[0]), o1, pc)
    tp1 = [list2str(item) for item in o1]

    # variation
    tp1_variation = variation(tp1, pm)

    temp_bin = init_group + tp1_variation
    temp_int = binstr2pair(temp_bin, x1.m, x1, x2)

    tx1 = [item[0] for item in temp_int]
    tx2 = [item[1] for item in temp_int]
    norm_fits = cal_fitness_norm(tx1, tx2)
    fits = cal_fitness(tx1, tx2)
    next_gen_int = []
    next_gen_bin = []
    fir, sec = utils.top2idx(norm_fits)
    next_gen_int.append(temp_int[fir])
    next_gen_int.append(temp_int[sec])

    max_pair = temp_int[fir]
    max_value = Genetic_Algorithm.target_func(max_pair[0], max_pair[1])

    next_gen_bin.append(temp_bin[fir])
    next_gen_bin.append(temp_bin[sec])
    rw_selected = x1.roulette_wheel_select(norm_fits, 8)
    for item in rw_selected:
        next_gen_int.append(temp_int[item - 1])
        next_gen_bin.append(temp_bin[item - 1])
    temp_int = next_gen_int
    temp_bin = next_gen_bin

    early_stop = 0

    for iter in range(1000):
        tx1 = [item[0] for item in temp_int]
        tx2 = [item[1] for item in temp_int]
        norm_fits = cal_fitness_norm(tx1, tx2)

        # roulette_wheel_select
        rw_selected = x1.roulette_wheel_select(norm_fits, len(norm_fits))
        temp_int_list = [str2list(item) for item in temp_bin]
        temp_int_list_select = [temp_int_list[item - 1] for item in rw_selected]

        # cross
        o1 = []
        cross_pool(temp_int_list_select, len(temp_int_list_select), len(temp_int_list_select[0]), o1, pc)
        tp1 = [list2str(item) for item in o1]

        # variation
        tp1_variation = variation(tp1, pm)

        temp_bin = temp_bin + tp1_variation
        temp_int = binstr2pair(temp_bin, x1.m, x1, x2)

        tx1 = [item[0] for item in temp_int]
        tx2 = [item[1] for item in temp_int]
        norm_fits = cal_fitness_norm(tx1, tx2)
        fits = cal_fitness(tx1, tx2)
        next_gen_int = []
        next_gen_bin = []
        fir, sec = utils.top2idx(norm_fits)
        next_gen_int.append(temp_int[fir])
        next_gen_int.append(temp_int[sec])
        max_pair_temp = temp_int[fir]

        next_gen_bin.append(temp_bin[fir])
        next_gen_bin.append(temp_bin[sec])
        rw_selected = x1.roulette_wheel_select(norm_fits, x1.m - 2)
        for item in rw_selected:
            next_gen_int.append(temp_int[item - 1])
            next_gen_bin.append(temp_bin[item - 1])

        temp_int = next_gen_int
        temp_bin = next_gen_bin
        print("the "+str(iter+1)+"th generation is(binary)" + str(temp_bin))
        print("the "+str(iter+1)+"th generation is(int)" + str(temp_int))
        maxx = round(Genetic_Algorithm.target_func(max_pair_temp[0], max_pair_temp[1]), 4)
        if maxx > max_value:
            max_value = maxx
            max_pair = max_pair_temp
        else: early_stop += 1

        print("After these generations, the opi-sol is", max_value, ", x1 =", max_pair[0], ", x2 =", max_pair[1])
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # if early_stop > 800: break
