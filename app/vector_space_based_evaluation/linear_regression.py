import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
import numpy as np

matplotlib.use('Agg')

output_file = 'app/vector_space_based_evaluation/output_with_similarities.csv'
df = pd.read_csv(output_file)

df = df.rename(
    columns={
        'Similarity Z1': 'Similarity Llama3 Z1',
        'Similarity Z2': 'Similarity Llama3 Z2',
        'Similarity Z3': 'Similarity Llama3 Z3',
    }
)

df['Lesezeit (in min)'] = pd.to_numeric(
    df['Lesezeit (in min)'], errors='coerce'
)

df = df.dropna(subset=['Lesezeit (in min)'])

grouped_llama3_qwen2_mistral = df.groupby('Lesezeit (in min)')[
    [
        'Similarity Llama3 Z1',
        'Similarity Llama3 Z2',
        'Similarity Llama3 Z3',
        'Similarity Qwen2 Z1',
        'Similarity Qwen2 Z2',
        'Similarity Qwen2 Z3',
        'Similarity Mistral Z1',
        'Similarity Mistral Z2',
        'Similarity Mistral Z3',
    ]
].mean()

lesezeit = grouped_llama3_qwen2_mistral.index.values.reshape(
    -1, 1
)  # Reshape for sklearn


def plot_linear_regression(lesezeit, similarity, label, color, marker):
    lesezeit_clean, similarity_clean = (
        lesezeit[~np.isnan(similarity)],
        similarity[~np.isnan(similarity)],
    )

    model = LinearRegression()
    model.fit(lesezeit_clean, similarity_clean)
    predicted = model.predict(lesezeit_clean)

    plt.scatter(
        lesezeit_clean,
        similarity_clean,
        label=f'Actual {label}',
        color=color,
        marker=marker,
    )
    plt.plot(
        lesezeit_clean,
        predicted,
        label=f'Linear Fit {label}',
        color=color,
        linestyle='--',
    )

    print(
        f'{label} -> Slope: {model.coef_[0]:.4f}, Intercept: {model.intercept_:.4f}'
    )


plt.figure(figsize=(12, 6))
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Llama3 Z1'],
    'Llama3 Z1',
    'blue',
    'o',
)
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Llama3 Z2'],
    'Llama3 Z2',
    'green',
    'o',
)
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Llama3 Z3'],
    'Llama3 Z3',
    'orange',
    'o',
)

plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Qwen2 Z1'],
    'Qwen2 Z1',
    'purple',
    'x',
)
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Qwen2 Z2'],
    'Qwen2 Z2',
    'red',
    'x',
)
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Qwen2 Z3'],
    'Qwen2 Z3',
    'cyan',
    'x',
)

plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Mistral Z1'],
    'Mistral Z1',
    'magenta',
    's',
)
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Mistral Z2'],
    'Mistral Z2',
    'yellow',
    's',
)
plot_linear_regression(
    lesezeit,
    grouped_llama3_qwen2_mistral['Similarity Mistral Z3'],
    'Mistral Z3',
    'brown',
    's',
)

plt.title(
    'Linear Regression of Llama3, Qwen2, and Mistral Similarities vs Lesezeit (in min)'
)
plt.xlabel('Lesezeit (in min)')
plt.ylabel('Average Cosine Similarity')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()

plt.savefig('app/vector_space_based_evaluation/llama3_qwen2_mistral_linear_regression_vs_lesezeit.png')

plt.clf()
