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

	for lang_name1, model_path1, regression_path1, test_path1 in languages:
		for lang_name2, model_path2, regression_path2, test_path2 in languages:
			if lang_name1 != lang_name2:
				lang_model = kenlm.LanguageModel(model_path2)
				log_model = torch.load(regression_path1)
				log_model.eval()

				output_foldername = 'cross_lang_eval_lm_log_results'
				test_path1_updated = test_path1.split('/')[1].replace('.csv', '')
				test_path2_updated = test_path2.split('/')[1].replace('.csv', '')
				filename_string = '{0}-{1}.csv'.format(test_path1_updated, test_path2_updated)
				filename_string = os.path.join(output_foldername, filename_string)


				output_file = open(filename_string, 'w', newline='')
				column_names = ['Correct word', 'Correct word score', 'Correct word predicted correct', 'Incorrect word', 'Incorrect word score', 'Incorrect word predicted incorrect', 'Wreck type']

				writer = csv.DictWriter(output_file, fieldnames=column_names)
				data = []

				with open(test_path1, mode='r') as f:
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
				output_file.close()

if __name__ == '__main__':
	main()
