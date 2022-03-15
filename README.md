# dcase2022_task2_baseline_ae
Autoencoder-based baseline system for [DCASE2022 Challenge Task 2](http://dcase.community/challenge2022/task-unsupervised-detection-of-anomalous-sounds).

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
  - Download `dev_data_<machine_type>.zip` from https://zenodo.org/record/4562016.
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
section AUC (source) AUC (target) pAUC precision (source) precision (target) recall (source) recall (target) F1 score (source) F1 score (target)
00 0.8488 0.4542 0.6136 0.7741 0.4948 0.48 0.96 0.5925 0.6530
01 0.7150 0.46   0.5089 0.5609 0.5057 0.46 0.88 0.5054 0.6423
02 0.8042 0.6477 0.6131 0.7254 0.5937 0.74 0.76 0.7326 0.6666
arithmetic mean 0.7893 0.5206 0.5785 0.6868 0.5314 0.5599 0.8666 0.6102 0.6540
harmonic mean 0.7852 0.5068 0.5741 0.6737 0.5279 0.5348 0.8586 0.5963 0.6538

  ...
valve
section AUC (source) AUC (target) pAUC precision (source) precision (target) recall (source) recall (target) F1 score (source) F1 score (target)
00 0.5432 0.5116 0.5231 0.5217 0.4651 0.48 0.4 0.4999 0.4301
01 0.489 0.5448 0.4968 0.5384 0.5312 0.42 0.34 0.4719 0.4146
02 0.5298 0.4432 0.4973 0.5102 0.4561 0.5 0.52 0.5050 0.4859
arithmetic mean 0.5206 0.4998 0.5057 0.5234 0.4841 0.4666 0.42 0.4923 0.4435
harmonic mean 0.5196 0.4961 0.5054 0.5232 0.4819 0.4640 0.4073 0.4918 0.4415

						
 AUC (source) AUC (target) pAUC precision (source) precision (target) recall (source) recall (target) F1 score (source) F1 score (target)
"arithmetic mean over all machine types  sections  and domains" 0.7193 0.4836 0.5420 0.6265 0.5160 0.6104 0.7809 0.5439 0.6018
"harmonic mean over all machine types  sections  and domains" 0.6862 0.4371 0.5385 0.6007 0.5127 0.3458 0.6692 0.4389 0.5806

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
- Python == 3.6.5
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
