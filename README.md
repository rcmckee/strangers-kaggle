# strangers-kaggle
A ragtag bunch of strangers. Each having a set of unique skills and backgrounds. Joining forces to learn for fun by working on kaggle.com competitions. Probably while drinking.


## recommendations for getting started

1. Download [all the data files](https://www.kaggle.com/c/dstl-satellite-imagery-feature-detection/data).
   I put them in a `~/kaggle` directory, and then unpacked them.

2. Download miniconda2 for your OS from [here](http://conda.pydata.org/miniconda.html).
3. Install it somewhere.  On OSX, here's what I would do...

        curl -sS https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -o ~/miniconda2.sh
        sudo mkdir /conda
        sudo chown $USER /conda
        bash ~/miniconda2.sh -bfp /conda
        echo "export PATH=/conda/bin:$PATH" >> ~/.bash_profile
        source ~/.bash_profile
        conda update conda

4. Add the conda-forge channel for conda to use.

        conda config --set auto_update_conda false
        conda config --add channels conda-forge

5. Install a bunch of packages from conda-forge.

        conda install gdal jupyter scikit-image tifffile

  Those four packages explode to about 97 with dependencies.

6. Make sure your cwd is `~/kaggle`, then run `jupyter-notebook`.
   Start a new notebook to experiment with.

7. Run these commands to get started.

        %matplotlib inline
        from skimage.external import tifffile
        tifffile.imshow(tifffile.imread('three_band/6010_0_1.tif'))

  and

      import gdal
      from gdalconst import *
      img_filename_16bandA = 'sixteen_band/6100_1_3_A.tif'
      datasetA = gdal.Open(img_filename_16bandA, GA_ReadOnly)
      print('Size is %d x %d x %d' % (datasetA.RasterXSize, datasetA.RasterYSize, datasetA.RasterCount))

