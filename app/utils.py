from better_profanity import profanity
import re

# FIX: Filter out non-string objects to prevent TypeError in better-profanity updates
DEFAULT_PROFANITY_SET = {w for w in profanity.CENSOR_WORDSET if isinstance(w, str)}

def get_custom_wordset(blacklist=None, whitelist=None):
    """
    Combines default set with user inputs safely.
    """
    current_set = DEFAULT_PROFANITY_SET.copy()
    if blacklist:
        current_set.update(set([w.lower() for w in blacklist]))
    if whitelist:
        current_set.difference_update(set([w.lower() for w in whitelist]))
    return current_set

def check_logic(text, custom_set):
    """
    Helper function to check a specific string against library + custom set
    """
    # 1. Use the library's powerful check (handles h3ll0, etc.)
    if profanity.contains_profanity(text):
        return True

    # 2. If the user added NEW bad words (Blacklist), we must check manually
    if custom_set != DEFAULT_PROFANITY_SET:
        words = text.split()
        for word in words:
            # Strip punctuation for manual check
            clean_word = word.lower().strip('.,!?-_')
            if clean_word in custom_set:
                return True
    return False

def analyze_text(text, custom_set):
    """
    Checks for profanity with Evasion Detection (s.h.i.t).
    """
    # 1. Check the raw text
    if check_logic(text, custom_set):
        return True
        
    # 2. Check Evasion Text (The "Pro" Feature)
    # Remove all non-alphanumeric characters except spaces.
    # "s.h.i.t" -> "shit"
    normalized_text = re.sub(r'[^\w\s]', '', text)
    
    if check_logic(normalized_text, custom_set):
        return True
        
    return False

def censor_text(text, censor_char, custom_set):
    """
    Censors the text.
    """
    # Load custom set into library temporarily to handle censoring logic
    profanity.load_censor_words(custom_set)
    censored = profanity.censor(text, censor_char)
    profanity.load_censor_words(DEFAULT_PROFANITY_SET) # Restore default
    return censored
