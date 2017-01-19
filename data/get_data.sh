#!/usr/bin/env bash

# GISTEMP gridded data
for fn in gistemp250; do
    wget http://data.giss.nasa.gov/pub/gistemp/${fn}.nc.gz
    gzip -d ${fn}.nc.gz
done

# GISTEMP spatially-averaged anomalies
for fn in GLB SH NH; do
    wget http://data.giss.nasa.gov/gistemp/tabledata_v3/${fn}.Ts+dSST.txt
    wget http://data.giss.nasa.gov/gistemp/tabledata_v3/${fn}.Ts+dSST.csv
done

# USHCN data
wget http://cdiac.ornl.gov/ftp/ushcn_v2.5_monthly/readme.txt
wget http://cdiac.ornl.gov/ftp/ushcn_v2.5_monthly/ushcn-stations.txt

for obs in tmax tmin tavg prcp; do
    wget http://cdiac.ornl.gov/ftp/ushcn_v2.5_monthly/ushcn2014_raw_${obs}.txt.gz
    gzip -d ushcn2014_raw_${obs}.txt.gz
done

# wget http://cdiac.ornl.gov/ftp/ushcn_daily/us.txt.gz
# gzip -d us.txt.gz

for obs in prcp tmax tmin; do
    wget http://cdiac.ornl.gov/ftp/ushcn_daily/ushcn_${obs}.nc.gz
    gzip -d ushcn_${obs}.nc.gz
done
