# Legacy scripts

These scripts downloaded map tiles from `mapserver1.biochemical-pathways.com` and stitched them into a single image with Pillow and ImageMagick. That server no longer resolves, so the scripts are kept for reference only.

- `extract_metabol.py`: Part 1, Metabolic Pathways (produced the images in the repo root).
- `extract_cell.py`: Part 2, Cellular and Molecular Processes. Unfinished; it was never verified against the map2 tiles.
- `layer_info.txt`: notes on the tile URL scheme and layer names.
- `requirements.txt`: the 2016 Pillow pin (doesn't install on current Python).
