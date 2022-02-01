# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import multiprocessing as mp
import time
from function import *
import geojson
#import geopandas as gpd
#import geojsonio

if __name__ == '__main__':
    Type_Lancement='ecole' #ecole ou gare
    # Import les gares
    #df_gare=pd.read_csv('/Users/thomasdoucet/Documents/GitHub/ML_ENSAE/gare_France.csv',sep=',')
    #df_gare = pd.read_csv('C:/Users/NovaCloudUser/ML_ENSAE/gare_France.csv', sep=',')

    # Import les annonces
    #df_orig=pd.read_csv('/Users/thomasdoucet/Documents/GitHub/ML_ENSAE/X_train.csv',sep=',')
    df_orig = pd.read_csv('C:/Users/NovaCloudUser/ML_ENSAE/X_train.csv', sep=',')

    df_orig=df_orig[['approximate_latitude','approximate_longitude']]
    df_orig.columns = ['latitude', 'longitude']

    # Import les écoles
    #df_school=gpd.read_file('/Users/thomasdoucet/Documents/GitHub/ML_ENSAE/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.geojson')
    #df_school = gpd.read_file('D:/Téléchargements/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.geojson')

    if Type_Lancement == "gare":
        nDiv = 5
        df_dest = pd.read_csv('C:/Users/NovaCloudUser/ML_ENSAE/gare_France.csv', sep=',')
    else: # Cas école
        nDiv= 50
        df_dest = pd.read_csv(
            'D:/Téléchargements/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.csv', sep=';')
        df_dest = df_dest[['Latitude', 'Longitude']].dropna()
        df_dest.columns = ['latitude', 'longitude']

    N=df_orig.shape[0]
    index_a = [N // nDiv * i for i in range(nDiv)]
    index_b = [N // nDiv * (i + 1) for i in range(nDiv)]
    if N // nDiv != 0:
        index_b[-1]=N

    for i in range(nDiv):
       start=time.time()
       res =Distance_MultiProcess(df_orig[index_a[i]:index_b[i]], df_dest, nProc =4)
       print("Temps d'éxécution pour gares (Division {}: {} secondes".format(i,round(time.time() - start, 2)))
       name='distance_'+Type_Lancement+str(i)+'.csv'
       res[0].to_csv('D:/Téléchargements/'+name)
       print(res[1])
       del res #Libérer de la mémoire





    #elem_max=500
    #df_dest2 = df_gare[:elem_max]
    #df_origin2=df_orig[:100]
    #start=time.time()
    #res_gare =Distance_MultiProcess(df_orig, df_gare, nProc =4)
    #print("Temps d'éxécution pour gares: {} secondes".format(round(time.time() - start, 2)))
    #res_gare[0].to_csv('D:/Téléchargements/distance_gare.csv')
    #print(res_gare[1])
    #start=time.time()
    #res_ecole =Distance_MultiProcess(df_orig, df_school, nProc =4)
    #res_ecole[0].to_csv('D:/Téléchargements/distance_école.csv')
    #print("Temps d'éxécution pour école: {} secondes".format(round(time.time() - start, 2)))
    #print(res_ecole[1])
    print("FIN")
