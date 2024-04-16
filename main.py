import numpy as np
from pathlib import Path

MEDIABENCH = ['adpcmdecode', 'adpcmencode', 'epic', 'unepic', 'g721decode', 'g721encode', 'ghostsript', 'gsmdecode', 'gsmencode', 'jpegdecode', 'jpegencode', 'mesamipmap', 'mesaosdemo', 'mesatexgen', 'mpeg2decode', 'mpeg2encode']
MIBENCH_DICT = {'automotive': ['basicmath', 'bitcount', 'qsort', 'susans', 'susane', 'susanc'], 'consumer': ['jpegc', 'jpegd', 'lame', 'mad', 'typeset'], 'network': ['dijkstra', 'patricia'], 'office': ['ghostscriptstatic', 'rsynth', 'sphinx', 'stringsearch'], 'security': ['blowfishd', 'blowfishe', 'rijndaeld', 'rijndaele', 'sha'], 'telecomm': ['adpcmdecodestatic', 'adpcmencodestatic', 'crc32', 'fft', 'ffti', 'gsmdecodestatic', 'gsmencodestatic']}

MIBENCH = []
for x in MIBENCH_DICT.values():
    MIBENCH.extend(x)

RESOURCES = MEDIABENCH + MIBENCH
NUM_RUNS = 11
GROUP = {1: [0, 1, 2], 2: [0, 3], 3: [0, 4], 4: [0, 5, 6], 5: [0, 7], 6: [0, 8], 7: [0, 9, 10]}
SPEED_UP = {1: False, 2: False, 3: True, 4: True, 5: True, 6: True, 7: True}

cwd = Path.cwd()
output_dir = cwd / 'output'
result_dir = cwd / 'result'
Path.mkdir(result_dir, exist_ok=True)

# check gem5 output files
for i in range(NUM_RUNS):
    for resource in RESOURCES:
        work_dir = output_dir / str(i) / resource
        out_file = work_dir / 'out.txt'
        with open(out_file) as f:
            lines = f.readlines()
            if len(lines) == 14 and 'Exiting @ tick' in lines[-1] and 'because exiting with last active thread context.' in lines[-1]:
                continue
            else:
                print(f'Error in {out_file}')
                exit(0)

# parse gem5 output files
table = np.ones((NUM_RUNS, len(MEDIABENCH)+1))
for i in range(NUM_RUNS):
    for id, resource in enumerate(MEDIABENCH):
        work_dir = output_dir / str(i) / resource
        out_file = work_dir / 'out.txt'
        with open(out_file) as f:
            line = f.readlines()[-1]
            table[i][id] = int(line.split()[3])
table = table / table[0]
table[:, -1] = table.prod(axis=1) ** (1/len(MEDIABENCH))

# write result files
for i in GROUP.keys():
    with open(result_dir / f'mediabench_{i}.perf', 'w') as f:
        m1, m2 = float('inf'), 0
        f.write('=table,\n')
        f.write('supergroup=mediabench\n')
        for j in range(len(MEDIABENCH)):
            f.write(f'{MEDIABENCH[j]}')
            for k in GROUP[i]:
                val = 1 / table[k][j] if SPEED_UP[i] else table[k][j]
                f.write(f',{val}')
                m1 = min(m1, val)
                m2 = max(m2, val)
            f.write('\n')
        f.write('gmean')
        for k in GROUP[i]:
            val = 1 / table[k][-1] if SPEED_UP[i] else table[k][-1]
            f.write(f',{val}')
        f.write('\n')
        f.write(f'\n# min = {m1}, max = {m2}, Speedup = {SPEED_UP[i]}\n')

# for MiBench
table = np.ones((NUM_RUNS, len(MIBENCH)+len(MIBENCH_DICT)+1))
for i in range(NUM_RUNS):
    for id, resource in enumerate(MIBENCH):
        work_dir = output_dir / str(i) / resource
        out_file = work_dir / 'out.txt'
        with open(out_file) as f:
            line = f.readlines()[-1]
            table[i][id] = int(line.split()[3])
table = table / table[0]
table[:, -1] = table.prod(axis=1) ** (1/len(MIBENCH))
j = 0
for idx, x in enumerate(MIBENCH_DICT.keys()):
    for _ in MIBENCH_DICT[x]:
        table[:, len(MIBENCH)+idx] *= table[:, j]
        j += 1
    table[:, len(MIBENCH)+idx] **= 1/len(MIBENCH_DICT[x])

for i in GROUP.keys():
    with open(result_dir / f'mibench_{i}.perf', 'w') as f:
        m1, m2 = float('inf'), 0
        f.write('=table,\n')
        j = 0
        for x in MIBENCH_DICT.keys():
            f.write(f'supergroup={x}\n')
            for y in MIBENCH_DICT[x]:
                f.write(f'{y}')
                for k in GROUP[i]:
                    val = 1 / table[k][j] if SPEED_UP[i] else table[k][j]
                    f.write(f',{val}')
                    m1 = min(m1, val)
                    m2 = max(m2, val)
                f.write('\n')
                j += 1
        f.write('supergroup=gmean\n')
        for idx, x in enumerate(MIBENCH_DICT.keys()):
            f.write(f'{x}')
            for k in GROUP[i]:
                val = 1 / table[k][len(MIBENCH)+idx] if SPEED_UP[i] else table[k][len(MIBENCH)+idx]
                f.write(f',{val}')
            f.write('\n')
        f.write('allgmean')
        for k in GROUP[i]:
            val = 1 / table[k][-1] if SPEED_UP[i] else table[k][-1]
            f.write(f',{val}')
        f.write('\n')
        f.write(f'\n# min = {m1}, max = {m2}, Speedup = {SPEED_UP[i]}\n')
