import math

def sum(v0, v1):
    return (v0[0] + v1[0], v0[1] + v1[1])

def scalar_product(alpha, v):
    return (alpha * v[0], alpha * v[1])

def dist(v0, v1):
    diff_v = sum(v1, scalar_product(-1, v0))
    sum_sq = diff_v[0] ** 2 + diff_v[1] ** 2

    return math.sqrt(sum_sq)

