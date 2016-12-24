import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt


def segment(img, name):
    n = 10
    l = 256
    im = ndimage.gaussian_filter(img, sigma=l/(4.*n))
    mask = im > im.mean()
    label_im, nb_labels = ndimage.label(mask)

    plt.imshow(label_im)
