import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

output_file = 'output_with_similarities.csv'
df = pd.read_csv(output_file)

df = df.rename(columns={
    'Similarity Z1': 'Similarity Llama3 Z1',
    'Similarity Z2': 'Similarity Llama3 Z2',
    'Similarity Z3': 'Similarity Llama3 Z3'
})

avg_llama3_z1 = df['Similarity Llama3 Z1'].mean()
avg_llama3_z2 = df['Similarity Llama3 Z2'].mean()
avg_llama3_z3 = df['Similarity Llama3 Z3'].mean()

avg_qwen2_z1 = df['Similarity Qwen2 Z1'].mean()
avg_qwen2_z2 = df['Similarity Qwen2 Z2'].mean()
avg_qwen2_z3 = df['Similarity Qwen2 Z3'].mean()

avg_mistral_z1 = df['Similarity Mistral Z1'].mean()
avg_mistral_z2 = df['Similarity Mistral Z2'].mean()
avg_mistral_z3 = df['Similarity Mistral Z3'].mean()

averages_llama3 = [avg_llama3_z1, avg_llama3_z2, avg_llama3_z3]
averages_qwen2 = [avg_qwen2_z1, avg_qwen2_z2, avg_qwen2_z3]
averages_mistral = [avg_mistral_z1, avg_mistral_z2, avg_mistral_z3]

columns = ['Llama3 Z1', 'Llama3 Z2', 'Llama3 Z3', 
           'Qwen2 Z1', 'Qwen2 Z2', 'Qwen2 Z3', 
           'Mistral Z1', 'Mistral Z2', 'Mistral Z3']
averages = averages_llama3 + averages_qwen2 + averages_mistral

plt.figure(figsize=(12, 6))
bars = plt.bar(columns, averages, color=['blue', 'green', 'orange', 'purple', 'red', 'cyan', 'magenta', 'yellow', 'brown'])
plt.title('Overall Average Similarity Scores for Llama3, Qwen2, and Mistral')
plt.ylabel('Average Cosine Similarity')
plt.xlabel('Similarity Columns')
plt.ylim(0, 1)
plt.grid(axis='y')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height - 0.05, f'{height:.2f}', ha='center', va='bottom')

plt.savefig('overall_average_llama3_qwen2_mistral_similarity_scores.png')

plt.clf()

df['Lesezeit (in min)'] = pd.to_numeric(df['Lesezeit (in min)'], errors='coerce')

df = df.dropna(subset=['Lesezeit (in min)'])

grouped_llama3_qwen2_mistral = df.groupby('Lesezeit (in min)')[
    ['Similarity Llama3 Z1', 'Similarity Llama3 Z2', 'Similarity Llama3 Z3',
     'Similarity Qwen2 Z1', 'Similarity Qwen2 Z2', 'Similarity Qwen2 Z3',
     'Similarity Mistral Z1', 'Similarity Mistral Z2', 'Similarity Mistral Z3']].mean()

lesezeit = grouped_llama3_qwen2_mistral.index

similarity_llama3_z1 = grouped_llama3_qwen2_mistral['Similarity Llama3 Z1']
similarity_llama3_z2 = grouped_llama3_qwen2_mistral['Similarity Llama3 Z2']
similarity_llama3_z3 = grouped_llama3_qwen2_mistral['Similarity Llama3 Z3']

similarity_qwen2_z1 = grouped_llama3_qwen2_mistral['Similarity Qwen2 Z1']
similarity_qwen2_z2 = grouped_llama3_qwen2_mistral['Similarity Qwen2 Z2']
similarity_qwen2_z3 = grouped_llama3_qwen2_mistral['Similarity Qwen2 Z3']

similarity_mistral_z1 = grouped_llama3_qwen2_mistral['Similarity Mistral Z1']
similarity_mistral_z2 = grouped_llama3_qwen2_mistral['Similarity Mistral Z2']
similarity_mistral_z3 = grouped_llama3_qwen2_mistral['Similarity Mistral Z3']

plt.figure(figsize=(12, 6))

plt.plot(lesezeit, similarity_llama3_z1, label='Similarity Llama3 Z1', marker='o', color='blue')
plt.plot(lesezeit, similarity_llama3_z2, label='Similarity Llama3 Z2', marker='o', color='green')
plt.plot(lesezeit, similarity_llama3_z3, label='Similarity Llama3 Z3', marker='o', color='orange')

plt.plot(lesezeit, similarity_qwen2_z1, label='Similarity Qwen2 Z1', marker='x', color='purple', linestyle='--')
plt.plot(lesezeit, similarity_qwen2_z2, label='Similarity Qwen2 Z2', marker='x', color='red', linestyle='--')
plt.plot(lesezeit, similarity_qwen2_z3, label='Similarity Qwen2 Z3', marker='x', color='cyan', linestyle='--')

plt.plot(lesezeit, similarity_mistral_z1, label='Similarity Mistral Z1', marker='s', color='magenta')
plt.plot(lesezeit, similarity_mistral_z2, label='Similarity Mistral Z2', marker='s', color='yellow')
plt.plot(lesezeit, similarity_mistral_z3, label='Similarity Mistral Z3', marker='s', color='brown')

plt.title('Llama3, Qwen2, and Mistral Similarities vs Lesezeit (in min)')
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

plt.savefig('llama3_qwen2_mistral_similarities_vs_lesezeit_no_values.png')

plt.clf()
