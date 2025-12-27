#!/usr/bin/env python3
"""
Comprehensive test suite for the profanity filter API
"""
import requests
import json

# Update this to your API URL
BASE_URL = "https://advanced-profanity-filter.p.rapidapi.com"
API_KEY = "f762ca5eacmsh1a509f9d6eedadap17f006jsn1b8ef06f4fcb"

HEADERS = {
    'Content-Type': 'application/json',
    'x-rapidapi-host': 'advanced-profanity-filter.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

def test_check(text, expected_profane, description, blacklist=None, whitelist=None):
    """Test the /check endpoint"""
    payload = {
        "text": text,
        "blacklist": blacklist or [],
        "whitelist": whitelist or []
    }
    
    response = requests.post(f"{BASE_URL}/check", headers=HEADERS, json=payload)
    result = response.json()
    
    status = "✓" if result.get("is_profane") == expected_profane else "✗"
    print(f"{status} {description}")
    print(f"   Text: '{text}'")
    print(f"   Expected: {expected_profane}, Got: {result.get('is_profane')}")
    print()
    
    return result.get("is_profane") == expected_profane

def test_censor(text, should_censor, description, censor_char='*', blacklist=None, whitelist=None):
    """Test the /censor endpoint"""
    payload = {
        "text": text,
        "censor_char": censor_char,
        "blacklist": blacklist or [],
        "whitelist": whitelist or []
    }
    
    response = requests.post(f"{BASE_URL}/censor", headers=HEADERS, json=payload)
    result = response.json()
    
    was_censored = result.get("original") != result.get("censored")
    status = "✓" if was_censored == should_censor else "✗"
    
    print(f"{status} {description}")
    print(f"   Original: '{result.get('original')}'")
    print(f"   Censored: '{result.get('censored')}'")
    print(f"   Expected censoring: {should_censor}, Got: {was_censored}")
    print()
    
    return was_censored == should_censor

def run_tests():
    print("=" * 70)
    print("PROFANITY FILTER - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()
    
    passed = 0
    total = 0
    
    # Test 1: Basic profanity detection
    print("--- BASIC PROFANITY DETECTION ---")
    total += 1
    if test_check("This is shit", True, "Direct profanity"):
        passed += 1
    
    total += 1
    if test_check("This is a nice day", False, "Clean text"):
        passed += 1
    
    # Test 2: Evasion with dots
    print("--- EVASION: DOTS ---")
    total += 1
    if test_check("This is s.h.i.t", True, "Profanity with dots"):
        passed += 1
    
    total += 1
    if test_censor("This is s.h.i.t", True, "Censor profanity with dots"):
        passed += 1
    
    # Test 3: Evasion with special characters
    print("--- EVASION: SPECIAL CHARACTERS ---")
    total += 1
    if test_check("You are a piece of sh!t", True, "Profanity with exclamation"):
        passed += 1
    
    total += 1
    if test_censor("You are a piece of sh!t", True, "Censor profanity with exclamation"):
        passed += 1
    
    # Test 4: L33t speak
    print("--- EVASION: L33T SPEAK ---")
    total += 1
    if test_check("What the h3ll", True, "L33t speak (h3ll)"):
        passed += 1
    
    total += 1
    if test_check("Damn th1s sh!t", True, "Mixed l33t speak"):
        passed += 1
    
    total += 1
    if test_censor("Damn th1s sh!t", True, "Censor l33t speak"):
        passed += 1
    
    # Test 5: Multiple profanities
    print("--- MULTIPLE PROFANITIES ---")
    total += 1
    if test_check("This shit is damn hell", True, "Multiple profanities"):
        passed += 1
    
    total += 1
    if test_censor("This shit is damn hell", True, "Censor multiple profanities"):
        passed += 1
    
    # Test 6: Dashes and underscores
    print("--- EVASION: DASHES AND UNDERSCORES ---")
    total += 1
    if test_check("This is s-h-i-t", True, "Profanity with dashes"):
        passed += 1
    
    total += 1
    if test_check("This is s_h_i_t", True, "Profanity with underscores"):
        passed += 1
    
    # Test 7: Mixed evasion techniques
    print("--- EVASION: MIXED TECHNIQUES ---")
    total += 1
    if test_check("F.u.c.k this sh!t", True, "Dots + l33t speak"):
        passed += 1
    
    total += 1
    if test_censor("F.u.c.k this sh!t", True, "Censor mixed evasion"):
        passed += 1
    
    # Test 8: Blacklist functionality
    print("--- BLACKLIST ---")
    total += 1
    if test_check("This is unicorn", True, "Custom blacklist word", blacklist=["unicorn"]):
        passed += 1
    
    total += 1
    if test_censor("The unicorn is magical", True, "Censor blacklisted word", blacklist=["unicorn"]):
        passed += 1
    
    # Test 9: Whitelist functionality
    print("--- WHITELIST ---")
    total += 1
    if test_check("This is hell", False, "Whitelisted profanity", whitelist=["hell"]):
        passed += 1
    
    total += 1
    if test_censor("This is hell", False, "Don't censor whitelisted word", whitelist=["hell"]):
        passed += 1
    
    # Test 10: Edge cases
    print("--- EDGE CASES ---")
    total += 1
    if test_check("", False, "Empty string"):
        passed += 1
    
    total += 1
    if test_check("ass", True, "Single profane word"):
        passed += 1
    
    total += 1
    if test_check("assumption", False, "Word containing profanity substring"):
        passed += 1
    
    # Test 11: Punctuation preservation
    print("--- PUNCTUATION PRESERVATION ---")
    total += 1
    if test_censor("What the hell!", True, "Censor with punctuation"):
        passed += 1
    
    total += 1
    if test_censor("This is shit, damn!", True, "Censor with comma"):
        passed += 1
    
    # Test 12: Custom censor character
    print("--- CUSTOM CENSOR CHARACTER ---")
    payload = {
        "text": "This is shit",
        "censor_char": "#"
    }
    response = requests.post(f"{BASE_URL}/censor", headers=HEADERS, json=payload)
    result = response.json()
    total += 1
    if "#" in result.get("censored", ""):
        print("✓ Custom censor character (#)")
        passed += 1
    else:
        print("✗ Custom censor character (#)")
    print(f"   Censored: '{result.get('censored')}'")
    print()
    
    # Test 13: Numbers in text
    print("--- NUMBERS AND SPECIAL CASES ---")
    total += 1
    if test_check("$hit happens", True, "$ substitution"):
        passed += 1
    
    total += 1
    if test_check("@ss", True, "@ substitution"):
        passed += 1
    
    # Test 14: Case insensitivity
    print("--- CASE INSENSITIVITY ---")
    total += 1
    if test_check("SHIT", True, "Uppercase profanity"):
        passed += 1
    
    total += 1
    if test_check("ShIt", True, "Mixed case profanity"):
        passed += 1
    
    # Test 15: Word boundaries
    print("--- WORD BOUNDARIES ---")
    total += 1
    if test_check("assess the situation", False, "Contains 'ass' but not profane"):
        passed += 1
    
    # Summary
    print("=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    print("=" * 70)
    
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)