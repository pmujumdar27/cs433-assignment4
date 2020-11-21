import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

protocol = input()
mode = input()

persist_indiv_time_df = pd.read_csv(f"{protocol}_indiv_time_mode_{mode}.csv")
persist_indiv_throughput_df = pd.read_csv(f"{protocol}_indiv_throughput_mode_{mode}.csv")
persist_agg_df = pd.read_csv(f"{protocol}_agg_log_mode_{mode}.csv")

plt.plot(persist_agg_df)
plt.show()
plt.plot(persist_indiv_throughput_df)
plt.show()
plt.plot(persist_indiv_time_df)
plt.show()

print(persist_indiv_time_df)
print(persist_indiv_throughput_df)
print(persist_agg_df)