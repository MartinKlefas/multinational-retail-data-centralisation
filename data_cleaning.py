import pandas as pd

class DataCleaning:
    def clean_user_data(self, df: pd.DataFrame):
        df['index'] = df['index'].astype('int64')
        df['date_of_birth']=pd.to_datetime(df['date_of_birth'],infer_datetime_format=True, errors='coerce')
        df['join_date']=pd.to_datetime(df['join_date'],infer_datetime_format=True, errors='coerce')
        df["country"] = df["country"].astype("category")
        df["country_code"] = df["country_code"].astype("category")

        df.drop_duplicates(subset=["first_name", "last_name", "date_of_birth", "country"],keep="first",inplace=True)

        

        for index, row in df.iterrows():
            row["phone_number"] = self.standardise_phone_number(row["phone_number"])

        return df

    def standardise_phone_number(number: str):
        if number[:1] == "+" :
            number = number[1:]
        number = number.replace(" ","")
        number = number.replace("-","")

        if number[:2] != "00":
            number = "00" + number

    def clean_card_data(self, df : pd.DataFrame):
        df["country"] = df["country"].astype("category")