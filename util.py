""" Utilities to accompany Python for Climate Data Science """

import numpy as np
import pandas as pdb
import xarray as xr

def read_ushcn_data(field, data_fn="data/ushcn2014_tob_tmax.txt",
                    stat_fn="data/ushcn-stations.txt"):
    """ Read in fixed-width format data from the USHCN. """

    # Set column widths for the data field, accounting for blank spaces
    widths = [
        11, # STAID
         1, # -
         4, # YEAR
         1, # -
    ] + [
        5, # VALUE
        1, 1, 1, # FLAGS
        1, # -
    ]*13

    # Construct column names to accompany widths
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG',
              'SEP', 'OCT', 'NOV', 'DEC', 'ANN']
    names = ['STATION', '-', 'YEAR', '-']
    for month in months:
        names.extend([month, month+'-DM', month+'-QC', month+'-DS', '-'])
    # Read in the fixed-width data
    df = pd.read_fwf(data_fn, widths=widths, header=None, names=names,
                     na_values=-9999)

    # Drop out all except known, named columns
    df = df[[n for n in names if n != '-']]

    # Re-shape from "long" format to continuous timeseries format,
    # accounting for data, flags, and timestamps.
    dm_flags = ['A', 'B',' C', 'D', 'E', 'F', 'G', 'H',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                '.', '']
    qc_flags = ['d', 'g', '']
    ds_flags = list(range(1, 9)) + ['B', 'D', 'G']

    month_dfs = []
    for i, month in enumerate(months, 1):
        print(i)
        if month == 'ANN':
            continue
        month_df = (
            df
            [['STATION', 'YEAR',
              month, month+'-DM', month+'-QC', month+'-DS']]
            .rename(columns={month+'-DM': 'DM',
                             month+'-QC': 'QC',
                             month+'-DS': 'DS',
                             month: field})
        )
        month_df['month'] = i
        month_df['date'] =  (
            month_df.YEAR.astype(str) + "{:02d}01".format(i)
        ).apply(pd.Timestamp)

        month_df["DM"] = (
            month_df["DM"]
            .astype("category", categories=dm_flags)
            .replace(np.NaN, '')
        )
        month_df["QC"] = (
            month_df["QC"]
            .astype("category", categories=qc_flags)
            .replace(np.NaN, '')
        )
        month_df["DS"] = (
            month_df["DS"]
            .astype("category", categories=ds_flags)
            .replace(np.NaN, '')
        )

        month_dfs.append(month_df)
    df = pd.concat(month_dfs)

    # Set the COOP_ID for easy reference against the station data.
    df['COOP_ID'] = df.STATION.apply(lambda x: int(x[3:]))

    # Read in the station data, which is much simpler
    colspecs = (
        (0, 7), # COOP ID
        (8, 16), # LATITUDE
        (17, 26), # LONGITUDE
        (27, 33), # ELEVATION
        (33, 36), # STATE
        (36, 66), # NAME
        (67, 73), # COMPONENT 1
        (74, 80), # COMPONENT 2
        (81, 87), # COMPONENT 3
        (88, 90), # UTC OFFSET
    )
    stations = pd.read_fwf(\
        stat_fn, colspecs,
        names=['COOP_ID', 'LAT', 'LON', 'ELEV', 'STATE',
               'NAME', 'COMP1', 'COMP2', 'COMP3', 'dUTC'])
    stations = stations.set_index('COOP_ID')

    # Fix longitudes - some are easterly instead of west.
    stations.loc[stations.LON > 0, 'LON'] = -stations.LON

    return df, stations
