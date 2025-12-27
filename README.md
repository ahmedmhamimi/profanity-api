# Advanced Profanity Filter & Censor API

A production-ready Flask API designed to detect and censor profanity with high accuracy. It goes beyond simple word matching by detecting **evasion attempts** (e.g., s.h.i.t, h3ll0) and supporting dynamic **whitelisting/blacklisting**.

---

## Key Features

*   **Evasion Detection:** Automatically strips punctuation and handles l33t speak to catch hidden profanity.
*   **Context Control:** Pass a whitelist to allow specific words (e.g., allow "Class" or "Analyst") or a blacklist to block specific competitors.
*   **Smart Censoring:** Replace bad words with *, #, or any custom character while preserving the rest of the sentence.
*   **High Performance:** Built with Flask and optimized set-lookups for <50ms latency.

---

## API Reference

### 1. Check Text (/check)

Analyzes text and returns a boolean status. Useful for preventing bad usernames or bio submissions.

**Endpoint:** POST /check

**Request Body:**

    {
        "text": "This is s.h.i.t",
        "blacklist": ["competitor_name"],
        "whitelist": ["class"]
    }

**Response:**

    {
        "is_profane": true,
        "char_count": 15,
        "language_detected": "en"
    }

### 2. Censor Text (/censor)

Returns a sanitized version of the text. Useful for chat apps and comments.

**Endpoint:** POST /censor

**Request Body:**

    {
        "text": "You are a piece of sh!t",
        "censor_char": "*",
        "blacklist": [],
        "whitelist": []
    }

**Response:**

    {
        "original": "You are a piece of sh!t",
        "censored": "You are a piece of ****",
        "bad_word_count_approx": 1
    }

---

## Local Installation

If you want to run this API on your own machine or develop it further:

1. Clone the repository:

    git clone https://github.com/ahmedmhamimi/profanity-api
    cd profanity-api

2. Install Dependencies:

    pip install -r requirements.txt

3. Run the Server:

    python run.py

The API will be live at http://127.0.0.1:5000.
