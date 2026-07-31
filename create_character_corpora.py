import re
import os
import os.path as path
import string

def save_word(outfile, word):
	outfile.write(word + "\n")

def space_out_chars_for_kenlm(input_file, output_file):
	outfile = open(output_file, "w", encoding="utf-8")
	with open(input_file, "r", encoding="utf-8") as infile:
		
		for line in infile:
			line = line.strip()

			space_separated_word = ' '.join(list(line))
			save_word(outfile, space_separated_word)


clean_folder_name = 'clean_corpora'
character_folder_name = 'character_corpora'

filenames = os.listdir(clean_folder_name)
for filename in filenames:
	if filename.endswith('nolicense.txt'):
		input_filename = path.join(clean_folder_name, filename)
		output_filename = path.join(character_folder_name, filename)
		space_out_chars_for_kenlm(input_filename, output_filename)
