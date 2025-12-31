import pandas as pd
from nltk.tokenize import word_tokenize
from typing import Dict

# --- Configuration ---
INPUT_CSV_PATH = 'D:/urduify/mkpucit_with_reversed_ru.csv'
OUTPUT_MAP_FILE = 'D:/urduify/new_phonetic_mappings.txt' 
MIN_TOKEN_LENGTH = 2 # Exclude single-character tokens to reduce noise

def generate_new_mapping_pairs(df: pd.DataFrame) -> Dict[str, str]:
    new_map_candidates: Dict[str, str] = {}
    
    for index, row in df.iterrows():
        try:

            target_urdu_tokens = str(row['Urdu_Sentence']).split() 
            noisy_roman_tokens = str(row['Roman_Urdu_Reversed']).lower().split()

            if len(target_urdu_tokens) == len(noisy_roman_tokens):
                for ru_token, urdu_token in zip(noisy_roman_tokens, target_urdu_tokens):

                    if len(ru_token) >= MIN_TOKEN_LENGTH and len(urdu_token) >= MIN_TOKEN_LENGTH:
        
                        new_map_candidates[ru_token] = urdu_token
                        
        except Exception as e:
            continue
            
    return new_map_candidates

def save_map_to_file(mapping: Dict[str, str], filename: str):
    """Saves the generated dictionary to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for ru, urdu in mapping.items():
            f.write(f'"{ru}":"{urdu}",\n')

# --- Execution ---
print("🚀 Starting generation of new phonetic mappings...")

try:
    df = pd.read_csv(INPUT_CSV_PATH)
except FileNotFoundError:
    print(f"❌ Error: Input file not found at {INPUT_CSV_PATH}. Please check the path.")
    exit()

new_mappings = generate_new_mapping_pairs(df)

if new_mappings:
    save_map_to_file(new_mappings, OUTPUT_MAP_FILE)
    print(f"✅ Success! Generated {len(new_mappings):,} new mappings.")
    print(f"The new mappings are saved in {OUTPUT_MAP_FILE}")
else:
    print("⚠️ Warning: No new mapping pairs were generated.")