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




# Project Structure

The project conforms to the popular PyScaffold putup command structure for a basic python project.  The current package is only one level deep and consists of skeleton and currently only computes Fibonacci numbers.  To build and see this in action, the fibonacci command is exposed in the setup.cfg file so to build the project, in the directory run:

```
python setup.py build
```

Then run this to install the fibonacci command:

```
python setup.py install
```

And finally you should be able to put in commands like:

```
fibonacci 7
```

To see the seventh fib number.  To run the tests execute the following command:

```
python setup.py test
```

Right now it does test coverage but that can be disabled to just be straight up tests only.

## Developing Your Own Pipeline

Given the project structure above, it's trivial to implement your own script/entry point to the project.  Open setup.cfg and add a line to the console_scripts construct like so:

```
console_scripts =
    fibonacci = strangers_kaggle.skeleton:run
    skimagerun = strangers_kaggle.image_processor:run
```

Here I've added a command called skimagerun and assigned it to the newly added image_processor file.  If you open that up, it's got the same structure as skeleton.py and the argsparse shows one argument that it accepts.  So to compile this the first step is to install the new requirements that are imported in the file.  Do that by running this (or just the pip command if you have it):

```
sudo python -m pip install -r requirements.txt
```

Then compile and install the project with

```
python setup.py install
```

 After that's done you can see it enumerate a directory if you pass it into it by running the new command:

 ```
 skimagerun /media/david/63A92C5A7385D4CA/data/dstlsatellite/three_band/
 ```

 Where the directory is one on your computer that contains the TIFs.  You should see it enumerate the files in the directory.  

 In order to get the transform data in (yMin and xMax), provide the csv file as input to skimagerun for example:

 ```
 skimagerun /media/david/63A92C5A7385D4CA/data/dstlsatellite/sixteen_band/ -f /media/david/63A92C5A7385D4CA/data/dstlsatellite/grid_sizes.csv
 ```

 The program will now display the file dimension data followed by the tuple read from the supplied csv.  A nice cookbook for gdal is [here](https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html).

Now you can segment based on the training like this:

```
skimagerun /media/david/63A92C5A7385D4CA/data/dstlsatellite/three_band/ -f /media/david/63A92C5A7385D4CA/data/dstlsatellite/grid_sizes.csv -t /media/david/63A92C5A7385D4CA/data/dstlsatellite/train_wkt_v4.csv
```

That command will create a directory next to "three_band" with masks to show what has been classified as what in the training data.
