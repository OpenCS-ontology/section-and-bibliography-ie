FROM python:3.8
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-11-jre
RUN java --version
COPY repo_setup.sh repo_setup.sh
RUN ./repo_setup.sh
WORKDIR /s2orc-doc2json
RUN ./scripts/setup_grobid.sh; exit 0
COPY parse_json.py parse_json.py
COPY run.sh run.sh
ENV PYTHONPATH=/s2orc-doc2json
CMD ./scripts/run_grobid.sh
