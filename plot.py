import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('day.csv')

balance = df['balance'].iloc[0]
used_tokens = df['used_tokens'].iloc[0]

percentages = [balance, used_tokens]
labels = ['Balance', 'Used Tokens']

plt.figure(figsize=(8, 6))
plt.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightgreen'])
plt.axis('equal')
plt.title('Distribution of Balance and Used Tokens')
plt.show()
