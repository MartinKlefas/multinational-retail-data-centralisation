import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np

class DataCleaning:
    def clean_user_data(self, df: pd.DataFrame):
        df['index'] = df['index'].astype('int64')
        df['date_of_birth']=pd.to_datetime(df['date_of_birth'],infer_datetime_format=True, errors='coerce')
        df['join_date']=pd.to_datetime(df['join_date'],infer_datetime_format=True, errors='coerce')
        df["country"] = df["country"].astype("category")
        df["country_code"] = df["country_code"].astype("category")
        df["address"] = df["address"].str.replace('\W', ' ', regex=True)
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

    def geoCode(self, df: pd.DataFrame):
        geolocator = Nominatim(timeout=10, user_agent = "myGeolocator")
        df['full_address'] = df.address +"," + df.country
        df['gcode'] = df.full_address.apply(geolocator.geocode)
        df['lat'] = [g.latitude for g in df.gcode]
        df['long'] = [g.longitude for g in df.gcode]

        return df

    def clean_store_data(self, df : pd.DataFrame):
        df = df.drop(columns=["lat","message"])
        df['index'] = pd.to_numeric(df['index'],errors="coerce")
        df['longitude']= pd.to_numeric(df['longitude'],errors="coerce")
        df['latitude'] = pd.to_numeric(df['latitude'],errors="coerce")
        df.dropna(inplace=True,axis="index",how="any") # drops the whole row if any columns have an nan
        df['opening_date']=pd.to_datetime(df['opening_date'],infer_datetime_format=True, errors='coerce')
        df["continent"] = df["continent"].astype("category")
        df["country_code"] = df["country_code"].astype("category")
        df["store_type"] = df["store_type"].astype("category")
        df["address"] = df["address"].str.replace('\W', ' ', regex=True) # remove the special chars from address

        return df
    
    def convert_product_weights(self, df : pd.DataFrame):
        newWeights = list()
        for thisValue in df["weight"]:
            if type(thisValue) == str:
                try:
                    if " x " in thisValue: # some weight lines appear to be in the form of 6 x 10g or similar - interpreted to mean 6 lots of 10g
                        splitWeight = thisValue.split(" x ")
                        if splitWeight[1][-2:] == "kg":
                            number = float(splitWeight[0])*float(splitWeight[1][:-2])
                        elif splitWeight[1][-2:] == "ml":
                            number = float(splitWeight[0])*float(splitWeight[1][:-2]) / 1000.0
                        else:
                            number = float(splitWeight[0])*float(splitWeight[1][:-1]) / 1000.0

                        newWeights.append(number)

                    else:
                        if thisValue[-2:] == "kg":
                            number = float(thisValue[:-2])
                            newWeights.append(number) # don't multiply KG
                        elif thisValue[-2:] == "ml":
                            number = float(thisValue[:-2])
                            newWeights.append(number / 1000.0)  # otherwise it's ml and needs dividing by 1000
                        else:
                            number = float(thisValue[:-1])
                            newWeights.append(number / 1000.0)  # otherwise it's g and needs dividing by 1000
                except Exception as ex:
                    print(ex)
                    newWeights.append(np.nan)
            else:
                newWeights.append(thisValue)
    


        
        df["weight"] = newWeights

        return df        
