import re
import os
import os.path as path
import string
import subprocess

def train_model_via_kenlm(input_file, output_file):
	cmd = 'kenlm/build/bin/lmplz -o 5 --discount_fallback < \"{0}\" > \"{1}\"'.format(input_file, output_file)
	subprocess.run(cmd, shell=True, check=True)

clean_folder_name = 'character_corpora'
character_folder_name = 'trained_models'

filenames = os.listdir(clean_folder_name)
for filename in filenames:
	if filename.endswith('nolicense.txt'):
		input_filename = path.join(clean_folder_name, filename)
		output_filename = path.join(character_folder_name, filename+'.arpa')
		train_model_via_kenlm(input_filename, output_filename)
