import os
import csv

def calc_with_zero_denom_possibility(num, den):
	return num / den if den > 0 else 0

def get_f1(p, r):
	return 2 * calc_with_zero_denom_possibility(p * r, p + r)
	
folder_name = 'cross_lang_eval_lm_log_results'
filenames = os.listdir(folder_name)
for filename in filenames:
	full_filename = os.path.join(folder_name, filename)

	num_correct_words = 0
	num_incorrect_words = 0

	num_correct_words_predicted_as_correct = 0
	num_incorrect_words_predicted_as_incorrect = 0

	num_correct_words_predicted_as_incorrect = 0
	num_incorrect_words_predicted_as_correct = 0

	with open(full_filename, mode='r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['Correct word predicted correct'] == 'True':
				num_correct_words_predicted_as_correct += 1
			else:
				num_correct_words_predicted_as_incorrect += 1

			if row['Incorrect word predicted incorrect'] == 'True':
				num_incorrect_words_predicted_as_incorrect += 1
			else:
				num_incorrect_words_predicted_as_correct += 1

			num_correct_words += 1
			num_incorrect_words += 1

	prec_inc = calc_with_zero_denom_possibility(num_incorrect_words_predicted_as_incorrect, num_incorrect_words_predicted_as_incorrect + num_correct_words_predicted_as_incorrect)
	rec_inc = calc_with_zero_denom_possibility(num_incorrect_words_predicted_as_incorrect, num_incorrect_words)
	f1_inc = get_f1(prec_inc, rec_inc)

	prec_cor = calc_with_zero_denom_possibility(num_correct_words_predicted_as_correct, num_correct_words_predicted_as_correct + num_incorrect_words_predicted_as_correct)
	rec_cor = calc_with_zero_denom_possibility(num_correct_words_predicted_as_correct, num_correct_words)
	f1_cor = get_f1(prec_cor, rec_cor)

	print(filename)
	print(f"Metrics for Incorrect Words: Prec={prec_inc:.3f}, Rec={rec_inc:.3f}, F1={f1_inc:.3f}")
	print(f"Metrics for Correct Words:   Prec={prec_cor:.3f}, Rec={rec_cor:.3f}, F1={f1_cor:.3f}")
	print()