import urllib.request

VALID_WORDS = []
ANSWERS = []

try:
    # Use a small common set of valid words to ensure it runs fast and reliably without external deps failure
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    url = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
    content = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
    all_words = [w.strip().upper() for w in content.split('\n') if len(w.strip()) == 5]
    if all_words:
        VALID_WORDS = all_words
        ANSWERS = all_words # For simplicity, any valid word can be an answer
except Exception as e:
    print(f"Could not load words from URL: {e}")

if not VALID_WORDS:
    VALID_WORDS = [
        "APPLE", "TRAIN", "HOUSE", "MOUSE", "SMILE", "RIGHT", "PLANT", "HEART", 
        "FRAME", "WORLD", "REACT", "GAMES", "BUILD", "DREAM", "LIGHT", "WATER",
        "EARTH", "SPACE", "STONE", "RIVER", "BEACH", "GHOST", "NIGHT", "PIZZA"
    ]
    ANSWERS = VALID_WORDS.copy()
