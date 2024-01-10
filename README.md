
# timeseriesqualitycheck

`timeseriesqualitycheck` is a Python package designed to assess the quality of time-series data. It provides a straightforward way to evaluate the integrity and cleanliness of time-series datasets by analyzing their Time Pattern Cohesion Score (TPCS) and Signal-to-Noise Ratio (SNR).

## Installation

To install `timeseriesqualitycheck`, simply use pip:

```bash
pip install timeseriesqualitycheck
```

## Usage

### check_quality Function

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

#### Example

```python
import pandas as pd
from timeseriesqualitycheck import check_quality

# Sample time-series data
data = {'ds': ['2023-01-01', '2023-01-02', ...], 'y': [123, 150, ...]}
signal = pd.DataFrame(data)

# Perform quality check
quality_report = check_quality(signal, 12, '2023-12-31')
print(quality_report)
```

## Contributing
Contributions to `timeseriesqualitycheck` are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License
This project is licensed under the [MIT License](LICENSE.txt).

# Additional Notes on check_quality Function:

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
