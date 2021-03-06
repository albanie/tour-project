import os
import csv

def get_paths(root_path, stage_id):
    """returns all required paths and ensures that 
    the path to each defirectory is valid."""
    paths = {}
    stage_str = str(stage_id)
    paths['tete'] = root_path + 'tete_frames/' + stage_str + '/'
    paths['dense_tete'] = root_path + 'dense_tete_frames/' + stage_str + '/'
    paths['log'] = root_path + 'camera_states/' + stage_str + '.pickle'
    paths['precis'] = root_path + 'precis_frames/' + stage_str + '/'
    paths['src_video'] = root_path + 'raw/Stage' + stage_str +'.m4v'
    paths['tmp_clusters'] = root_path + 'tmp_clusters/' + stage_str + '/'
    paths['faces'] = root_path + 'faces_with_gradients/' + stage_str + '/'
    paths['templates'] = root_path + 'templates/'
    paths['fused'] = root_path + 'ocr/fused/'
    paths['digit_model'] = root_path + 'ocr/model/'
    paths['test_figures'] = root_path + 'ocr/test_figures/' + stage_str + '/'
    paths['dlib_detector'] = root_path + 'dlib/cyclist_detector.svm'
    paths['digit_training_frames'] = root_path + 'ocr/digit_frames/training/'
    paths['digit_testing_frames'] = root_path + 'ocr/digit_frames/testing/'
    paths['strava'] = root_path + 'gradient_data/raw/Stage' + stage_str + ".tcx"
    paths['offset'] = find_offset(root_path, stage_id)
    paths['meta'] = root_path + 'meta/Stage' + stage_str + '.csv'
    paths['shot_boundaries'] = root_path + 'shot_boundaries/Stage' + stage_str + '.csv'
    paths['face_shots'] = root_path + 'face_shots/' + stage_str + '/'
    paths['face_tracks'] = root_path + 'face_tracks/' + stage_str + '/'
    paths['stage'] = stage_str    
    paths['annotations'] = root_path + 'camera_annotations/Stage' + stage_str + '.csv'
    directories = ['tete', 'dense_tete', 'precis', 'faces', 'tmp_clusters', 'templates', 'fused', 
                   'digit_model', 'test_figures', 'digit_training_frames', 'face_shots', 'face_tracks']
    for key in directories:
        if not os.path.exists(paths[key]):
            os.makedirs(paths[key]) 
    return paths

def find_offset(root_path, stage_id):
    """returns the offset that calibrates gps data with 
    official Tdf distances."""
    calibration_path = root_path + 'gradient_data/stage_calibrations.csv'
    with open(calibration_path, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        offsets = [row[-1] for row in reader]
    return float(offsets[int(stage_id)])

def get_jpgs_in_dir(image_dir):
    """returns list of the .jpg files in the given
    directory, together with the root path."""
    frames = []
    root = None
    for root, dirs, fnames in os.walk(image_dir):
        for fname in fnames:
            if is_img_name(fname):
                frames.append(fname)
        root = root
    return root, frames

def get_img_paths_in_dir(image_dir):
    """returns a list of full paths to .jpg files in 
    the given directory."""
    root, frames = get_jpgs_in_dir(image_dir)
    img_paths = [root + frame for frame in frames]
    return img_paths

def is_img_name(fname):
    """returns true if the file is a jpg and ignores
    hidden files sometimes created on ubuntu"""
    return fname.endswith('.jpg') and not fname[::-1].endswith('_.')

def get_target_dir(path, selected_time):
    target_dir = path + selected_time + '/'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir
