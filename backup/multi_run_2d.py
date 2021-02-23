#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# v0.3 210221
#
# -------------------- Section 1. TODO: --------------------
#  1) Make searchable parameters variable
#     could have a dict with {var: [val1, val2, val3]} for
#     search vars, and {var: val} for other variables.
#     Then `{var}` placeholders in file names and template.
#     Then, a function could flatten the search, and create
#     a list of dicts, replacing lists with a single grid
#     point values; dicts could be used for all .format().
#  2) Read configurations from file
#  3) Add consistency checks
#
# ------------------- Section 2. USAGE: --------------------
"""
  Multi_Run_2D.py

  1) Create a  parameter file template (paramfile_template);
     it  must  contain   all  configurations  required,  and
     placeholders ({...})  for the variables that  are to be
     configured in the run (including the search variables).
     For example the partial example below:
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

------------------------------------------------------------
     The placeholders  ({...}) will be replaced  in the code
     below.  {pa}  and {pb}={pc} will be  replaced with each
     of  the values  from liste_pa  and liste_pb.  {kex_ab},
     {kex_bc}  and {kex_ac}  will  be  replaced with  values
     taken from the parameters  dict below. Search variables
     can have None value in  the parameters dict.  Note that
     paramfile_name    and    outfile_name   also    contain
     placeholders ({pa:.2f}) that will  be replaced in order
     to generate a different file at each iteration.
  2) Modify variables  in  Section  4. Configuration  below;
     note that the script will  fail if mentioned folders do
     not exist.
  3) Run with
     python multi_run_2d.py

"""
# ------------------- Section 3. IMPORTS -------------------
import os, sys, glob
from chemex import chemex  # uncomment this line
# from dummy import dummy as chemex  # comment this line

# ---------------- Section 4. CONFIGURATION ----------------
verbose = False
kexfile = "3st.pb_kex"
function = "powell"
experiment_glob = "Experiments/*.cfg"
methodfile = "Methods/method_3st_III_n15.cfg"
paramfile_template = "Parameters_tmp/params.template"  # Parameter file template
paramfile_name = "Parameters_tmp/params_A{pa:.2f}_B{pb:.2f}.cfg"  # Parameter file names
outfile_name = "Output_A{pa:.2f}_B{pb:.2f}"  # Output names
liste_pa=[0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
liste_pb=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]

# Default parameter values (cfr. Parameter file template)
parameters = dict(
    pa=None,
    pb=None,
    pc=None,
    kex_ab=300,
    kex_bc=600,
    kex_ac=600)

# --------------------- Section 5. RUN ---------------------
def make_parameter_file(template, output, params):
    """Format template to output using params"""
    with open(template) as fin, open(output, 'w') as fout:
       fout.write(fin.read().format(**params))

if verbose:
    print(kexfile, function, methodfile, paramfile_template, outfile_name)

# Create chemex args
args = ["fit"]
args.extend(["-e"] + glob.glob(experiment_glob))
args.extend(["-m", methodfile])
args.extend(["-d", kexfile])
args.extend(["-f", function])

for i in liste_pa:  # run through grid dimension 1
    for k in liste_pb:  # run through grid dimension 2
        if verbose:
            print("Running pa={}, pb=pc={}".formate(i, k))
        # Create Parameter file name by replacing placeholders
        paramfile = paramfile_name.format(pa=i, pb=k)
        # Replace placeholders in paramfile_template combining
        # information about current grid point and the parameters
        # dict, to create the output paramfile.
        make_parameter_file(
           paramfile_template, paramfile,
           dict(parameters, pa=i, pb=k, pc=k))
        # Create Output file name by replacing placeholders
        outfile = outfile_name.format(pa=i, pb=k)
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
