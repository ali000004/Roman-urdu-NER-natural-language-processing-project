import pandas as pd
import pickle
import sys
import os

# --- 1. Define the necessary function (from your main.py) ---

# We need the translateToRoman function which loads the pickled model.
# Since we are running this code block externally, we need to redefine the API function
# and ensure the pickle file is accessible.

def translateToRoman(text):
    """
    API function to load and use the pickled urdu_to_roman model.
    Assumes 'urdu_to_roman.pickle' exists in the current directory.
    """
    try:
        with open("urdu_to_roman.pickle", "rb") as f:
            # Load the pickled urdutoroman function
            model = pickle.load(f)
            return model(text)
    except FileNotFoundError:
        print("Error: 'urdu_to_roman.pickle' not found. Ensure main.py was run to save the model.")
        # Return original text with a flag to indicate error, or raise error
        return "PICKLE_ERROR: " + text
    except Exception as e:
        print(f"Error during deserialization or translation: {e}")
        return "TRANSLATION_ERROR: " + text
    
# --- 2. Function to Process the CSV ---

def reverse_transliterate_csv(input_csv_path: str, output_csv_path: str):
    """
    Loads the CSV, applies the Urdu -> Roman Urdu transliteration (reverse),
    and saves the updated DataFrame to a new CSV file.
    """
    try:
        # Load the CSV file created in the previous step
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_csv_path}")
        return
    except Exception as e:
        print(f"❌ Error loading input CSV: {e}")
        return
    
    print(f"Loaded {len(df)} sentences. Starting Reverse Transliteration (Urdu -> Roman Urdu)...")

    # Apply the translateToRoman function to the 'Urdu_Sentence' column
    # This creates the new Roman Urdu column (your noisy input)
    df['Roman_Urdu_Reversed'] = df['Urdu_Sentence'].apply(translateToRoman)
    
    # Check if there were any errors during translation
    error_count = df['Roman_Urdu_Reversed'].astype(str).str.contains('ERROR').sum()
    if error_count > 0:
        print(f"⚠️ Warning: Found {error_count} rows with translation errors. Check the 'Roman_Urdu_Reversed' column.")

    print("Transliteration complete. Saving new CSV...")

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Successfully saved data with reversed Roman Urdu to {output_csv_path}")

# --- Example Execution ---

INPUT_CSV = 'D:/urduify/urdusent.csv' 
OUTPUT_CSV = 'D:/urduify/mkpucit_with_reversed_ru.csv'

reverse_transliterate_csv(INPUT_CSV, OUTPUT_CSV)