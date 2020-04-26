from itertools import cycle
from torch.utils.data import IterableDataset
import pandas as pd
import numpy as np


class MyIterableDataset(IterableDataset):
    TOKENS_INDEX = 0
    REPLIED_INDEX = 1
    RETWEETED_INDEX = 2
    RETWEETED_WITH_COMMENT_INDEX = 3
    LIKE_INDEX = 4

    def __init__(self, file_path):
        self.max_token_len = pd.read_csv(file_path, header=None)[0].apply(lambda x: x.count("\t") + 1).max()
        self.file_path = file_path

    def parse_file(self, file_path):
        with open(file_path, encoding="utf-8") as fileobject:
            for line in fileobject:
                features = line.strip().split("\x01")
                tokens = np.fromstring(features[0], sep="\t", dtype=int)
                yield [
                    np.concatenate((tokens, np.zeros(self.max_token_len - len(tokens), dtype=int))),
                    1 if features[20] else 0,
                    1 if features[21] else 0,
                    1 if features[22] else 0,
                    1 if features[23] else 0
                ]

    def get_stream(self, file_path):
        return cycle(self.parse_file(file_path))

    def __iter__(self):
        return self.get_stream(self.file_path)
