import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
import numpy as np

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
lesezeit = grouped_llama3_qwen2_mistral.index.values.reshape(-1, 1)  # Reshape for sklearn

# Function to perform linear regression and plot the result
def plot_linear_regression(lesezeit, similarity, label, color, marker):
    # Drop NaN values from both 'lesezeit' and 'similarity'
    lesezeit_clean, similarity_clean = lesezeit[~np.isnan(similarity)], similarity[~np.isnan(similarity)]
    
    model = LinearRegression()
    model.fit(lesezeit_clean, similarity_clean)
    predicted = model.predict(lesezeit_clean)

    plt.scatter(lesezeit_clean, similarity_clean, label=f'Actual {label}', color=color, marker=marker)
    plt.plot(lesezeit_clean, predicted, label=f'Linear Fit {label}', color=color, linestyle='--')

    # Print the slope and intercept for each model
    print(f'{label} -> Slope: {model.coef_[0]:.4f}, Intercept: {model.intercept_:.4f}')

# Llama3 Similarities
plt.figure(figsize=(12, 6))
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Llama3 Z1'], 'Llama3 Z1', 'blue', 'o')
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Llama3 Z2'], 'Llama3 Z2', 'green', 'o')
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Llama3 Z3'], 'Llama3 Z3', 'orange', 'o')

# Qwen2 Similarities
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Qwen2 Z1'], 'Qwen2 Z1', 'purple', 'x')
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Qwen2 Z2'], 'Qwen2 Z2', 'red', 'x')
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Qwen2 Z3'], 'Qwen2 Z3', 'cyan', 'x')

# Mistral Similarities
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Mistral Z1'], 'Mistral Z1', 'magenta', 's')
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Mistral Z2'], 'Mistral Z2', 'yellow', 's')
plot_linear_regression(lesezeit, grouped_llama3_qwen2_mistral['Similarity Mistral Z3'], 'Mistral Z3', 'brown', 's')

# Adding labels and title
plt.title('Linear Regression of Llama3, Qwen2, and Mistral Similarities vs Lesezeit (in min)')
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

# Save the plot as a file
plt.savefig('llama3_qwen2_mistral_linear_regression_vs_lesezeit.png')

# Clear the plot
plt.clf()
