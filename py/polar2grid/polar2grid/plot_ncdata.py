from numpy import *
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from glob import glob
import sys
import os

DEF_DIR = "."
DEF_PAT = "SSEC_AWIPS_*"

def exc_handler(exc_type, exc_value, traceback):
    print "Uncaught error creating png images"

def main(base_dir=DEF_DIR, base_pat=DEF_PAT, vmin=0, vmax=255):
    glob_pat = os.path.join(base_dir, base_pat)
    for nc_name in glob(glob_pat):
        nc_name = os.path.split(nc_name)[1]
        print "Drawing for NC name %s" % nc_name

        # Get the data and mask it
        nc = Dataset(nc_name, "r")
        data_var = nc.variables["image"]
        data_var.set_auto_maskandscale(False)
        data = data_var[:]
        data = data.astype(uint8) # How AWIPS reads it

        # Create a new figure everytime so things don't get shared
        plt.figure()

        # Plot the data
        print data.min(), data.max()
        plt.imshow(data, vmin=vmin, vmax=vmax)

        # Add a colorbar and force the colormap
        plt.colorbar()
        #plt.spectral()
        plt.bone()

        plt.savefig("plot_ncdata.%s.png" % nc_name)
        plt.close()

if __name__ == "__main__":
    import optparse
    usage = "python %prog [options] [ base directory | '.' ]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--vmin', dest="vmin", default=None,
            help="Specify minimum brightness value. Defaults to minimum value of data.")
    parser.add_option('--vmax', dest="vmax", default=None,
            help="Specify maximum brightness value. Defaults to maximum value of data.")
    parser.add_option('--pat', dest="base_pat", default=DEF_PAT,
            help="Specify the glob pattern of NetCDF files to look for. Defaults to '%s'" % DEF_PAT)
    options,args = parser.parse_args()
    sys.excepthook=exc_handler

    if len(args) == 0:
        base_dir = DEF_DIR
    elif len(args) == 1:
        base_dir = args[0]

    if options.vmin is None:
        vmin = None
    else:
        vmin = int(options.vmin)

    if options.vmax is None:
        vmax = None
    else:
        vmax = int(options.vmax)

    sys.exit(main(base_dir=base_dir, base_pat=options.base_pat, vmin=vmin, vmax=vmax))

