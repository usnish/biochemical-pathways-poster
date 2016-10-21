import urllib.request
from subprocess import call
from PIL import Image

zoomLevel = 3
dim = {
    3: [7, 5, 7168, 5120, 6829, 4795],
    4: [14, 10]
}


def download_tiles(zoom_level, layer, dimensions=dim):
    base_url = 'http://mapserver1.biochemical-pathways.com/map1/'
    base_url_suffix = '.png?v=4'

    for row in range(dimensions[zoom_level][1]):
        for col in range(dimensions[zoom_level][0]):
            url = base_url + layer + '/' + \
                str(zoom_level) + '/' + str(col) + \
                '/' + str(row) + base_url_suffix
            filename = layer + '_' + \
                str(zoom_level) + '_' + str(row) + '_' + str(col) + '.png'
            urllib.request.urlretrieve(url, 'images/' + filename)


def assemble_tiles(zoom_level, layer, dimensions=dim):
    dimstring = str(dimensions[zoom_level][0]) + \
        'x' + str(dimensions[zoom_level][1])
    filename = 'images/' + layer + '_' + str(zoom_level) + '_*.png'
    outfile = 'assembled/' + layer + '_' + str(zoom_level) + '.png'
    command = 'montage -mode concatenate -tile ' + \
        dimstring + ' ' + filename + ' ' + outfile
    call(command, shell=True)


def white2alpha(img):
    img = img.convert("RGBA")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    return img

layers = ['background', 'enzymes', 'coenzymes', 'substrates',
          'regulatoryEffects', 'higherPlants', 'unicellularOrganisms', 'grid']

finalimg = Image.new('RGBA', (dim[zoomLevel][2], dim[zoomLevel][3]), "white")

for l in layers:
    download_tiles(zoomLevel, l)
    assemble_tiles(zoomLevel, l)
    filename = 'assembled/' + l + '_' + str(zoomLevel) + '.png'
    tempimg = Image.open(filename)
    finalimg.paste(tempimg, (0, 0), white2alpha(tempimg))
    finalimg.save('in-progress/progress' + l + '.png')
    tempimg.close()

finalimg = finalimg.crop((0, 0, dim[zoomLevel][4], dim[zoomLevel][5]))
finalimg.save('finalimg.png')
