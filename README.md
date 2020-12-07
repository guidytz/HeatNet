# HeatNet
A simple script that receives a SUMO network and a csv containing occupation information through time and generates
a gif file with the heatmap of the network in each step time.

## Dependencies 
You need to have [SUMO](https://github.com/eclipse/sumo) and [matplotlib](https://matplotlib.org/) installed. 

To install SUMO, run the following:

```
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc 
```

To install matplotlib, simply run the following:

```
python3 -m pip install -U matplotlib
```


## Usage
In order to execute script one must type the following sequence:

```
python3 main.py -n <path_to_network_file> -p <path_to_csv_file>
```

Other options are available, and the user may refer to the following options:

```
usage: main.py [-h] [-n NET_PATH] [-p PATH] [--avg] [--fps FPS]

HeatNet - A heatmap maker to evaluate a network load over time

optional arguments:
  -h, --help            show this help message and exit
  -n NET_PATH, --network NET_PATH
                        Path to the network file (mandatory)
  -p PATH, --path PATH  Path to folder containing csv files to take average (mandatory)
  --avg                 Informs if path has one or multiple csv files and, in case of multiple files, 
                        the heatmap considers an average of those files
  --fps FPS             Set the the gif fps (default = 4)
```

One can test the scrip with the example [5x5 network](https://github.com/guidytz/HeatNet/tree/master/scenario/5x5).

The resulting gifs can be seen in [animations](https://github.com/guidytz/HeatNet/tree/master/animations).