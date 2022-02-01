import numpy as np
import pandas as pd
import multiprocessing as mp
import time
import logging
import math
import geopy.distance
import geopandas as gdp
import pickle

def extract_coord(geostring: str):
    where = geostring.find(',')
    return [float(geostring[:where]), float(geostring[where + 1:])]

def distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def distance2(lat1,lon1,lat2,lon2):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    lat1 : float
        latitude of the original point
    lon1 : float
        longitude of the original point
    lat2 : float
        latitude of the point of destination
    lon2 : float
        longitude of the point of destination
    Returns
    -------
    distance_in_km : float
    """
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d



def CalculDistance(df_orig : pd.DataFrame,df_dest : pd.DataFrame):
    res=pd.DataFrame(index=df_orig.index,columns=df_dest.index)
    start=time.time()
    for i in res.index:
        lat1=df_orig.loc[i,'latitude']
        lon1=df_orig.loc[i,'longitude']
        for j in res.columns:
            lat2=df_dest.loc[j,'latitude']
            lon2=df_dest.loc[j,'longitude']
            res.loc[i,j]=distance2(lat1,lon1,lat2,lon2)
    #print("Temps d'éxécution: {} secondes".format(round(time.time()-start,2)))
    return res

def CalculDistance_proc(q,df_orig : pd.DataFrame,df_dest : pd.DataFrame):
    res=pd.DataFrame(index=df_orig.index,columns=df_dest.index)
    start=time.time()
    for i in res.index:
        lat1=df_orig.loc[i,'latitude']
        lon1=df_orig.loc[i,'longitude']
        for j in res.columns:
            lat2=df_dest.loc[j,'latitude']
            lon2=df_dest.loc[j,'longitude']
            res.loc[i,j]=distance2(lat1,lon1,lat2,lon2)
    Letime=time.time()-start
    q.put(np.array([res,Letime], dtype=object))

def CalculDistance_proc_geopy(q,df_orig : pd.DataFrame,df_dest : pd.DataFrame):
    res=pd.DataFrame(index=df_orig.index,columns=df_dest.index)
    start=time.time()
    for i in res.index:
        lat1=df_orig.loc[i,'latitude']
        lon1=df_orig.loc[i,'longitude']
        coord1=(lat1,lon1)
        for j in res.columns:
            lat2=df_dest.loc[j,'latitude']
            lon2=df_dest.loc[j,'longitude']
            coord2 = (lat2, lon2)
            res.loc[i,j]=geopy.distance.geodesic(coord1,coord2)
    Letime=time.time()-start
    q.put(np.array([res,Letime], dtype=object))

def Distance_MultiProcess(df_origin :pd.DataFrame, df_destination :pd.DataFrame, nProc =2):
    ctx = mp.get_context('spawn')
    N = df_origin.shape[0]
    exec_time=[]
    Sorti=[]
    index_a = [N // nProc * i for i in range(nProc)]
    index_b = [N // nProc * (i + 1) for i in range(nProc)]
    if N % nProc != 0:
        index_b[-1]=N
    process = list()
    q_list = list()
    start = time.time()
    print('AOU')
    for p in range(nProc):
        q = ctx.Queue()
        q_list.append(q)
        logging.info("Main    : create and start process %d.", p)
        x = ctx.Process(target=CalculDistance_proc,
                        args=(q, df_origin.iloc[index_a[p]:index_b[p], :], df_destination))
        process.append(x)
        logging.info("start" + str(p))
        x.start()
    for q in q_list:
        temp = q.get()
        Sorti.append(temp[0])
        exec_time.append(temp[1])
        logging.info(str(temp[1]))
    for p, proc in enumerate(process):
        logging.info("Main    : before joining process %d.", p)
        proc.join()
        proc.close()
        logging.info("Main    : process %d done", p)

    for j in range(len(Sorti)):
       if j==0:
           df_final=Sorti[j]
       else:
           df_final=pd.concat([df_final,Sorti[j]],ignore_index=True)
    return np.array([df_final,exec_time], dtype=object)


gareratp = pd.read_csv('/Users/thomasdoucet/Documents/GitHub/ML_ENSAE/emplacement-des-gares-idf.csv', sep=';')
    gareratp["latitude"] = gareratp.apply(
        lambda x: extract_coord(x['Geo Point'])[0],
        axis=1
    )

    gareratp["longitude"] = gareratp.apply(
        lambda x: extract_coord(x['Geo Point'])[1],
        axis=1
    )
    df_gare=pd.read_csv('/Users/thomasdoucet/Documents/GitHub/ML_ENSAE/referentiel-gares-voyageurs.csv',sep=';')
    # Suppression des 11 gares sans coordonnéées GPS
    df_gare = df_gare[df_gare['WGS 84'].isnull() == False]
    # Concatenation des gares RATP + SNCF

    df_gare[['Latitude', 'Longitude', 'WGS 84']]
    df_gare2 = df_gare[['Latitude', 'Longitude', 'WGS 84']]
    gareratp2 = gareratp[['latitude', 'longitude', 'Geo Point']]
    df_gare2.columns = gareratp2.columns

    # concatenation des DataFrame SNCF & RATP
    df_train = pd.concat([df_gare2, gareratp2], ignore_index=True)
    df_train.drop_duplicates(inplace=True)  # Suppresion des gares en doublon en IDF
    df_train
elem_max = 500
df_test = df_dest[:elem_max]
start = time.time()
# res1=CalculDistance(df_test,df_test)
print("Temps d'éxécution: {} secondes".format(round(time.time() - start, 2)))
# Tentative parallelisation mais ne marche pas.

ctx = mp.get_context('spawn')
nProc = 2
N = df_test.shape[0]
exec_time = []
Sorti = []
index_a = [N // nProc * i for i in range(nProc)]
index_b = [N // nProc * (i + 1) for i in range(nProc)]
if N % nProc != 0:
    index_b[-1] = N

process = list()
q_list = list()
start = time.time()
print('AOU')
for p in range(nProc):
    q = ctx.Queue()
    q_list.append(q)
    logging.info("Main    : create and start process %d.", p)
    x = ctx.Process(target=CalculDistance_proc,
                    args=(q, df_test.iloc[index_a[p]:index_b[p], :], df_test))
    process.append(x)
    logging.info("start" + str(p))
    x.start()
for q in q_list:
    # temp = pickle.loads(q.get())
    temp = q.get()
    Sorti.append(temp[0])
    exec_time.append(temp[1])
    logging.info(str(temp[1]))
for p, proc in enumerate(process):
    logging.info("Main    : before joining process %d.", p)
    proc.join()
    proc.close()
    logging.info("Main    : process %d done", p)
