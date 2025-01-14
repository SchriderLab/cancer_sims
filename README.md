This repository contains simulation codes and parsing scripts for the paper "Evolutionary rescue model informs strategies for driving cancer cell populations to extinction."

# Simulation Scripts
The simulation scripts both for all non-fixed-trajectory sims (`base_sim.slim`) and fixed_trajectory sims (`fixed_traj_patients.slim`) are in the `sims/` directory. 

`base_sim.slim` needs to be modified (refer to the file itself for which lines to comment and uncomment) if two different rates are to be specified for each mutation type. 

# HPC Submission Job Generation
In order to facilitate submitting the simulation scripts and passing the appropriate parameters to them on a high-perofrmance computing cluster (HPC), a helpful `create_hpc_script.py` has been provided in the `scripts/` folder. This file accepts one required argument and two optional ones.

The first argument must always be the path to the configuration file. This file specifies the parameters and their ranges to be passed to the slim script. The script takes the combination of values from each section and produces a corresponding `params.csv` file detailing all the parameter names, values, and their corresonding identifier `param_id`. Note that while the script produces a combination of all values between sections, parameters sharing a section will have their values synchronized, and combinations between their values will not be used. An example configuration file has been provided in `scripts/example_settings.conf`. 