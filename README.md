
# timeseriesqualitycheck

`timeseriesqualitycheck` is a Python package designed to assess the quality of time-series data. It provides a straightforward way to evaluate the integrity and cleanliness of time-series datasets by analyzing their Time Pattern Cohesion Score (TPCS) and Signal-to-Noise Ratio (SNR).

## Installation

To install `timeseriesqualitycheck`, simply use pip:

```python
pip install timeseriesqualitycheck
```



### check_quality Function 

- `check_quality` requires a signal input in pandas DataFrame format, with at least two columns:
  - `y`: column where the values of the signal are stored.
  - `ds`: column where the date information is stored.

- The `END_OF_TIME` parameter is useful when we have extra information about the time period for the signal. 
  For example, the signal may have values until May but should also include values for April. 
  The `END_OF_TIME` parameter helps determine possible missing values.

- The `MAX_LEN_MONTHS` parameter works in a similar way to the `END_OF_TIME` parameter. 
  However, its purpose is to gauge the existence of missing values from the beginning of the defined data gathering period.

- The function returns a dictionary of values:
  ```python
  cleaning_score_data_dict = {
      "TPC_features": TPC_features,
      "TPC_score": TPC_score,
      "SNR_features": SNR_features,
      "SNR_score": SNR_score,
      "cleaning_score_weights": cleaning_score_weights,
      "cleaning_score": cleaning_score,
  }
  ```
  You can access any value you need; the final output key is `"cleaning_score"`.


## Usage


```python
import pandas as pd
from timeseriesqualitycheck import check_quality

END_OF_TIME= pd.to_datetime("2021-05-01")
MAX_LEN_MONTHS=13

list_of_timestamps= ["2020-05-01","2020-06-01","2020-07-01","2020-08-01","2020-09-01","2020-10-01","2020-11-01","2020-12-01","2021-01-01", "2021-03-01","2021-04-01","2021-05-01" ]
#notice that "2021-02-01" is missing
list_of_timestamps= [pd.to_datetime(e) for  e in list_of_timestamps]

signal_values_for_timestamps=[20,30,40, 50,600, 70, 80, 70, 60, 50,40, 30 ]
#notice that we have an outlier(600) value


dict = {'ds': list_of_timestamps, 'y': signal_values_for_timestamps} 
df = pd.DataFrame(dict)

quality_report = check_quality(df, 12, '2023-12-31')
print(quality_report)
```


#### Description

The `check_quality` function evaluates the quality of a time-series signal. It analyzes the signal for pattern consistency, contiguity, and noise levels to produce a comprehensive quality score.

#### Syntax

```python
timeseriesqualitycheck.check_quality(signal, MAX_LEN_MONTHS, END_OF_TIME, snr_limit=3.5)
```

#### Parameters
- **signal** (`pd.DataFrame`): A pandas DataFrame containing the time-series data with 'y' and 'ds' columns.
- **MAX_LEN_MONTHS** (`int`): The maximum length of the time series in months.
- **END_OF_TIME** (`datetime`): The end date for the time series data.
- **snr_limit** (`float`, optional): The threshold for the signal-to-noise ratio. Default is 3.5.

#### Returns
- **dict**: A dictionary containing the cleanliness score, TPC and SNR features, and detailed scores.


## Contributing
Contributions to `timeseriesqualitycheck` are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License
This project is licensed under the [MIT License](LICENSE.txt).

# Additional Notes on check_quality Function:

