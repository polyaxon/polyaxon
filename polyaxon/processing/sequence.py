# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from six.moves import xrange

import numpy as np


def pad_sequences(sequences, maxlen=None, dtype='int32', padding='pre', truncating='pre', value=0.):
    """Pads each sequence to the same length (length of the longest sequence).
    If maxlen is provided, any sequence longer
    than maxlen is truncated to maxlen.
    Truncation happens off either the beginning (default) or
    the end of the sequence.
    Supports post-padding and pre-padding (default).

    Args:
        sequences: list of lists where each element is a sequence.
        maxlen: int, maximum length.
        dtype: type to cast the resulting sequence.
        padding: 'pre' or 'post', pad either before or after each sequence.
        truncating: 'pre' or 'post', remove values from sequences larger than
            maxlen either in the beginning or in the end of the sequence
        value: float, value to pad the sequences to the desired value.

    Returns:
        x: `numpy array` with dimensions (number_of_sequences, maxlen)

    Raises:
        ValueError: in case of invalid values for `truncating` or `padding`,
            or in case of invalid shape for a `sequences` entry.

    Credits: Keras `pad_sequences` function.

    Examples:
        >>> sequences = [[1,1,1,1,1],[2,2,2],[3,3]]
        >>> sequences = pad_sequences(sequences, maxlen=None, dtype='int32',
        ...                  padding='post', truncating='pre', value=0.)
        ... [[1 1 1 1 1]
        ...  [2 2 2 0 0]
        ...  [3 3 0 0 0]]
    """
    lengths = [len(s) for s in sequences]

    nb_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for s in sequences:
        sample_shape = np.asarray(s).shape[1:]
        break

    x = (np.ones((nb_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if truncating == 'pre':
            trunc = s[-maxlen:]  # pylint: disable=invalid-unary-operand-type
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample {} of sequence at position {} '
                             'is different from expected shape {}'.format(trunc.shape[1:],
                                                                          idx,
                                                                          sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x


def process_sequences(sequences, end_token=0, pad_val=0, is_shorten=True, remain_end_id=False):
    """Set all tokens(ids) after END token to the padding value, and then shorten (option) it to
    the maximum sequence length in this batch.

    Args:
        sequences: `numpy array` or `list of list` with token IDs.
            e.g. [[4,3,5,3,2,2,2,2], [5,3,9,4,9,2,2,3]]
        end_token: `int`. the special token for END.
        pad_val: `int`. replace the end_id and the ids after end_id to this value.
        is_shorten: `boolean`. Shorten the sequences.
        remain_end_id: `boolean`. Keep an end_id in the end.

    Examples:
    ```python
    >>> sentences_ids = [[4, 3, 5, 3, 2, 2, 2, 2],  <-- end_id is 2
    ...                  [5, 3, 9, 4, 9, 2, 2, 3]]  <-- end_id is 2
    >>> sentences_ids = precess_sequences(sentences_ids, end_token=2,
    ...                                   pad_val=0, is_shorten=True)
    ... [[4, 3, 5, 3, 0], [5, 3, 9, 4, 9]]
    ```
    """
    max_length = 0
    for seq in sequences:
        is_end = False
        for i_token, token in enumerate(seq):
            if token == end_token and not is_end:  # 1st time to see end_id
                is_end = True
                if max_length < i_token:
                    max_length = i_token
                if not remain_end_id:
                    seq[i_token] = pad_val  # set end_id to pad_val
            elif is_end:
                seq[i_token] = pad_val

    if remain_end_id:
        max_length += 1
    if is_shorten:
        sequences = [seq[:max_length] for seq in sequences]
    return sequences


def sequences_add_start_token(sequences, start_token=0, remove_last=False):
    """Add special start token in the beginning of each sequence.

    Examples:
        ```python
        >>> sentences = [[4,3,5,3,2,2,2,2], [5,3,9,4,9,2,2,3]]
        >>> sentences = sequences_add_start_token(sentences, start_token=2)
        ... [[2, 4, 3, 5, 3, 2, 2, 2, 2], [2, 5, 3, 9, 4, 9, 2, 2, 3]]
        >>> sentences = sequences_add_start_token(sentences, start_token=2, remove_last=True)
        ... [[2, 4, 3, 5, 3, 2, 2, 2], [2, 5, 3, 9, 4, 9, 2, 2]]
        - For Seq2seq
        >>> input = [a, b, c]
        >>> target = [x, y, z]
        >>> decode_seq = [start_token, a, b] <-- sequences_add_start_token(input, start_token, True)
        ```
    """
    return [[start_token] + seq[:1] if remove_last else [start_token] + seq for seq in sequences]


def sequences_get_mask(sequences, pad_val=0):
    """Return mask for sequences.

    Examples:
        ```python
        >>> sentences_ids = [[4, 0, 5, 3, 0, 0],
        ...                  [5, 3, 9, 4, 9, 0]]
        >>> mask = sequences_get_mask(sentences_ids, pad_val=0)
        ... [[1 1 1 1 0 0]
        ...  [1 1 1 1 1 0]]
        ```
    """
    mask = np.ones_like(sequences)
    for i_seq, seq in enumerate(sequences):
        for i_token in xrange(len(seq) - 1, -1, -1):
            if seq[i_token] == pad_val:
                mask[i_seq, i_token] = 0
            else:
                break  # <-- exit the for loop, preprocess next sequence
    return mask
