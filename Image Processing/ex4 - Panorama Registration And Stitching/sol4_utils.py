# -*- coding: utf-8 -*-
"""
@author: Ofir
"""
import numpy as np
from scipy import signal
import scipy as scipy
from skimage import color
from scipy.misc import imread
import matplotlib.pyplot as plt

def read_image(filename, representation):
    """
    Read image 
    @filename: file name
    @representation: 1 == gray, other=RGB
    """
    im = imread(filename)
    if representation == 1 and im.ndim == 3 and im.shape[2] == 3:
        im = color.rgb2gray(im)
    if im.dtype == np.uint8:
        im = im.astype(np.float32) / 255.0
    return im

def get_guassian(kernel_size):
    """ Create gaussian kernel """
    first_gaussian_array = np.array([1,1]).reshape(1,2)
    middle_kernel_row = first_gaussian_array
    for i in range(kernel_size):
        middle_kernel_row = signal.convolve2d(middle_kernel_row, 
                                              first_gaussian_array)
        if middle_kernel_row.shape[1] == kernel_size:
            break
    return middle_kernel_row/np.sum(middle_kernel_row)
    
def sub_sample(im):
    """
    Take every 2nd pixel of 2nd row
    """
    return np.transpose((np.transpose(im[::2]))[::2])
    
def build_gaussian_pyramid(im, max_levels, filter_size):
    """ buid gaussian pyramid """
    pyr = [im]
    filter_vec = get_guassian(filter_size)
    for i in range(1, max_levels):
        pyr.append(sub_sample(blur_spatial(pyr[i-1], filter_vec)))
        if pyr[i].shape[0] < 16 or pyr[i].shape[1] < 16:
            pyr = pyr[:-1]
            break
    return pyr,filter_vec

def blur_spatial(im, filter_vec):
    """ blur image """
    ret_im = scipy.ndimage.filters.convolve(im, filter_vec, mode='wrap')
    return scipy.ndimage.filters.convolve(ret_im, np.transpose(filter_vec), 
                                          mode='wrap')
    
def build_laplacian_pyramid(im, max_levels, filter_size):
    """" build laplacian pyramid """
    gaussian_pyr, im_filter = build_gaussian_pyramid(im, max_levels, filter_size)
    laplacian_pyr = []
    for i in range(len(gaussian_pyr)-1):
        r,c = gaussian_pyr[i].shape
        im = gaussian_pyr[i] - expand(gaussian_pyr[i+1], im_filter*2, r, c)
        laplacian_pyr.append(im.astype(np.float32))
    laplacian_pyr.append((gaussian_pyr[len(gaussian_pyr)-1]).astype(np.float32))
    return laplacian_pyr, im_filter

def expand(im, im_filter, new_r, new_c):
    """ 
    Expand image to (new_r, new_c)
    """
    r,c= im.shape
    ret_im = np.zeros(new_r*new_c).reshape(new_r, new_c)
    ret_im[::2,::2] = im
    return blur_spatial(ret_im, im_filter)
    
def laplacian_to_image(lpyr, filter_vec, coeff):
    """ create image from laplacian pyramid """
    im = lpyr[len(lpyr)-1]
    for i in range(len(lpyr)-1, 0, -1):
        r, c = lpyr[i-1].shape
        im = lpyr[i-1] + expand(coeff[i]*im, filter_vec*2, r,c)
    return im.astype(np.float32)
    
def pyramid_blending(im1, im2, mask, max_levels, filter_size_im, filter_size_mask):
    lpyr1, im1_vec = build_laplacian_pyramid(im1, max_levels, filter_size_im)
    lpyr2, im2_vec = build_laplacian_pyramid(im2, max_levels, filter_size_im)
    gpyr, mask_vec = build_gaussian_pyramid(mask.astype(np.double), max_levels, filter_size_mask)
    lpyr_out = list()
    for k in range(min(len(lpyr1),len(lpyr2))):
        lpyr_out.append(gpyr[k]*lpyr1[k] + (1-gpyr[k])*(lpyr2[k]))
    im_blend = laplacian_to_image(lpyr_out, mask_vec, np.ones(max_levels))
    return im_blend.astype(np.float32)
