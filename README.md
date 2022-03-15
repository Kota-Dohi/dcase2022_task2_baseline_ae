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
  - After April. 1, 2022, download `eval_data_train_<machine_type>.zip` from https://zenodo.org/record/4660992.
- "Evaluation dataset", i.e. the evaluation dataset for test
  - After June. 1, 2022, download `eval_data_test_<machine_type>.zip` from https://zenodo.org/record/4884786.

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
section	domain	AUC	pAUC	precision	recall	F1 score
0	source	0.6738	0.573157895	0.654545455	0.36	0.464516129
1	source	0.6786	0.505263158	0.625	0.3	0.405405405
2	source	0.6542	0.532631579	0.685714286	0.24	0.355555556
0	target	0.6955	0.548421053	0.657142857	0.46	0.541176471
1	target	0.4953	0.483157895	0.5	0.35	0.411764706
2	target	0.6441	0.559473684	0.497461929	0.98	0.65993266
arithmetic mean		0.64025	0.533684211	0.603310754	0.448333333	0.473058488
harmonic mean		0.631866714	0.531826049	0.592999386	0.367438982	0.453732583
  ...
valve						
section	domain	AUC	pAUC	precision	recall	F1 score
0	source	0.5026	0.506842105	0.588235294	0.2	0.298507463
1	source	0.5404	0.494210526	0.512195122	0.21	0.29787234
2	source	0.596	0.516315789	0.615384615	0.24	0.345323741
0	target	0.4716	0.485263158	0.382352941	0.13	0.194029851
1	target	0.5857	0.548421053	0.519230769	0.81	0.6328125
2	target	0.5489	0.489473684	0.55	0.22	0.314285714
arithmetic mean		0.540866667	0.506754386	0.52789979	0.301666667	0.347138602
harmonic mean		0.537267925	0.505885378	0.515602416	0.218970897	0.307394569
						
		AUC	pAUC	precision	recall	F1 score
arithmetic mean over all machine types, sections, and domains		0.634334516	0.537946639	0.511821964	0.448497815	0.439585489
harmonic mean over all machine types, sections, and domains		0.620051253	0.534340265	1.55E-15	1.55E-15	1.55E-15
```

### 8. Run training script for the additional training dataset (after April 1, 2021)
After the additional training dataset is launched, download and unzip it.
Move it to `eval_data/<machine_type>/train/`.
Run the training script `00_train.py` with the option `-e`. 
```
$ python 00_train.py -e
```
Models are trained by using the additional training dataset `eval_data/<machine_type>/train/`.

### 9. Run test script for the evaluation dataset (after June 1, 2021)
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
- Keras                         == 2.3.0
- Keras-Applications            == 1.0.8
- Keras-Preprocessing           == 1.0.5
- matplotlib                    == 3.0.3
- numpy                         == 1.18.1
- PyYAML                        == 5.1
- scikit-learn                  == 0.22.2.post1
- scipy                         == 1.1.0
- librosa                       == 0.6.0
- audioread                     == 2.1.5 (more)
- setuptools                    == 41.0.0
- tensorflow                    == 1.15.0
- tqdm                          == 4.43.0

## Citation
We will publish papers on the dataset and task description and will announce the citation information for them by the submission deadline, so please make sure to refer to them in your technical report.
