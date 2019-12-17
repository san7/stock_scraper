import pandas as pd

df = pd.read_csv('shareholder.csv', header=None, index_col=0)
df2 = df.astype(float)
#print(df2)

pd.set_option('display.max_columns',200)

selectedList = df2[(df2[1] > df2[2])].index.tolist()
print(selectedList)
