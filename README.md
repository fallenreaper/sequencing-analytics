# Information

## Requirements:
- Docker installed.
- python3 installed.

## How To:
- Processing your fa/fai files is done linearly and is automatic.  You will need to build a docker image with the attached Docker Image.  This is done by doing: `docker build -t bam-processing .` and will create an image you can use called "bam-processing".

you will need to run a container with an attached volume.  That Volume will need to have hg38.fa in it as well as all BAM files you want processed.  Each BAM file will take anywhere from 12 to 72 hours to process, so depending you may want to just run this 1 BAM file at a time.

```
docker run --name bam-instance -d -v /path/to/bam/folder:/data bam-processing
```

In our experimentation, i would have 3 different computers each running its own BAM file to maximize my resources.

this will run reditools with the hg38 genome against the bam file in order to create an output csv with a similar name to the bam file.  Instead it will be `{bamfile}_output.tsv`.  a TSV file is a Tab-Seperated Value file, similar to CSV, but instead of a comma, it is a tab character to seperate things.

Afterwards, you will run the resulting file against `analysis.py` in order to build the resulting dataset for you to make use of.  it will return a filename similar to input but end in `_analysis.json` and will tell you everything you will need.

### What is VCF Processing?
  It was used to trim up VCF Files such that they only contained relevant row data.  A and G respectively for REF and ALT properties.  This was useful for creating smaller datasets, but was not ideal for large sets as the entire object needs to live in RAM.  This was a primitive older tool, which was phased out as we needed different data.  To run this file you would need to have both Python3 installed as well as pandas.  It may be removed at a later time due to its earlier use cases.

## Step by Step for analysis
You have your TSV File, now what?
- Ensure you have Python3 installed.  You can open a terminal or command prompt to test the command `python3 --version` to verify.  if this works, you can move to the next step. It id does not you need to install python and add it to the path and try again.

now from the source code directory you can run: `python3 analysis.py myfile.tsv` and it will run and process the entire file.  This MAY Take 30 minutes, but is dependant on the size and it processes each line.  Initial attempts wanted me to use pandas, but i decided to keep it as vanilla as possible, since chunking data to handle ram limits, may cause issues regarding analysis requests.  I wanted to keep it open ended to data processing across numbers and a full set instead of chunked data which may create rounding errors.

The results will be placed in a json file.

- Now that your analysis is done, you can kill your docker container.  `docker rm -f bam-processing`  You have no need for it now that the data was processed.  