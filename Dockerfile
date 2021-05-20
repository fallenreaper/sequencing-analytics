FROM debian:latest

RUN apt-get update

RUN mkdir /data 

# Environment:
RUN apt-get install -y git python-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip zlib1g zlib1g-dev libbz2-dev zlib1g-dev libncurses5-dev libncursesw5-dev liblzma-dev samtools tabix libopenmpi-dev
# apt-get install -y zlib-devel zlib # may fail
RUN cd /opt && git clone https://github.com/tflati/reditools2.0.git
RUN cd /opt/reditools2.0/ && pip install -r requirements.txt 

COPY run.sh /opt/run.sh
RUN chmod 771 /opt/run.sh

CMD ["cd", "/opt", "&&", "./run.sh"]
