import nltk
from nltk.corpus import words

# Download once (comment out after first run)
nltk.download('words')

# Load 5-letter English words
word_list = [word.lower() for word in words.words() if len(word) == 5 and word.isalpha()]

def get_input_set(prompt):
    raw = input(prompt).strip().lower()
    return set(raw) if raw else set()

def get_input_dict(prompt):
    fixed = {}
    print(prompt)
    while True:
        entry = input("Enter position and letter (e.g. 3 i), or press Enter to finish: ").strip().lower()
        if not entry:
            break
        try:
            pos, letter = entry.split()
            pos = int(pos) - 1  # convert to 0-based index
            fixed[pos] = letter
        except:
            print("Invalid format. Try again.")
    return fixed

def get_required_letter_positions(prompt):
    req = {}
    print(prompt)
    while True:
        letter = input("Enter a letter (or press Enter to finish): ").strip().lower()
        if not letter:
            break
        pos_input = input(f"Enter possible positions (e.g. 1 4 for positions 1 and 4): ").strip()
        try:
            positions = [int(p) - 1 for p in pos_input.split()]
            req[letter] = positions
        except:
            print("Invalid format. Try again.")
    return req

def filter_words(word_list, fixed_letters, required_positions, forbidden_letters, floating_letters):
    valid_words = []
    for word in word_list:
        # Fixed letters at fixed positions
        if any(word[pos] != char for pos, char in fixed_letters.items()):
            continue

        # Letters that must be present at any of certain positions
        passed = True
        for letter, positions in required_positions.items():
            if not any(word[pos] == letter for pos in positions):
                passed = False
                break
        if not passed:
            continue

        # Letters that must be present somewhere
        if not all(letter in word for letter in floating_letters):
            continue

        # Forbidden letters must not appear
        if any(letter in word for letter in forbidden_letters):
            continue

        valid_words.append(word)
    return valid_words

# === INTERACTIVE RUN ===
print("🧩 Wordle Puzzle Solver")

forbidden_letters = get_input_set("Enter forbidden letters (e.g. 'ertsh'): ")
fixed_letters = get_input_dict("Enter known letters in known positions (e.g. 3 i):")
required_positions = get_required_letter_positions("Enter known letters with possible positions (e.g. 'm' in 2 or 5):")
floating_letters = get_input_set("Enter known letters in unknown positions (e.g. 'o'): ")

valid = filter_words(word_list, fixed_letters, required_positions, forbidden_letters, floating_letters)

print(f"\n🔍 Found {len(valid)} valid word(s):")
for word in sorted(valid):
    print(word)
    
