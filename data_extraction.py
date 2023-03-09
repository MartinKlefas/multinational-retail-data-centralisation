import tabula
import pandas as pd

class DataExtractor:
    def retrieve_pdf_data(self, link : str):
        tables = tabula.read_pdf(link,pages="all")
        joined =pd.concat(tables,ignore_index=True)
        return joined
