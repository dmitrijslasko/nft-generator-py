
# NFT Image Generator (Layers to Single Image)

#### A Python script to generate NFT-style images (unique combinations of multiple individual layers)

## Description
#### The script contains two directories:

**(1) layers** \
This folder should contain the layers to be used in the image generation.
**It is advised to use the format that already exists there, i.e. "1 body", "2 eyes", etc.**
Here, the number defines the order of how the layers get added to the image (the lowest the number – the earlier it is used in the generation).
The number of directories (layers) can be any number, it is not anyhow limited.

**Filenames inside the folders don't matter that much, but they will affect the resulting file names.**
If there is demand, the script will later get updated to allow custom output image size / quality (ppi).

  

**(2) results** \
This folder will contain the results of the generation.

  

### Usage & flags:

1) Clone the folder to your system (git clone ...)
2) Create virtual environment (python -m venv .venv)
3) Activate virtual environment (source ./venv/bin/activate)
4) Install the required dependencies (pip install -r requirements.txt)
5) Paste the layer individual images (PNG) into the layers folder, grouped in individual layer directories
6) Run the script (python generate.py)
7) Open the folder (open .) to see the results (in the results folder)


#### Flags:

--all: generate all possible combinations. Before the launch, the script will calculate the number of possible combinations and ask for a y/n confirmation.

-r, --random [count]: generate a number of random combinations. The files that were generated with this flag, will have a "random_" prefix.	\
-b, --black: set the background color to black	\
-w, --white: set the background color to white	\
-t, --transparent: set the background color to transparent (default option)

##### In progress:

-s, --size: set the output size.
Currently, because of the output size limitations, the advised size to be used for the layers if 1000px (1000 x 1000 px).


#### Launch examples:

python generate.py --random 5: generate 5 random image combinations \
python generate.py --random 10: generate 10 random image combinations \
python generate.py --all: generate all possible image combinations

##### Message me here on github or anywhere else if you have any questions, want to request a feature or want to collaborate.
E-mail: dmitrijs.lasko@gmail.com \
Instagram: @dimilasko

