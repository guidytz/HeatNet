import os
import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import sumolib
from math import ceil
import pandas as pd


mpl.use("Agg")
mpl.rcParams['axes.prop_cycle'] = mpl.cycler('color', ["#00ff00", "#77ff00", "#ffff00", "#ff7700", "#ff0000"])
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
ax.set_axis_off()
legend = [plt.Line2D([0], [0], color="C0", lw=1.2),
                plt.Line2D([0], [0], color="C1", lw=1.2),
                plt.Line2D([0], [0], color="C2", lw=1.2),
                plt.Line2D([0], [0], color="C3", lw=1.2),
                plt.Line2D([0], [0], color="C4", lw=1.2)]
df = None
network = None


def get_color(occupation):
    n = int(occupation * 10)
    n = ceil(n / 2)
    color_str = f"C{n}"
    return color_str


def update(i):
    plt.cla()
    step = str(df.iloc[i]["Step"])[:-2]
    text = f"Network Occupation\nStep {step}"
    ax.set_title(text)
    ax.set_axis_off()
    plt.axis('scaled')
    ax.legend(legend, ["0% - 20%", "20% - 40%", "40% - 60%", "60% - 80%", "80% - 100%"], loc="upper center",
              bbox_to_anchor=(1, 0.1))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Rendering step {step}")
    for edge in network.getEdges(withInternal=False):
        for lane in edge.getLanes():
            shape = lane.getShape()
            for j in range(1, len(shape)):
                x = (shape[j-1][0], shape[j][0])
                y = (shape[j-1][1], shape[j][1])
                col = get_color(df.iloc[i][edge.getID()])
                ax.plot(x, y, lw=1.2, color=col)
    return ax


def main():
    parser = argparse.ArgumentParser(description="HeatNet - A heatmap maker to evaluate a network load over time")

    parser.add_argument("-n", "--network", action="store", dest="net_path", help="Path to the network file (mandatory)")
    parser.add_argument("-p", "--path", action="store", dest="path",
                        help="Path to folder containing csv files to take average (mandatory)")
    parser.add_argument("--avg", action="store_true", dest="isAvg", 
                       help="Informs if path has one or multiple csv files and, in case of multiple files, the heatmap\
                             considers an average of those files")
    parser.add_argument("--fps", action="store", dest="fps", default=4, help="Set the the gif fps (default = 4)")
    

    args = parser.parse_args()
    if not args.net_path and not args.path:
        print("Wrong usage!")
        print()
        parser.print_help()
        quit()

    global df, network
    if args.isAvg:
        stream = os.popen(f"ls {args.path}")
        output = stream.read()
        files = output.split('\n')
        files.pop()

        frames = [pd.read_csv(f"{args.path}/{file}") for file in files]
        result = pd.concat(frames)
        by_row_index = result.groupby(result.index)
        df = by_row_index.mean()
        # std = by_row_index.std()
    else:
        df = pd.read_csv(args.path)
        network = sumolib.net.readNet(args.net_path)


    net_file = args.net_path
    network = sumolib.net.readNet(args.net_path)

    [rows, _] = df.shape
    anim = animation.FuncAnimation(fig, update, frames=rows, interval=250, blit=False)
    name_ref = str(args.path).split('/')[-2] if args.isAvg else str(args.path).split('/')[-1][:-4]
    name = f"animations/{str(args.net_path).split('/')[1]}_{name_ref}.gif"
    writer = animation.PillowWriter(fps=args.fps)
    anim.save(name, writer=writer)

if __name__ == "__main__":
    main()