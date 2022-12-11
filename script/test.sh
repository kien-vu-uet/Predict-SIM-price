# Extract and preprocess test
python feature_extraction.py --input="test.csv" --output="features_test.csv" --is-test-set=True
python preprocess.py --input="features_test.csv" --output="preprocess_test.csv"

# For testing
python test.py --input="preprocess_test.csv" --output="test_results/test_result_without_segment.csv" --model="models/catboost_regressor_1.sav"

# For testing with segmentation = 2
python segmentation.py --input="preprocess_test.csv" --output="segmentation_2_test.csv" --is-test-set=True 
python test.py --input="segmentation_2_test.csv" --output="test_results/test_result_with_binary_segment.csv" --model="models/xgboost_regressor_2.sav"


# For testing with segmentation = 4
python segmentation.py --input="preprocess_test.csv" --output="segmentation_4_test.csv" --is-test-set=True --cfg="cfg/segment_4_cfg.json"
python test.py --input="segmentation_4_test.csv" --output="test_results/test_result_with_4_segment.csv" --model="models/xgboost_regressor_4.sav"
