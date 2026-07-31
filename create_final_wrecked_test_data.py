import random
import re
from pathlib import Path
import os
import csv
from itertools import islice

class SpellingWrecker:
	"""Generate realistic spelling errors for testing."""
	
	def __init__(self, language="isiZulu"):
		self.language = language
		
		# Common keyboard-adjacent characters (QWERTY layout)
		self.adjacent_keys = {
			'a': 'sqwz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wrsd',
			'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn',
			'k': 'jiolm', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
			'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
			'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
			'z': 'asx'
		}
		
		# Common character confusions in African languages
		self.phonetic_confusions = {
			'b': 'p', 'p': 'b',
			'd': 't', 't': 'd',
			'g': 'k', 'k': 'g',
			'v': 'f', 'f': 'v',
			'z': 's', 's': 'z',
			'c': 'k', 'k': 'c',
		}
	
	def substitute_char(self, word):
		"""Substitute one character with an adjacent key."""
		if len(word) < 2:
			return word
		
		pos = random.randint(0, len(word) - 1)
		char = word[pos].lower()
		
		if char in self.adjacent_keys:
			replacement = random.choice(self.adjacent_keys[char])
			# Preserve case
			if word[pos].isupper():
				replacement = replacement.upper()
			return word[:pos] + replacement + word[pos+1:]
		return word
	
	def delete_char(self, word):
		"""Delete a random character."""
		if len(word) <= 2:
			return word
		
		pos = random.randint(0, len(word) - 1)
		return word[:pos] + word[pos+1:]
	
	def insert_char(self, word):
		"""Insert a random character."""
		pos = random.randint(0, len(word))
		char = word[pos-1] if pos > 0 else word[0]
		char = char.lower()
		
		# Insert adjacent key or duplicate
		if random.random() < 0.5 and char in self.adjacent_keys:
			insert_char = random.choice(self.adjacent_keys[char])
		else:
			insert_char = char  # Duplicate
		
		return word[:pos] + insert_char + word[pos:]
	
	def transpose_chars(self, word):
		"""Swap two adjacent characters."""
		if len(word) < 2:
			return word
		
		pos = random.randint(0, len(word) - 2)
		return word[:pos] + word[pos+1] + word[pos] + word[pos+2:]
	
	def phonetic_error(self, word):
		"""Replace with phonetically similar character."""
		if len(word) < 2:
			return word
		
		for i, char in enumerate(word.lower()):
			if char in self.phonetic_confusions and random.random() < 0.3:
				replacement = self.phonetic_confusions[char]
				if word[i].isupper():
					replacement = replacement.upper()
				return word[:i] + replacement + word[i+1:]
		return word
	
	def wreck_word(self, word, error_types=None):
		"""
		Apply a random error to a word.
		
		Args:
			word: The correct word
			error_types: List of error types to use, or None for all
		
		Returns:
			Tuple of (wrecked_word, error_type)
		"""
		if error_types is None:
			error_types = ['substitute', 'delete', 'insert', 'transpose', 'phonetic']
		
		error_type = random.choice(error_types)
		
		if error_type == 'substitute':
			return self.substitute_char(word), 'substitution'
		elif error_type == 'delete':
			return self.delete_char(word), 'deletion'
		elif error_type == 'insert':
			return self.insert_char(word), 'insertion'
		elif error_type == 'transpose':
			return self.transpose_chars(word), 'transposition'
		elif error_type == 'phonetic':
			return self.phonetic_error(word), 'phonetic'
		
		return word, 'none'
	
	def wreck_corpus(self, word, num_errors=1000):
		
		# Read and extract unique words
		words = set()
		with open(corpus_file, 'r', encoding='utf-8') as f:
			for line in f:
				# Extract words, remove punctuation
				line_words = re.findall(r'\b\w+\b', line)
				for word in line_words:
					if len(word) >= min_word_length and not any(c.isdigit() for c in word):
						words.add(word)
		
		words = list(words)
		print(f"Found {len(words)} unique words (length >= {min_word_length})")
		
		if len(words) < num_errors:
			print(f"Warning: Only {len(words)} words available, generating that many errors")
			num_errors = len(words)
		
		# Generate errors
		print(f"Generating {num_errors} spelling errors...")
		error_pairs = []
		error_stats = {'substitution': 0, 'deletion': 0, 'insertion': 0, 'transposition': 0, 'phonetic': 0}
		
		sampled_words = random.sample(words, num_errors)
		
		for word in sampled_words:
			wrecked, error_type = self.wreck_word(word)
			
			# Make sure we actually created an error
			if wrecked != word:
				error_pairs.append((wrecked, word))
				error_stats[error_type] += 1


def main():
	"""Generate wrecked test data for all languages."""
	
	min_word_length=4
	wrecker = SpellingWrecker()

	raw_folder_name = 'raw_final_test_data'
	wrecked_folder_name = 'wrecked_final_test_data'

	column_names = ['Correct word', 'Incorrect word', 'Wreck type']

	filenames = os.listdir(raw_folder_name)
	for filename in filenames:
		full_input_filename = os.path.join(raw_folder_name, filename)
		full_output_filename = os.path.join(wrecked_folder_name, filename)

		output_file = open(full_output_filename, 'w', newline='')
		writer = csv.DictWriter(output_file, fieldnames=column_names)

		data = []

		with open(full_input_filename, mode='r') as file:
			reader = csv.DictReader(file)
			for row in islice(reader, 600): #the value is selected for memory reasons when it comes to isiZulu
				words = row['text'].split()
				words = [word for word in words if len(word) >= min_word_length]

				for word in words:
					incorrect_word, wreck_type = wrecker.wreck_word(word)
					data.append({'Correct word': word, 'Incorrect word': incorrect_word, 'Wreck type': wreck_type})

		writer.writeheader()
		writer.writerows(data)

if __name__ == '__main__':
	main()
