
# super-resolution-api

Super Resolution Application Programming Interface (API) for Weather/Climate Data Framework.

## Pre-Requisites

1. Surface Water and Ocean Topography (SWOT) input data 
2. GPU support 

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
    > mkdir test
    > cd test
    > pwd
    > mkdir results
    > mkdir results/checkpoints
    > cd results/checkpoints 
    > <install checkpoint file here from browser with URL=https://drive.google.com/file/d/1qyrui4DnCKiP0ENJRCUDhN8hKU_gOWJs/view?usp=drive_link>
    > cd ../../..
    > export PYTHONPATH=.:./super-resolution-climate:$PYTHONPATH

Override default value of 'root:' parameter in `./super-resolution-api/super-resolution-climate/config/platform/platform-deploy.yaml` with fully qualified path returned from **pwd** command above.

    > change: **root: "<insert fully qualified path to super-resolution-api/test here>"** to something
    > like:   **root: "/<install path>/super-resolution-api/test"** (e.g., /home/gtamkin/super-resolution-api/test)

## Configuration

This project uses [hydra](https://hydra.cc) for workflow configuration.  All configuration files are found in the super-resolution-api/super-resolution-climate/config directory.  Default configuration values are specified here for a variety of internal parameters related to model tuning and inference derivations.  These initial values are reasonable for many scenarios.  However, the paths of the inputs and outputs *must* be correctly updated prior to execution in the `dataset_root:` and `root:` parameters respectively.

*This version of the API specifically supports the **SWOT** (Surface Water and Ocean Topography) dataset and the **SST** (sea surface temperature) variable.  The corresponding model (i.e., valid checkpoint=sres-rcan-10-20-64-swot_20-60n-SST-tiles-48.valid.pt) can be downloaded according to the Setup instructions above.*  

User-specifiable runtime parameters are described in the table below.

## Parameters

| Parameter | Description | Value |
| --- | --- | --- |
| `action` | process to run | `infer`, `train` |
| `region` | region of interest | `south_pacific` [*roi:  {  y0: 3500, ys: 3000, x0: 8797, xs: 7073 }*], `south_pacific_1200` [*roi:  { x0: 12480, y0: 4720, xs: 1200, ys: 1200 }*], `south_indian` [*roi:  {  y0: 3500, ys: 3000, x0: 2670, xs: 6037 }*], `20-20e` [*roi:  {  y0: 6500, ys: 3000 }*], `20-60n` [*roi:  {  y0: 9500, ys: 3000 }*], `60-20s` [*roi:  {  y0: 3500, ys: 3000 }*]|
| `epochs` | maximum epochs during training | >0 |
| `structure` | inference output format | `image`, `tiles` |

### Description

This API supports two processing modes: 1) inference and 2) training.  The inference process [`infer`] generates one or more images based on the `structure` parameter. Results for either individual `tiles` or assembled `image`s for the specified `region` are supported.  

The training process [`train`] will generate a new model or tune an existing one according to `region` and the desired number of `epochs`.

*Note that an inference can be derived from existing models without running a training process.*

## Example Runs

### Inference

    > python ./sresConfig/view/super-resolution-cli.py -action infer -region 20-60n -structure tiles -timesteps 3
    > python ./sresConfig/view/super-resolution-cli.py -action infer -region 20-60n -structure image

### Training

    > python ./sresConfig/view/super-resolution-cli.py -action train -region 20-60n -epochs 10 
 