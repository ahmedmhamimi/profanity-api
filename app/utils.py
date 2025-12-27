from better_profanity import profanity
import re

# FIX: Filter out non-string objects
DEFAULT_PROFANITY_SET = {w for w in profanity.CENSOR_WORDSET if isinstance(w, str)}

def get_custom_wordset(blacklist=None, whitelist=None):
    current_set = DEFAULT_PROFANITY_SET.copy()
    if blacklist:
        current_set.update(set([w.lower() for w in blacklist]))
    if whitelist:
        current_set.difference_update(set([w.lower() for w in whitelist]))
    return current_set

def is_word_dirty(word, custom_set):
    """
    Checks a single word against the set using two methods:
    1. Direct match (Fast)
    2. Normalized match (remove dots/symbols)
    """
    word_lower = word.lower()
    
    # Check 1: Exact match
    if word_lower in custom_set:
        return True
        
    # Check 2: Evasion match (s.h.i.t -> shit)
    # Remove anything that isn't a letter or number
    clean = re.sub(r'[^\w]', '', word_lower)
    if clean in custom_set:
        return True
        
    # Check 3: Library Check (catches l33t speak like h3ll0)
    # We only check this if the user didn't modify the set, for performance
    if custom_set == DEFAULT_PROFANITY_SET:
        return profanity.contains_profanity(word)
        
    return False

def analyze_text(text, custom_set):
    # 1. Check raw text using library (handles sentences well)
    profanity.load_censor_words(custom_set)
    if profanity.contains_profanity(text):
        profanity.load_censor_words(DEFAULT_PROFANITY_SET)
        return True
    profanity.load_censor_words(DEFAULT_PROFANITY_SET)

    # 2. Check Evasion Text (Fix: Keep Spaces!)
    # "This is s.h.i.t" -> "This is shit"
    normalized_text = re.sub(r'[^\w\s]', '', text)
    
    profanity.load_censor_words(custom_set)
    if profanity.contains_profanity(normalized_text):
        profanity.load_censor_words(DEFAULT_PROFANITY_SET)
        return True
    profanity.load_censor_words(DEFAULT_PROFANITY_SET)
        
    return False

def censor_text(text, censor_char, custom_set):
    """
    Smart Censor: Tokenizes text to catch evasion word-by-word.
    """
    # We split by space to handle the sentence word by word
    words = text.split()
    final_words = []
    
    for word in words:
        # Check if this specific word is dirty
        if is_word_dirty(word, custom_set):
            final_words.append(censor_char * len(word))
        else:
            final_words.append(word)
            
    return " ".join(final_words)