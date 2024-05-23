import csv
import string

letters = list(string.ascii_lowercase)
letters.extend(('ą','ę','ó','ż','ź','ł','ć','ś'))

# Initialize a dictionary to store the frequencies
frequencies = dict()

# Open the CSV file and count the total number of sentences
with open('zdania.csv', encoding="utf-8") as input:
    csv_reader = csv.reader(input, delimiter=',')
    # Count the total number of rows
    rows = list(csv_reader)  
    total_rows = len(rows)  
    
    # Loop through all the letters
    for letter in letters:
        letter_count = 0
        # Loop through the rows to count occurrences of each letter
        for row in rows:
            # Check if the letter is in the sentence
            if letter in row[0].lower():
                letter_count += 1  
        
        # Calculate the frequency and round it to 1 decimal place
        frequency = letter_count / total_rows
        frequencies[letter] = frequency

best_letter = "NWM"
best_score = 0.5
for key, value in frequencies.items():
    score = abs(value - 0.5)
    if score < best_score:
        best_score = score
        best_letter = key
    print("'{}' found in {:.0%} of sentences".format(key, value))

print("The best letter is '{}' with a score of {:.0%}".format(best_letter, frequencies[best_letter]))
