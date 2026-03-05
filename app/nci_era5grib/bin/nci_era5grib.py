#!/g/data/hh5/public/apps/miniconda3/envs/analysis3/bin/python

"""
Set up era5 grib files for use by the nesting suite

The nesting suite expects grib files to be named like
    AINITIAL="$ROSE_DATA/era5grib/ec_grib_${FDATE}.t+000"
where FDATE is in YYYYmmddHHMM format
"""

import os
import argparse
import pandas
from pathlib import Path
import era5grib

boolopt = {
    "True": True,
    "False": False,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mask', required=True)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--start', required=True, type=pandas.to_datetime)
    parser.add_argument('--count', default=1, type=int)
    parser.add_argument('--freq', default=60*60, type=lambda x: pandas.to_timedelta(int(x), unit='s'))
    parser.add_argument('--era5land', default=True, type=lambda x: boolopt[x])
    parser.add_argument('--polar', default=False, type=lambda x: boolopt[x])
    args = parser.parse_args()

    print(vars(args))

    for t in pandas.date_range(args.start, freq=args.freq, periods=args.count):
        fdate = t.strftime("%Y%m%d%H%M")
        out = args.output / f"ec_grib_{fdate}.t+000"
        era5grib.era5grib_um(t, output=out, target=args.mask, era5land=args.era5land, polar=args.polar)



if __name__ == '__main__':
    main()
