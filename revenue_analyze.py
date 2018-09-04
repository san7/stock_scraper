import pandas as pd

df = pd.read_csv('revenue.csv', header=None, index_col=0)
df2 = df.astype(float)
print(df2)
print(df2.dtypes.value_counts())

print(df2.index)
print(df2.columns)

print(df2.loc[[1102]])


