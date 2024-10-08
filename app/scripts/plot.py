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

# Calculate the averages of the three Llama3 similarity columns
avg_llama3_z1 = df['Similarity Llama3 Z1'].mean()
avg_llama3_z2 = df['Similarity Llama3 Z2'].mean()
avg_llama3_z3 = df['Similarity Llama3 Z3'].mean()

# Prepare data for plotting Llama3 similarities
averages_llama3 = [avg_llama3_z1, avg_llama3_z2, avg_llama3_z3]
columns_llama3 = ['Similarity Llama3 Z1', 'Similarity Llama3 Z2', 'Similarity Llama3 Z3']

# Plot the averages for Llama3
plt.figure(figsize=(8, 6))
bars_llama3 = plt.bar(columns_llama3, averages_llama3, color=['blue', 'green', 'orange'])
plt.title('Average Llama3 Similarity Scores')
plt.ylabel('Average Cosine Similarity')
plt.xlabel('Columns')
plt.ylim(0, 1)  # Cosine similarity ranges from 0 to 1
plt.grid(axis='y')

# Annotate the bars with the exact values
for bar in bars_llama3:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height - 0.05, f'{height:.2f}', ha='center', va='bottom')

# Save the plot as a file
plt.savefig('average_llama3_similarity_scores_with_values.png')

# Clear the plot
plt.clf()

# Calculate the averages of the three Qwen2 similarity columns
avg_qwen2_z1 = df['Similarity Qwen2 Z1'].mean()
avg_qwen2_z2 = df['Similarity Qwen2 Z2'].mean()
avg_qwen2_z3 = df['Similarity Qwen2 Z3'].mean()

# Prepare data for plotting Qwen2 similarities
averages_qwen2 = [avg_qwen2_z1, avg_qwen2_z2, avg_qwen2_z3]
columns_qwen2 = ['Similarity Qwen2 Z1', 'Similarity Qwen2 Z2', 'Similarity Qwen2 Z3']

# Plot the averages for Qwen2
plt.figure(figsize=(8, 6))
bars_qwen2 = plt.bar(columns_qwen2, averages_qwen2, color=['purple', 'red', 'cyan'])
plt.title('Average Qwen2 Similarity Scores')
plt.ylabel('Average Cosine Similarity')
plt.xlabel('Columns')
plt.ylim(0, 1)  # Cosine similarity ranges from 0 to 1
plt.grid(axis='y')

# Annotate the bars with the exact values
for bar in bars_qwen2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height - 0.05, f'{height:.2f}', ha='center', va='bottom')

# Save the plot as a file
plt.savefig('average_qwen2_similarity_scores_with_values.png')

# Clear the plot
plt.clf()

# Reload the CSV file to ensure clean data processing
df = pd.read_csv(output_file)

# Ensure that the 'Lesezeit (in min)' column is numeric
df['Lesezeit (in min)'] = pd.to_numeric(df['Lesezeit (in min)'], errors='coerce')

# Drop rows where 'Lesezeit (in min)' is NaN
df = df.dropna(subset=['Lesezeit (in min)'])

# Group by 'Lesezeit (in min)' and calculate the mean for each Llama3 similarity column
grouped_llama3 = df.groupby('Lesezeit (in min)')[['Similarity Llama3 Z1', 'Similarity Llama3 Z2', 'Similarity Llama3 Z3']].mean()

# Extract the grouped data for each Llama3 similarity column
lesezeit_llama3 = grouped_llama3.index
similarity_llama3_z1 = grouped_llama3['Similarity Llama3 Z1']
similarity_llama3_z2 = grouped_llama3['Similarity Llama3 Z2']
similarity_llama3_z3 = grouped_llama3['Similarity Llama3 Z3']

# Plot Llama3 similarities against reading time
plt.figure(figsize=(10, 6))

# Plot Similarity Llama3 Z1
plt.plot(lesezeit_llama3, similarity_llama3_z1, label='Similarity Llama3 Z1', marker='o', color='blue')

# Plot Similarity Llama3 Z2
plt.plot(lesezeit_llama3, similarity_llama3_z2, label='Similarity Llama3 Z2', marker='o', color='green')

# Plot Similarity Llama3 Z3
plt.plot(lesezeit_llama3, similarity_llama3_z3, label='Similarity Llama3 Z3', marker='o', color='orange')

# Adding labels and title
plt.title('Llama3 Similarities vs Lesezeit (in min)')
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

# Annotate the plot with the exact values for Llama3
for x, y in zip(lesezeit_llama3, similarity_llama3_z1):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='blue')
for x, y in zip(lesezeit_llama3, similarity_llama3_z2):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='green')
for x, y in zip(lesezeit_llama3, similarity_llama3_z3):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='orange')

# Save the plot as a file
plt.savefig('llama3_similarities_vs_lesezeit_with_values.png')

# Clear the plot
plt.clf()

# Group by 'Lesezeit (in min)' and calculate the mean for each Qwen2 similarity column
grouped_qwen2 = df.groupby('Lesezeit (in min)')[['Similarity Qwen2 Z1', 'Similarity Qwen2 Z2', 'Similarity Qwen2 Z3']].mean()

# Extract the grouped data for each Qwen2 similarity column
lesezeit_qwen2 = grouped_qwen2.index
similarity_qwen2_z1 = grouped_qwen2['Similarity Qwen2 Z1']
similarity_qwen2_z2 = grouped_qwen2['Similarity Qwen2 Z2']
similarity_qwen2_z3 = grouped_qwen2['Similarity Qwen2 Z3']

# Plot Qwen2 similarities against reading time
plt.figure(figsize=(10, 6))

# Plot Similarity Qwen2 Z1
plt.plot(lesezeit_qwen2, similarity_qwen2_z1, label='Similarity Qwen2 Z1', marker='o', color='purple')

# Plot Similarity Qwen2 Z2
plt.plot(lesezeit_qwen2, similarity_qwen2_z2, label='Similarity Qwen2 Z2', marker='o', color='red')

# Plot Similarity Qwen2 Z3
plt.plot(lesezeit_qwen2, similarity_qwen2_z3, label='Similarity Qwen2 Z3', marker='o', color='cyan')

# Adding labels and title
plt.title('Qwen2 Similarities vs Lesezeit (in min)')
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

# Annotate the plot with the exact values for Qwen2
for x, y in zip(lesezeit_qwen2, similarity_qwen2_z1):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='purple')
for x, y in zip(lesezeit_qwen2, similarity_qwen2_z2):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='red')
for x, y in zip(lesezeit_qwen2, similarity_qwen2_z3):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='cyan')

# Save the plot as a file
plt.savefig('qwen2_similarities_vs_lesezeit_with_values.png')

# Clear the plot
plt.clf()

# Calculate the averages of the three Mistral similarity columns
avg_mistral_z1 = df['Similarity Mistral Z1'].mean()
avg_mistral_z2 = df['Similarity Mistral Z2'].mean()
avg_mistral_z3 = df['Similarity Mistral Z3'].mean()

# Prepare data for plotting Mistral similarities
averages_mistral = [avg_mistral_z1, avg_mistral_z2, avg_mistral_z3]
columns_mistral = ['Similarity Mistral Z1', 'Similarity Mistral Z2', 'Similarity Mistral Z3']

# Plot the averages for Mistral
plt.figure(figsize=(8, 6))
bars_mistral = plt.bar(columns_mistral, averages_mistral, color=['brown', 'pink', 'yellow'])
plt.title('Average Mistral Similarity Scores')
plt.ylabel('Average Cosine Similarity')
plt.xlabel('Columns')
plt.ylim(0, 1)  # Cosine similarity ranges from 0 to 1
plt.grid(axis='y')

# Annotate the bars with the exact values
for bar in bars_mistral:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height - 0.05, f'{height:.2f}', ha='center', va='bottom')

# Save the plot as a file
plt.savefig('average_mistral_similarity_scores_with_values.png')

# Clear the plot
plt.clf()

# Group by 'Lesezeit (in min)' and calculate the mean for each Mistral similarity column
grouped_mistral = df.groupby('Lesezeit (in min)')[['Similarity Mistral Z1', 'Similarity Mistral Z2', 'Similarity Mistral Z3']].mean()

# Extract the grouped data for each Mistral similarity column
lesezeit_mistral = grouped_mistral.index
similarity_mistral_z1 = grouped_mistral['Similarity Mistral Z1']
similarity_mistral_z2 = grouped_mistral['Similarity Mistral Z2']
similarity_mistral_z3 = grouped_mistral['Similarity Mistral Z3']

# Plot Mistral similarities against reading time
plt.figure(figsize=(10, 6))

# Plot Similarity Mistral Z1
plt.plot(lesezeit_mistral, similarity_mistral_z1, label='Similarity Mistral Z1', marker='o', color='brown')

# Plot Similarity Mistral Z2
plt.plot(lesezeit_mistral, similarity_mistral_z2, label='Similarity Mistral Z2', marker='o', color='pink')

# Plot Similarity Mistral Z3
plt.plot(lesezeit_mistral, similarity_mistral_z3, label='Similarity Mistral Z3', marker='o', color='yellow')

# Adding labels and title
plt.title('Mistral Similarities vs Lesezeit (in min)')
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

# Annotate the plot with the exact values for Mistral
for x, y in zip(lesezeit_mistral, similarity_mistral_z1):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='brown')
for x, y in zip(lesezeit_mistral, similarity_mistral_z2):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='pink')
for x, y in zip(lesezeit_mistral, similarity_mistral_z3):
    plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color='yellow')

# Save the plot as a file
plt.savefig('mistral_similarities_vs_lesezeit_with_values.png')

# Clear the plot
plt.clf()

