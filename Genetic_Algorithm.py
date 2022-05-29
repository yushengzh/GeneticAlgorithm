import math
import random


class Variable:

    def __init__(self, lb, ub, alpha, N):
        self.low_bound = lb
        self.up_bound = ub
        self.alpha = alpha
        self.N = N
        self.m = 0

    # 编码
    def code_generator(self) -> (int, list):
        temp = self.up_bound - self.low_bound
        m = math.ceil(math.log2(temp * pow(10, self.alpha) + 1))
        self.m = m
        codes = []
        for i in range(self.N):
            codes.append(random.randint(0, pow(2, m) - 1))
        return codes

    # 解码
    def decode(self, source: list) -> list:
        temp = self.up_bound - self.low_bound
        m = math.ceil(math.log2(temp * pow(10, self.alpha) + 1))
        res = [round(self.low_bound + temp * code / (pow(2, m) - 1), self.alpha) for code in source]
        return res

    def decode_single(self, source: int) -> list:
        temp = self.up_bound - self.low_bound
        m = math.ceil(math.log2(temp * pow(10, self.alpha) + 1))
        res = round(self.low_bound + temp * source / (pow(2, m) - 1), self.alpha)
        return res

    # 轮盘赌
    def roulette_wheel_select(self, norm_fitness: list, cnt: int) -> list:
        rw_selected = []
        scale = []
        delay = 0
        scale.append(delay)
        for item in norm_fitness:
            scale.append(round(delay + item, self.alpha))
            delay = delay + item
        # print("the roulette_wheel looks like: "+ str(scale))
        for i in range(cnt): # len(norm_fitness)
            seed = round(random.random(), self.alpha)
            for j in range(len(scale) - 1):
                if scale[j] < seed <= scale[j + 1]:
                    rw_selected.append(j + 1)
                    break
        return rw_selected


def target_func(x1: float, x2: float) -> float:
    return 21.5 + x1 * math.sin(4*math.pi*x1) + x2 * math.sin(20*math.pi*x2)


def bat_target_func(x1: list, x2: list, N) -> list:
    return [21.5 + x1[i] * math.sin(4*math.pi*x1[i]) + x2[i] * math.sin(20 * math.pi*x2[i]) for i in range(N)]


# 计算适应度(normalized)
def cal_fitness_norm(x1: list, x2: list) -> list:
    fitness = bat_target_func(x1, x2, len(x1))
    sum_all = sum(fitness)
    norm_fitness = [item / sum_all for item in fitness]
    return norm_fitness


# 计算适应度(without normalization)
def cal_fitness(x1: list, x2: list) -> list:
    fitness = bat_target_func(x1, x2, len(x1))
    return fitness


def __binary_cross(e1: list, e2: list, code_len: int) -> (list, list):
    split = random.randint(0, code_len - 2)
    temp = e1[split:split + 2]
    e1[split:split + 2] = e2[split:split + 2]
    e2[split:split + 2] = temp
    return e1, e2


def cross_pool(select_in: list, N: int, code_len: int, o1: list, pc: int):
    cnt = N // 2
    #pc = 0.6
    for i in range(cnt):
        if random.random() < pc:
            a, b = __binary_cross(select_in[i], select_in[N-i-1], code_len)
            o1.append(a)
            o1.append(b)


def variation(crossed: list, pm: int) -> list:
    res = []
    for item in crossed:
        it_re = ""
        for i in range(len(item)):
            r = random.random()
            if r <= pm:
                it_re = it_re + str(1 - int(item[i]))
            else: it_re = it_re + item[i]
        res.append(it_re)
    return res
