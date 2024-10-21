import pandas as pd
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Load SBERT model
model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

csv_file = 'KGK Zusammenfassungen.csv'
df = pd.read_csv(csv_file)

tokenizer = AutoTokenizer.from_pretrained('deepset/gbert-base')

# Function to calculate SBERT-based semantic similarity
def sbert_similarity(str1, str2):
    print(str1)
    print(str2)
    if isinstance(str1, str) and isinstance(str2, str):
        embedding1 = model.encode(str1, convert_to_tensor=True)
        embedding2 = model.encode(str2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embedding1, embedding2)
        return similarity.item()
    else:
        return np.nan  # Return NaN if either input is not a string

df['Similarity Llama3 Z1'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Llama 3 Z1']), axis=1)
df['Similarity Llama3 Z2'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Llama3 Z2']), axis=1)
df['Similarity Llama3 Z3'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Llama3 Z3']), axis=1)

df['Similarity Qwen2 Z1'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Qwen2 Z1']), axis=1)
df['Similarity Qwen2 Z2'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Qwen2 Z2']), axis=1)
df['Similarity Qwen2 Z3'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Qwen2 Z3']), axis=1)

df['Similarity Mistral Z1'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Mistral Z1']), axis=1)
df['Similarity Mistral Z2'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Mistral Z2']), axis=1)
df['Similarity Mistral Z3'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Mistral Z3']), axis=1)

output_file = 'output_with_similarities.csv'
df.to_csv(output_file, index=False)

print(f"Similarity scores (including Mistral, Llama3, and Qwen2) saved to {output_file}")
