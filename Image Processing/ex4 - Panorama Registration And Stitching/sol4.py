# -*- coding: utf-8 -*-
"""
@author: Ofir
"""
import numpy as np
import sol4_utils as sol4_utils
import sol4_add as sol4_add
import scipy as scipy
import matplotlib.pyplot as plt


def harris_corner_detector(im):
    der_array = np.array([1,0,-1]).reshape(3,1)
    Ix = scipy.ndimage.filters.convolve(im, der_array)
    Iy = scipy.ndimage.filters.convolve(im, np.transpose(der_array))
    kernel = sol4_utils.get_guassian(3)
    IxIx = sol4_utils.blur_spatial(Ix*Ix, kernel)
    IxIy = sol4_utils.blur_spatial(Ix*Iy, kernel)
    IyIx = sol4_utils.blur_spatial(Iy*Ix, kernel)
    IyIy = sol4_utils.blur_spatial(Iy*Iy, kernel)
    R = (IxIx*IyIy-IyIx*IxIy) - 0.04*((IxIx+IyIy)**2)
    binary_local_maximum = sol4_add.non_maximum_suppression(R)
    return np.transpose(np.roll(np.nonzero(binary_local_maximum), 1, axis=0))
    
    
def sample_descriptor(im, pos, desc_rad=3):
    """
    im − grayscale image to sample within.
    pos − An array with shape (N,2) of [x,y] positions to sample descriptors in im.
    desc rad − ”Radius” of descriptors to compute (see below).
    desc − A 3D array with shape (K,K,N) containing the ith descriptor at desc(:,:,i). The per−descriptor dimensions KxK
    are related to the desc rad argument as follows K = 1+2∗desc rad.
    """
    k = 1 + 2*desc_rad
    desc = np.zeros((k,k,pos.shape[0]), dtype=np.float32)
    rows, cols = im.shape
    for i in range(pos.shape[0]):
        x, y = pos[i]
        g1 = np.meshgrid(y + np.arange(-desc_rad,+desc_rad+1),
                         x + np.arange(-desc_rad,+desc_rad+1))
        sample = scipy.ndimage.map_coordinates(im, (g1), 
                                               order=1,prefilter=False) 
        sample = sample - np.mean(sample)
        diff = np.linalg.norm(sample - np.mean(sample))
        if diff != 0:
            sample = (sample)/np.linalg.norm(diff)
        desc[:,:,i] = sample
    return desc
        
    
    
def find_features(pyr):
    """
    pyr − Gaussian pyramid of a grayscale image having 3 levels.
    pos − An array with shape (N,2) of [x,y] feature location per row found in the (third pyramid level of the) image. These
    coordinates are provided at the pyramid level pyr[0].
    desc − A feature descriptor array with shape (K,K,N).
    """
    pos = sol4_add.spread_out_corners(pyr[0], 7, 7, 3)
    pos_3 = pos[:] / 4
    desc = sample_descriptor(pyr[2], pos_3)
    return pos, desc
    

def match_features(desc1, desc2, min_score=0.8):
    flat_desc1 = np.reshape(desc1, (-1, desc1.shape[-1]))
    flat_desc2 = np.reshape(desc2, (-1, desc2.shape[-1]))
    scores = np.dot(np.transpose(flat_desc1), flat_desc2)
    
    scores_rows_sort = np.sort(scores,axis=1)
    sec_max_each_row = scores_rows_sort[:,-2]
    sec_max_each_row[sec_max_each_row < min_score] = 1
    res1 = np.transpose(np.transpose(scores) - sec_max_each_row + 0.0001)
    
    scores_cols_sort = np.sort(scores, axis=0)
    sec_max_each_col = scores_cols_sort[-2,:]   
    sec_max_each_col[sec_max_each_col < min_score] = 1
    res2 = scores - sec_max_each_col + 0.0001

    res1[res1 < 0] = 0
    res2[res2 < 0] = 0
    return np.where(res1*res2 > 0)

    
def apply_homography(pos1, H12):
    pos2 = np.zeros((pos1.shape[0],pos1.shape[1]+1))
    pos1 = np.insert(pos1, pos1.shape[1], 1, axis=1)
    p00 = H12[0,0]*pos1[:,0]
    p01 = H12[0,1]*pos1[:,1]
    p02 = H12[0,2]*pos1[:,2]
    p10 = H12[1,0]*pos1[:,0]
    p11 = H12[1,1]*pos1[:,1]
    p12 = H12[1,2]*pos1[:,2]
    p20 = H12[2,0]*pos1[:,0]
    p21 = H12[2,1]*pos1[:,1]
    p22 = H12[2,2]*pos1[:,2]
    pos2[:,0] = p00+p01+p02
    pos2[:,1] = p10+p11+p12
    pos2[:,2] = p20+p21+p22
    
    pos2[:,0] = pos2[:,0] / pos2[:,2]
    pos2[:,1] = pos2[:,1] / pos2[:,2]
    return pos2[:,[0,1]]
    
    
def ransac_homography(pos1, pos2, num_iters=10000, inlier_tol=6):
    maxInliers = 0
    inliers = np.zeros(pos1.shape[0])
    current_inliers = np.zeros(pos1.shape[0])
    for j in range(num_iters):
        idx_sample = np.random.permutation(pos1.shape[0])[:4]
        H12 = sol4_add.least_squares_homography(pos1[idx_sample], pos2[idx_sample])
        if H12 is None:
            continue
        P2_tag = apply_homography(pos1, H12)
        Ej = (P2_tag-pos2)
        summed_rows = np.abs(Ej[:,0]) + np.abs(Ej[:,1])
        current_inliers = np.where(summed_rows < inlier_tol)[0]
        if np.size(current_inliers) > maxInliers:
            maxInliers = np.size(current_inliers)
            inliers = current_inliers
    H12 = sol4_add.least_squares_homography(pos1[inliers], pos2[inliers])
    return H12, inliers
    
    
def display_matches(im1, im2, pos1, pos2, inliers):
    im = np.hstack((im1,im2))
    plt.imshow(im, 'gray')
    width_im1 = im1.shape[1]
    plt.plot([pos1[:,0],width_im1+pos2[:,0]], [pos1[:,1],pos2[:,1]], mfc='r', c='b', lw=.1, ms=4, marker='o')
    plt.plot([pos1[:,0][inliers],width_im1+pos2[:,0][inliers]], [pos1[:,1][inliers],pos2[:,1][inliers]], mfc='r', c='y', lw=.4, ms=4, marker='o')
    plt.show()

    
def accumulate_homographies(H_successive, m):
    hm_length = len(H_successive)
    H2m = np.empty((hm_length + 1,3,3))
    H2m[m] = np.eye(3)
    for i in reversed(range(m)):
        H2m[i] = np.dot(H2m[i+1], H_successive[i])
        H2m[i] = H2m[i]/(H2m[i][2,2])
    for i in range(m+1, hm_length+1):   
        H2m[i] = np.dot(H2m[i-1], np.linalg.inv(H_successive[i-1]))
        H2m[i] = H2m[i]/(H2m[i][2,2])   
    return list(H2m)
    

def render_panorama(ims, Hs):
    max_row, min_row, max_col, min_col, trans_centers,min_max_corners = compute_pano(ims,Hs)
    Rowscord,Colscord = np.meshgrid(np.arange(min_row,max_row+1),
                                    np.arange(min_col,max_col+1),
                                    indexing='ij')
    panorama = np.empty(Rowscord.shape).astype(np.float32)
    cols_borders = np.empty((len(ims)+1), dtype=np.int)
    cols_borders[0] = 0
    cols_borders[len(ims)] = panorama.shape[1]
    for i in range(1, len(ims)):
        cols_borders[i] = ((trans_centers[i-1,0] + 
                            trans_centers[i,0])/2) - min_col
    for i in range(len(ims)):
        x = Rowscord[:, np.arange(panorama.shape[1])]
        y = Colscord[:, np.arange(panorama.shape[1])]
        rev_im_pos = np.transpose(np.vstack((y.flatten(), x.flatten())))
        pano_im_pos = apply_homography(rev_im_pos, np.linalg.inv(Hs[i]))
        xPan = pano_im_pos[:,0]
        yPan = pano_im_pos[:,1]
        xPan = xPan.reshape(x.shape)
        yPan = yPan.reshape(y.shape)
        pano_im = scipy.ndimage.map_coordinates(ims[i],
                       [yPan,xPan],order=1, prefilter=False)
        panorama = stiching(panorama, pano_im, cols_borders[i])
    return panorama
    
    
def compute_pano(ims, Hs):
    max_row, min_row, max_col, min_col = 0,0,0,0
    corners = np.empty((4, 2))
    trans_centers = np.empty((len(ims),2))
    min_max_corners = np.empty((len(ims),2))
    for i in range(len(ims)):
        corners = np.array([[0,0], [ims[i].shape[1],0], [0,ims[i].shape[0]], 
                            [ims[i].shape[1],ims[i].shape[0]]])
        trans_corners = apply_homography(corners, Hs[i])
        min_max_corners[i,0] = np.amin(trans_corners[:,0])
        min_max_corners[i,1] = np.amax(trans_corners[:,0])
        max_row = max(max_row, np.amax(trans_corners[:,1]))
        min_row = min(min_row, np.amin(trans_corners[:,1]))
        max_col = max(max_col, np.amax(trans_corners[:,0]))
        min_col = min(min_col, np.amin(trans_corners[:,0]))
        centersX = (ims[i].shape[1])/2
        centersY = (ims[i].shape[0])/2
        trans_centers[i,:] = apply_homography(np.transpose(np.vstack((centersX,centersY))), Hs[i])  
    return max_row,min_row,max_col,min_col, trans_centers, min_max_corners-min_col
        
 
def stiching(panorama, im_pano, border):
    mask = np.zeros(panorama.shape)
    mask[:,np.arange(border)] = 1
    pano_blend = sol4_utils.pyramid_blending(panorama,im_pano,mask,5,7,7)
    return pano_blend
    
