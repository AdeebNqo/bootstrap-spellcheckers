from datasets import load_dataset
import os.path as path

ds = load_dataset("anrilombard/sa-nguni-languages")

folder_name = 'raw_test_data'

lang_names = list(set(ds['train']['language']))
for lang_name in lang_names:
	filename = path.join(folder_name, lang_name + '.csv')

	train_ds = ds['train']

	ds_filtered = train_ds.filter(lambda ex: ex['language'] == lang_name)
	ds_filtered.to_csv(filename)