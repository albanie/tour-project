import os
import shutil
import pickle
from tqdm import *

from camera import Camera
from file_utils import get_img_paths_in_dir
from time_utils import get_time_from_path
from time_utils import get_times_in_interval
from time_utils import get_contiguous_intervals
from snapshot_utils import snapshot
from snapshot_utils import get_dar_dimensions
from snapshot_cluster import take_cluster_snapshots_at_targets
from file_utils import get_paths

def get_tete_images(paths):
    with open(paths['log'], 'rb') as f:
        camera_states_log = pickle.load(f)
    img_names = get_img_paths_in_dir(paths['precis'])
    labeled_imgs = zip(camera_states_log, sorted(img_names))
    tete_imgs = [img for (state, img) in labeled_imgs if state == Camera.Tete]
    return tete_imgs

def get_tete_intervals(paths):
    tete_imgs = get_tete_images(paths)
    times = [get_time_from_path(tete_img) for tete_img in tete_imgs]
    intervals = get_contiguous_intervals(times)
    return intervals   

def get_tete_target_frames(paths, step):
    intervals = get_tete_intervals(paths)
    if not intervals:
        return []
    target_lists = [get_times_in_interval(interval, step) for interval in intervals]
    targets = sum(target_lists, []) # flattens the list
    return targets

def extract_all_tete_frames(root_path, stage_id, step=40, DAR=(16.0 / 9.0)):
    paths = get_paths(root_path, stage_id)
    targets = get_tete_target_frames(paths, step)
    dar_dims = get_dar_dimensions(paths['src_video'], DAR=DAR)
    for time in tqdm(targets):
        snapshot(paths['src_video'], paths['tete'], stage_id, time=time, dimensions=dar_dims)

def extract_tete_snapshots(root_path, stage_id, step):
    paths = get_paths(root_path, stage_id)
    targets = get_tete_target_frames(paths, step)
    take_cluster_snapshots_at_targets(targets, paths, stage_id)
