# Extract and preprocess train
python feature_extraction.py
python preprocess.py

# For training without segment
python train.py --n-segment=1


# For training with segment
python segmentation.py --input="preprocess_train.csv" --output="segmentation_2_train.csv" --cfg="cfg/segment_2_cfg.json"
python train.py --input="segmentation_2_train.csv" --n-segment=2

# For training with segment = 4

python segmentation.py --input="preprocess_train.csv" --output="segmentation_4_train.csv" --cfg="cfg/segment_4_cfg.json"
python train.py --input="segmentation_4_train.csv" --n-segment=4
