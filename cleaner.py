import re
import os
import os.path as path
import string

def save_word(outfile, word):
	outfile.write(word + "\n")

def clean_text_for_kenlm(input_file, output_file):
	outfile = open(output_file, "w", encoding="utf-8")
	with open(input_file, "r", encoding="utf-8") as infile:
		
		for line in infile:
			line = line.strip()
			
			if not line.startswith("<fn>"):

				words = line.split()
				for word in words:
					if word.endswith('.') or word.endswith(',') or word.endswith(')'):
						word = word[:-1]
					if word.startswith('(') or word.startswith('"'):
						word = word[1:]
					
					if '/' in word:
						actual_words = word.split('/')
						for w in actual_words:
							save_word(outfile, w)
					else:
						if not (word in string.punctuation) and not (word.isdigit()):
							save_word(outfile, word)


raw_folder_name = 'raw_corpora'
clean_folder_name = 'clean_corpora'

filenames = os.listdir(raw_folder_name)
for filename in filenames:
	if filename.endswith('nolicense.txt'):
		input_filename = path.join(raw_folder_name, filename)
		output_filename = path.join(clean_folder_name, filename)
		clean_text_for_kenlm(input_filename, output_filename)