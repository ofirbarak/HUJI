# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:00:26 2016

@author: Ofir
"""
import numpy as np
from scipy import misc
from scipy import signal
import matplotlib.pyplot as plt
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
    
def get_dft_mat(N,invert=False):
    coefficient = -1
    if invert:
        coefficient = 1
    i = np.arange(N)
    j = i.reshape(N, 1)
    omega = np.exp(coefficient * 2 * np.pi * (i * j) * 1J / N)
    return omega
 
def DFT(signal):
    N = signal.shape[0]
    return get_dft_mat(N).dot(signal).astype(np.complex128)    

def IDFT(fourier_signal):
    N = fourier_signal.shape[0]
    return (((get_dft_mat(N, True)).dot(fourier_signal))/N).astype(np.complex128)

def DFT2(image):
    N, M = image.shape
    temp = np.zeros(image.shape, dtype=np.complex128)
    for i in range(M):
        temp[:,i] = (DFT(image[:,i]))
    for i in range(N):
        temp[i,:] = (DFT(temp[i,:]))
    return temp

def IDFT2(fourier_image):
    N,M = fourier_image.shape
    temp = np.empty(fourier_image.shape, dtype=np.complex128)
    for i in range(M):
        temp[:,i] = IDFT(fourier_image[:,i])
    for i in range(N):
        temp[i,:] = IDFT(temp[i,:])
    return temp 
    
def conv_der(im):
    derY = signal.convolve2d(im, (np.array([-1, 0, 1]).reshape(3,1)),'same')
    derX = signal.convolve2d(im, (np.array([-1, 0, 1]).reshape(1,3)),'same')
    return np.sqrt(np.abs(derY)**2 + np.abs(derX)**2)
    
def fourier_der(im):
    N, M = im.shape
    fourier_im = DFT2(im)
    shift_im = np.fft.fftshift(fourier_im)
    u_y = np.tile(np.arange(-M/2, M/2), (N,1))
    u_x = np.transpose(np.tile(np.arange(-N/2, N/2), (M,1)))
    derX = shift_im*u_x
    derY = shift_im*u_y
    ishift_derX = np.real(IDFT2(np.fft.ifftshift(derX))*(2*np.pi*1j)/(N*M))
    ishift_derY = np.real(IDFT2(np.fft.ifftshift(derY))*(2*np.pi*1j)/(M*N))
    return np.sqrt(np.abs(ishift_derY)**2 + np.abs(ishift_derX)**2)

def get_guassian(kernel_size):
    first_gaussian_array = np.array([1,1]).reshape(1,2)
    middle_kernel_row = first_gaussian_array
    for i in range(kernel_size):
        middle_kernel_row = signal.convolve2d(middle_kernel_row, first_gaussian_array)
        if middle_kernel_row.shape[1] == kernel_size:
            break
    kernel = signal.convolve2d(middle_kernel_row, middle_kernel_row.reshape(kernel_size,1))
    return kernel/sum(kernel)
    
def blur_spatial(im, kernel_size):
    return signal.convolve2d(im, get_guassian(kernel_size), 
                             mode='same', boundary='wrap')
        
def blur_fourier(im, kernel_size):
    N, M = im.shape
    padded_kernel = np.pad(get_guassian(kernel_size), 
                           ((N//2-kernel_size//2 -1, N//2-kernel_size//2), 
                            (M//2-kernel_size//2 -1, M//2-kernel_size//2)), 
                            'constant', constant_values=0)
    fourier_kernel = np.fft.fftshift(DFT2(padded_kernel))                      
    fourier_image = DFT2(im)
    return np.real(np.fft.ifftshift(IDFT2(fourier_image*np.fft.ifftshift(fourier_kernel))))

