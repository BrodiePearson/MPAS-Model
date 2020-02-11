#!/usr/bin/env python
"""
This script creates plots of the initial condition.
"""
# import modules
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import argparse
import datetime
import matplotlib
matplotlib.use('Agg')


def main():
    # parser
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--input_file_name', dest='input_file_name',
        default='initial_state.nc',
        help='MPAS file name for input of initial state.')
    parser.add_argument(
        '-o', '--output_file_name', dest='output_file_name',
        default='initial_state.png',
        help='File name for output image.')
    args = parser.parse_args()

    # load mesh variables
    ncfile = Dataset(args.input_file_name, 'r')
    nCells = ncfile.dimensions['nCells'].size
    nEdges = ncfile.dimensions['nEdges'].size
    nVertLevels = ncfile.dimensions['nVertLevels'].size

    fig = plt.figure()
    fig.set_size_inches(16.0, 12.0)
    plt.clf()

    print('plotting histograms of the initial condition')
    print('see: init/initial_state/initial_state.png')
    d = datetime.datetime.today()
    txt = \
        'MPAS-Ocean initial state\n' + \
        'date: {}\n'.format(d.strftime('%m/%d/%Y')) + \
        'number cells: {}\n'.format(nCells) + \
        'number cells, millions: {:6.3f}\n'.format(nCells / 1.e6) + \
        'number layers: {}\n\n'.format(nVertLevels) + \
        '  min val   max val  variable name\n'

    plt.subplot(3, 3, 2)
    varName = 'maxLevelCell'
    var = ncfile.variables[varName]
    plt.hist(var, bins=nVertLevels - 4)
    plt.ylabel('frequency')
    plt.xlabel(varName)
    txt = txt + ' {:9.2e}'.format(np.min(var)) + \
        ' {:9.2e}'.format(np.max(var)) + ' ' + varName + '\n'

    plt.subplot(3, 3, 3)
    varName = 'bottomDepth'
    var = ncfile.variables[varName]
    plt.hist(var, bins=nVertLevels - 4)
    plt.xlabel(varName)
    txt = txt + ' {:9.2e}'.format(np.min(var)) + \
        ' {:9.2e}'.format(np.max(var)) + ' ' + varName + '\n'

    plt.subplot(3, 3, 4)
    varName = 'temperature'
    var = ncfile.variables[varName]
    plt.hist(np.ndarray.flatten(var[:]), bins=100, log=True)
    plt.ylabel('frequency')
    plt.xlabel(varName)
    txt = txt + ' {:9.2e}'.format(np.min(var)) + \
        ' {:9.2e}'.format(np.max(var)) + ' ' + varName + '\n'

    plt.subplot(3, 3, 5)
    varName = 'salinity'
    var = ncfile.variables[varName]
    plt.hist(np.ndarray.flatten(var[:]), bins=100, log=True)
    plt.xlabel(varName)
    txt = txt + ' {:9.2e}'.format(np.min(var)) + \
        ' {:9.2e}'.format(np.max(var)) + ' ' + varName + '\n'

    plt.subplot(3, 3, 6)
    varName = 'layerThickness'
    var = ncfile.variables[varName]
    plt.hist(np.ndarray.flatten(var[:]), bins=100, log=True)
    plt.xlabel(varName)
    txt = txt + ' {:9.2e}'.format(np.min(var)) + \
        ' {:9.2e}'.format(np.max(var)) + ' ' + varName + '\n'

    rx1Edge = ncfile.variables['rx1Edge']
    plt.subplot(3, 3, 7)
    varName = 'rx1Edge'
    var = ncfile.variables[varName]
    plt.hist(np.ndarray.flatten(var[:]), bins=100, log=True)
    plt.ylabel('frequency')
    plt.xlabel('Haney Number, max={:4.2f}'.format(
        np.max(np.ndarray.flatten(rx1Edge[0, :, :]))))
    txt = txt + ' {:9.2e}'.format(np.min(var)) + \
        ' {:9.2e}'.format(np.max(var)) + ' ' + varName + '\n'

    print(txt)
    plt.subplot(3, 3, 1)
    plt.text(0, 1, txt, fontsize=12, verticalalignment='top')
    plt.axis('off')

    plt.savefig(args.output_file_name)


if __name__ == '__main__':
    # If called as a primary module, run main
    main()

# vim: foldmethod=marker ai ts=4 sts=4 et sw=4 ft=python