#/bin/python3
import sys
import io
import pandas as pd

def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    )

def write_vcf(path, df):
  with open(f'{path}', 'r') as f:
    lines = [ l for l in f if l.startswith("##") ]
  with open(f'NEW_{path}', 'w') as f:
    f.writelines(lines)
  df.to_csv(f'NEW_{path}', sep='\t', mode='a', index=False)

if __name__ == "__main__":
  # Load a CSV into Base Dataframe.
  if len(sys.argv) < 2:
    print("--- Needs a Filename.  Exiting.")
    print("    File needs to be a Tab Delimited varient on a CSV. ( Reditools outputs a tab delimited file )")
    print("    You may feed absolute or Relative path from pwd.")
    exit(1)
  f = sys.argv[1]
  df = read_vcf(f)
  subset = df[ (df["REF"] == 'A') & (df["ALT"] == 'G') ]
  write_vcf(f, subset)
