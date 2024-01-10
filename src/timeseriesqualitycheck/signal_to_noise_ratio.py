import numpy as np
import scipy.stats as stats

class SignalNoiseRatio:
    def __init__(self, debug=False, ):

        self.SNR_COMPATIBLE = False
        self.debug = debug

    def find_index_of_outliers(self, y, z_threshold):

        z_scores = abs(stats.zscore(y))
        filter_arr = z_scores > z_threshold
        indexes_of_outliers = np.where(filter_arr == True)[0]

        return indexes_of_outliers

    def find_index_and_strength_of_outliers(self, signal):
        indexes_of_outliers = self.find_index_of_outliers(signal, 3)

        no_outlier_signal = signal.copy()
        for indx in indexes_of_outliers:
            no_outlier_signal[indx] = 0
        no_outlier_signal_mean = sum(no_outlier_signal) / (len(signal) - len(indexes_of_outliers))
        no_outlier_signal_std = np.std(no_outlier_signal)

        outlier_strengths = []
        for indx in indexes_of_outliers:
            outlier_value = signal[indx]
            outlier_strength = (outlier_value - no_outlier_signal_mean) / no_outlier_signal_std
            outlier_strengths.append(round(outlier_strength, 2))

        recency_of_outliers = [round(i / len(signal), 2) for i in indexes_of_outliers]

        return indexes_of_outliers, recency_of_outliers, outlier_strengths

    def calculate_snr(self, signal):

        indexes_of_outliers, recency_of_outliers, outlier_strengths = self.find_index_and_strength_of_outliers(signal)

        noise_scores = []
        for r, s in zip(recency_of_outliers, outlier_strengths):
            STRENGTH_coeff = 3
            # 3 is used because outlier detection assumes normal distribution and 3 ((signal_point-signal_mean)/ std) is the limit to detect outliers.
            # STRENGTH_coeff=5
            noise = r * ((1 - STRENGTH_coeff / s) ** 0.5 * 5)
            noise_scores.append(round(noise, 2))

        if self.debug == True:
            print("recency_of_outliers:", recency_of_outliers)
            print("strengths:", outlier_strengths)
            print("noise_scores:", noise_scores)

        outliers = signal[indexes_of_outliers].to_list()

        snr = 5 - sum(noise_scores)
        snr = round(snr, 2)
        snr = float(snr)

        snr_details = {
            "indices": indexes_of_outliers,
            "strengths": outlier_strengths,
            "outliers": outliers

        }

        # snr_results=SNRResults(snr,snr_details)

        return snr, snr_details


