import pandas as pd
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Load SBERT model
model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

# Load the CSV file
csv_file = 'KGK Zusammenfassungen.csv'
df = pd.read_csv(csv_file)

tokenizer = AutoTokenizer.from_pretrained('deepset/gbert-base')

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def truncate_to_token_limit(text, max_tokens=864, punctuation=['.', '!', '?']):
    if not isinstance(text, str):
        return text  # Return if text is not a string
    
    # Tokenize and check token length
    tokens = tokenizer.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    # Decode the tokens up to the maximum limit
    decoded_text = tokenizer.decode(tokens[:max_tokens])
    
    # Find the position of the last punctuation mark within the token limit
    last_punctuation_index = -1
    for punct in punctuation:
        index = decoded_text.rfind(punct)
        if index > last_punctuation_index:
            last_punctuation_index = index

    # Truncate the text at the last punctuation mark
    if last_punctuation_index != -1:
        truncated_text = decoded_text[:last_punctuation_index + 1]
    else:
        truncated_text = decoded_text[:max_tokens]  # Fallback to simple truncation if no punctuation found
    
    return truncated_text

def embed_sentences(sentences):
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/paraphrase-MiniLM-L6-v2')

    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling. In this case, max pooling.
    return mean_pooling(model_output, encoded_input['attention_mask'])

# Function to calculate SBERT-based semantic similarity
def sbert_similarity(str1, str2):
    print(str1)
    print(str2)
    # Check if both inputs are valid strings, else return NaN for similarity
    if isinstance(str1, str) and isinstance(str2, str):
        embedding1 = model.encode(str1, convert_to_tensor=True)
        embedding2 = model.encode(str2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embedding1, embedding2)
        return similarity.item()
    else:
        return np.nan  # Return NaN if either input is not a string

# Calculate similarities and store them in new columns for Llama 3
df['Similarity Llama3 Z1'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Llama 3 Z1']), axis=1)
df['Similarity Llama3 Z2'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Llama3 Z2']), axis=1)
df['Similarity Llama3 Z3'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Llama3 Z3']), axis=1)

# Calculate similarities and store them in new columns for Qwen 2
df['Similarity Qwen2 Z1'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Qwen2 Z1']), axis=1)
df['Similarity Qwen2 Z2'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Qwen2 Z2']), axis=1)
df['Similarity Qwen2 Z3'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Qwen2 Z3']), axis=1)

# Calculate similarities and store them in new columns for Mistral
df['Similarity Mistral Z1'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Mistral Z1']), axis=1)
df['Similarity Mistral Z2'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Mistral Z2']), axis=1)
df['Similarity Mistral Z3'] = df.apply(lambda row: sbert_similarity(row['Zusammenfassung'], row['Mistral Z3']), axis=1)

# Save the updated DataFrame to a new CSV file
output_file = 'output_with_similarities.csv'
df.to_csv(output_file, index=False)

print(f"Similarity scores (including Mistral, Llama3, and Qwen2) saved to {output_file}")
