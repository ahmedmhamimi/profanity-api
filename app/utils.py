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

def check_logic(text, custom_set):
    """
    Checks if a string matches the library OR the custom set
    """
    # 1. Library check (fast)
    if profanity.contains_profanity(text):
        return True
    
    # 2. Custom set check (manual)
    if custom_set != DEFAULT_PROFANITY_SET:
        # Check exact word
        if text.lower() in custom_set:
            return True
    return False

def analyze_text(text, custom_set):
    # 1. Check raw
    if check_logic(text, custom_set):
        return True
    # 2. Check normalized (evasion detection)
    normalized = re.sub(r'[^\w]', '', text)
    if check_logic(normalized, custom_set):
        return True
    return False

def censor_text(text, censor_char, custom_set):
    """
    Smart Censor: Handles both standard profanity AND evasion attempts.
    """
    # 1. Run the standard library censor first (Best for phrases)
    profanity.load_censor_words(custom_set)
    first_pass = profanity.censor(text, censor_char)
    profanity.load_censor_words(DEFAULT_PROFANITY_SET)
    
    # 2. Run our "Smart Pass" word by word to catch s.h.i.t / sh!t
    # We split by whitespace to process individual tokens
    words = first_pass.split()
    final_words = []
    
    for word in words:
        # If it's already censored by step 1 (****), skip logic
        if set(word) == set(censor_char):
            final_words.append(word)
            continue
            
        # Normalize: "sh!t" -> "shit", "s.h.i.t" -> "shit"
        # We strip everything that isn't a letter/number
        normalized = re.sub(r'[^\w]', '', word)
        
        # Check if the normalized version is bad
        # We use check_logic but we need to ensure we don't flag empty strings
        is_bad = False
        if normalized:
             is_bad = check_logic(normalized, custom_set)
        
        if is_bad:
            # Replace with censor chars matching original length
            final_words.append(censor_char * len(word))
        else:
            final_words.append(word)
            
    # Reconstruct the sentence
    return " ".join(final_words)