#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# v0.4 210222
#
# -------------------- Section 1. TODO: --------------------
#  2) Read configurations from file
#  3) Add consistency checks
#
# ------------------- Section 2. USAGE: --------------------
"""
  gridsearch.py
  Usage instructions:

  1) Copy this script to  your working directory,  where all
     files required for the run are available.
  2) Create a parameter file  template that must contain all
     parameters  required to  run, and  placeholders ({...})
     for the parameters that are to be set during the search
     (including the search variables).  The path of the file
     must be  specified in the  variable paramfile_template,
     see instructions below).
     For example the partial template file below:
-------------- parameter file template example -------------
[global]

#########
# default fitted parameters
#########
pa                  = {pa}
pb                  = {pb}
pc                  = {pc}
kex_ab              = {kex_ab}
kex_bc              = {kex_bc}
kex_ac              = {kex_ac}
dw_ab               = 3.5
dw_ac               = 3.5
dw_bc               = 1.0

... etc ...
------------------------------------------------------------
     The placeholders  ({...}) will  be replaced  during the
     search [using str.format],  according to definitions in
     the  parameters dict,  which should  contain a  key for
     each  placeholder; the  corresponding values  are lists
     containing all  values of  the variable that  should be
     searched; single-element lists are possible.
     For example, the parameters dict below:
------------------ parameters dict example -----------------
parameters = dict(
  pa = [0.9, 0.95, 0.99],
  pb = [0.01, 0.05, 0.1],
  pc = [0.01],
  kex_ab = [300],
  kex_bc = [600],
  kex_ac = [600])
------------------------------------------------------------
     will search on a 3x3 grid of pa, pb, with others fixed:
     on  each of  the 9  iterations, {pa}  and {pb}  will be
     replaced with  each of  the values from  the respective
     lists, while {pc}, {kex_ab}, {kex_bc} and {kex_ac} will
     be fixed at the specified value. 
     Note that paramfile_name and outfile_name (specified in
     Section  4.  Configuration,  see  below)  also  contain
     placeholders ({pa:.2f}) that will be replaced, in order
     to generate a different file at each iteration.
  2) Modify variables  in  Section  4. Configuration  below;
     note that the script will  fail if mentioned folders do
     not exist.
  3) Run with
     python multi_run_2d.py

"""
# ------------------- Section 3. IMPORTS -------------------
import os, sys, glob
from chemex import chemex
# from dummy import dummy as chemex  # this line for testing
from sklearn.model_selection import ParameterGrid

# ---------------- Section 4. CONFIGURATION ----------------
verbose = False
kexfile = "3st.pb_kex"
function = "powell"
experiment_glob = "Experiments/*.cfg"
methodfile = "Methods/method_3st_III_n15.cfg"
paramfile_template = "Parameters_tmp/params.template"  # Parameter file template
paramfile_name = "Parameters_tmp/params_A{pa:.2f}_B{pb:.2f}.cfg"  # Parameter file names
outfile_name = "Output_A{pa:.2f}_B{pb:.2f}"  # Output names

# Default parameter values (cfr. Parameter file template).
# Fixed (non-search) parameters must be specified in single-element lists.
parameters = dict(
    pa=[0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99],
    pb=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
    kex_ab=[300],
    kex_bc=[600],
    kex_ac=[600])

# --------------------- Section 5. RUN ---------------------
def make_parameter_file(template, output, params):
    """Format template to output using params"""
    with open(template) as fin, open(output, 'w') as fout:
       fout.write(fin.read().format(**params))

if verbose:
    print(kexfile, function, methodfile, paramfile_template, outfile_name)

# Create chemex args
args = ["chemex", "fit"]
args.extend(["-e"] + glob.glob(experiment_glob))
args.extend(["-m", methodfile])
args.extend(["-d", kexfile])
args.extend(["-f", function])

for params in ParameterGrid(parameters):
    if verbose:
        print("Running {}".formate(params))
    # Create Parameter file name by replacing placeholders
    try:
        paramfile = paramfile_name.format(**params)
    except KeyError:
        print("Missing parameter definition for paramfile_name '{}'".format(paramfile_name))
    # Replace placeholders in paramfile_template combining
    # information about current grid point and the parameters
    # dict, to create the output paramfile.
    try:
        make_parameter_file(
            paramfile_template, paramfile, params)
    except KeyError:
        print("Missing parameter definition for paramfile_template '{}'".format(paramfile_template))
    # Create Output file name by replacing placeholders
    try:
        outfile = outfile_name.format(**params)
    except KeyError:
        print("Missing parameter definition for outfile_name '{}'".format(outfile_name))
    # Create dummy sys.argv to pass arguments to chemex.main
    t_args = args + \
        ["-p", paramfile] + \
        ["-o", outfile]
    sys.argv = t_args
    # Call chemex.main to execute:
    #    python -m chemex fit
    #        -e experiment_glob
    #        -p paramfile
    #        -d kexfile
    #        -m methodfile
    #        -o outfile
    #        -f function
    chemex.main()

# ----------------------------------------------------------