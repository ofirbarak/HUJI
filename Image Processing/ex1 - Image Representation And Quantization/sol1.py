# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread as imread, imsave as imsave
from skimage.color import rgb2gray

def read_image(filename, representation):
    """
    Read image 
    @filename: file name
    @representation: 1 == gray, other=RGB
    """
    im = imread(filename)
    if representation == 1:
        return rgb2gray(im).astype(np.float32)
    im_float = im.astype(np.float32)
    im_float /= 255
    return im_float

def imdisplay(im, representation):
    """
    Display image
    @im: image to display
    @representation: 1==gray, other=RGB
    """
    if representation == 1:
        plt.imshow(im, cmap=plt.cm.gray)
    else:
         plt.imshow(im)

def getMatrix():
    """
    Return the matrix to convert from RGB to YIQ
    """
    return np.array([[0.299,0.587,0.114],
                   [0.596,-0.275,-0.321],
                   [0.212,-0.523,0.311]])

def mul_matrix(a):
    """
    Mul matrix
    """
    return np.dot(getMatrix(), np.array(a))
         
def rgb2yiq(imRGB):
    """
    convert from RGB to YIQ
    """
    return np.apply_along_axis(mul_matrix, 2, imRGB)

def mul_rev_matrix(a):
    """
    mul the invert matrix
    """
    return np.dot(np.linalg.inv(getMatrix()), a)
    
def yiq2rgb(imYIQ):
    """
    convert from YIQ to RGB
    """
    return np.apply_along_axis(mul_rev_matrix, 2, imYIQ)
    
def histogram_equalize(im_orig):
    """
    Preform a histogram equlization
    """
    cut_im = im_orig
    ret = im_orig
    if len(im_orig.shape) > 2: # RGB image
        ret = rgb2yiq(im_orig)
        cut_im = ret[:,:,0]
    im256 = (cut_im*255).round().astype(np.uint8)
    hist_orig, bins = np.histogram(im256, 256,[0,256])
    chist = np.cumsum(hist_orig).astype(np.float32)
    chist = chist/chist[-1] * 255   
    cdf_m = np.ma.masked_equal(chist,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    streach = np.ma.filled(cdf_m,0).astype('uint8')
    streach = np.around(streach)
    temp = np.interp(im256.flatten(), bins[:-1], streach, right=1, left=0)  
    temp = temp / 255
    if len(im_orig.shape) > 2: # RGB image
        ret[:,: ,0] = temp.reshape(cut_im.shape)
        im_eq = np.clip(yiq2rgb(ret), 0, 1)
        calc_hist_eq = ret[:,:,0]
    else:
        im_eq = temp.reshape(cut_im.shape)
        calc_hist_eq = im_eq

    return (im_eq, hist_orig, np.histogram((calc_hist_eq*255).astype(np.uint8),
                                           256,[0,256])[0])
    
def find_nearest(array,value):
    """
    find the index in array that is nearest to value
    """
    idx = (np.abs(array-value)).argmin()
    return idx

def quantize(im_orig, n_quant, n_iter):
    """
    preform quatize
    """
    cut_im = im_orig
    ret = im_orig
    if len(im_orig.shape) > 2: # RGB image
        ret = rgb2yiq(im_orig)
        cut_im = ret[:,:,0]
    im256 = (cut_im*255).round().astype(np.uint8)
    hist_orig, bins = np.histogram(im256, 256,[0,256])
    z = np.zeros(n_quant+1, dtype=np.uint8)
    sum_hist = np.cumsum(hist_orig)
    for i in range(1, n_quant):
        z[i] = find_nearest(np.ma.masked_equal(sum_hist,0), 
                            i/n_quant*sum_hist[-1])
    z[n_quant] = 255
    error = list()
    q = np.zeros(n_quant, dtype=np.float32)
    for iteration in range(n_iter):
        last_z = np.ndarray.copy(z)
        for i in range(len(q)):
            sumD = np.sum(hist_orig[z[i]: z[i+1]+1])
            temp = np.arange(z[i], z[i+1]+1)
            sumM = np.sum(np.multiply(hist_orig[z[i]: z[i+1]+1], temp))
            q[i] = sumM/sumD
        for i in range(1, len(z)-1):
            z[i] = round((q[i-1] + q[i])/2.0)
        error_sum = 0
        for i in range(n_quant):
            temp = np.arange(z[i], z[i+1])
            temp = np.apply_along_axis(lambda x: (q[i]-x)**2, 0 ,temp)
            error_sum += np.sum(np.multiply(hist_orig[z[i]:z[i+1]], temp))
        error.append((error_sum))
        if (np.asarray(last_z) == np.asarray(z)).all():
            break
    
    temp = cut_im.flatten()
    im256 = im256.flatten()
    # Build LUT
    lut = np.array([q[0]], dtype=np.uint8)
    for i in range(n_quant):
        lut = np.append(lut, np.array([q[i]]*(z[i+1]-z[i])))
    temp = lut[im256]
    temp = temp / 255
    if len(im_orig.shape) > 2: # RGB image
        ret[:,: ,0] = temp.reshape(cut_im.shape)
        im_quant = yiq2rgb(ret)
        #im_quant = np.clip(im_quant, 0, 1)
    else:
        im_quant = temp.reshape(cut_im.shape)
    return (im_quant, error)