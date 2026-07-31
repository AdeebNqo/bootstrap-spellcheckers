#./build #build kenlm + (you may need to install it)
python cleaner.py
python create_character_corpora.py
python train_models.py

python get_raw_test_data.py
python create_wrecked_test_data.py
python create_spellchecker_plots.py
#python create_plots.py
python create_logistic_model.py

python get_raw_final_test_data.py
python create_final_wrecked_test_data.py
python evaluate_lm_and_regression.py
python compute_stats_individual_langs.py

python evaluate_lm_and_regression_in_cross_lingual_setting.py
python compute_stats_for_cross_lingual_tests.py