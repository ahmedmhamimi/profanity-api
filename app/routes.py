from flask import Blueprint, request, jsonify
from .utils import get_custom_wordset, analyze_text, censor_text

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "version": "2.0",
        "endpoints": {
            "POST /check": "Check text for profanity",
            "POST /censor": "Censor profanity in text"
        }
    })

@api.route('/check', methods=['POST'])
def check_profanity():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
             
        text = data.get('text', '')
        blacklist = data.get('blacklist', [])
        whitelist = data.get('whitelist', [])
        
        # Validate text type
        if not isinstance(text, str):
            return jsonify({"error": "Text must be a string"}), 400
        
        # Allow empty string (it's valid - just returns False)
        if text == "":
            return jsonify({
                "is_profane": False,
                "char_count": 0,
                "language_detected": "en"
            })
        
        # Validate lists
        if not isinstance(blacklist, list):
            return jsonify({"error": "Blacklist must be an array"}), 400
        
        if not isinstance(whitelist, list):
            return jsonify({"error": "Whitelist must be an array"}), 400

        word_set = get_custom_wordset(blacklist, whitelist)
        is_profane = analyze_text(text, word_set)
        
        return jsonify({
            "is_profane": is_profane,
            "char_count": len(text),
            "language_detected": "en"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/censor', methods=['POST'])
def censor_profanity():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        text = data.get('text', '')
        censor_char = data.get('censor_char', '*')
        blacklist = data.get('blacklist', [])
        whitelist = data.get('whitelist', [])

        # Validate text type
        if not isinstance(text, str):
            return jsonify({"error": "Text must be a string"}), 400
        
        # Allow empty string (just return as-is)
        if text == "":
            return jsonify({
                "original": "",
                "censored": "",
                "bad_word_count": 0
            })
        
        # Validate censor_char
        if not isinstance(censor_char, str):
            return jsonify({"error": "censor_char must be a string"}), 400
            
        if len(censor_char) != 1:
            return jsonify({"error": "censor_char must be exactly 1 character"}), 400
        
        # Validate lists
        if not isinstance(blacklist, list):
            return jsonify({"error": "Blacklist must be an array"}), 400
        
        if not isinstance(whitelist, list):
            return jsonify({"error": "Whitelist must be an array"}), 400

        word_set = get_custom_wordset(blacklist, whitelist)
        censored_text = censor_text(text, censor_char, word_set)
        
        # Count censored words more accurately
        bad_word_count = 0
        if text != censored_text:
            # Count sequences of censor characters
            import re
            # Find all sequences of 2+ censor characters
            pattern = re.escape(censor_char) + '{2,}'
            bad_word_count = len(re.findall(pattern, censored_text))

        return jsonify({
            "original": text,
            "censored": censored_text,
            "bad_word_count": bad_word_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500