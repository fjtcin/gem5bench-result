# gem5bench-result

This project contains a single python script `main.py` to process the output of the gem5 simulator.
The result of this processing is a bunch of `.perf` files, which will be used by [BarGraphGenerator](https://gitlab.com/JianpingZeng/BarGraphGenerator) to generate neat `.pdf` figures.

This project is just a demo. You need to understand and modify the contents of `main.py` for customized usage, but normally you will only change the `RESOURCES`, `NUM_RUNS`, `GROUP` and `SPEED_UP` constants if your `output` directory shares the same structure as mine.

To generate the `output` directory from benchmark binaries automatically, you may like to check the [gem5bench](https://github.com/fjtcin/gem5bench) project.

## Procedure to Run

Make sure your working directory contains the `output` directory and the `main.py` script. Then run:

```bash
python main.py
```

This will generate the `result` directory containing the data part of the `.perf` file. Combine it with the header part (samples below), and run BarGraphGenerator.

In the `figure` directory are some example figures with corresponding `.perf` configs.

## BarGraphGenerator `.perf` File Header Samples

For comparing 2 runs:

```text
=cluster;Baseline;L1dmshr
colors=black,yellow
ylabel=Slowdown
ymax=1.5
ymin=0.5
#specify the width and height of the generated bar graph
figsize=70,15
rotateby=-90
fontsize=70
x_label_size=70
y_label_size=90
=horizontal_legend
legend_loc=upper left
groupfont=90
group_rotateby=0
supergroupfont=90
ncol=6
=valuelabel
grid_linewidth=2
```

For comparing 3 runs:

```text
=cluster;Baseline;L1dmshr\&L2mshr;L1dmshr
colors=black,yellow,red
ylabel=Slowdown
ymax=1.5
ymin=0.5
#specify the width and height of the generated bar graph
figsize=70,15
rotateby=-90
fontsize=70
x_label_size=70
y_label_size=90
=horizontal_legend
legend_loc=upper left
groupfont=90
group_rotateby=0
supergroupfont=90
ncol=6
=valuelabel
grid_linewidth=2
```

## Example Benchmark Results

There is one baseline (setting #0) and 10 experiments based on the armv7a system. Implementation details can be found at the [gem5bench](https://github.com/fjtcin/gem5bench) project.

| Setting # | CPU Width | CPU CLK | L1D Size | L1D Assoc | L1D MSHRs | L1I Size | L1I Assoc | L1I MSHRs | L2 Size | L2 Assoc | L2 MSHRs | L2 Policy | Block Size |
|-----------|-----------|---------|----------|-----------|-----------|----------|-----------|-----------|---------|----------|----------|-----------|------------|
| 0         | 8         | 1GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 1MiB    | 16       | 16       | Random    | 64B        |
| 1         | 8         | 1GHz    | 32KiB    | 2         | 2         | 32KiB    | 2         | 2         | 1MiB    | 16       | 2        | Random    | 64B        |
| 2         | 8         | 1GHz    | 32KiB    | 2         | 2         | 32KiB    | 2         | 2         | 1MiB    | 16       | 16       | Random    | 64B        |
| 3         | 4         | 1GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 1MiB    | 16       | 16       | Random    | 64B        |
| 4         | 8         | 4GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 1MiB    | 16       | 16       | Random    | 64B        |
| 5         | 8         | 1GHz    | 64KiB    | 2         | 6         | 64KiB    | 2         | 2         | 1MiB    | 16       | 16       | Random    | 64B        |
| 6         | 8         | 1GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 2MiB    | 16       | 16       | Random    | 64B        |
| 7         | 8         | 1GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 1MiB    | 16       | 16       | Random    | 128B       |
| 8         | 8         | 1GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 1MiB    | 16       | 16       | LRU       | 64B        |
| 9         | 8         | 1GHz    | 32KiB    | 4         | 6         | 32KiB    | 4         | 2         | 1MiB    | 16       | 16       | Random    | 64B        |
| 10        | 8         | 1GHz    | 32KiB    | 2         | 6         | 32KiB    | 2         | 2         | 1MiB    | 4        | 16       | Random    | 64B        |

### Group 1

In group 1, we draw a comparison between the baseline, setting #1 and setting #2.

![mediabench_1](img/mediabench_1.png)
![mibench_1](img/mibench_1.png)

### Group 2

In group 2, we draw a comparison between the baseline and setting #3.

![mediabench_2](img/mediabench_2.png)
![mibench_2](img/mibench_2.png)

### Group 3

In group 3, we draw a comparison between the baseline and setting #4.

![mediabench_3](img/mediabench_3.png)
![mibench_3](img/mibench_3.png)

### Group 4

In group 4, we draw a comparison between the baseline, setting #5 and setting #6.

![mediabench_4](img/mediabench_4.png)
![mibench_4](img/mibench_4.png)

### Group 5

In group 5, we draw a comparison between the baseline and setting #7.

![mediabench_5](img/mediabench_5.png)
![mibench_5](img/mibench_5.png)

### Group 6

In group 6, we draw a comparison between the baseline and setting #8.

![mediabench_6](img/mediabench_6.png)
![mibench_6](img/mibench_6.png)

### Group 7

In group 7, we draw a comparison between the baseline, setting #9 and setting #10.

![mediabench_7](img/mediabench_7.png)
![mibench_7](img/mibench_7.png)
