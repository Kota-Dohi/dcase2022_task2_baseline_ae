# dcase2022_task2_baseline_ae
Autoencoder-based baseline system for [DCASE2022 Challenge Task 2](https://dcase.community/challenge2022/task-unsupervised-anomalous-sound-detection-for-machine-condition-monitoring).

## Description
This system consists of two main scripts:
- `00_train.py`
  - "Development" mode: 
    - This script trains a model for each machine type by using the directory `dev_data/<machine_type>/train/`.
  - "Evaluation" mode: 
    - This script trains a model for each machine type by using the directory `eval_data/<machine_type>/train/`. (This directory will be from the "additional training dataset".)
- `01_test.py`
  - "Development" mode:
    - This script makes a csv file for each section including the anomaly scores for each wav file in the directories `dev_data/<machine_type>/test/`.
    - The csv files are stored in the directory `result/`.
    - It also makes a csv file including AUC, pAUC, precision, recall, and F1-score for each section.
  - "Evaluation" mode: 
    - This script makes a csv file for each section including the anomaly scores for each wav file in the directories `eval_data/<machine_type>/test/`. (These directories will be from the "evaluation dataset".)
    - The csv files are stored in the directory `result/`.

## Usage

### 1. Clone repository
Clone this repository from Github.

### 2. Download datasets
We will launch the datasets in three stages. 
So, please download the datasets in each stage:
- "Development dataset"
  - Download `dev_data_<machine_type>.zip` from https://zenodo.org/record/6355122.
- "Additional training dataset", i.e. the evaluation dataset for training
  - After April. 15, 2022, download additional training dataset.
- "Evaluation dataset", i.e. the evaluation dataset for test
  - After June. 1, 2022, download evaluation dataset.

### 3. Unzip dataset
Unzip the downloaded files and make the directory structure as follows:


- ./dcase2022_task2_baseline_ae  
    - /00_train.py  
    - /01_test.py  
    - /common.py  
    - /keras_model.py  
    - /baseline.yaml  
    - /readme.md  
- ./dcase2022_task2_baseline_mobile_net_v2  
    - /00_train.py  
    - /01_test.py  
    - /common.py  
    - /keras_model.py  
    - /baseline.yaml  
    - /readme.md  
- /dev_data  
    - /fan
        - /train (only normal clips)  
            - /section_00_source_train_normal_0000_<attribute>.wav  
            - ...  
            - /section_00_source_train_normal_0989_<attribute>.wav  
            - /section_00_target_train_normal_0000_<attribute>.wav  
            - ...  
            - /section_00_target_train_normal_0009_<attribute>.wav  
            - /section_01_source_train_normal_0000_<attribute>.wav  
            - ...  
            - /section_02_target_train_normal_0009_<attribute>.wav  
        - /test 
            - /section_00_source_test_normal_0000_<attribute>.wav    
            - ...  
            - /section_00_source_test_normal_0049_<attribute>.wav    
            - /section_00_source_test_anomaly_0000_<attribute>.wav  
            - ...  
            - /section_00_source_test_anomaly_0049_<attribute>.wav  
            - /section_00_target_test_normal_0000_<attribute>.wav
            - ...  
            - /section_00_target_test_normal_0049_<attribute>.wav 
            - /section_00_target_test_anomaly_0000_<attribute>.wav  
            - ...  
            - /section_00_target_test_anomaly_0049_<attribute>.wav 
            - /section_01_source_test_normal_0000_<attribute>.wav
            - ...  
            - /section_02_target_test_anomaly_0049_<attribute>.wav
        - attributes_00.csv (attribute csv for section 00)
        - attributes_01.csv (attribute csv for section 01)
        - attributes_02.csv (attribute csv for section 02)      
    - /gearbox (The other machine types have the same directory structure as fan.)  
    - /bearing
    - /slider (`slider` means "slide rail")
    - /ToyCar  
    - /ToyTrain  
    - /valve  
- /eval_data  
    - /fan  
        - /train (after launch of the additional training dataset)  
            - /section_03_source_train_normal_0000_<attribute>.wav  
            - ...  
            - /section_03_source_train_normal_0989_<attribute>.wav  
            - /section_03_target_train_normal_0000_<attribute>.wav  
            - ...  
            - /section_03_target_train_normal_0009_<attribute>.wav  
            - /section_04_source_train_normal_0000_<attribute>.wav  
            - ...  
            - /section_05_target_train_normal_0009_<attribute>.wav  
        - /test (after launch of the evaluation dataset)  
            - /section_03_test_0000.wav  
            - ...  
            - /section_03_test_0199.wav  
            - /section_04_test_0000.wav  
            - ...  
            - /section_05_test_0199.wav  
        - attributes_03.csv (attribute csv for train data in section 03)
        - attributes_04.csv (attribute csv for train data in section 04)
        - attributes_05.csv (attribute csv for train data in section 05) 
    - /gearbox (The other machine types have the same directory structure as fan.)  
    - /bearing  
    - /slider (`slider` means "slide rail")
    - /ToyCar  
    - /ToyTrain  
    - /valve  

### 4. Change parameters
You can change parameters for feature extraction and model definition by editing `baseline.yaml`.

### 5. Run training script (for the development dataset)
Run the training script `00_train.py`. 
Use the option `-d` for the development dataset `dev_data/<machine_type>/train/`.
```
$ python 00_train.py -d
```
Options:

| Argument                    |                                   | Description                                                  | 
| --------------------------- | --------------------------------- | ------------------------------------------------------------ | 
| `-h`                        | `--help`                          | Application help.                                            | 
| `-v`                        | `--version`                       | Show application version.                                    | 
| `-d`                        | `--dev`                           | Mode for the development dataset                             |  
| `-e`                        | `--eval`                          | Mode for the additional training and evaluation datasets     | 

`00_train.py` trains a model for each machine type and store the trained models in the directory `model/`.

### 6. Run test script (for the development dataset)
Run the test script `01_test.py`.
Use the option `-d` for the development dataset `dev_data/<machine_type>/test/`.
```
$ python 01_test.py -d
```
The options for `01_test.py` are the same as those for `00_train.py`.
`01_test.py` calculates an anomaly score for each wav file in the directories `dev_data/<machine_type>/source_test/` and `dev_data/<machine_type>/target_test/`.
A csv file for each section including the anomaly scores will be stored in the directory `result/`.
If the mode is "development", the script also outputs another csv file including AUC, pAUC, precision, recall, and F1-score for each section.

### 7. Check results
You can check the anomaly scores in the csv files `anomaly_score_<machine_type>_section_<section_index>_test.csv` in the directory `result/`.
Each anomaly score corresponds to a wav file in the directories `dev_data/<machine_type>/test/`.

`anomaly_score_fan_section_00_test.csv`
```
section_00_source_test_normal_0000_m-n_W.wav	9.718018345
section_00_source_test_normal_0001_m-n_X.wav	8.132550224
section_00_source_test_normal_0002_m-n_W.wav	9.623403255
section_00_source_test_normal_0003_m-n_W.wav	9.545566524
section_00_source_test_normal_0004_m-n_X.wav	8.061900640
section_00_source_test_normal_0005_m-n_W.wav	9.450891629
  ...
```

Also, anomaly detection results after thresholding can be checked in the csv files `decision_result_<machine_type>_section_<section_index>_test.csv`:

`decision_result_fan_section_00_test.csv`
```
section_00_source_test_normal_0000_m-n_W.wav	1
section_00_source_test_normal_0001_m-n_X.wav	0
section_00_source_test_normal_0002_m-n_W.wav	1
section_00_source_test_normal_0003_m-n_W.wav	0
section_00_source_test_normal_0004_m-n_X.wav	0
section_00_source_test_normal_0005_m-n_W.wav	0
  ...
```

Also, you can check performance indicators such as AUC, pAUC, precision, recall, and F1 score:

`result.csv`
```  

fan
                AUC(source)  AUC(target)   pAUC  precision(source)  precision(target) recall(source) recall(target) F1 score(source)  F1 score(target)
00                 0.848        0.454     0.613       0.774            0.494            0.48           0.96           0.592              0.653
01                 0.715        0.46      0.508       0.560            0.505            0.46           0.88           0.505              0.642
02                 0.804        0.647     0.613       0.725            0.593            0.74           0.76           0.732              0.666
arithmetic mean    0.789        0.520     0.578       0.686            0.531            0.559          0.866          0.610              0.654
harmonic mean      0.785        0.506     0.574       0.673            0.527            0.534          0.858          0.596              0.653


  ...
valve
                AUC(source)  AUC(target)   pAUC  precision(source)  precision(target) recall(source) recall(target) F1 score(source)  F1 score(target)
00                 0.543        0.511     0.523       0.521            0.465            0.48           0.4            0.499              0.430
01                 0.489        0.544     0.496       0.538            0.531            0.42           0.34           0.471              0.414
02                 0.529        0.443     0.497       0.510            0.456            0.5            0.52           0.505              0.485
arithmetic mean    0.520        0.499     0.505       0.523            0.484            0.466          0.42           0.492              0.443
harmonic mean      0.519        0.496     0.505       0.523            0.481            0.464          0.407          0.491              0.441
						

                                                                   AUC(source)  AUC(target)   pAUC   precision(source)  precision(target) recall(source)  recall(target) F1 score(source)  F1 score(target)
"arithmetic mean over all machine types  sections  and domains"     0.719          0.483      0.542     0.626               0.516            0.610            0.780          0.543             0.601
"harmonic mean over all machine types  sections  and domains"       0.686          0.437      0.538     0.600               0.512            0.345            0.669          0.438             0.580


```

### 8. Run training script for the additional training dataset (after April 15, 2022)
After the additional training dataset is launched, download and unzip it.
Move it to `eval_data/<machine_type>/train/`.
Run the training script `00_train.py` with the option `-e`. 
```
$ python 00_train.py -e
```
Models are trained by using the additional training dataset `eval_data/<machine_type>/train/`.

### 9. Run test script for the evaluation dataset (after June 1, 2022)
After the evaluation dataset for test is launched, download and unzip it.
Move it to `eval_data/<machine_type>/test/`.
Run the test script `01_test.py` with the option `-e`. 
```
$ python 01_test.py -e
```
Anomaly scores are calculated using the evaluation dataset, i.e., `eval_data/<machine_type>/test/`.
The anomaly scores are stored as csv files in the directory `result/`.
You can submit the csv files for the challenge.
From the submitted csv files, we will calculate AUC, pAUC, and your ranking.

## Dependency
We develop the source code on Ubuntu 18.04 LTS Windows10.

### Software packages
- p7zip-full
- Python == 3.8.12
- FFmpeg

### Python packages
- Keras                         == 2.8.0
- Keras-Applications            == 1.0.8
- Keras-Preprocessing           == 1.1.2
- matplotlib                    == 3.5.1
- numpy                         == 1.21.5
- PyYAML                        == 6.0
- scikit-learn                  == 1.0.2
- scipy                         == 1.8.0
- librosa                       == 0.9.1
- audioread                     == 2.1.9
- setuptools                    == 60.9.3
- tensorflow                    == 2.8.0
- tqdm                          == 4.63.0

## Citation
We will publish papers on the dataset and task description and will announce the citation information for them by the submission deadline, so please make sure to refer to them in your technical report.
