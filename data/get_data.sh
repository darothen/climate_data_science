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

wget http://cdiac.ornl.gov/ftp/ushcn_v2.5_monthly/ushcn2014_tob_tmax.txt.gz
gzip -d ushcn2014_tob_tmax.txt.gz

wget http://cdiac.ornl.gov/ftp/ushcn_daily/us.txt.gz
gzip -d us.txt.gz
