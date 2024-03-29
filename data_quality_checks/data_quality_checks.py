from datetime import datetime
import numpy as np
import pandas as pd
from typing import List, Union, Dict, Tuple


#########################################################
# 1. Accuracy
#########################################################

# Population stability index (PSI)
def check_psi(expected: pd.Series, actual: pd.Series, threshold: float, buckettype: str ='bins', buckets: int =10, axis: int =0) -> float:
    '''Calculate the PSI (population stability index) for a given column.
    Args:
       expected (pandas.Series): Pandas Series of original values
       actual (pandas.Series): Pandas Series of new values, same size as expected
       threshold (float): The threshold that needs to be met for a successful test.
       buckettype (string): type of strategy for creating buckets, bins splits into even splits, quantiles splits into quantile buckets
       buckets (integer): number of quantiles to use in bucketing variables
       axis (integer): axis by which variables are defined, 0 for vertical, 1 for horizontal
    Returns:
       psi_values (tuple): ndarray of psi values for each variable
    Author:
       Matthew Burke
       github.com/mwburke
       worksofchart.com
    '''

    def psi(expected_array: pd.Series, actual_array: pd.Series, buckets: int) -> Tuple[bool, float]:
        '''Calculate the PSI for a single variable
        Args:
           expected_array: numpy array of original values
           actual_array: numpy array of new values, same size as expected
           buckets: number of percentile ranges to bucket the values into
        Returns:
           A tuple with a boolean flag if the test passed and calculated PSI value
        '''

        def scale_range (input, min, max):
            input += -(np.min(input))
            input /= np.max(input) / (max - min)
            input += min
            return input


        breakpoints = np.arange(0, buckets + 1) / (buckets) * 100

        if buckettype == 'bins':
            breakpoints = scale_range(breakpoints, np.min(expected_array), np.max(expected_array))
        elif buckettype == 'quantiles':
            breakpoints = np.stack([np.percentile(expected_array, b) for b in breakpoints])



        expected_percents = np.histogram(expected_array, breakpoints)[0] / len(expected_array)
        actual_percents = np.histogram(actual_array, breakpoints)[0] / len(actual_array)

        def sub_psi(e_perc: float, a_perc: float) -> float:
            '''Calculate the actual PSI value from comparing the values.
               Update the actual value to a very small number if equal to zero
            '''
            a_perc = 0.0001 if a_perc == 0 else a_perc
            e_perc = 0.0001 if e_perc == 0 else e_perc

            return (e_perc - a_perc) * np.log(e_perc / a_perc)

        generator = (sub_psi(expected_percents[i], actual_percents[i]) for i in range(0, len(expected_percents)))
        psi_value = np.sum(np.fromiter(generator, dtype=float))

        return( psi_value>psi_value, psi_value )

    if len(expected.shape) == 1:
        psi_values = np.empty(len(expected.shape))
    else:
        psi_values = np.empty(expected.shape[axis])

    for i in range(0, len(psi_values)):
        if len(psi_values) == 1:
            psi_values = psi(expected, actual, buckets)
        elif axis == 0:
            psi_values[i] = psi(expected[:,i], actual[:,i], buckets)
        elif axis == 1:
            psi_values[i] = psi(expected[i,:], actual[i,:], buckets)

    return(psi_values)
  
# Evaluate if the input data has the correct data type for all columns
def check_data_types(data: pd.DataFrame, column_spec) -> Tuple[bool, List]:
    """
    Evaluates if the input data has the correct data types according to the column specification

    Parameters:
    data (dict): The input data
    column_spec (dict): The column specification with keys as column names and values as data types

    Returns:
     A tuple with a boolean indicating if the test passed and the columns with wrong data types
    """
    wrong_dtype_columns = []
    for column in data.columns:
        # Check if the column is specified in the column specification
        if column not in column_spec.keys():
            print(f"Column {column} is not available in specs.")
            wrong_dtype_columns = wrong_dtype_columns + [column]
        else:
          # Check if the value has the correct data type
          if not data[column].dtype == column_spec[column]:
              print(f"Column {column} is not the expected data type. Expected is {column_spec[column]} but is {data[column].dtype}")
              wrong_dtype_columns = wrong_dtype_columns + [column]
    
    return ( len(wrong_dtype_columns) == 0, wrong_dtype_columns )
  
  
def check_outlier_ratio(data: pd.DataFrame, threshold: Union[dict, float]) -> Tuple[bool, List]:
    '''Calculate the ratio of outliers for each column.
    
    Args:
      data (pd.DataFrame): DataFrame containing the data to be checked.
      threshold (Dict | Float): If all columns shall be tested on the same threshold a float is passed. Otherwise a dict needs to be specified with the column name as key and the threshold value as value.
    Returns:
      A tuple with a boolean indicating if the test passed and the columns with a high ratio of outliers.
    '''
    high_outlier_columns = []
    
    # outlier remover for histogram
    def iqr_outlier_filter(data, var):
      q3, q1 = np.nanpercentile(df[var], [75 ,25])
      iqr = q3 - q1

      lower_bound = q1 - 1.5 * iqr
      upper_bound = q3 + 1.5 * iqr

      f = df[(df[var]>=lower_bound) & (df[var]<=upper_bound)]

      return f
    
    for column in data.columns:
      
      # Remove outliers and calculate removed ratio
      cleaned_df = iqr_outlier_filter(data, column)
      ratio_of_removed_rows = (len(data)-len(cleaned_df)) / len(data)
      
      if type(threshold) == 'dict':
        if ratio_of_removed_rows > threshold[column]:
          print(f"Column {column} has too many outliers. A relative amount of {ratio_of_removed_rows} outliers have been observed. Expected were {threshold[column]}.")
          high_outlier_columns = high_outlier_columns + [column]
      else:
        if ratio_of_removed_rows > threshold:
          print(f"Column {column} has too many outliers. A relative amount of {ratio_of_removed_rows} outliers have been observed. Expected were {threshold}.")
          high_outlier_columns = high_outlier_columns + [column]
      
      return (len(high_outlier_columns) == 0, high_outlier_columns)
  
  
#########################################################
# 2. Completeness
#########################################################

# Check expected number of missing values
def check_perc_of_missing_values(data: pd.DataFrame, thresholds: Dict) -> Tuple[bool, List]:
  '''Calculate the relative amount of missing values in a column.
  Args:
    data (pd.DataFrame): DataFrame containing the data that needs to be checked.
    threshold (Dict): Dictionary containing the columns which are tested as keys and the threshold for missing values to be accepted.
  
  Returns:
    A tuple with a boolean indicating if the test passed and the columns with a high ratio of missing values.
  
  '''
  columns_w_missing_values = []
    
  for column in thresholds.keys():
      percent_missing = data[column].isnull().sum() / len(data)

      if percent_missing > thresholds[column]:
        print(f"Column {column} has more than the expected amount of missing values. {percent_missing} is missing, but threshold is {thresholds[column]}.")
        
        columns_w_missing_values = columns_w_missing_values + [column]
      else:
        print(f"Column {column} has less then the expected amount of missing values.")
    
  return (len(percent_missing) == 0, columns_w_missing_values)

#########################################################
# 3. Reliability
#########################################################

# Test Uniqueness
def check_uniqueness(data: pd.DataFrame, no_dup_columns: List) -> Tuple[bool, List]:
  '''Investigate if columns which are expected to have no duplicates, only contain unique values.
  
  Args:
    data (pd.DataFrame): DataFrame containing the data which needs to be checked.
    no_dup_columns (List): List of columns for which no duplication is expected.
    
  Returns:
    A tuple with a boolean indicating if the test passed and the columns with duplicated values.
  '''
  columns_with_dups = []
  
  for column in data.columns:
    if data[column].nunique() != len(data):
      print(f" Column {column} is expected to not have any duplications. {data[column].nunique()} unique values are observed but the data contains {len(data)} entries.")
      columns_with_dups + [column]
            
  return (len(columns_with_dups) == 0, columns_with_dups)


#########################################################
# 4. Timelineness
#########################################################

def check_data_freshness(data: pd.DataFrame, thresholds: Dict) -> Tuple[bool, Dict]:
  '''Check if all columns with dates are fresh.
  Args:
    data (pd.DataFrame): DataFrame containing the data that needs to be checked.
    thresholds (Dict({string : int})): The keys represent the column and the value the number of days that the most recent entry should not exceed.
  
  Returns:
        A tuple with a boolean indicating if the test passed and the columns with outdate columns.
  '''

  outdated_columns = {}

  def get_difference(date1, date2):
    delta = pd.to_datetime(date2) - pd.to_datetime(date1)
    return delta.days

  for column in thresholds.keys():
    days_diff = get_difference(data[column].max(), datetime.now().date())

    if days_diff> thresholds[column]:
      print(f"Column {column} has outdated data. The most recent entry is {days_diff} days old but {thresholds[column]} is maximum accepted.")
      outdated_columns[column] = days_diff

  return ( len(outdated_columns.keys())==0, outdated_columns)
