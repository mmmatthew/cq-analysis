class Settings(object):
    swmm_model_template = 'swmm_model_template.inp'
    calibration_event = {}
    # list of periods to be used for validation
    validation_events = []
    sim_reporting_step_sec = 5  # in seconds
    forcing_data_file = 'data/all_p1_q_mid_endress_logi.txt'
    calibration_algorithm = 'sceua'
    calibration_parameters = {
        # 'r_surf': {
        #     "display_name": 'Surface roughness',
        #     'rank': 0,
        #     'bounds': [0, 0.03]
        # },
        'r_p3': {
            "display_name": 'Roughness (pipe p3)',
            'rank': 1,
            'bounds': [0.009, 0.03]
        },
        'r_px': {
            "display_name": 'Roughness (other pipes)',
            'rank': 2,
            'bounds': [0.009, 0.03]
        },
        'cd_m1': {
            "display_name": 'Discharge coefficient of manhole m1',
            'rank': 3,
            'bounds': [0.48, 0.72]
        },
        'cd_m2': {
            "display_name": 'Discharge coefficient of manhole m2',
            'rank': 4,
            'bounds': [0.48, 0.72]
        },
        'cd_m3': {
            "display_name": 'Discharge coefficient of manhole m3',
            'rank': 5,
            'bounds': [0.48, 0.72]
        },
        'cd_r4': {
            "display_name": 'Discharge coefficient of outflow',
            'rank': 6,
            'bounds': [0.48, 0.72]
        },
        'cd_r6': {
            "display_name": 'Discharge coefficient of outflow to basement',
            'rank': 7,
            'bounds': [0.48, 0.72]
        },
        'd_s6': {
            "display_name": 'Basement floor depth',
            'rank': 8,
            'bounds': [0.01, 0.1]
        },
    }
    obs_available = {
        's6_sensor': {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',
            "location": 's6',
            "data_type": 'sensor',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's6', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1  # 1.3.30: weight should be positive if obj_fun should be minimized
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
        'c3_sensor': {
            "data_file": 'data/all_c3_v_radar_nivus.txt',
            "location": 'c3',
            "data_type": 'sensor',
            "scale_factor": 1,
            "swmm_node": ['link', 'c3', 'Flow_velocity'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        },
        's6_trend': {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',
            "location": 's6',
            "data_type": 'trend',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's6', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -0.5  # for spotpy 1.4.5: weight should be positive if obj_fun should be maximized
            }
        }
        ,
        's5_trend': {
            "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
            "location": 's5',
            "data_type": 'trend',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -0.5
            }
        }
        ,
        's3_trend': {
            "data_file": 'data/all_s3_h_us_maxbotix.txt',
            "location": 's3',
            "data_type": 'trend',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -0.5
            }
        },
        'c3_trend': {
            "data_file": 'data/all_c3_v_radar_nivus.txt',
            "location": 'c3',
            "data_type": 'trend',
            "scale_factor": 1,
            "swmm_node": ['link', 'c3', 'Flow_velocity'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -0.5
            }
        }
    }
    obs_config_calibration = []
    # the list of observations that should be used to evaluate performance
    obs_config_validation = [
        's3_sensor',
        's5_sensor',
        's6_sensor',
        'c3_sensor'
    ]
