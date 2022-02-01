import numpy as np
import pandas as pd
import multiprocessing as mp
import time
import logging
import math
import geopy.distance

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

def CalculDistance_proc(q,df_orig : pd.DataFrame,df_dest : pd.DataFrame):
    """
    Function launched on an unique processor

    Parameters
    ----------
    df_orig : DataFrame
        DataFrame containing at least columns 'latitude' and 'longitude'
    df_dest : DataFrame
        DataFrame containing at least columns 'latitude' and 'longitude'
    Returns
    -------
    """
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


def Distance_MultiProcess(df_origin :pd.DataFrame, df_destination :pd.DataFrame, nProc =2):
    """
    Function which splits the data and organize the processor according to the number nProc

    Parameters
    ----------
    df_orig : DataFrame
        DataFrame containing at least columns 'latitude' and 'longitude'
    df_dest : DataFrame
        DataFrame containing at least columns 'latitude' and 'longitude'
    Returns
    array df_final
        (df_final : DataFrame, exec_time: list)
    -------
    """
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