FROM mambaorg/micromamba

# for building the conda env
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
# Build the environment based on the yml file
RUN micromamba install -y -n base -f /tmp/environment.yml \
  && micromamba clean --all --yes

ADD transform.py /usr/local/bin
ADD run.sh /usr/local/bin
USER root
RUN chmod +x /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/transform.py
USER $MAMBA_USER