import json
import numpy as np
import tabula
import pandas as pd
import http.client
import boto3


class DataExtractor:
    def retrieve_pdf_data(self, link : str):
        tables = tabula.read_pdf(link,pages="all")
        joined =pd.concat(tables,ignore_index=True)
        return joined
    
    def list_number_of_stores(self,endpoint: str, header: dict):
        
        conn = http.client.HTTPSConnection("aqj7u5id95.execute-api.eu-west-1.amazonaws.com")
        
        headers = {
            "x-api-key" : header["x-api-key"]
            }

        conn.request("GET", endpoint, headers=headers)

        res = conn.getresponse()
        data = res.read()
        
        conn.close()
        try :
            #print(data.decode("utf-8"))
            data = json.loads(data.decode("utf-8"))

            return(data["number_stores"])
        except Exception as ex:
            print(type(ex))
            
            return np.nan

    def retrieve_single_stores_data(self, connection : http.client.HTTPSConnection, endpoint : str, header: dict, storeNumber  : str):
             
        

        connection.request("GET", endpoint + str(storeNumber), headers=header)

        res = connection.getresponse()
        data = res.read()
        
        
      
        try :
            data = json.loads(data.decode("utf-8"))
            
            df = pd.DataFrame(data, index=[0])
            return df
        except ValueError as ex:
            print(ex)
            
            return None
        
    def retrieve_stores_data(self, endpoint : str, header: dict, totalStores : int):
        headers = {
            "x-api-key" : header["x-api-key"]
            }
        conn = http.client.HTTPSConnection ("aqj7u5id95.execute-api.eu-west-1.amazonaws.com")

        df = pd.DataFrame()

        for i in range(0,totalStores+1,1):
            single = self.retrieve_single_stores_data(connection=conn,endpoint=endpoint,header=headers,storeNumber=i)
            
            if len(df) > 0 :               
                df = pd.concat([df,single],ignore_index=True)
            else:
                df = single

            

        conn.close()

        return df

    def extract_from_s3(self, link : str):
        s3 = boto3.client('s3')

        s3.download_file("data-handling-public",'products.csv','products.csv')
        return pd.read_csv("products.csv")
