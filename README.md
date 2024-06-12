# mev-10x-import

This repository contains a WebMeV-compatible tool for combining the sparse/matrix-market formats distributed by 10X Genomics into a text-based tab-delimited file.

---

### To run external of WebMeV:

Either:
- build the Docker image using the contents of the `docker/` folder (e.g. `docker build -t myuser/10x_import:v1 .`) 
- pull the docker image from the GitHub container repository

To run, we assume you are located in a directory where you have the required files:
- `matrix.mtx.gz`
- `features.tsv.gz`
- `barcodes.tsv.gz`

These are usually located in a folder named `"feature_bc_matrix"` or `"filtered_feature_bc_matrix"`. Note that these are assumed to be gzip-compressed (typically, this is how they are distributed)

Then run:
```
docker run -it -v $PWD:/work <IMAGE> /usr/local/bin/run.sh \
    /work/<barcodes filename> \
    /work/<features filename> \
    /work/<matrix filename> \
    /work/<output TSV filename>
```
(here, we mount the current directory to `/work` inside the container so your files will be located in the `/work` directory)

The call to `run.sh` will double-check that files are gzip-compressed. Alternatively, you can call the python script directly, which bypasses the gzip sanity check:
```
docker run -it -v $PWD:/work <IMAGE> /usr/local/bin/transform.py \
    -b /work/<barcodes filename> \
    -f /work/<features filename> \
    -m /work/<matrix filename> \
    -o /work/<output TSV filename>
```
A successful run will place a tab-delimited file in your current working directory. Note that due to the typically sparse nature of single-cell and spatial transcriptomics datasets, the majority of this matrix will be zeros...this is why the sparse matrix format is advantageous, but sometimes we have no option other than to use a flat-file matrix.