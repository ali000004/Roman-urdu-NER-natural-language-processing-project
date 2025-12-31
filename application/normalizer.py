import pandas as pd
import re
import os
import ast
from typing import Dict

# --- Configuration for Data-Driven Map ---
PHONETIC_MAPPING_FILE = 'D:/nlp_proj/new_phonetic_mappings.txt' 

FINAL_NORMALIZATION_MAP: Dict[str, str] = {
    # --- LOCATIONS (LOC) ---
    'laehor': 'lahore', 'zfr': 'zafar', 'aslam aabad': 'islamabad', 
    'krachi': 'karachi', 'behaolpor': 'bhawalpur', 'faysl aabad': 'faisalabad', 
    'fisl aabad': 'faisalabad', 'pakptn': 'pakpatan', 'lndn': 'london', 
    'miri lindd': 'maryland', 'bnkak': 'bangkok', 'nioiark': 'new york', 
    'jkarteh': 'jakarta', 'astnbol': 'istanbul', 'mltan': 'multan', 
    'raiay ondd': 'raiwand', 'astak ehom': 'stockholm', 'bilfast': 'belfast', 
    'aairlindd': 'ireland', 'mmbii': 'mumbai', 'bhart': 'bharat', 'soat': 'swat', 
    'aiddnbrg': 'edinburgh', 'jdeh': 'jeddah', 'raol pnddi': 'rawalpindi', 
    'lnka': 'lanka', 'joehans brg': 'johannesburg', 'pshaor': 'peshawar', 
    'ozirstan': 'waziristan', 'khir por': 'khairpur', 'oshington': 'washington', 
    'msr': 'misr', 'oraq': 'iraq', 'oran': 'iran', 'saehioal': 'sahiwal', 
    'las ainjls': 'los angeles', 'nii dehli': 'new delhi', 'larrkaneh': 'larkana', 
    'misachosts': 'massachusetts', 'chin': 'china', 'kinidda': 'canada', 
    'sddni': 'sydney', 'gojranoaleh': 'gujranwala', 'anglindd': 'england', 
    'oilz': 'wales', 'brln': 'berlin', 'jrmni': 'germany', 'jnioa': 'geneva', 
    'zmbaboay': 'zimbabwe', 'mianoali': 'mianwali', 'khibr pkhtonkhoa': 'khyber pakhtunkhwa', 
    'rhim iar khan': 'rahim yar khan',
    
    # --- PEOPLE (PER) ---
    'zafar': 'zfr', 'oshrt': 'ishrat', 'ohid': 'waheed', 'nawaz sharif':'noazshrif', 
    'aasf': 'asif', 'ozir': 'wazir', 'ainddrsn': 'anderson', 'obdaloziz': 'abdulaziz', 
    'hidr': 'haider', 'kptan': 'kaptan', 'msbah': 'misbah', 'hsin': 'hussain', 
    'mzehr': 'mazhar', 'skndr': 'sikandar', 'sltan': 'sultan', 'mstfi': 'mustafa', 
    'choehdri': 'chowdhry', 'mhmd': 'muhammad', 'sror': 'sarwar', 'olameh': 'alama', 
    'oehab': 'wahab', 'eholddr': 'holder', 'oasa': 'vasa', 
    
    # --- ORGANIZATIONS/NATIONAL (ORG) ---
    'pakstan': 'pakistan', 'soodi': 'saudi', 'sikiorti': 'security', 'sndh': 'sindh', 
    'blochistan': 'balochistan', 'oraqi': 'iraqi', 'anjmn aslamieh': 'anjuman islamiah', 
    'sprim': 'supreme', 'larddz': 'lords', 'almnsor': 'al mansoor', 'mnsor': 'mansoor', 
    'krkt': 'cricket', 'nishnl': 'national', 'akkidmi': 'academy', 'asmbli': 'assembly', 
    'piplz': 'peoples', 'parti': 'party', 'mslm lig': 'muslim league', 'mslm': 'muslim', 
    'lig': 'league', 'polis': 'police', 'jmaot': 'jamat', 'jnobi': 'janubi', 
    'afriqe': 'africa', 'alqaodeh': 'alqaida', 'jnrl': 'general' , 'khi': 'karachi', 'lhr' : 'lahore'
    , 'usa' : 'america',

    
    # --- COMMON/MISC ---
    'aleh': 'allah', 'min': 'mein', 'oala': 'wala', 'aor': 'aur', 'oay': 'way', 
    'andds': 'indus', 'sharo': 'shahrah', 'fisl': 'faisal', 'sahi': 'sahi', 
    'oid': 'eid', 'u': 'aap', 'ap': 'aap', 'mjy': 'mujhe', 'boht': 'bohat', 
    'kese': 'kaise', 'thnx': 'thanks', 'nyc': 'nice', 'acha': 'acha', 'aj': 'aaj', 
    'sb': 'sab', 'pkstan': 'pakistan', 'govt': 'government', 'pm': 'prime minister',
    'cm': 'chief minister', 'pti': 'pti', 'pmln': 'pmln', 'ppp': 'ppp', 'usa': 'usa',
    'oziraozm': 'wazireazam', 'oina': 'vina', 'sint': 'saint'
}


def load_phonetic_map(filename: str) -> Dict[str, str]:
    new_map = {}
    if not os.path.exists(filename):
        print(f"⚠️ Warning: Phonetic mapping file '{filename}' not found. Skipping dynamic loading.")
        return new_map
        
    print(f"Loading and merging mappings from {filename}...")
    try:
        # Use simple string parsing instead of complex JSON/ast.literal_eval for robustness
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                # Expects a line format like: "ru_word":"urdu_word",
                line = line.strip().strip(',') 
                if not line:
                    continue

                # Find the colon separator
                if ':' in line:
                    parts = line.split(':', 1)
                    # Clean the keys and values by removing quotes
                    ru_token = parts[0].strip().strip('"').strip("'")
                    urdu_token = parts[1].strip().strip('"').strip("'")
                    
                    if ru_token and urdu_token:
                        # Use lowercase Roman Urdu as the key
                        new_map[ru_token.lower()] = urdu_token

    except Exception as e:
        print(f"❌ Error reading phonetic map file {filename}: {e}")
        return {}

    return new_map

# Load the dynamic map once at the module level
DYNAMIC_PHONETIC_MAP = load_phonetic_map(PHONETIC_MAPPING_FILE)

FINAL_NORMALIZATION_MAP = {**FINAL_NORMALIZATION_MAP, **DYNAMIC_PHONETIC_MAP}

print(f"Total entries in combined normalization map: {len(FINAL_NORMALIZATION_MAP):,}")
print("---")


# ---  Normalization Logic Function ---

def normalize_roman_urdu(text: str, normalization_map: Dict[str, str]) -> str:
    """Applies structural cleaning and lexical mapping to standardize Roman Urdu text."""
    if not isinstance(text, str):
        return str(text) 
    
    # Structural Cleaning
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    # Collapse repetitions (e.g., 'acha' -> 'achha')
    text = re.sub(r'(.)\1{2,}', r'\1\1', text) 

    # Lexical Mapping
    tokens = text.split()
    normalized_tokens = []
    
    for token in tokens:
        # Check the combined map (Static + Dynamic)
        normalized_token = normalization_map.get(token, token)
        normalized_tokens.append(normalized_token)
        
    return ' '.join(normalized_tokens)

# ---  Execution Function ---

def run_normalization_only(input_csv_path: str, output_csv_path: str):
    """
    Loads the CSV, applies the *combined* normalization to 
    'Roman_Urdu_Reversed', and saves the new CSV with the 'Roman_Urdu_Normalized' column.
    """
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_csv_path}")
        return
    except Exception as e:
        print(f"❌ Error loading input CSV: {e}")
        return
    
    print(f"Loaded {len(df)} rows. Starting Combined Normalization...")

    # Apply the normalization function using the large, combined map
    # Note: We pass the global FINAL_NORMALIZATION_MAP which now holds ALL rules
    df['Roman_Urdu_Normalized'] = df['Roman_Urdu_Reversed'].apply(
        lambda x: normalize_roman_urdu(x, FINAL_NORMALIZATION_MAP)
    )
    
    print("Normalization complete. Saving new CSV...")

    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Normalization Complete. Data saved to {output_csv_path}")

INPUT_CSV_AFTER_REVERSE = 'D:/nlp_proj/mkpucit_with_reversed_ru.csv'
OUTPUT_CSV_FINAL_PREP = 'D:/nlp_proj/mkpucit_with_normalized_ru.csv'

run_normalization_only(INPUT_CSV_AFTER_REVERSE, OUTPUT_CSV_FINAL_PREP)