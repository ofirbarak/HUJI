'''
        sys.stdout.write("”Wrong number of parameters. The correct usage is:\nex6.py %s %s %s %s %s"%(image_source,
                                                             images_dir, \
                                                             output_name,
                                                             tile_height,
                                                             num_candidates))
        '''

#python3 ex6.py <image_source> <images_dir> <output_name> <tile_height> <num_candidates>
    image_source = sys.argv[1]
    images_dir = sys.argv[2]
    output_name = sys.argv[3]
    tile_height = sys.argv[4]
    num_candidates = sys.argv[5]
    '''
    if tile_height != TILE_HEIGHT or NUM_CANDIDATES != num_candidates:
        sys.stdout.write(tile_height)
        sys.stdout.write(num_candidates)
    else:

    image = mosaic.load_image('im1.jpg')
    mosaic.show(image)
    tiles = mosaic.build_tile_base(images_dir, tile_height)
    photosomaic = make_mosaic(image, tiles, num_candidates)
    mosaic.save(photosomaic, output_name)



