from better_profanity import profanity
import re

# Initialize the profanity library
profanity.load_censor_words()

# Filter out non-string objects from the default set
try:
    DEFAULT_PROFANITY_SET = {w for w in profanity.CENSOR_WORDSET if isinstance(w, str)}
except:
    DEFAULT_PROFANITY_SET = set()

# Ensure common profanities are included (fallback)
COMMON_PROFANITIES = {
    'shit', 'fuck', 'damn', 'hell', 'ass', 'bitch', 'bastard', 
    'crap', 'piss', 'cock', 'dick', 'pussy', 'cunt', 'whore', 'slut'
}
DEFAULT_PROFANITY_SET.update(COMMON_PROFANITIES)


def get_custom_wordset(blacklist=None, whitelist=None):
    """Create a custom profanity wordset based on blacklist/whitelist"""
    current_set = DEFAULT_PROFANITY_SET.copy()
    
    if blacklist:
        for w in blacklist:
            if w:
                current_set.add(str(w).lower())
    
    if whitelist:
        for w in whitelist:
            if w:
                current_set.discard(str(w).lower())
    
    return current_set


def apply_leet_conversion(text):
    """Convert l33t speak to normal letters"""
    leet_map = {
        '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's',
        '7': 't', '8': 'b', '@': 'a', '$': 's', '!': 'i', '+': 't',
    }
    result = text.lower()
    for leet, normal in leet_map.items():
        result = result.replace(leet, normal)
    return result


def strip_to_alpha(text):
    """Remove ALL non-alphabetic characters (including underscores, numbers)"""
    return re.sub(r'[^a-z]', '', text.lower())


def is_word_profane(word, custom_set):
    """
    Comprehensive profanity check for a single word
    """
    if not word or not isinstance(word, str):
        return False
    
    word_lower = word.lower()
    
    # Check 1: Direct match (fast path)
    if word_lower in custom_set:
        return True
    
    # Check 2: Strip to alpha only (catches s.h.i.t, s-h-i-t, s_h_i_t)
    # Using [^a-z] instead of [^\w] to also remove underscores!
    alpha_only = strip_to_alpha(word_lower)
    if alpha_only and alpha_only in custom_set:
        return True
    
    # Check 3: Convert l33t speak first, then strip
    # sh!t -> shit, $hit -> shit, @ss -> ass
    leet_converted = apply_leet_conversion(word_lower)
    leet_alpha = strip_to_alpha(leet_converted)
    if leet_alpha and leet_alpha in custom_set:
        return True
    
    return False


def analyze_text(text, custom_set):
    """
    Analyze if text contains profanity
    Returns True if any profanity is detected, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    
    # Check each word individually using word boundaries
    words = re.findall(r'\S+', text)
    for word in words:
        if is_word_profane(word, custom_set):
            return True
    
    return False


def censor_text(text, censor_char, custom_set):
    """
    Censor profanity while preserving text structure
    """
    if not text or not isinstance(text, str):
        return text
    
    result = text
    replacements = []
    
    # Find all words (non-whitespace sequences)
    for match in re.finditer(r'\S+', text):
        word = match.group()
        start = match.start()
        end = match.end()
        
        if is_word_profane(word, custom_set):
            censored_word = censor_char * len(word)
            replacements.append((start, end, censored_word))
    
    # Apply replacements in reverse order to maintain positions
    for start, end, replacement in reversed(replacements):
        result = result[:start] + replacement + result[end:]
    
    return result