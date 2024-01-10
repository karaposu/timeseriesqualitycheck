import pandas as pd
from .signal_to_noise_ratio import SignalNoiseRatio
from time_pattern_cohesion_score import TPCS

# tpcs, scipy, numpy, pandas,

# check_quality requires a signal input pandas pd format. With at least 2 columns where y is where values are stored
# and ds where date information is stores

# END_OF_TIME parameter is useful when we have extra information about time period for the signal. F
# for example signal may have values until May but it should have values for april too.  In this case
# END_OF_TIME param help us determine possible missing values.

# MAX_LEN_MONTHS this parameter works similar way with END_OF_TIME parameter. However it's purpose is to
# gauge the existance of missing values from the beginning of defined data gathering period.

# function returns dict of values.\
#     cleaning_score_data_dict = {
#
#         "TPC_features": TPC_features,
#         "TPC_score": TPC_score,
#         "SNR_features": SNR_features,
#         "SNR_score": SNR_score,
#         "cleaning_score_weights": cleaning_score_weights,
#         "cleaning_score": cleaning_score,
#
#     }
# you can get any value you want, the final output key is "cleaning_score"

def check_quality(signal, MAX_LEN_MONTHS, END_OF_TIME=None, tpcs_limit_for_snr_calculation=3.5):
    assert isinstance(signal, pd.DataFrame)

    assert 'y' in signal.columns
    assert 'ds' in signal.columns

    y = signal["y"]

    x = signal["ds"].to_list()
    x = pd.to_datetime(x)

    # these weights are tested and working well. However you may adjust according to your need
    weights = {"contiguity_score": 0.5,
               "recent_contiguity_score": 3,
               "consistency_score": 0.8,
               "intra_consistency_score": 1

               }


    if END_OF_TIME:
        tpcs = TPCS(x, MAX_LEN_MONTHS, END_OF_TIME=END_OF_TIME, debug=False, return_details=False)
    else:
        last_date=x[-1]
        tpcs = TPCS(x, MAX_LEN_MONTHS, END_OF_TIME=last_date, debug=False, return_details=True)

    TPC_score, tpcs_details = tpcs.calculate_TPCS(weights=weights, printing=False)

    if TPC_score > tpcs_limit_for_snr_calculation:
        snr = SignalNoiseRatio()
        SNR_score, snr_details = snr.calculate_snr(y)
        outlier_count = len(snr_details["outliers"])

    else:

        snr_details = {}
        SNR_score = 0
        outlier_count = None
        snr_details["indices"] = None
        snr_details["strengths"] = None
        snr_details["outliers"] = None

    TPC_features = {'consistency': {'value': tpcs_details["consistency"],
                                    'weight': weights["consistency_score"],
                                    'weighted_value': tpcs_details["weighted_consistency"]
                                    },
                    'intra_consistency': {'value': tpcs_details["intra_consistency"],
                                          'weight': weights["intra_consistency_score"],
                                          'weighted_value': tpcs_details["weighted_intra_consistency"]
                                          },
                    'contiguity': {'value': tpcs_details["contiguity"],
                                   'weight': weights["contiguity_score"],
                                   'weighted_value': tpcs_details["weighted_contiguity"]
                                   },
                    'recent_contiguity': {'value': tpcs_details["recent_contiguity"],
                                          'weight': weights["recent_contiguity_score"],
                                          'weighted_value': tpcs_details["weighted_recent_contiguity"]
                                          }
                    }

    SNR_features = {'outlier_count': outlier_count,
                    'outlier_indices': snr_details["indices"],
                    'outliers': snr_details["outliers"],
                    'outlier_strengths': snr_details["strengths"]}



    TPC_weight = 0.5
    SNR_weight = 0.5

    cleaning_score_weights = {'TPC_weight': TPC_weight,
                              'SNR_weight': SNR_weight
                              }

    cleaning_score = (TPC_score + SNR_score) / 2
    cleaning_score = round(cleaning_score, 2)

    cleaning_score_data_dict = {

        "TPC_features": TPC_features,
        "TPC_score": TPC_score,
        "SNR_features": SNR_features,
        "SNR_score": SNR_score,
        "cleaning_score_weights": cleaning_score_weights,
        "cleaning_score": cleaning_score,

    }

    return cleaning_score_data_dict

