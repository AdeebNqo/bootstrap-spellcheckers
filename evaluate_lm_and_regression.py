import os
import kenlm
import csv
import torch
from create_logistic_model import LogisticRegression


def char_score(model, word):
	seq = " ".join(list(word.strip()))
	return model.score(seq, bos=True, eos=True)


def main():	
	folder_name = 'wrecked_final_test_data'

	languages = [
		('isiZulu', 'trained_models/CORP.NCHLT.zu.CLEAN.2.0 - nolicense.txt.arpa', 'logistic_models/isiZulu.pth', 'wrecked_final_test_data/isiZulu.csv'),
		('isiXhosa', 'trained_models/CORP.NCHLT.xh.CLEAN.2.0 - nolicense.txt.arpa', 'logistic_models/isiXhosa.pth', 'wrecked_final_test_data/isiXhosa.csv'),
		('isiNdebele', 'trained_models/CORP.NCHLT.nr.CLEAN.2.0 - nolicense.txt.arpa', 'logistic_models/isiNdebele.pth','wrecked_final_test_data/isiNdebele.csv'),
		('siSwati', 'trained_models/CORP.NCHLT.ss.CLEAN.2.0 - nolicense.txt.arpa', 'logistic_models/siSwati.pth', 'wrecked_final_test_data/siSwati.csv')
	]

	for lang_name, model_path, regression_path, test_path in languages:
		lang_model = kenlm.LanguageModel(model_path)
		log_model = torch.load(regression_path)
		log_model.eval()

		output_foldername = 'individual_eval_lm_log_results'
		full_output_filename = test_path.replace('wrecked_final_test_data', output_foldername)
		output_file = open(full_output_filename, 'w', newline='')
		column_names = ['Correct word', 'Correct word score', 'Correct word predicted correct', 'Incorrect word', 'Incorrect word score', 'Incorrect word predicted incorrect', 'Wreck type']
		writer = csv.DictWriter(output_file, fieldnames=column_names)
		data = []

		with open(test_path, mode='r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				row['Correct word score'] = char_score(lang_model, row['Correct word'])
				row['Incorrect word score'] = char_score(lang_model, row['Incorrect word'])
				
				logit = log_model(torch.tensor([row['Incorrect word score']]))
				probability = torch.sigmoid(logit)
				correctness = (probability > 0.5).int().item()
				row['Incorrect word predicted incorrect'] = True if correctness == 0 else False

				logit = log_model(torch.tensor([row['Correct word score']]))
				probability = torch.sigmoid(logit)
				correctness = (probability > 0.5).int().item()
				row['Correct word predicted correct'] = True if correctness == 1 else False

				data.append(row)

		writer.writeheader()
		writer.writerows(data)

if __name__ == '__main__':
	main()
