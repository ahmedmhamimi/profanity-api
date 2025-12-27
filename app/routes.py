from flask import Blueprint, request, jsonify
from .utils import get_custom_wordset, analyze_text, censor_text

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
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
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

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

        if not text:
            return jsonify({"error": "No text provided"}), 400
            
        if len(censor_char) > 1:
             return jsonify({"error": "censor_char must be 1 character"}), 400

        word_set = get_custom_wordset(blacklist, whitelist)
        censored_text = censor_text(text, censor_char, word_set)
        
        bad_word_count = 0
        if text != censored_text:
            bad_word_count = censored_text.count(censor_char * 3)

        return jsonify({
            "original": text,
            "censored": censored_text,
            "bad_word_count_approx": bad_word_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
