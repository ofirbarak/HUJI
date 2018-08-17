#######################################
# FILE : ex6.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex6 2015-2016
# DESCRIPTION: Photomosaic
#######################################
# Imports
import mosaic
import sys
import copy


#Constants
TILE_HEIGHT = 40
NUM_CANDIDATES = 10
ZERO = 0
THREE = 3
ONE = 1
TWO = 2
FOUR = 4
FIVE = 5
NUM_ARGUMENTS = 6
ZERO_LIST = [0]
ERROR_MSG = "Wrong number of parameters. The correct usage is:\n " \
            "ex6.py  <image_source> <images_dir> <output_name> <tile_height> " \
            "<num_candidates>"


def compare_pixel(pixel1, pixel2):
    '''
    Return distance between two pixels
    '''
    distance = ZERO
    for i in range(THREE):
        distance += abs(pixel1[i] - pixel2[i])
    return distance


def compare(image1, image2):
    '''
    Return distance between two pictures
    '''
    width = min(len(image1[0]), len(image2[0]))
    height = min(len(image1), len(image2))
    distance = ZERO
    for row in range(height):
        for col in range(width):
            distance += compare_pixel(image1[row][col], image2[row][col])
    return distance


def get_piece(image, upper_left, size):
    '''
    Return a piece from picture
    '''
    # Set the height and width for the piece
    height = min(size[0], len(image)-upper_left[0])
    width = min(size[1], len(image[0])-upper_left[1])
    piece_pic = [[] for i in range(height)]
    # Insert values to piece_pic list
    for row in range(height):
        for col in range(width):
            piece_pic[row].append(image[row+upper_left[0]][col+upper_left[1]])
    return piece_pic


def set_piece(image, upper_left, piece):
    '''
    Replace piece picture one in other
    '''
    # Set the height and width for the piece
    height = min(len(piece), len(image)-upper_left[0])
    width = min(len(piece[0]), len(image[0])-upper_left[1])
    for row in range(height):
        for col in range(width):
            image[row+upper_left[0]][col+upper_left[1]] = piece[row][col]


def average(image):
    '''
    Return average pixel's colors in an image
    '''
    avg_colors = [0,0,0]
    width = len(image[0])
    height = len(image)
    for row in range(height):
        for col in range(width):
            for i in range(THREE):
                avg_colors[i] += image[row][col][i]
    size_pic = width*height
    for i in range(THREE):
        avg_colors[i] = float(avg_colors[i]/size_pic)
    return tuple(avg_colors)


def preprocess_tiles(tiles):
    '''
    Return list of tuples that represent average color each tile
    '''
    avg_tiles_colors = list()
    for index_tile in range(len(tiles)):
        avg_tiles_colors.append(average(tiles[index_tile]))
    return avg_tiles_colors


def get_best_tiles(objective, tiles, averages , num_candidates):
    '''
    Return list of tiles that average color is most similar to a given picture
    '''
    best_tiles = list()
    avg_objective_colors = average(objective)
    compare_pixels_list = list()
    for index_tile in range(len(tiles)):
        compare_pixels_list.append(compare_pixel(tuple(averages[index_tile]),
                                                 avg_objective_colors))
    max_compare_pixels_list = max(compare_pixels_list)
    for i in range(num_candidates):
        min_distance = min(compare_pixels_list)
        best_tiles.append(tiles[compare_pixels_list.index(min_distance)])
        # Insert max value, that not will chosen once again
        compare_pixels_list[compare_pixels_list.index(min_distance)] = max_compare_pixels_list
    return best_tiles


def choose_tile(piece, tiles):
    '''
    Return best mach tile in distance
    '''
    distance_list = list()
    for tile in tiles:
        distance_list.append(compare(tile, piece))
    return tiles[distance_list.index(min(distance_list))]


def make_mosaic(image, tiles, num_candidates):
    '''
    Create photomosaic
    '''
    photomosaic = copy.deepcopy(image)
    height_tile = len(tiles[0])
    width_tile = len(tiles[0][0])
    avg_tiles_colors = preprocess_tiles(tiles)
    for row in range(0, len(image), height_tile):
        col = ZERO
        while col < len(image[0]):
            piece = get_piece(photomosaic, (row,col), (height_tile,width_tile))
            set_piece(photomosaic,
                      (row,col),
                      choose_tile(piece,
                                  get_best_tiles(piece,
                                                 tiles,
                                                 avg_tiles_colors,
                                                 num_candidates))
                      )
            col += width_tile
    return photomosaic


def main():
    '''
    Main function
    '''
    if len(sys.argv) == NUM_ARGUMENTS:
        # Gets the values
        image_source = sys.argv[ONE]
        images_dir = sys.argv[TWO]
        output_name = sys.argv[THREE]
        tile_height = int(sys.argv[FOUR])
        num_candidates = int(sys.argv[FIVE])
        image = mosaic.load_image(image_source)
        tiles = mosaic.build_tile_base(images_dir, tile_height)
        photosomaic = make_mosaic(image, tiles, num_candidates)
        mosaic.save(photosomaic, output_name)
    else:
        sys.stdout.write(ERROR_MSG)


# If the current module is the first one to run
if __name__ == '__main__':
    main()
