# this script will download and assemble the metabolic pathways poster from biochemical-pathways.com
# Usnish Majumdar, 10/21/16
# IMPORTS
import urllib.request
from subprocess import call
from PIL import Image

zoomLevel = 3  # change this to either 3 or 4, 4 is higher-resolution than 3
dim = {
    3: [7, 5, 7 * 1024, 5 * 1024, 6829, 4795],
    4: [14, 10, 14 * 1024, 10 * 1024, 13659, 9574]
}  # contains all the dimensions required given a certain zoom level

# quick function to create two-digit number strings so everything stays in
# order


def dig2(i):
    if len(str(i)) == 2:
        return str(i)
    else:
        return '0' + str(i)

# downloads tiles


def download_tiles(zoom_level, layer, dimensions=dim):
    base_url = 'http://mapserver1.biochemical-pathways.com/map1/'
    base_url_suffix = '.png?v=4'
    filenames = []
    for row in range(dimensions[zoom_level][1]):
        for col in range(dimensions[zoom_level][0]):
            url = base_url + layer + '/' + \
                str(zoom_level) + '/' + str(col) + \
                '/' + str(row) + base_url_suffix
            filename = layer + '_' + \
                str(zoom_level) + '_' + dig2(row) + '_' + dig2(col) + '.png'
            filenames.append('images/' + filename)
            urllib.request.urlretrieve(
                url, 'images/' + filename)  # 1024x1024px

    # at higher magnification, some of the grid images are actually blank 1x1 px
    # images. We have to scale them back so that they'll tile properly
    for filename in filenames:
        with Image.open(filename) as im:
            if im.size[0] < 1024:
                im = im.resize((1024, 1024))
                im.save(filename)

# these will stich together tiles via imagemagick


def assemble_tiles(zoom_level, layer, dimensions=dim):
    dimstring = str(dimensions[zoom_level][0]) + \
        'x' + str(dimensions[zoom_level][1])
    filename = 'images/' + layer + '_' + str(zoom_level) + '_*.png'
    outfile = 'assembled/' + layer + '_' + str(zoom_level) + '.png'
    command = 'montage -mode concatenate -tile ' + \
        dimstring + ' ' + filename + ' ' + outfile
    call(command, shell=True)

# quick function to aid in layering the layers together


def white2alpha(img):
    img = img.convert("RGBA")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    return img

# these are the seven layers of images that come together on the website,
# in order of z-position from back to front
layers = ['background', 'enzymes', 'coenzymes', 'substrates',
          'regulatoryEffects', 'higherPlants', 'unicellularOrganisms', 'grid']

# start with a blank canvas
finalimg = Image.new('RGBA', (dim[zoomLevel][2], dim[zoomLevel][3]), "white")

# iterate through each layer
for l in layers:
    download_tiles(zoomLevel, l)
    assemble_tiles(zoomLevel, l)
    filename = 'assembled/' + l + '_' + str(zoomLevel) + '.png'
    tempimg = Image.open(filename)
    # compose layer on top of previous layers
    finalimg.paste(tempimg, (0, 0), white2alpha(tempimg))
    finalimg.save('in-progress/progress' + l + '.png')
    tempimg.close()

finalimg = finalimg.crop((0, 0, dim[zoomLevel][4], dim[zoomLevel][5]))
finalimg.save('finalimg.png')
