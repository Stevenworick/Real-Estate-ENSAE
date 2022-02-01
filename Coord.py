import pandas as pd
#import seaborn as sns
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import os
import time
#import scipy.stats as ss





# In[4]:


df_company = pd.read_csv("D:\Téléchargements\StockEtablissement_utf8.csv", index_col=False, sep=";",
                         encoding='unicode_escape')
df_company

# In[5]:


df_company = df_company.replace(np.nan, "")[['siret','complementAdresseEtablissement',
       'numeroVoieEtablissement',
       'typeVoieEtablissement', 'libelleVoieEtablissement',
       'codePostalEtablissement', 'libelleCommuneEtablissement','activitePrincipaleEtablissement','etatAdministratifEtablissement']]


# In[6]:


def from_float_to_str(postal_code):
    if postal_code != "" and postal_code < 95890:
        return str(int(postal_code))
    if postal_code == "":
        return ""
    else:
        return str(int(postal_code))


df_company["codePostalEtablissement"] = df_company.apply(
    lambda x: from_float_to_str(x["codePostalEtablissement"]), axis=1
)


# In[7]:


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def from_int_to_str(numero):
    if numero != "" and isfloat(numero):
        return str(int(numero))
    if numero != "" and not isfloat(numero):
        print(numero)
        return str(numero)
    if numero == '':
        return ''


df_company["numeroVoieEtablissement"] = df_company.apply(
    lambda x: from_int_to_str(x["numeroVoieEtablissement"]), axis=1)

# ### Drop des lignes dont le code postale  au dessus du dernier code postal francais (95880)
# ### les codes postaux vides et enfin ceux qui ont ni adresses ni complément d'adresses

# In[8]:


df_company = df_company.drop(index=df_company[df_company["codePostalEtablissement"] > "95880"].index)
df_company = df_company.drop(index=df_company[df_company["codePostalEtablissement"] == ""].index)
df_company = df_company.drop(index=df_company[df_company["libelleVoieEtablissement"] == ""][
    df_company["complementAdresseEtablissement"] == ""].index)

# In[9]:


df_company["Adresse"] = df_company['numeroVoieEtablissement'] + " " + df_company['libelleVoieEtablissement'] + "," + \
                        df_company['codePostalEtablissement'] + " " + df_company['libelleCommuneEtablissement']

# In[10]:


df_company[df_company["Adresse"] == ""]

# In[11]:


import requests, json
import urllib.parse


def get_coord(adress):
    session = requests.Session()
    session.headers = {"Accept-Encoding": "*", "Connection": "keep-alive"}
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    r = session.get(api_url + urllib.parse.quote(adress))
    if r.status_code == 200:
        # output_dic=json.loads(r.text)
        try:
            output_dic = json.loads(r.text)
            output_dic["features"][0]["geometry"]["coordinates"]
            return (output_dic["features"][0]["geometry"]["coordinates"][0],
                    output_dic["features"][0]["geometry"]["coordinates"][1],
                    output_dic["features"][0]["properties"]["score"])
        except IndexError or JSONDecodeError or ConnectionError:
            pass
    else:
        pass

print("Jackson")
# In[ ]:

df_company400k = df_company[400000:]
start = time.time()

df_company400k["coord"] = df_company400k.apply(lambda x: get_coord(x["Adresse"]), axis=1)

print("Temps d'éxécution: {} secondes".format(round(time.time() - start, 2)))
df_company400k.to_excel("stock_reste.xlsx")

