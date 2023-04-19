# %%
import numpy as np 
# %%
class Agent:
    def __init__(self, a0, b0, q):
        self.a0 = a0
        self.b0 = b0
        self.q = q
        self.p = 0.0
        self.pickP()

    def pickP(self):  # PICK P  FROM BETA DISTRIBUTION
        self.p = np.random.beta(self.a0, self.b0)

    # def notPickP(self):
    #     self.p = 1 - np.random.beta(self.a0, self.b0)

    def draw(self):
        if np.random.uniform(0, 1) < self.p:
            return True
        else:
            return False

    def turn(self):
        if np.random.uniform(0, 1) < self.q:
            self.pickP()

        return self.draw()


#%%
ag = Agent(0.1, 0.5, 0.1)
n = 6

results = []
prob = []
for i in range(n):
    results.append(ag.turn())
results


# %%
class DBMAgent:
    def __init__(self, a0, b0, q, gamma, outcomes):
        self.a0 = a0
        self.b0 = b0
        self.q = q
        self.p = 0.0
        self.outcomes = outcomes
        self.num = len(outcomes)
        self.tb = np.zeros((self.num + 1, self.num + 1))
        self.tb[0, 0] = 1
        self.gamma = gamma

    def likelihood(self):
        pass

    def mu(self, i, j):
        # if i == 0 and j == 0:
        #     self.a0 = self.a0
        #     self.b0 = self.b0
        # # elif i == 0:
        # #     self.a0 = 0.1
        # #     self.b0 = 0.5 + j
        # # elif j == 0:
        # #     self.a0 = 0.1 + i
        # #     self.b0 = 0.5
        # else:
        self.a0 = self.a0 + i
        self.b0 = self.b0 + j
        return self.a0 / (self.a0 + self.b0)

    def turn(self):

        for o in self.outcomes:
            tb_new = self.tb.copy()

            for n in range(self.tb.shape[0]):
                for m in range(self.tb.shape[1]):
                    if n == 0 and m == 0:
                        self.tb[n, m] = self.tb[n, m] + self.gamma
                    else:
                        self.tb[n, m] = self.tb[n, m] * (1 - self.gamma)

            for n in range(self.tb.shape[0]):
                for m in range(self.tb.shape[1]):
                    if o:
                        if m > 0:
                            tb_new[n, m] = self.tb[n, m-1] * self.mu(n, m)
                        else:
                            tb_new[n, m] = 0.0
                    else:
                        if n > 0:
                            tb_new[n, m] = self.tb[n-1, m] * self.mu(n, m)
                        else:
                            tb_new[n, m] = 0.0
            z = 0.0
            for n in range(self.tb.shape[0]):
                for m in range(self.tb.shape[1]):
                    z += tb_new[n, m]
                    # print(z)
            for n in range(self.tb.shape[0]):
                for m in range(self.tb.shape[1]):
                    self.tb[n, m] = tb_new[n, m] / z

            print(o, z, '\n', self.tb)


# %%
agent = DBMAgent(0.1, 0.5, 0.1, 0.2, results)
agent.turn()
agent.outcomes
# %%
# print(outcomes)
# n = len(outcomes)
# tb = np.zeros((n + 1, n + 1))
# t = []
# tb[0, 0] = 1
# p_t = 1
# p_f = 1
# gm = 0.2
# for n in range(tb.shape[0]):
#     for m in range(tb.shape[1]):
#         def like():
#             pass
#
#
#         def mu(i, j):
#             if i == 0 and j == 0:
#                 a = 0.1
#                 b = 0.5
#             elif i == 0:
#                 a = 0.1
#                 b = 0.5 + j
#             elif j == 0:
#                 a = 0.1 + i
#                 b = 0.5
#             else:
#                 a = 0.1 + i
#                 b = 0.5 + j
#             return a / (a + b)
#
#
#         for o in outcomes:
#             if o:
#                 tb[n, m] = 1
#                 tb[n, m] *= (1 - gm)
#
#                 tb[abs(n - 1), m] += gm if (tb[abs(n - 1), m] == 0) else gm * tb[abs(n - 1), m]
#
#                 u = mu(abs(n - 1), m)
#                 z = tb[abs(n - 1), m] + tb[n, m]  # gm*tb[n-1,m] + (1-gm)*tb[n,m]
#
#                 tb[n, m] = tb[abs(n - 1), m] * u / z
#                 tb[0, m] = 0
#
#                 # print(o, (n, m), u, z, tb[n, m], '\n', tb)
#             #
#             else:
#                 # p = 1 - np.random.beta(0.1 + n, 0.5 + m)
#                 tb[n, m] = 1
#                 tb[n, m] *= (1 - gm)
#                 tb[n, abs(m - 1)] += gm if (tb[n, abs(m - 1)] == 0) else gm * tb[n, abs(m - 1)]
#                 # tb[n, m - 1] = 0
#                 # tb[n, m - 1] += gm
#                 u = 1 - mu(n, abs(m - 1))
#                 z = tb[n, abs(m - 1)] + tb[n, m]  # gm*tb[n ,m-1] + (1-gm)*tb[n,m]
#                 tb[n, m] = tb[n, abs(m - 1)] * u / z
#                 tb[n, 0] = 0
#
#             print(o, (n, m), tb[n, m], '\n', tb)
