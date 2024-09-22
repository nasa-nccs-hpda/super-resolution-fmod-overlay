
# super-resolution-api

Super Resolution Application Programming Interface (API) for Weather/Climate Data Framework.

## Pre-Requisites

Requires GPU support. 

## Environment

If mamba is not available, install [miniforge](https://github.com/conda-forge/miniforge).
Execute the following to set up a conda environment for super-resolution-api:

    >  mamba create -n sres python=3.11
    >  mamba activate sres
    >  mamba install -c conda-forge dask scipy xarray netCDF4 ipywidgets=7.8 jupyterlab=4.0 jupyterlab_widgets ipykernel=6.29 ipympl=0.9 ipython=8.26
    >  mamba install -c pytorch -c nvidia -c conda-forge litdata pytorch lightning lightning-utilities torchvision torchaudio pytorch-cuda cuda-python
    >  pip install parse  nvidia-dali-cuda120
    >  pip install hydra-core --upgrade
    >  ipython kernel install --user --name=sres

## Setup

Execute the following to install and setup the super-resolution-api framework.

    > git clone https://github.com/nasa-nccs-hpda/super-resolution-api.git
    > cd super-resolution-api/
    > export PYTHONPATH=.:./super-resolution-climate:$PYTHONPATH

## Configuration

This project uses [hydra](https://hydra.cc) for workflow configuration.  All configuration files are found in the super-resolution-api/super-resolution-climate/config directory.  
Default values are specified here for a variety of internal parameters related to model tuning and inference derivations.  Pertinent runtime parameters are described in the table below.

## Parameters

| Parameter | Description | Value |
| --- | --- | --- |
| 'action' | process to run | infer, train |
| 'region' | region of interest | south_pacific, south_indian, 20-20e [roi:  {  y0: 6500, ys: 3000 }], 20-60n [roi:  {  y0: 9500, ys: 3000 }], 60-20s |
| 'epochs' | maximum epochs during training | >0 |
| 'structure' | inference output format | image, tiles |

Notes:
image & tiles
dataset_root: 

## Example Runs

This API supports two processing modes: 1) infer() and 2) train().  The infer() process generates one or more images based on the structure parameter. 
Results for individual tiles, or assembled images for each region, are supported.  The train() process will generate a new model or tune an existing one.

*Note that existing models can be plugged in without running the training process.*

### Inference

    > 'python ./sresConfig/view/super-resolution-cli.py -action infer -region 20-60n -structure tiles -timesteps 3' 
    > python ./sresConfig/view/super-resolution-cli.py -action infer -region 20-60n -structure image

### Training

    > python ./sresConfig/view/super-resolution-cli.py -action train -region 20-60n -epochs 10 


## Inference

The scripts under *super-resolution-api/scripts/inference* are used to run inference for the trained super-resolution networks. 

## Pre-Requisites

Requires GPU support. 
