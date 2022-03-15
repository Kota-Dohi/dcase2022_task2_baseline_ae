########################################################################
# import default libraries
########################################################################
import os
import csv
import sys
import gc
########################################################################


########################################################################
# import additional libraries
########################################################################
import numpy as np
import scipy.stats
# from import
from tqdm import tqdm
from sklearn import metrics
try:
    from sklearn.externals import joblib
except:
    import joblib

# original lib
import common as com
import keras_model

########################################################################


########################################################################
# load parameter.yaml
########################################################################
param = com.yaml_load()
#######################################################################


########################################################################
# output csv file
########################################################################
def save_csv(save_file_path,
             save_data):
    with open(save_file_path, "w", newline="") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(save_data)


########################################################################


########################################################################
# main 01_test.py
########################################################################
if __name__ == "__main__":
    # check mode
    # "development": mode == True
    # "evaluation": mode == False
    mode = com.command_line_chk()

    if mode is None:
        sys.exit(-1)

    # make output result directory
    os.makedirs(param["result_directory"], exist_ok=True)

    # load base directory
    dirs = com.select_dirs(param=param, mode=mode)

    # initialize lines in csv for AUC and pAUC
    csv_lines = []

    if mode:
        performance_over_all = []

    # loop of the base directory
    for idx, target_dir in enumerate(dirs):
        print("\n===========================")
        print("[{idx}/{total}] {target_dir}".format(target_dir=target_dir, idx=idx+1, total=len(dirs)))
        machine_type = os.path.split(target_dir)[1]

        print("============== MODEL LOAD ==============")
        # load model file
        model_file = "{model}/model_{machine_type}.hdf5".format(model=param["model_directory"],
                                                                machine_type=machine_type)
        if not os.path.exists(model_file):
            com.logger.error("{} model not found ".format(machine_type))
            sys.exit(-1)
        model = keras_model.load_model(model_file)
        model.summary()

        # load anomaly score distribution for determining threshold
        score_distr_file_path = "{model}/score_distr_{machine_type}.pkl".format(model=param["model_directory"],
                                                                    machine_type=machine_type)
        shape_hat, loc_hat, scale_hat = joblib.load(score_distr_file_path)

        # determine threshold for decision
        decision_threshold = scipy.stats.gamma.ppf(q=param["decision_threshold"], a=shape_hat, loc=loc_hat, scale=scale_hat)

        if mode:
            # results for each machine type
            csv_lines.append([machine_type])
            csv_lines.append(["section", "AUC (source)", "AUC (target)", "pAUC", 
                            "precision (source)", "precision (target)", "recall (source)", "recall (target)",
                            "F1 score (source)", "F1 score (target)"])
            performance = []

        dir_name = "test"
        
        #list machine id
        section_names = com.get_section_names(target_dir, dir_name)

        for section_name in section_names:
            # load test file
            files, y_true = com.file_list_generator(target_dir=target_dir,
                                                    section_name=section_name,
                                                    dir_name=dir_name,
                                                    mode=mode)

            # setup anomaly score file path
            anomaly_score_csv = "{result}/anomaly_score_{machine_type}_{section_name}_{dir_name}.csv".format(result=param["result_directory"],
                                                                                                            machine_type=machine_type,
                                                                                                            section_name=section_name,
                                                                                                            dir_name=dir_name)
            anomaly_score_list = []

            # setup decision result file path
            decision_result_csv = "{result}/decision_result_{machine_type}_{section_name}_{dir_name}.csv".format(result=param["result_directory"],
                                                                                                                machine_type=machine_type,
                                                                                                                section_name=section_name,
                                                                                                                dir_name=dir_name)
            decision_result_list = []

            if mode:
                domain_list = []

            print("\n============== BEGIN TEST FOR A SECTION ==============")
            y_pred = [0. for k in files]
            for file_idx, file_path in tqdm(enumerate(files), total=len(files)):
                try:
                    data = com.file_to_vectors(file_path,
                                                    n_mels=param["feature"]["n_mels"],
                                                    n_frames=param["feature"]["n_frames"],
                                                    n_fft=param["feature"]["n_fft"],
                                                    hop_length=param["feature"]["hop_length"],
                                                    power=param["feature"]["power"])
                except:
                    com.logger.error("File broken!!: {}".format(file_path))

                y_pred[file_idx] = np.mean(np.square(data - model.predict(data)))
                
                # store anomaly scores
                anomaly_score_list.append([os.path.basename(file_path), y_pred[file_idx]])

                # store decision results
                if y_pred[file_idx] > decision_threshold:
                    decision_result_list.append([os.path.basename(file_path), 1])
                else:
                    decision_result_list.append([os.path.basename(file_path), 0])

                if mode:
                    domain_list.append("source" if "source" in file_path else "target")

            # output anomaly scores
            save_csv(save_file_path=anomaly_score_csv, save_data=anomaly_score_list)
            com.logger.info("anomaly score result ->  {}".format(anomaly_score_csv))

            # output decision results
            save_csv(save_file_path=decision_result_csv, save_data=decision_result_list)
            com.logger.info("decision result ->  {}".format(decision_result_csv))

            if mode:
                # extract scores for calculation of AUC (source) and AUC (target)
                y_true_s_auc = [y_true[idx] for idx in range(len(y_true)) if domain_list[idx]=="source" or y_true[idx]==1]
                y_pred_s_auc = [y_pred[idx] for idx in range(len(y_true)) if domain_list[idx]=="source" or y_true[idx]==1]
                y_true_t_auc = [y_true[idx] for idx in range(len(y_true)) if domain_list[idx]=="target" or y_true[idx]==1]
                y_pred_t_auc = [y_pred[idx] for idx in range(len(y_true)) if domain_list[idx]=="target" or y_true[idx]==1]

                # extract scores for calculation of precision, recall, F1 score for each domain
                y_true_s = [y_true[idx] for idx in range(len(y_true)) if domain_list[idx]=="source"]
                y_pred_s = [y_pred[idx] for idx in range(len(y_true)) if domain_list[idx]=="source"]
                y_true_t = [y_true[idx] for idx in range(len(y_true)) if domain_list[idx]=="target"]
                y_pred_t = [y_pred[idx] for idx in range(len(y_true)) if domain_list[idx]=="target"]

                # calculate AUC, pAUC, precision, recall, F1 score 
                auc_s = metrics.roc_auc_score(y_true_s_auc, y_pred_s_auc)
                auc_t = metrics.roc_auc_score(y_true_t_auc, y_pred_t_auc)
                p_auc = metrics.roc_auc_score(y_true, y_pred, max_fpr=param["max_fpr"])
                tn_s, fp_s, fn_s, tp_s = metrics.confusion_matrix(y_true_s, [1 if x > decision_threshold else 0 for x in y_pred_s]).ravel()
                tn_t, fp_t, fn_t, tp_t = metrics.confusion_matrix(y_true_t, [1 if x > decision_threshold else 0 for x in y_pred_t]).ravel()
                prec_s = tp_s / np.maximum(tp_s + fp_s, sys.float_info.epsilon)
                prec_t = tp_t / np.maximum(tp_t + fp_t, sys.float_info.epsilon)
                recall_s = tp_s / np.maximum(tp_s + fn_s, sys.float_info.epsilon)
                recall_t = tp_t / np.maximum(tp_t + fn_t, sys.float_info.epsilon)
                f1_s = 2.0 * prec_s * recall_s / np.maximum(prec_s + recall_s, sys.float_info.epsilon)
                f1_t = 2.0 * prec_t * recall_t / np.maximum(prec_t + recall_t, sys.float_info.epsilon)

                csv_lines.append([section_name.split("_", 1)[1],
                                auc_s, auc_t, p_auc, prec_s, prec_t, recall_s, recall_t, f1_s, f1_t])

                performance.append([auc_s, auc_t, p_auc, prec_s, prec_t, recall_s, recall_t, f1_s, f1_t])
                performance_over_all.append([auc_s, auc_t, p_auc, prec_s, prec_t, recall_s, recall_t, f1_s, f1_t])

                com.logger.info("AUC (source) : {}".format(auc_s))
                com.logger.info("AUC (target) : {}".format(auc_t))
                com.logger.info("pAUC : {}".format(p_auc))
                com.logger.info("precision (source) : {}".format(prec_s))
                com.logger.info("precision (target) : {}".format(prec_t))
                com.logger.info("recall (source) : {}".format(recall_s))
                com.logger.info("recall (target) : {}".format(recall_t))
                com.logger.info("F1 score (source) : {}".format(f1_s))
                com.logger.info("F1 score (target) : {}".format(f1_t))

            print("\n============ END OF TEST FOR A SECTION ============")

        if mode:
            # calculate averages for AUCs and pAUCs
            amean_performance = np.mean(np.array(performance, dtype=float), axis=0)
            csv_lines.append(["arithmetic mean"] + list(amean_performance))
            hmean_performance = scipy.stats.hmean(np.maximum(np.array(performance, dtype=float), sys.float_info.epsilon), axis=0)
            csv_lines.append(["harmonic mean"] + list(hmean_performance))
            csv_lines.append([])

        del data
        del model
        keras_model.clear_session()
        gc.collect()

    if mode:
        csv_lines.append(["", "AUC (source)", "AUC (target)", "pAUC", 
                        "precision (source)", "precision (target)", "recall (source)", "recall (target)",
                        "F1 score (source)", "F1 score (target)"])      
                          
        # calculate averages for AUCs and pAUCs                        
        amean_performance = np.mean(np.array(performance_over_all, dtype=float), axis=0)
        csv_lines.append(["arithmetic mean over all machine types, sections, and domains"] + list(amean_performance))
        hmean_performance = scipy.stats.hmean(np.maximum(np.array(performance_over_all, dtype=float), sys.float_info.epsilon), axis=0)
        csv_lines.append(["harmonic mean over all machine types, sections, and domains"] + list(hmean_performance))
        csv_lines.append([])
        
        # output results
        result_path = "{result}/{file_name}".format(result=param["result_directory"], file_name=param["result_file"])
        com.logger.info("results -> {}".format(result_path))
        save_csv(save_file_path=result_path, save_data=csv_lines)
