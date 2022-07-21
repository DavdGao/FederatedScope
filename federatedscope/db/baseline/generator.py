import pandas as pd
import numpy as np

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'HI', 'MA', 'MI', 'MN', 'NY', 'WA']

oss = ['Win', 'iOS', 'Android']


part_size = [5000, 3000, 4000]

record_num = sum(part_size)

rows = []
for i in range(record_num):
  id = i
  activatetime = np.random.rand() * 4 + 1.0
  purchase = np.random.randint(80, 120)
  age = np.random.randint(17, 81)
  salary = np.random.randint(5, 10) * 10
  state = np.random.choice(states)
  os = np.random.choice(oss)
  rows.append([id, activatetime, purchase, age, salary, state, os])

df = pd.DataFrame(rows, columns=['id', 'activatetime', 'purchase', 'age', 'salary', 'state', 'os'])

df.to_csv('dataset/dataset.csv', index=False, float_format="%.2f")

df[['id', 'activatetime', 'purchase']].to_csv('dataset/server.csv', index=False, float_format="%.2f")

base = 0
top = 0
cid = 0
for part in part_size:
  top += part
  cid += 1
  df[['id', 'age', 'salary', 'state', 'os']].iloc[base:top].to_csv('dataset/client%d.csv' % cid, index=False, float_format="%.2f")