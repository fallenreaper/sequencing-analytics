#/bin/python3
# from pandas import DataFrame
# import pandas as pd
import sys
import functools
import json
from pprint import pprint
# from collections import defaultdict

# # (1) Count all 'A' in Reference where MeanQ >= 20
# def count_a_with_ge_20_meanq(df: DataFrame) -> int:
#   return len(get_df_with_ge_20_meanq(df))

# def get_df_with_ge_20_meanq(df: DataFrame) -> DataFrame:
#   return df[ (df['Reference'] == 'A') & (df['MeanQ'] >= 20)]

# def get_df_for_allsubs_equals_g_from_meanq_ge_20(df: DataFrame) -> DataFrame:
#   _df = get_df_with_ge_20_meanq(df)
#   return _df[ _df['AllSubs'] == 'G' ]

# # (2) Count all 'AllSubs' == 'G' as a subset of (1)
# def count_df_for_allsubs_equals_g_from_meanq_ge_20(df: DataFrame) -> int:
#   return len(get_df_for_allsubs_equals_g_from_meanq_ge_20(df))

# def get_df_for_allsubs_containing_g(df: DataFrame) -> DataFrame:
#   _df = get_df_with_ge_20_meanq(df)
#   return _df[ df['AllSubs'].str.contains('G') ]

# # (3) Count all 'AllSubs' CONTAINING 'G' as a subset of (1)
# def count_df_for_allsubs_containing_g(df: DataFrame) -> int:
#   return len(get_df_for_allsubs_containing_g(df))

# def load_file(filename: str) -> DataFrame:
#   return pd.read_csv(filename,sep="\t")

# def sum_basecount_for_all_rows(df: DataFrame) -> int:
#   count = 0
#   for idx, row in df.iterrows():
#     arr = json.loads(row['BaseCount[A,C,G,T]'])
#     count = count + functools.reduce( lambda a,b: a+b, arr)
#   return count

# def sum_basecount_g_for_all_rows(df: DataFrame) -> int:
#   count = 0
#   for idx, row in df.iterrows():
#     arr = json.loads(row['BaseCount[A,C,G,T]'])
#     count = count + arr[2]
#   return count

# if __name__ == '__main__':
#   # Load a CSV into Base Dataframe.
#   #   [Key Note]  This reqquires us to store the full dataset in memory, per the rules of Pandas.
#   #               This is not good doe insanely large files as it would take like 3-5 minutes to load a 12G file.
#   #               To remove file sizes from the equation and that the values arent Insane, we will need to count line by line.
#   if len(sys.argv) < 2:
#     print("--- Needs a Filename.  Exiting.")
#     print("    File needs to be a Tab Delimited varient on a CSV. ( Reditools outputs a tab delimited file )")
#     print("    You may feed absolute or Relative path from pwd.")
#     exit(1)
#   f = sys.argv[1]
#   print(f"Loading '{f}'...")
#   df = load_file(f)
#   print("...Loaded.")
#   # Make sure required Columns exist.
#   if not not ( set(['BaseCount[A,C,G,T]', 'AllSubs', 'Reference', 'MeanQ']) - set(df.columns) ):
#     print("--- Dataframe does not contain relevant required columns. { Reference, MeanQ, AllSubs }")
#     exit(1)
#   _1 = get_df_for_allsubs_containing_g(df)
#   print( f"1. Count of all 'A' in 'Reference' where MeanQ >= 20: {len(_1)}")
#   # instead of me passing in FULL DF, since i already have a trimmed set, am using this to speed it up.
#   #  Sure it still checks that the items and calls the same function but the row count is trimmed so it executes faster.
#   _2 = count_df_for_allsubs_equals_g_from_meanq_ge_20(_1)
#   print( f"2. Count of all 'AllSubs' == 'G' as a subset of (1): {_2}")
#   # instead of me passing in FULL DF, since i already have a trimmed set, am using this to speed it up.
#   #  Sure it still checks that the items and calls the same function but the row count is trimmed so it executes faster.
#   _3 = count_df_for_allsubs_containing_g(_1)
#   print( f"3. Count of all 'AllSubs' CONTAINING 'G' as a subset of (1): {_3}")
#   # Get a dataframe filtered based on 'A', MeanQ>=30, Coverage-q30>=30
#   _filtered = df[ (df['Reference'] == 'A') & (df['Coverage-q30'] > 30) & (df['MeanQ'] > 30)]
#   # Sum each Array up, and sum for EACH item in df.
#   resulting_bases = sum_basecount_for_all_rows(_filtered)
#   print( f"4. Sum all bases in EVERY row, for Reference 'A', and both MeanQ and Coverage-q30 >=30: {resulting_bases}")
#   # Sum all G with an Additional Filter of AllSubs being AG:
#   _filteredAG = _filtered[ _filtered['AllSubs'] == 'AG' ]
#   resulting_baseG = sum_basecount_g_for_all_rows(_filteredAG)
#   print( f"5. Sum all G Bases in EVERY row, for Reference 'A', AllSubs 'AG', MeanQ and Coverage-q30 >= 30: {resulting_baseG}")
#   # Min and Max of Frequency COLUMN, given AllSubs==AG, Reference A, MeanQ and Coverage-q30 >= 30
#   # 
#   # Sum Cell 0 of BaseCount Array, in Reference A, Coverage-q30 and MeanQ >= 30
#   # 
#   # 4. 783937043 is the sum of all basees across 4348064 rows meeting the (4) criteria
#   # 5. 439245 is number of G, across 100824 rows meeting the (5) criteria.


def process_large_file(filename: str, referenceCompare = 'A', allSubsCompare='G'):
  _results = {}
  _results["sum_bases30"] = 0
  _results[f"sum_{allSubsCompare}30"] = 0
  _results["sum_bases20"] = 0
  _results[f"sum_{allSubsCompare}20"] = 0

  _results[f"count_number_of_entries_where_{referenceCompare}"] = 0
  _results[f"count_all_rows_where_allsubs_eq_{allSubsCompare}"] = 0
  _results[f"count_all_rows_where_allsubs_contains_{allSubsCompare}"] = 0
  _results["min_frequency"] = None
  _results["max_frequency"] = None
  _results[f"sum_{referenceCompare}_from_baseCount_ref_eq_{referenceCompare}_and_meanqcoverage_gte_30"] = 0

  # [ A, C, G, T]
  baseCodes = [ 'A', 'C', 'G', 'T']
  try:
    _location_index = baseCodes.index(allSubsCompare)
  except ValueError as e:
    print("AllSubsCompare Property Does not Exist in [A,C,G,T].")
    return {}
  with open(filename, "r") as fp:
    line = fp.readline()
    print(f"Header Data:\n{line}")
    while line != "":
      line = fp.readline()
      if line == "":
        break
      line = line[:-1] # The last character in readline is a \n which we want to remove. from the string, as a previous iteration auto trimmed the character.
      data = line.split("\t")
      _region, _position, _reference, _strand, _coverageq30, _meanq, _baseCount, _allsubs, _frequency, _gcoverageq30, _gmeanq, _gbaseCount, _gAllSubs, _gFrequency = data
      _reference = data[2] or None
      _coverageq30 = float(_coverageq30) or -1
      _meanq = float(_meanq) or -1
      _frequency = float(_frequency) or None
      if _reference == referenceCompare:
        
        _baseCount = json.loads(_baseCount) # Converts _baseCount from json array to python list.
        if _meanq >= 20:
          # Reference = 'A' and MeanQ >= 20
          _results[f"count_number_of_entries_where_{referenceCompare}"] += 1
          if _allsubs == allSubsCompare:
            # Reference = 'A' and MeanQ >= 20, AllSubs == 'G'
            _results[f"count_all_rows_where_allsubs_eq_{allSubsCompare}"] += 1
          if allSubsCompare in _allsubs:
            # Reference = 'A' and MeanQ >= 20, AllSubs CONTAINS 'AG'
            _results[f'count_all_rows_where_allsubs_contains_{allSubsCompare}'] += 1
        if _coverageq30 >= 20 and _meanq >= 20:
          # Reference = 'A', CoverageQ30 >= 20, MeanQ >= 20
          _results["sum_bases20"] += functools.reduce( lambda a,b: a+b, _baseCount)
          if _allsubs == f'{referenceCompare}{allSubsCompare}':
            # Reference = 'A', CoverageQ30 > 20, MeanQ >= 20, AllSubs = 'AG'
            _results[f"sum_{allSubsCompare}20"] += _baseCount[_location_index]
        if _coverageq30 >= 30 and _meanq >= 30:
          # Reference = 'A', CoverageQ30 >= 30, MeanQ >= 30
          _results["sum_bases30"]  += functools.reduce( lambda a,b: a+b, _baseCount)
          _results[f"sum_{referenceCompare}_from_baseCount_ref_eq_{referenceCompare}_and_meanqcoverage_gte_30"] += _baseCount[0]
          if _allsubs == f'{referenceCompare}{allSubsCompare}':
            # Reference = 'A', CoverageQ30 > 30, MeanQ >= 30, AllSubs = 'AG'
            _results[f"sum_{allSubsCompare}30"] += _baseCount[_location_index]
            if _frequency is not None:
              if _results["min_frequency"] is None:
                _results["min_frequency"] = _frequency
              if _frequency < _results['min_frequency']:
                _results["min_frequency"] = _frequency
              if  _results['max_frequency'] is None:
                _results['max_frequency'] = _frequency
              if _frequency > _results['max_frequency']:
                _results['max_frequency'] = _frequency
  return _results

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("--- Needs a Filename.  Exiting.")
    print("    File needs to be a Tab Delimited Value file, a TSV. ( Reditools outputs a tab delimited file )")
    print("    You may feed absolute or Relative path from pwd.")
    exit(1)
  f = sys.argv[1]
  print("Running AG Processing...")
  agRep = process_large_file(f)
  print("A-G DataDump: ")
  pprint(agRep)
  print("Running TC Processing...")
  tcRep = process_large_file(f, referenceCompare='T', allSubsCompare='C')
  print("T->C DataDump")
  pprint(tcRep)

  open(f'{f}_analysis.json', 'w') as fp:
    json.dump({"AG": agRep, "TC": tcRep}, fp, indent=4)

  print("Done!")
