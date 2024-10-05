import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Use a non-interactive backend to avoid display issues
matplotlib.use('Agg')

# Load the CSV file
output_file = 'output_with_similarities.csv'
df = pd.read_csv(output_file)

# Rename columns for Llama3 similarities
df = df.rename(columns={
    'Similarity Z1': 'Similarity Llama3 Z1',
    'Similarity Z2': 'Similarity Llama3 Z2',
    'Similarity Z3': 'Similarity Llama3 Z3'
})

# Calculate overall averages for Llama3 similarities
avg_llama3_z1 = df['Similarity Llama3 Z1'].mean()
avg_llama3_z2 = df['Similarity Llama3 Z2'].mean()
avg_llama3_z3 = df['Similarity Llama3 Z3'].mean()

# Calculate overall averages for Qwen2 similarities
avg_qwen2_z1 = df['Similarity Qwen2 Z1'].mean()
avg_qwen2_z2 = df['Similarity Qwen2 Z2'].mean()
avg_qwen2_z3 = df['Similarity Qwen2 Z3'].mean()

# Calculate overall averages for Mistral similarities
avg_mistral_z1 = df['Similarity Mistral Z1'].mean()
avg_mistral_z2 = df['Similarity Mistral Z2'].mean()
avg_mistral_z3 = df['Similarity Mistral Z3'].mean()

# Prepare data for the bar plot
averages_llama3 = [avg_llama3_z1, avg_llama3_z2, avg_llama3_z3]
averages_qwen2 = [avg_qwen2_z1, avg_qwen2_z2, avg_qwen2_z3]
averages_mistral = [avg_mistral_z1, avg_mistral_z2, avg_mistral_z3]

# Combine Llama3, Qwen2, and Mistral averages for plotting
columns = ['Llama3 Z1', 'Llama3 Z2', 'Llama3 Z3', 
           'Qwen2 Z1', 'Qwen2 Z2', 'Qwen2 Z3', 
           'Mistral Z1', 'Mistral Z2', 'Mistral Z3']
averages = averages_llama3 + averages_qwen2 + averages_mistral

# Plot the overall averages as a bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(columns, averages, color=['blue', 'green', 'orange', 'purple', 'red', 'cyan', 'magenta', 'yellow', 'brown'])
plt.title('Overall Average Similarity Scores for Llama3, Qwen2, and Mistral')
plt.ylabel('Average Cosine Similarity')
plt.xlabel('Similarity Columns')
plt.ylim(0, 1)
plt.grid(axis='y')

# Annotate the bars with the exact values
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height - 0.05, f'{height:.2f}', ha='center', va='bottom')

# Save the bar plot as a file
plt.savefig('overall_average_llama3_qwen2_mistral_similarity_scores.png')

# Clear the plot
plt.clf()

# Ensure that the 'Lesezeit (in min)' column is numeric
df['Lesezeit (in min)'] = pd.to_numeric(df['Lesezeit (in min)'], errors='coerce')

# Drop rows where 'Lesezeit (in min)' is NaN
df = df.dropna(subset=['Lesezeit (in min)'])

# Group by 'Lesezeit (in min)' and calculate the mean for each Llama3, Qwen2, and Mistral similarity column
grouped_llama3_qwen2_mistral = df.groupby('Lesezeit (in min)')[
    ['Similarity Llama3 Z1', 'Similarity Llama3 Z2', 'Similarity Llama3 Z3',
     'Similarity Qwen2 Z1', 'Similarity Qwen2 Z2', 'Similarity Qwen2 Z3',
     'Similarity Mistral Z1', 'Similarity Mistral Z2', 'Similarity Mistral Z3']].mean()

# Extract the grouped data for each similarity column
lesezeit = grouped_llama3_qwen2_mistral.index

# Llama3 Similarities
similarity_llama3_z1 = grouped_llama3_qwen2_mistral['Similarity Llama3 Z1']
similarity_llama3_z2 = grouped_llama3_qwen2_mistral['Similarity Llama3 Z2']
similarity_llama3_z3 = grouped_llama3_qwen2_mistral['Similarity Llama3 Z3']

# Qwen2 Similarities
similarity_qwen2_z1 = grouped_llama3_qwen2_mistral['Similarity Qwen2 Z1']
similarity_qwen2_z2 = grouped_llama3_qwen2_mistral['Similarity Qwen2 Z2']
similarity_qwen2_z3 = grouped_llama3_qwen2_mistral['Similarity Qwen2 Z3']

# Mistral Similarities
similarity_mistral_z1 = grouped_llama3_qwen2_mistral['Similarity Mistral Z1']
similarity_mistral_z2 = grouped_llama3_qwen2_mistral['Similarity Mistral Z2']
similarity_mistral_z3 = grouped_llama3_qwen2_mistral['Similarity Mistral Z3']

# Plot Llama3, Qwen2, and Mistral similarities against reading time
plt.figure(figsize=(12, 6))

# Plot Llama3 Similarities
plt.plot(lesezeit, similarity_llama3_z1, label='Similarity Llama3 Z1', marker='o', color='blue')
plt.plot(lesezeit, similarity_llama3_z2, label='Similarity Llama3 Z2', marker='o', color='green')
plt.plot(lesezeit, similarity_llama3_z3, label='Similarity Llama3 Z3', marker='o', color='orange')

# Plot Qwen2 Similarities
plt.plot(lesezeit, similarity_qwen2_z1, label='Similarity Qwen2 Z1', marker='x', color='purple', linestyle='--')
plt.plot(lesezeit, similarity_qwen2_z2, label='Similarity Qwen2 Z2', marker='x', color='red', linestyle='--')
plt.plot(lesezeit, similarity_qwen2_z3, label='Similarity Qwen2 Z3', marker='x', color='cyan', linestyle='--')

# Plot Mistral Similarities
plt.plot(lesezeit, similarity_mistral_z1, label='Similarity Mistral Z1', marker='s', color='magenta')
plt.plot(lesezeit, similarity_mistral_z2, label='Similarity Mistral Z2', marker='s', color='yellow')
plt.plot(lesezeit, similarity_mistral_z3, label='Similarity Mistral Z3', marker='s', color='brown')

# Adding labels and title
plt.title('Llama3, Qwen2, and Mistral Similarities vs Lesezeit (in min)')
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

# Save the plot as a file
plt.savefig('llama3_qwen2_mistral_similarities_vs_lesezeit_no_values.png')

# Clear the plot
plt.clf()
