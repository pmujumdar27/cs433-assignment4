import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

protocol = input()
mode = input()

# persist_indiv_time_df = pd.read_csv(f"{protocol}_thread_indiv_time_mode_{mode}.csv")
# persist_indiv_throughput_df = pd.read_csv(f"{protocol}_thread_indiv_throughput_mode_{mode}.csv")
# persist_agg_df = pd.read_csv(f"{protocol}_thread_agg_log_mode_{mode}.csv")

persist_indiv_time_df = pd.read_csv("out1.csv")
persist_indiv_throughput_df = pd.read_csv("out2.csv")
persist_agg_df = pd.read_csv("out3.csv")

# plt.plot(persist_agg_df)
# plt.show()
# plt.plot(persist_indiv_throughput_df)
# plt.show()
# plt.plot(persist_indiv_time_df)
# plt.show()

s = persist_indiv_throughput_df.mean()
print(s)
print(persist_agg_df.mean())
print(persist_indiv_time_df.mean())

# print(persist_indiv_time_df)
# print(persist_indiv_throughput_df)
# print(persist_agg_df)