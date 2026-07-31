import os
import kenlm
import csv

def char_score(model, word):
	seq = " ".join(list(word.strip()))
	return model.score(seq, bos=True, eos=True)

def main():	
	languages = [
		('isiZulu', 'trained_models/CORP.NCHLT.zu.CLEAN.2.0 - nolicense.txt.arpa', 'wrecked_test_data/isiZulu.csv'),
		('isiXhosa', 'trained_models/CORP.NCHLT.xh.CLEAN.2.0 - nolicense.txt.arpa', 'wrecked_test_data/isiXhosa.csv'),
		('isiNdebele', 'trained_models/CORP.NCHLT.nr.CLEAN.2.0 - nolicense.txt.arpa', 'wrecked_test_data/isiNdebele.csv'),
		('siSwati', 'trained_models/CORP.NCHLT.ss.CLEAN.2.0 - nolicense.txt.arpa', 'wrecked_test_data/siSwati.csv')
	]
	
	results = []

	for lang_name, model_path, test_path in languages:
		fieldnames = ['Correct word', 'Correct word score', 'Incorrect word', 'Incorrect word score', 'Wreck type']

		output_file = open(test_path.replace('wrecked_test_data/', 'wrecked_scored_test_data/'), mode='w', newline='')
		writer = csv.DictWriter(output_file, fieldnames=fieldnames)

		model = kenlm.LanguageModel(model_path)

		new_rows = []

		with open(test_path, mode='r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				row['Correct word score'] = char_score(model, row['Correct word'])
				row['Incorrect word score'] = char_score(model, row['Incorrect word'])
				new_rows.append(row)

		writer.writeheader()
		writer.writerows(new_rows)


if __name__ == '__main__':
	main()
