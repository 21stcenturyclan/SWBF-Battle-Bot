import math

def reset(p):
    return max(min(0.4 * p, 20), 20 * math.log(p + 4.5) - 60) * 1.5

def performance(kd, cp, w, m):
    return kd + 0.1 * cp + w * 0.25 / m


print(reset(40) + performance(1.63, 15, 0, 1))
print(reset(40) + performance(0.65, 18, 0, 1))
print(reset(40) + performance(0.69, 12, 0, 1))
print(reset(40) + performance(1, 9, 0, 1))
