"""
Purpose: Build and apply regression model for coefficient identification of raster data using
         low resolution data (~30m) and TARGET inputs. Apply the coefficients to high resolution data (~2m)
         to generate a surface reflectance product (aka, SR-Lite). Usage requirements are referenced in README.

Data Source: This script has been tested with very high-resolution WV data.
             Additional testing will be required to validate the applicability
             of this model for other datasets.

Original Author: Glenn Tamkin, CISTO, Code 602
"""
# --------------------------------------------------------------------------------
# Import System Libraries
# --------------------------------------------------------------------------------
import sys

# import veto.config
# sys.modules["sres.base.util.config"] = veto.config
sys.path.insert(0,'.')
sys.path.insert(1,'./veto')
sys.path.insert(2,'./super-resolution-climate')
sys.path.insert(3,'../../veto')
sys.path.insert(4,'../../super-resolution-climate')
print('\n', sys.path)

import veto.gpu
import veto.dual_trainer
sys.modules["sres.base.gpu"] = veto.gpu
sys.modules["sres.controller.dual_trainer"] = veto.dual_trainer

# import _fmod.base.util.config
# sys.modules["fmod.base.util.config"] = _fmod.base.util.config

from typing import Any, Dict, List, Tuple, Type, Optional, Union
import time  # tracking time
from pathlib import Path
#sys.path.insert(0,'/explore/nobackup/people/gtamkin/dev/super-resolution-sst/tm/FMod')

from sresConfig.model.parms import parms
from sresConfig.controller.actions import ActionController

from omegaconf import DictConfig
from hydra.core.global_hydra import GlobalHydra
import hydra


def main():
    """
    Main routine for SR-Lite
    """
    ##############################################
    # Default configuration values
    ##############################################
    start_time = time.time()  # record start time
    print('Command line executed:    {'+str(sys.argv)+'}')

    # Initialize context
    contextClazz = parms(1)
    context = contextClazz.getDict()

    # hydra.initialize(version_base=None, config_path=context[parms.DIR_CONFIG])
    # fmod.base.util.config.bark = funcType(new_bark, foo, fmod.base.util.config)
    
    try:
        cname = context[parms.SRES_PIPELINE] #"sres"
        model =  context[parms.SRES_MODEL] #'dbpn'  # [ 'dbpn', 'srdn', 'unet', 'vdsr', 'mscnn', 'edsr' ]
        models: List[str] = [ str(context[parms.SRES_MODEL]) ]
        ccustom: Dict[str,Any] = {}
        if (context[parms.SRES_DEVICE] != None):
            cli_device_override: Dict[str,Any] = { 'sres_device': context[parms.SRES_DEVICE] }
        else:
            cli_device_override: Dict[str,Any] = {}

        yscale = "log"

        configuration = dict(
            platform = context[parms.SRES_PLATFORM], #"explore",
            task = context[parms.SRES_TASK], #"cape_basin",
            dataset = context[parms.SRES_DATASET], # "LLC4320"
        )

        if str(context[parms.SRES_ACTION]).endswith('train'):
            refresh =  False
            controller = ActionController( cname, configuration, refresh_state=refresh, interp_loss=True )
            controller.train( models, **ccustom )
        elif str(context[parms.SRES_ACTION]).endswith('infer'):
            # refresh =  False
            controller = ActionController( cname, configuration, interp_loss=True )
            model = models[0]
            controller.infer( model, [ 0, 10 ], **cli_device_override )
        else:
            print("Invalid action = " + str(context[parms.SRES_ACTION]))
   
    except BaseException as err:
            print('\nWorkflow processing failed - Error details: ', err)

    elapsed_time = (time.time() - start_time) / 60.0
    print("\n" + str("{0:0.2f}".format(elapsed_time)) + " Total Elapsed Minutes for :" + str(context))


if __name__ == "__main__":
    from unittest.mock import patch

    start_time = time.time()  # record start time

    maindir = '/adapt/nobackup/projects/ilab/data/srlite'

    r_fn_ccdc = \
        '/panfs/ccds02/nobackup/people/iluser/projects/srlite/test/input/baseline/WV02_20150911_M1BS_1030010049148A00-ccdc.tif'
    r_fn_evhr = \
        '/panfs/ccds02/nobackup/people/iluser/projects/srlite/test/input/baseline/WV02_20150911_M1BS_1030010049148A00-toa.tif'
    r_fn_cloud = \
        '/panfs/ccds02/nobackup/people/iluser/projects/srlite/test/input/baseline/WV02_20150911_M1BS_1030010049148A00-toa.cloudmask.v1.2.tif'


    # If not arguments specified, use the defaults
    numParms = len(sys.argv) - 1
    if numParms == 0:

        with patch("sys.argv",

                   ["SrliteWorkflowCommandLineView.py",
                    "-toa_dir", r_fn_evhr,
                    "-target_dir", r_fn_ccdc,
                    "-cloudmask_dir", r_fn_cloud,
                    "-bandpairs",
                    #"[['blue_ccdc', 'BAND-B'],['green_ccdc','BAND-G'],['red_ccdc','BAND-R'],['nir_ccdc','BAND-N']]",
                    #                "-bandpairs", "[['BAND-B', 'blue_ccdc'], ['BAND-G', 'green_ccdc'],
                    #                ['BAND-R', 'red_ccdc'], ['BAND-N', 'nir_ccdc']]",
                    "[['blue_ccdc', 'BAND-B'], ['green_ccdc', 'BAND-G'], ['red_ccdc', 'BAND-R'], ['nir_ccdc', 'BAND-N'], ['blue_ccdc', 'BAND-C'], ['green_ccdc', 'BAND-Y'], ['red_ccdc', 'BAND-RE'], ['nir_ccdc', 'BAND-N2']]",
                    "-output_dir", "/explore/nobackup/people/gtamkin/dev/srlite/test/v2_srlite-2.0-rma-baseline/20240305-cantfingbelieveit",
                    "--debug", "1",
                    "--regressor", "rma",
                    "--clean",
                    "--cloudmask",
                    "--pmask",
                    "--csv",
                    ]):
            ##############################################
            # main() using default application parameters
            ##############################################
            print("Default application parameters: {sys.argv}")
            main()
    else:

        ##############################################
        # main() using command line parameters
        ##############################################
        main()
