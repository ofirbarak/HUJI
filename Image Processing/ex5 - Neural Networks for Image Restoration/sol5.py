from keras.models import Model
from keras.layers import Input,Convolution2D,Activation,merge
from keras.optimizers import Adam
import sol5_utils as sol5_utils
import numpy as np
from skimage import color
from scipy.misc import imread
from scipy.ndimage.filters import convolve

images = dict()

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
    
    
def load_dataset(filenames, batch_size, corruption_func, crop_size):
    while True:
        source = []
        target = []
        for i in np.random.permutation(len(filenames))[:batch_size]:
            filename = filenames[i]
            im = None
            if filename not in images:
                im = read_image(filename, 1)
                #im = im.reshape(1,im.shape[0],im.shape[1])
                images[filename] = im
            else:
                im = images[filename]
            x = corruption_func(im)
            x = x[np.newaxis,...]
            im = im[np.newaxis,...]
            cx = crop_size[1]//2
            cy = crop_size[0]//2
            crop_x = np.random.randint(cx,im.shape[2]-cx)
            crop_y = np.random.randint(cy,im.shape[1]-cy)
            crop_x = np.arange(-cx,cx)+crop_x
            crop_y = np.arange(-cy,cy)+crop_y
            crop_x,crop_y = np.meshgrid(crop_y,crop_x, indexing='ij')
            source.append(x[:,crop_x,crop_y]-0.5)
            target.append(im[:,crop_x,crop_y]-0.5)
        yield np.array(source).astype(np.float32),np.array(target).astype(np.float32)
        
        
def resblock(input_tensor, num_channels):
    a = Convolution2D(num_channels,3,3, border_mode='same')(input_tensor)
    b = Activation('relu')(a)
    c = Convolution2D(num_channels,3,3,border_mode='same')(b)
    d = merge([input_tensor,c], mode='sum')
    return d
    
    
def build_nn_model(height, width, num_channels):
    a = Input(shape=(1, height, width))
    b = Convolution2D(num_channels,3,3,border_mode='same')(a)
    c = Activation('relu')(b)
    d = resblock(c, num_channels)
    for i in range(4):
        d = resblock(d, num_channels)
    e = merge([c, d], mode='sum')
    f = Convolution2D(1,3,3,border_mode='same')(e)
    model = Model(input=a, output=f)
    return model
    
    
def train_model(model,images, corruption_func, batch_size,
                samples_per_epoch ,num_epochs, num_valid_samples):
    images = np.array(images)
    im_len = len(images)
    indexes = np.random.permutation(im_len).astype(int)
    indexes1 = indexes[:round(0.8*im_len)]
    training_set = load_dataset(images[indexes1], batch_size, 
                                corruption_func, model.input_shape[2:])
    indexes2 = indexes[round(0.8*im_len):]
    testing_set = load_dataset(images[indexes2], batch_size, 
                               corruption_func, model.input_shape[2:])
    model.compile(loss='mean_squared_error', optimizer=Adam(beta_2=0.9))
    model.fit_generator(training_set, samples_per_epoch=samples_per_epoch,
                        nb_epoch=num_epochs, validation_data=testing_set,
                        nb_val_samples=num_valid_samples)
    
    
def restore_image(corrupted_image, base_model, num_channels):
    streched_model = build_nn_model(corrupted_image.shape[0],
                                    corrupted_image.shape[1], 
                                    num_channels)
    streched_model.set_weights(base_model.get_weights())
    im = corrupted_image-0.5
    im = im.reshape(1,im.shape[0],im.shape[1])
    result_im = streched_model.predict(im[np.newaxis,...])[0]
    result_im = result_im.reshape(corrupted_image.shape)
    return np.clip(result_im+0.5,0,1).astype(np.float32)
    
    
def add_gaussian_noise(image, min_sigma, max_sigma):
    sigma = np.random.uniform(min_sigma, max_sigma)
    noise = np.random.normal(0, sigma, image.shape)        
    return np.clip(image+noise,0,1).astype(np.float32)


def learn_denoising_model(quick_mode=False):
    files = sol5_utils.images_for_denoising()
    num_channels = 48
    model = build_nn_model(24,24,num_channels)
    if quick_mode:
        train_model(model, files, lambda x: add_gaussian_noise(x,0,0.2), 
                    10, 30, 2, 30)
    else:
        train_model(model, files, lambda x: add_gaussian_noise(x,0,0.2), 
                    100, 10000, 5, 1000)
    return model,num_channels
    
    
    
def add_motion_blur(image, kernel_size, angle):
    kernel2d = sol5_utils.motion_blur_kernel(kernel_size, angle)
    #kernel2d = kernel2d.reshape(kernel2d.shape[0], kernel2d.shape[1])
    return convolve(image, kernel2d).astype(np.float32)
    
    
def random_motion_blur(image, list_of_kernel_sizes):
    angle = np.random.uniform(0, np.pi)
    kernel_size = list_of_kernel_sizes[int(np.random.uniform(0, len(list_of_kernel_sizes)))]
    return add_motion_blur(image, kernel_size, angle)
    
    
def learn_deblurring_model(quick_mode=False):
    images = sol5_utils.images_for_deblurring()
    num_channels = 32
    model = build_nn_model(16,16,num_channels)
    if quick_mode:
        train_model(model, images, lambda x: random_motion_blur(x,[7]),
                    10, 30, 2, 30)
    else:
        train_model(model, images, lambda x: random_motion_blur(x,[7]),
                    100, 10000, 10, 1000)
    return model, num_channels
    
