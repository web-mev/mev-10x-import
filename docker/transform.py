#!/opt/conda/bin/python3

import pandas as pd
from scipy.io import mmread
import argparse
import gzip
import sys


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--matrix', \
        required=True, \
        dest = 'matrix',
        help='The matrix file'
    )
    parser.add_argument('-f', '--features', \
        required=True, \
        dest = 'features',
        help='The features file'
    )
    parser.add_argument('-b', '--barcodes', \
        required=True, \
        dest = 'barcodes',
        help='The barcodes file'
    )
    parser.add_argument('-o', '--output', \
        required=True, \
        dest = 'output_fname',
        help='The output filename'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    with gzip.open(args.matrix, 'rb') as fin:
        m = mmread(fin)

    with gzip.open(args.features, 'rb') as fin:
        features_df = pd.read_table(fin, header=None)

    feature_ids = features_df[0]

    if len(feature_ids) != m.shape[0]:
        sys.stderr.write(f'Dimensions of the matrix ({m.shape[0]}) and the features file ({len(feature_ids)}) do not match.')
        sys.exit(1)

    with gzip.open(args.barcodes, 'rb') as fin:
        barcodes = [x.decode('utf-8').strip() for x in fin.readlines()]

    if len(barcodes) != m.shape[1]:
        sys.stderr.write(f'Dimensions of the matrix ({m.shape[1]}) and the barcodes file ({len(barcodes)}) do not match.')
        sys.exit(1)

    df = pd.DataFrame.sparse.from_spmatrix(m, index=feature_ids, columns=barcodes)
    df.to_csv(args.output_fname, sep='\t')
