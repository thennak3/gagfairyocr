import re
import time
import keyboard
import pydirectinput
import mss
from PIL import Image
import numpy as np
from datetime import datetime
import difflib

# --- OCR ---
import easyocr
try:
    from rapidfuzz import process, fuzz
    HAVE_RAPIDFUZZ = True
except Exception:
    HAVE_RAPIDFUZZ = False
    print("[WARN] rapidfuzz not installed; falling back to exact matching only.")

# -------------------
# Configuration
# -------------------

# Deduplicated target list
TARGET_WORDS = [
    "Apple", "Bamboo", "Beanstalk", "Blueberry", "Burning Bud", "Cacao", "Cactus",
    "Corn", "Coconut", "Daffodil", "Dragon Fruit", "Elder Strawberry", "Ember Lily",
    "Giant Pinecone", "Glowthorn", "Grape", "Lightshoot", "Mango",
    "Mushroom", "Orange Tulip", "Pepper", "Pumpkin", "Romanesco", "Strawberry",
    "Sugar Apple", "Sunbulb", "Tomato", "Watermelon"
]

# Thresholds
FUZZY_THRESHOLD = 85          # fuzzy match score
OCR_CONF_THRESHOLD = 0.6      # minimum OCR confidence

# Capture area covering the list
large_region = {"top": 308, "left": 1320, "width": 1100, "height": 650}

# OCR Reader
reader = easyocr.Reader(['en'], gpu=True)

# Queue + FSM state
names_queue = []
seen_targets = set()
state = "idle"

# -------------------
# Helpers
# -------------------

def normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

TARGET_NORM_MAP = {normalize_text(t): t for t in TARGET_WORDS}
TARGET_NORMS = list(TARGET_NORM_MAP.keys())

def best_match(ocr_word):
    """
    Return the best valid word match within 1 character difference.
    """
    ocr_word = ocr_word.lower()
    candidates = []
    
    for w in TARGET_WORDS:
        lw = w.lower()
        # simple character difference
        seq = difflib.SequenceMatcher(None, ocr_word, lw)
        ratio = seq.ratio() * 100  # similarity %
        # only allow 1 char difference (roughly len difference <= 1)
        if abs(len(lw) - len(ocr_word)) <= 1 and ratio >= 80:  # ratio threshold
            candidates.append((w, ratio))
    
    if candidates:
        # pick highest ratio
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0]
    else:
        return None, 0

# -------------------
# Capture + OCR
# -------------------

def capture_and_read(region):
    with mss.mss() as sct:
        shot = sct.grab(region)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        #img.save(f"raw_{timestamp}.png")

        np_img = np.array(img)
        results = reader.readtext(np_img, detail=1, paragraph=False)
        texts = [(r[1], float(r[2])) for r in results if isinstance(r, (list, tuple)) and len(r) >= 3]

        return texts

# -------------------
# Parsing + Queueing
# -------------------

def parse_words(ocr_items):
    remaining = []
    found_any = False

    for text, conf in ocr_items:
        raw = text.strip()
        if not raw:
            continue

        match, score = best_match(raw)
        if match and score >= FUZZY_THRESHOLD:
            # Allow lower OCR confidence for fuzzy matches
            if conf >= OCR_CONF_THRESHOLD or score > 85:  # override if fuzzy is strong
                names_queue.append(match)
                found_any = True
                print(f"[MATCH] OCR='{raw}' → '{match}' | fuzzy={score:.1f}% | ocr_conf={conf:.2f}")
                continue  # do not add to remaining
            else:
                print(f"[LOW CONF] OCR='{raw}' → '{match}' fuzzy={score:.1f}% conf={conf:.2f} ignored")
        
        remaining.append(raw)

    return found_any, remaining


# -------------------
# Automation routine
# -------------------

def SendName(name):
    with open(r"D:\Projects\python\fruitocr\next_fruit.txt", "w") as f:
        f.write(name)

# -------------------
# FSM actions
# -------------------

def start_ocr():
    global state
    if state == "idle":
        state = "scanning"
        print("OCR scanning started!")

def process_next():
    global state
    if state == "waiting_confirm":
        state = "processing"
        print("Confirmed. Processing now...")
    elif state == "processing":
        if names_queue:
            name = names_queue.pop(0)
            print(f"Sending: {name}")
            SendName(name)
            time.sleep(2)  # <-- allow AHK to finish typing/clicking
            keyboard.press_and_release("e")
        else:
            print("Resuming scanning...")
            state = "scanning"
    elif state == "waiting_resume":
        state = "scanning"
        print("Resuming scanning...")


def exit_script():
    keyboard.unhook_all_hotkeys()
    print("Exiting...")
    raise SystemExit

# -------------------
# Hotkeys
# -------------------

keyboard.add_hotkey("]", start_ocr)
keyboard.add_hotkey("n", process_next)
keyboard.add_hotkey("q", exit_script)

print("Ready. ']' to start, 'N' to proceed, 'Q' to exit.")

# -------------------
# Main loop
# -------------------

try:
    while True:
        if state == "scanning":
            ocr_items = capture_and_read(large_region)
            if ocr_items:
                print("OCR results:", [t for t, _ in ocr_items])

            found, remaining = parse_words(ocr_items)

            if names_queue:
                print("Queue:", names_queue)
                if remaining:
                    print("Unmatched:", remaining)
                keyboard.press_and_release("e")
                state = "processing"
                #print("Press 'N' to continue...")
            else:
                if not found:
                    print("No target words yet... scanning.")

        time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopped.")
