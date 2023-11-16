FROM python:3.8.15
RUN apt-get update && apt-cache search jdk && apt-get install -y openjdk-11-jdk
RUN sudo apt-get install python3-pip -y \
    && pip install rapidfuzz
RUN java --version
COPY repo_setup.sh repo_setup.sh
RUN ./repo_setup.sh
WORKDIR /s2orc-doc2json
RUN ./scripts/setup_grobid.sh; exit 0
COPY parse_json.py parse_json.py
COPY container_run.sh container_run.sh
COPY run.sh run.sh
COPY merge_ttl_files.py merge_ttl_files.py
RUN mkdir /input_pdf_files
RUN mkdir /common
RUN mkdir /home/input_ttl_files
RUN mkdir /home/output_ttl_files
ENV PYTHONPATH=/s2orc-doc2json
CMD ./scripts/run_grobid.sh
