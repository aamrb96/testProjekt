import wbgapi as wb
import pandas as pd


class wbAPI(object):
    def __init__(self, countries: list, series: dict, dateRange: range) -> None:
        self.countries = countries
        self.series = series
        self.dateRange = dateRange

    def extract_wb_api_data(self) -> None:
        """
        Funktion, die Daten der Weltbank extrahiert,
        indem sie sich mit der offiziellen und öffentlichen Weltbank-API verbindet.
        * Dokumentation: https://blogs.worldbank.org/opendata/introducing-wbgapi-new-python-package-accessing-world-bank-data



        Parameters:
            countries (list): List of ISO3 Codes of countries for which series should be downloaded
            series (list): List of series IDs which should be downloaded
            dateRange (range): Range for which the data should be downloaded in years
        """

        # Für eine sinnvolle benamung werden die Zeitreihen IDs in einem
        # dictionary gepflegt. Die Keys sind der sprechende Name, die
        # values die von der WB verwendete ID
        series = [key for key in self.series.keys()]

        data = wb.data.DataFrame(
            series,
            self.countries,
            self.dateRange,
            # Wichtig, damit Graphen später einfacher korrekt dargestellt werden können
            numericTimeKeys=True,
        )

        self.wbData = data

    def transform_wb_data(self) -> pd.DataFrame:
        """
        Funktion um die Weltbank Daten in ein Datenformat zu bringen,
        welches gut in SQLite abgespeichert werden kann und die
        Abfrage von Daten im Frontend erleichtert.
        """

        self.wbData = self.wbData.reset_index()
        # Umbenennung der Spalte series in etwas sprechendes
        self.wbData["series"] = self.wbData["series"].replace(self.series)
        self.wbData.index = self.wbData["economy"] + "_" + self.wbData["series"]
        self.wbData = self.wbData.drop(["economy", "series"], axis=1)

        self.wbData = self.wbData.transpose()

    def main(self) -> pd.DataFrame:
        """
        Funktion, die die Orchestrierung der anderen Teile des
        Programms steuert
        """

        self.extract_wb_api_data()
        self.transform_wb_data()

        return self.wbData


if __name__ == "__main__":
    COUNTRIES = ["KEN", "SOM"]
    WB_SERIES = {"NY.GDP.MKTP.PP.CD": "GDP_ppp", "FP.CPI.TOTL.ZG": "Inflation"}
    DATERANGE = range(2000, 2024)

    wb_data = wbAPI(countries=COUNTRIES, series=WB_SERIES, dateRange=DATERANGE).main()
