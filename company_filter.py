import pandas as pd

df = pd.read_csv('company_in.txt', sep='\s+',header=None)
#print(df)
df2 = df[[2,3,6]]
df2.to_csv('company_out.csv', index=False, header=None)
