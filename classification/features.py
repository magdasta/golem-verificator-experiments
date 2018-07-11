import os
import pickle
import itertools
import collections

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def get_feature_labels_path():
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), "../feature_labels"))

def get_all_feature_labels():
    with open(os.path.join(
            get_feature_labels_path(), 'all_feature_labels.pickle'), 'rb') as handle:
        return pickle.load(handle)

def get_train_feature_labels():
    with open(os.path.join(
            get_feature_labels_path(), 'train_feature_labels.pickle'), 'rb') as handle:
        return pickle.load(handle)

def save_all_feature_labels(features):
    labels = [feature.get_labels() for feature in features]
    with open(os.path.join(
            get_feature_labels_path(), 'all_feature_labels.pickle'), 'wb') as handle:
        pickle.dump(list(flatten(labels)), handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_train_feature_list(feature_list):
    with open(os.path.join(
            get_feature_labels_path(), 'train_feature_labels.pickle'), 'wb') as handle:
        pickle.dump(feature_list, handle, protocol=pickle.HIGHEST_PROTOCOL)