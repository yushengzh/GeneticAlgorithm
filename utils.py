
'''
tools for algorithm
'''
from Genetic_Algorithm import Variable


# 十进制 --> 二进制 return (list(str), str):
def dec2bin(value: int, width: int) -> (list, str):
    bins = ""
    temp = value
    for i in range(width):
        bins_char = bin(temp % 2)[-1]
        temp = temp // 2
        bins = bins + bins_char
    res = []
    i = width - 1
    while i >= 0:
        res.append(bins[i])
        i -= 1
    return res, bins[::-1]


# 二进制 --> 十进制
def bin2dec(value: str) -> int:
    return int(value, 2)


# 编码list --> str
def list2str(value: list) -> str:
    res = ""
    for i in value:
        res = res + str(i)
    return res


# str --> 编码list
def str2list(value: str) -> list:
    res = []
    for i in range(len(value)):
        res.append(str(value[i]))
    return res


# binary string --> <int>pair(x1, x2)
def binstr2pair(source: list, first_len: int, x1: Variable, x2: Variable) -> list:
    tp2 = [[source[i][0:first_len], source[i][first_len:len(source[0])]] for i in range(len(source))]
    tp3 = [[x1.decode_single(bin2dec(tp2[i][0])), x2.decode_single(bin2dec(tp2[i][1]))] for i in range(len(tp2))]
    return tp3


# obtain index of the top 2(max) of the list
def top2idx(in_list: list) -> (int, int):
    fir = in_list.index(max(in_list))
    cop = in_list.copy()
    cop.remove(max(in_list))
    sec = cop.index(max(cop))
    return fir, sec

