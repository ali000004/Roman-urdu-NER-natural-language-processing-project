import sys
sys.setrecursionlimit(5000) 
from main import translateToRoman, translateToUrdu
import pandas as pd
import pickle
import os
from typing import List, Dict

global row_counter
row_counter = 0
total_rows = 0

def apply_and_track_transliteration(text_input):
    """Applies Roman_to_urdu to a single input, prints the sentence, and updates progress."""
    global row_counter, total_rows

    row_counter += 1

    if row_counter % 100 == 0 or row_counter < 10: 
        percentage = (row_counter / total_rows) * 100 if total_rows > 0 else 0
        print(f"[{row_counter:,}/{total_rows:,} | {percentage:.1f}%] Processing: {text_input}")

    result = translateToUrdu(text_input) 
    
    return result


def run_forward_transliteration(input_csv_path: str, output_csv_path: str):
    """
    Loads the CSV, applies forward transliteration with progress tracking, and saves.
    """
    global total_rows, row_counter
    
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_csv_path}")
        return
    except Exception as e:
        print(f"❌ Error loading input CSV: {e}")
        return

    row_counter = 0
    total_rows = len(df)
    
    print(f"Loaded {total_rows:,} rows. Starting Final Forward Transliteration...")

    print("\nStarting Baseline Transliteration (Noisy Input)...")

    df['Urdu_Trans_Baseline'] = df['Roman_Urdu_Reversed'].apply(apply_and_track_transliteration)
    

    row_counter = 0
    

    print("\nStarting Optimized Transliteration (Clean Input)...")
    df['Urdu_Trans_Optimized'] = df['Roman_Urdu_Normalized'].apply(apply_and_track_transliteration)
    
    print("\nForward Transliteration complete. Saving final CSV...")

    final_df = df[['Sentence_ID', 'Urdu_Sentence', 'Ground_Truth_Tags', 
                   'Urdu_Trans_Baseline', 'Urdu_Trans_Optimized']]
    
    final_df.to_csv(output_csv_path, index=False, encoding='utf-8')
    
    print(f"✅ FINAL PRE-PROCESSING STEP COMPLETE. Data prepared and saved to {output_csv_path}")


INPUT_CSV_AFTER_NORM = 'D:/urduify/mkpucit_with_normalized_ru.csv'
OUTPUT_CSV_FINAL_NER_INPUT = 'D:/urduify/mkpucit_final_ner_input.csv'

run_forward_transliteration(INPUT_CSV_AFTER_NORM, OUTPUT_CSV_FINAL_NER_INPUT)