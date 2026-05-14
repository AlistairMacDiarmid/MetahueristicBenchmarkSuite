import pandas as pd

#load the csv
df = pd.read_csv("../results/tsp_results.csv")
print(df)

#group stats
summary = df.groupby("algorithm").agg({
    "best_cost": ["mean", "std", "min", "max"],
    "runtime_seconds": ["mean", "std"]
})

print("summary stats:")
print(summary)

