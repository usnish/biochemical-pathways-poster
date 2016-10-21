# Biochemical Pathways Poster

After officially shutting down print production of its famous biochemical pathways posters, Roche made the posters available via a [nifty online interface](http://biochemical-pathways.com/#/map/1).
This script will download and assemble the Metabolic Pathways poster from the tiles hosted on their server to give you a printable, large PNG file.

[For the lazy: lower-quality JPEG of whole image](https://github.com/usnish/biochemical-pathways-poster/blob/master/finalimg.jpg)

![preview jpeg](preview.jpg)

## Requirements
You will need `Python > 3.5.2` and [ImageMagick](http://www.imagemagick.org/script/index.php). I ran this script on OSX, and do not know if it works on Windows.
Additionally, make sure you have all the requirements in `requirements.txt` by running `pip install -r requirements.txt`.

## Usage
`python extract_matabol.py` will dump all the raw tiles in `images/`, assembled layers in `assembled/`, and final images in the root directory.

## Future features
Higher zoom level (massive image)
Printable part 2: cellular mechanisms
