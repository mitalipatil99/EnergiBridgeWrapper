import csv
import platform
import subprocess
import os
import sys
import numpy as np
import pandas as pd

from extract_code import *
import matplotlib.pyplot as plt


def extract_time_and_power(dataset, cumulative=False):
    res = []
    index = 18 if platform.system().lower() == 'darwin' else 27
    for data in dataset:
        # get rid of header
        data = data[1:]
        # change the data to numpy array
        data = np.array(data)
        # keep only the power data and delta time
        time = data[:, 0]
        power = data[:, index]
        # make diff of power
        if not platform.system().lower() == 'darwin':
            power = np.diff(power)
        # insert 0 at the beginning
        power = np.insert(power, 0, 0)
        if cumulative:
            time = np.cumsum(time) / 1_000
            power = np.cumsum(power)
            power = power[0:-1]
            time = time[0:-1]
        else:
            power = power[1:-1]
            time = time[1:-1]
        #make numpy array from time and power
        res.append(np.column_stack((time, power)))
    return res


def make_violin_plot(time_power_dataset):
    data = []
    # extract joul data from time_power_dataset
    for time_power in time_power_dataset:
        time = time_power[:, 0]
        power = time_power[:, 1]
        # multiply power usage by delta time to get energy usage
        power += power * (time / 1000)
        data.append(np.sum(power))
    fig, ax = plt.subplots()
    # Create the violin plot
    violins = ax.violinplot(
        data,
        showextrema=False)

    for pc in violins['bodies']:
        pc.set_facecolor('white')
        pc.set_edgecolor('black')
        pc.set_linewidth(0.6)
        pc.set_alpha(1)

    # Create the boxplot
    lineprops = dict(linewidth=0.5)
    medianprops = dict(color='black')
    ax.boxplot(
        data,
        whiskerprops=lineprops,
        boxprops=lineprops,
        medianprops=medianprops)

    # Style
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel("Energy Consumption (J)")

    plt.show()


def make_time_series_plot(time_power_dataset, cumulative=False):
    for time_power in time_power_dataset:
        time = time_power[:, 0]
        power = time_power[:, 1]
        if not cumulative:
            # multiply power usage by delta time to get energy usage
            power = power * (time / 100)
            time = np.cumsum(time) / 1000
        plt.plot(time, power)
    # add legend
    plt.legend([f'Run {i+1}' for i in range(len(time_power_dataset))])
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')
    plt.title(f'Power vs Time, cumulative={cumulative}')
    plt.show()


def run(program=None, no_runs=1):
    current_os = platform.system().lower()
    data = []
    
    if current_os == 'darwin':  # Mac OS
        if program is None:
            extract_and_write_code(notebook_path, start_marker, end_marker)
        else:
            with open('temp.py', 'w') as f:
                f.write(program)
        current_directory = os.getcwd()
        path = os.path.join(current_directory, 'temp.py')
        for i in range(no_runs):
            subprocess.run(['chmod', '+x', path ])
            # Run the temporary file with energibridge as a subprocess
            energibridge_executable = "../target/release/energibridge"
            result = subprocess.run([energibridge_executable, '-o', 'temp.csv', '--summary', 'python3', path], capture_output=True,
                        text=True)
            print(result.stdout)
            print(result.stderr)
            # Check if the command executed successfully
            if result.returncode == 0:
                print("Command executed successfully.")
                # Load the data from temp.csv into the data variable
                try:
                    data.append(pd.read_csv('temp.csv'))
                    print("Data loaded successfully.")
                except Exception as e:
                    print("Error loading data:", e)
            else:
                print("Error executing command.")
        
        if program is None:
            os.remove('temp.py')

    elif current_os == 'windows':
        if program is None:
            extract_and_write_code(notebook_path, start_marker, end_marker)
        else:
            with open('temp.py', 'w') as f:
                f.write(program)
        # make empty list to store data
        for i in range(no_runs):
            # run the temporary file with energibridge.exe as admin
            res = subprocess.run(['../target/release/energibridge.exe', '-o', 'temp.csv', '--summary', 'py', 'temp.py'], capture_output=True,
                        text=True)
            if res.stdout is not None: print(res.stdout)
            if res.stderr is not None: print(res.stderr)
            # get data from temp.csv with pandas and append it to the dataframe
            data.append(pd.read_csv('temp.csv'))

        os.remove('temp.py')
        os.remove('temp.csv')

    else:
        raise NotImplementedError(f"Unsupported operating system: {current_os}")

    return data


def test_run():
    data = np.genfromtxt('../temp.csv', delimiter=',', skip_header=1)
    res = extract_time_and_power(data, cumulative=True)
    make_time_series_plot(res, cumulative=True)
    print(res)



