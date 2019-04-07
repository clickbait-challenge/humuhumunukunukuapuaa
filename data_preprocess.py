import json
import pandas as pd
import numpy as np

def generate_data(config_data_prefix, logger):
  all_config_keys = [key.lower() for key in list(logger.config_dict.keys()
    ) if config_data_prefix in key.lower()]

  folder_key  = [key for key in all_config_keys if "folder" in key][-1].upper()
  data_key    = [key for key in all_config_keys if "data" in key][-1].upper()
  targets_key = [key for key in all_config_keys if "targets" in key][-1].upper()

  data = []
  data_filename = logger.get_data_file(logger.config_dict[data_key], 
    logger.config_dict[folder_key])

  logger.log("Start reading data file from {} ...".format(data_filename))
  data_file = open(data_filename, mode = "r", encoding = "utf8")
  for line in data_file:
    data.append(json.loads(line))
  data_file.close()
  logger.log("Finish reading", show_time = True)

  targets = []
  targets_filename = logger.get_data_file(logger.config_dict[targets_key], 
    logger.config_dict[folder_key])
  logger.log("Start reading targets file from {} ...".format(targets_filename))
  targets_file = open(targets_filename, mode = "r", encoding = "utf8")
  for line in targets_file:
    targets.append(json.loads(line))
  targets_file.close()
  logger.log("Finish reading", show_time = True)

  dataset = []
  for element, target in zip(data, targets):
    dataset.append(element)
    dataset[-1]['clickBaitScore'] = target['truthMean']
  
  return dataset


def generate_final_training_dataset(config_data_prefix, logger):

  dataset = generate_data(config_data_prefix, logger)

  ids_list = [str(elem['id']) for elem in dataset]
  scores_list = [float(elem['clickBaitScore']) for elem in dataset]

  original_df   = pd.read_csv(logger.get_data_file(config_data_prefix + "_original.csv"))
  additional_df = pd.read_csv(logger.get_data_file(config_data_prefix + "_train.csv"))
  # TODO Also join Lorena's csv file

  logger.log("Dropping ID column from one dataframe")
  original_df.drop('id', inplace = True, axis = 1)
  additional_df.drop('ID', inplace = True, axis = 1)
  #additional_df.drop(['EMB_' + str(i) for i in range(1, 101)], axis = 1)


  logger.log("Concatenate dataframes")
  final_df = pd.concat([original_df, additional_df], axis = 1)
  logger.log("Add target column")
  final_df['Click_Bait'] = np.array(scores_list)
  final_df['ID'] = np.array(ids_list)
  logger.log("Feature cols {}".format([elem[:10] + ".." for elem in final_df.columns[:-2]]))
  logger.log("Final dataframe snippet \n {}".format(final_df.head()))

  return final_df

