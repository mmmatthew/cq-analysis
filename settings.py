import os

if not os.path.isfile('env.py'):
    print('Error: create env.py file with SWMM executable location. Exiting application.')
    quit(1)
from env import *


class Settings(object):
    swmm_executable = SWMM_EXECUTABLE
    swmm_model_template = 'swmm_model_template_simple.inp'
    calibration_event = {}
    # list of periods to be used for validation
    validation_events = []
    sim_reporting_step_sec = 5  # in seconds
    forcing_data_file = 'data/all_p1_q_mid_endress_logi_no_outliers.txt'
    calibration_algorithm = 'sceua'
    calibration_parameters = {
        # 'r_surf': {
        #     "display_name": 'Surface roughness',
        #     'rank': 0,
        #     'bounds': [0, 0.03]
        # },
        'h_w1': {
            "display_name": 'Height of weir w1',
            'rank': 0,
            'bounds': [0.45, 0.55]
        },
        'r_px': {
            "display_name": 'Roughness (other pipes)',
            'rank': 1,
            'bounds': [0.005, 0.02]
        },
        'cd_m1': {
            "display_name": 'Discharge coefficient of manhole m1',
            'rank': 2,
            'bounds': [0.48, 0.72]
        },
        'cd_m3': {
            "display_name": 'Discharge coefficient of manhole m3',
            'rank': 3,
            'bounds': [0.42, 0.78]
        },
        'cd_r4': {
            "display_name": 'Discharge coefficient of outflow',
            'rank': 4,
            'bounds': [0.1, 0.72]
        },
        'cd_w1': {
            "display_name": 'Discharge coefficient of weir w1',
            'rank': 5,
            'bounds': [1.1, 2.1]
        },
        'r_p3': {
            "display_name": 'Roughness (pipe p3)',
            'rank': 6,
            'bounds': [0.009, 0.03]
        },
    }
    obs_available = {
        's6_sensor': {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',  # where to find data
            "location": 's6',  # code name of location
            "data_type": 'sensor',  # type of data source
            "scale_factor": 0.001,  # how to scale data so that it is comparable to model output
            "swmm_node": ['node', 's6', 'Depth_above_invert'],  # how to access model output
            "calibration": {
                "obj_fun": 'rmse',  # which objective function to use
                "weight": 1  # weight should be positive if obj_fun should be minimized (for spotpy 1.3.30)
            }
        }
        ,
        's5_sensor': {
            "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
            "location": 's5',
            "data_type": 'sensor',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        }
        ,
        's3_sensor': {
            "data_file": 'data/all_s3_h_us_maxbotix.txt',
            "location": 's3',
            "data_type": 'sensor',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        },
        's6_trend': {
            "data_file": 'data/all_s6_h_us_maxbotix_normalized.txt',
            "location": 's6',
            "data_type": 'trend',
            "scale_factor": 1,
            "swmm_node": ['node', 's6', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_simple_zero',
                "weight": -0.5,
                "zero_threshold_obs": 0.02,  # for spearman zero obj_fun, we define a
                "zero_threshold_sim": 0.02  # threshold below which the data and model are considered zero
            }
        }
        ,
        's5_trend': {
            "data_file": 'data/all_s5_h_us_maxbotix_2_normalized.txt',
            "location": 's5',
            "data_type": 'trend',
            "scale_factor": 1,
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_simple_zero',
                "weight": -0.5,
                "zero_threshold_obs": 0.02,  # for spearman zero obj_fun, we define a
                "zero_threshold_sim": 0.02  # threshold below which the data and model are considered zero
            }
        }
        ,
        's3_trend': {
            "data_file": 'data/all_s3_h_us_maxbotix_normalized.txt',
            "location": 's3',
            "data_type": 'trend',
            "scale_factor": 1,
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_simple_zero',
                "weight": -0.5,
                "zero_threshold_obs": 0.02,  # for spearman zero obj_fun, we define a
                "zero_threshold_sim": 0.02  # threshold below which the data and model are considered zero
            }
        }
    }
    obs_config_calibration = []
    # the list of observations that should be used to evaluate performance
    obs_config_validation = [
        's3_sensor',
        's5_sensor',
        's6_sensor'
    ]
