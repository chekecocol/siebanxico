import requests
import pandas as pd

class SIEBanxico():

    def _verify_idSeries(self, idSeries):

        if isinstance(idSeries, list):
            idSeriesString = ",".join(idSeries)
        elif isinstance(idSeries, str):
            idSeriesString = idSeries
        else:
            raise TypeError("idSeries must be either string or list of strings.")

        return idSeriesString

    def __init__(self, token, locale = "en"):

        self.setToken(token)
        self.setLocale(locale)

        self.ApiBaseUrl = "https://www.banxico.org.mx/SieAPIRest/service/v1/"

    def getSeriesData(self, idSeries, startDate = None, endDate = None):

        if not isinstance(idSeries, str):
            raise Exception("This method only supports a single idSeries formatted as string.")

        if isinstance(startDate, str) and isinstance(endDate, str):
            url = f"{self.ApiBaseUrl}series/{idSeries}/datos/{startDate}/{endDate}?token={self.token}&locale={self.locale}"
        else:
            url = f"{self.ApiBaseUrl}series/{idSeries}/datos?token={self.token}&locale={self.locale}"

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("SIE returned error code.")

        jsonData = response.json()
        df = pd.json_normalize(jsonData['bmx']['series'], record_path = 'datos', meta = ['idSerie', 'titulo'])

        series = pd.DataFrame(df[["fecha","dato"]], copy = True)
        series.index = pd.to_datetime(series["fecha"], dayfirst = True)
        series = series[["dato"]]
        series["dato"] = pd.to_numeric(series["dato"].astype(str).str.replace(',',''))
        series.columns = pd.MultiIndex.from_arrays([[df["idSerie"].iloc[0]],[df["titulo"].iloc[0]]])

        series = series.sort_index()

        if self.locale == "en":
            series.index.name = "date"

        return series

    def getSeriesDataFrame(self, idSeries, periodicity, startDate, endDate):
        """
        Warning: the whole list idSeries must have the same periodicity for this function to work as expected.
        """

        if not isinstance(periodicity, pd.offsets.BaseOffset):
            raise TypeError("periodicity must be specified as an instance of pandas.offsets.")

        if not isinstance(idSeries, list):
            raise TypeError("idSeries must be a list of str specifying the series to download.")

        df = pd.DataFrame(index = pd.date_range(start = startDate, end = endDate, freq = periodicity),
                          columns = pd.MultiIndex.from_product([["empty"],["empty"]]))

        for id in idSeries:
            series = self.getSeriesData(id, startDate, endDate)
            df = df.merge(series, how = "left", left_index = True, right_index = True)

        df = df.drop(columns = ("empty","empty"))

        return df.copy()


    def getSeriesMetaData(self, idSeries):

        idSeriesString = self._verify_idSeries(idSeries)

        url = f"{self.ApiBaseUrl}series/{idSeriesString}?token={self.token}&locale={self.locale}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("SIE returned error code.")

        jsonData = response.json()
        df = pd.json_normalize(jsonData['bmx']['series'], meta = ['idSerie', 'titulo', 'fechaInicio',
                                                                  'fechaFin', 'periodicidad', 'cifra',
                                                                  'unidad', 'versionada'])

        if self.locale == "en":
            columnNames = ["id","description","start date","end date","periodicity","type","unit","versioned"]
        elif self.locale == "es":
            columnNames = ["id","descripcion","fecha inicio","fecha fin","periodicidad","tipo","unidad","versionada"]
        else:
            raise Exception("Locale is badly specified. Must be either 'en' or 'es'.")

        df.columns = columnNames

        return df

    def getSeriesCurrentValue(self, idSeries):

        idSeriesString = self._verify_idSeries(idSeries)

        url = f"{self.ApiBaseUrl}series/{idSeriesString}/datos/oportuno?token={self.token}&locale={self.locale}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("SIE returned error code.")

        jsonData = response.json()
        df = pd.json_normalize(jsonData['bmx']['series'], record_path = 'datos', meta = ['idSerie', 'titulo'])

        columnNames = ["date","data","id","description"] if self.locale == "en" else ["fecha","datos","id","descripcion"]
        df.columns = columnNames

        return df

    def setToken(self, token):

        if len(token) != 64:
            raise Exception("API token must be 64 characters long. Visit Banxico's website for further information.")

        self.token = token

    def setLocale(self, locale):

        if locale == "en":
            self.locale = "en"
        elif locale == "es":
            self.locale = "es"
        else:
            raise Exception("Locale is badly specified. Must be either 'en' or 'es'.")