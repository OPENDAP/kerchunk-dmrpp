# Kerchunk-dmrpp 

## Description:
 This software is a proof of concept that a geotiff file can be converted to a json file

## To install:
1. clone the git repository `git clone https://github.com/OPENDAP/kerchunk-dmrpp.git`
2. create a conda/mamba env `conda env create -f environment.yml`
3. install additional libraries `conda env update -n dmrpp_tests -c conda-forge fsspec ujson tifffile`

## To Run:
1. activate the conda/mamba env `conda activate dmrpp_tests`
2. copy desired geotiff file into the 'input_files' directory
3. run `python test_kerchunk.py -i input_files/'geotiff_filename_here' -o 'output_filename_here'`
4. Alternatively you can just provide the input filename and the script will generate an output filename automatically \
`python test_kerchunk.py -i input_files/'geotiff_filename_here'`

## To Run Notebook
1. activate the conda/mamba env `mamba activate dmrpp_tests`
2. Launch the jupyterlab server to run the notebook on the browser `jupyter lab`


## Helpful Links:
 - https://fsspec.github.io/kerchunk/
 - https://fsspec.github.io/kerchunk/reference.html
 - https://fsspec.github.io/kerchunk/tutorial.html
 - https://projectpythia.org/kerchunk-cookbook/
 - https://guide.cloudnativegeo.org/zarr/virtual-zarr.html
 - https://guide.cloudnativegeo.org/kerchunk/kerchunk-in-practice.html
    
