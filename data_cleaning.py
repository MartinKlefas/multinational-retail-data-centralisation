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
        df["card_provider"] = df["card_provider"].astype("category")
        df['card_number'] = pd.to_numeric(df['card_number'],errors="coerce")
        df['expiry_date']=pd.to_datetime(df['expiry_date'],errors='coerce',format="%m/%y")
        df['date_payment_confirmed']=pd.to_datetime(df['date_payment_confirmed'],infer_datetime_format=True, errors='coerce') 
        df.drop_duplicates(subset=["card_number",	"expiry_date",	"card_provider"	],keep="first",inplace=True)
        df.dropna(inplace=True,axis="index",how="any") # drops the whole row if any columns have an nan

        return df
