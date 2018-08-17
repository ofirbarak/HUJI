# -*- coding: utf-8 -*-
"""
@author: Ofir
"""
import os as os
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc,signal
import scipy as scipy
from skimage.color import rgb2gray

def read_image(filename, representation):
    """
    Read image 
    @filename: file name
    @representation: 1 == gray, other=RGB
    """
    im = misc.imread(filename)
    if representation == 1:
        return rgb2gray(im).astype(np.float32)
    im_float = im.astype(np.float32)
    im_float /= 255
    return im_float

    
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
    
    
def blur_spatial(im, filter_vec):
    """ blur image """
    ret_im = scipy.ndimage.filters.convolve(im, filter_vec, mode='wrap')
    return scipy.ndimage.filters.convolve(ret_im, np.transpose(filter_vec), 
                                          mode='wrap')

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
    
    
def render_pyramid(pyr, levels):
    height = 0
    for im in pyr:
        height = max(height, im.shape[0])                
    for i in range(levels):
        pyr[i].clip(0,1)
        pyr[i] = (pyr[i] - np.min(pyr[i]))/ (np.max(pyr[i]-np.min(pyr[i])))
    res = pyr[0]
    last_c = pyr[0].shape[1]
    for i in range(1, levels):
        r,c = pyr[i].shape
        ex_im = np.pad(np.transpose(pyr[i]), [(0,0), (0,height-r)],'constant')
        res = np.insert(res, last_c, ex_im, axis=1)
        last_c += c
    return res 
    
    
def display_pyramid(pyr, levels):
    plt.imshow(render_pyramid(pyr, levels), cmap=plt.cm.gray)
    
    
def pyramid_blending(im1, im2, mask, max_levels, filter_size_im, filter_size_mask):
    lpyr1, im1_vec = build_laplacian_pyramid(im1, max_levels, filter_size_im)
    lpyr2, im2_vec = build_laplacian_pyramid(im2, max_levels, filter_size_im)
    gpyr, mask_vec = build_gaussian_pyramid(mask.astype(np.double), max_levels, filter_size_mask)
    lpyr_out = list()
    for k in range(max_levels):
        lpyr_out.append(gpyr[k]*lpyr1[k] + (1-gpyr[k])*(lpyr2[k]))
    im_blend = laplacian_to_image(lpyr_out, mask_vec, np.ones(max_levels))
    return im_blend.astype(np.float32)
    
    
def blending_example1():
    im1 = read_image(relpath('example1/man_strech_smile.jpg'), 0).astype(np.float32)
    im2 = read_image(relpath('example1/monkey_smile2.jpg'), 0).astype(np.float32)
    mask_im = read_image(relpath('example1/mask.jpg'), 1).astype(np.float32)
    mask = (mask_im == 1)
    max_levels = 2
    filter_size_image = 5
    filter_size_mask = 5
    plt.figure()
    plt.subplot(221)
    plt.imshow(im1)
    plt.subplot(222)
    plt.imshow(im2)
    plt.subplot(223)
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.subplot(224)
    b = np.zeros(im1.shape).astype(np.float32)
    for i in range(3):
        b[:,:,i] = pyramid_blending(im1[:,:,i], im2[:,:,i], mask, max_levels, 
                                    filter_size_image, filter_size_mask)
    plt.imshow(b)
    plt.show()
    return im1, im2, mask.astype(np.bool), b
    
    
def blending_example2():
    im1 = read_image(relpath('example2/dog.jpg'), 0).astype(np.float32)
    im2 = read_image(relpath('example2/man_with_glasses.jpg'), 0).astype(np.float32)
    mask_im = read_image(relpath('example2/mask2.jpg'), 1).astype(np.float32)
    mask = (mask_im == 1)
    max_levels = 4
    filter_size_image = 5
    filter_size_mask = 5
    plt.figure()
    plt.subplot(221)
    plt.imshow(im1)
    plt.subplot(222)
    plt.imshow(im2)
    plt.subplot(223)
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.subplot(224)
    b = np.zeros(im1.shape).astype(np.float32)
    for i in range(3):
        b[:,:,i] = pyramid_blending(im1[:,:,i], im2[:,:,i], mask, max_levels, 
                                    filter_size_image, filter_size_mask)
    plt.imshow(b)
    plt.show()
    return im1, im2, mask, b

    
def relpath(filename):
    return os.path.join(os.path.dirname(__file__), filename)
    

