from matplotlib import pyplot as plt
import numpy as np

# fig.suptitle('max( min(0.4 * x, 20), 20 * log(x + 4.5) - 60) * a')

def scale_down(x, a):
    return np.maximum(np.minimum(0.4 * x, 20), 20 * np.log(x + 4.5) - 60) * a

def reset(p, kd, cp, m, w):
    return round(scale_down(p, 2) + kd + 0.1 * cp + w * 0.25 / m, 2)

# x = np.arange(100)
# y = scale_down(x, 2)
# d = (1 - y / x) * 100
# plt.plot(x, y)
# plt.plot(y)
# plt.plot(d)
# plt.xlim = [-5, 105]
# plt.ylim = [-5, 105]
# plt.show()

fmt1 = '{0:<10} {1:<10} {2:<10} {3:<10} {4:<10} {5:<10}'
fmt = '{0:<10} {1:<10} {2:<10} {3:<10} {4:<10} {5:<10}'

print(fmt1.format('Points', 'KD', 'CPs', 'Matches', 'Wins', 'Reset', ))
print(fmt.format(100, 3.1, 65, 30, 25, reset(100, 3.1, 65, 30, 25)))
print(fmt.format(100, 1.1, 15, 50, 15, reset(100, 1.1, 15, 50, 15)))
print(fmt.format(90, 2.46, 50, 10, 10, reset(90, 2.46, 50, 10, 10)))
print(fmt.format(70, 1.46, 32, 6, 3, reset(70, 1.46, 32, 6, 3)))
print(fmt.format(63, 1.1, 28, 4, 2, reset(63, 1.1, 28, 4, 2)))
print(fmt.format(35, 1.56, 60, 10, 5, reset(35, 1.56, 60, 10, 5)))
print(fmt.format(13, 1.25, 55, 8, 3, reset(13, 1.25, 55, 8, 3)))

for i in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    print(i, scale_down(i, 2), (1 - scale_down(i, 2) / i) * 100)

# import pandas as pd
#
#
# def f(k, c, w, m):
#     if m:
#         return round(2 * k + 0.5 * c + w * 2.5 / m, 2)
#     else:
#         return None
#
#
# t = str('2 * k + 0.5 * c + w * 2.5 / m')
#
# df = pd.DataFrame(index=range(5*5), columns=['KD-ratio', 'CPs', 'Wins', 'Matches', 'Points'])
#
# kds = [0.5, 1, 1.5, 2, 2.5]
# cps = [0, 5, 10, 15, 20]
# wins = [0, 10, 20, 30, 40]
# matches = [0, 10, 20, 30, 40]
#
# i = 0
# for kd in kds:
#     for cp in cps:
#         for win in wins:
#             for match in matches:
#                 df.loc[i] = [kd, cp, win, match, f(kd, cp, win, match)]
#                 i += 1
#
# open('points.txt', 'w').write(df.to_string(justify='right', index=False, index_names=False))
