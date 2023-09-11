
# Banxico-SIE

This packages enables downloading economic and financial time series hosted on Banco de Mexico's Sistema de Informacion Economica (SIE) directly as a time-indexed Pandas DataFrame. Time series metadata is available on English and Spanish.

Credentials are required by the website to download data. Visit [Banxico's Sistema de Informacion Economica API website](https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en) to request a token.

**Disclaimer: This package is not institutionally endorsed by Banco de Mexico and does not constitute an official Python package to access Banco de Mexico's data. Banco de Mexico does not provide any support to this package and is not liable by its use.**


## Installation

Install Banxico-SIE with pip

```bash
  pip install Banxico-SIE
```
## Usage

```python


## Firstly, obtain a token from Banxico's website:
# https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en
banxico_token = "..."  # 64 characters long

from siebanxico import SIEBanxico

# Choose language of metadata by choosing locale="es" (Spanish) or locale="en" (English).
api_client = SIEBanxico(token=banxico_token, locale="es")

## Get a single time series:
# Visit Banxico's website to find the id of a certain time series. E.g., "SP1" is Monthly CPI.
# https://www.banxico.org.mx/SieInternet/defaultEnglish.do
df = api_client.getSeriesData("SP1")  # Get whole CPI time series
df = api_client.getSeriesData("SP1", startDate="2020-01-01", endDate="2020-12-31")  # Get time series for a date range
# Note: startDate and endDate must be in the format YYYY-MM-DD.

# df is a time-indexed Pandas DataFrame.
# Use Pandas functionalities to manipulate data and perform transformations.
# For example:
df.head()
df.diff()
df.pct_change(12)

## Get multiple time series:

# This list must contain the ids of the time series. Visit Banxico's website to find this.
# https://www.banxico.org.mx/SieInternet/defaultEnglish.do
list_series = ["SP1", "SF311408", "SF311418", "SF311433"]  # CPI, M1, M2, M3 (all in monthly frequency)
# Note: Periodicity of the time series must be identical!

# This function requires a pandas.offsets object for the periodicity argument.
# For monthly data use: pandas.offsets.MonthBegin(1)
# This is important because the library uses this object to create the dataframe's time index.
import pandas as pd

df = api_client.getSeriesDataFrame(list_series, startDate="2000-01-01", endDate="2023-07-31",
                                   periodicity=pd.offsets.MonthBegin(1))
# Note: startDate and endDate must be in the format YYYY-MM-DD.

# df is a time-indexed Pandas DataFrame.
# Use Pandas functionalities to manipulate data and perform transformations.
# For example:
df.head()
df.diff()
df.pct_change(12)

## Get series metadata:
metadata_df = api_client.getSeriesMetaData(list_series)

## Get last values for a list of series:
lastvalues_df = api_client.getSeriesCurrentValue(list_series)


```


## Authors

- [Ezequiel Piedras Romero](https://www.github.com/chekecocol)


## License

[MIT](https://choosealicense.com/licenses/mit/)

