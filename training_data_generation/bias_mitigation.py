from typing import List
import pandas as pd
from sklearn.utils import resample

######################################################
# 1. Sampling methods
######################################################



# Simple over and under sampling
def sample_dataset(data: pd.DataFrame, majority_class: str, minority_classes: List , split_column: str ,downsample = True) -> pd.DataFrame:
  '''Sample the classes up/down equally by replicating existing rows. If downsample = True, the data will be downsampled to the class with the fewest instances. 
     If downsample=False, the minority classes will be randomly replicated to meet the majority class count. This function will not add artificially created data.
  
  Args:
    data (pd.DataFrame): DataFrame containing the data
    majority_class (str): Name of the majority class
    minority_class (List): List containing the names of all minority classes
    split_column (str): Name of the column containing the classes
    downsample (bool): Flag if the data will be downsampled or upsampled
    
   Returns:
    A resampled DataFrame.
  '''
  
  # Create an empty dataframe that will contain the sampled output
  sampled_data = pd.DataFrame()

  if downsample:

    # Save minority class count and corresponding class
    class_count = len(data[data[split_column] == majority_class]) # take majority class a starting point
    class_name = None

    # Investigate which column has the fewest instances and use the count and name for sampling.
    for classes in minority_classes:
      class_name = classes if (len(data[data[split_column] == classes]) < class_count) else class_name
      class_count = len(data[data[split_column] == classes]) if (len(data[data[split_column] == classes]) < class_count) else class_count
      
  else: 

    # Save majority class count and corresponding class
    class_count = len(data[data[split_column] == majority_class])
    class_name = majority_class
    
  # Sample classes
  for classes in [majority_class] + minority_classes:
    
    if classes != class_name:
      downsampled = resample(data[data[split_column]== classes],
            replace=True,
            n_samples=class_count,
            random_state=42)
      
      sampled_data = sampled_data.append(downsampled)
    else:
      sampled_data = sampled_data.append(data[data[split_column] == classes])

  return sampled_data


    

