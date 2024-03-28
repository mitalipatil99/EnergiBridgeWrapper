This readme contains two sections, the first section is the original readme from [EnergiBridge](https://github.com/tdurieux/EnergiBridge/tree/main). , the second section the readme of the Jupyter EnergiBridge extension.

# EnergiBridge

[![Release](https://github.com/tdurieux/EnergiBridge/actions/workflows/release.yml/badge.svg)](https://github.com/tdurieux/EnergiBridge/actions/workflows/release.yml) [![GitHub Release](https://img.shields.io/github/v/release/tdurieux/EnergiBridge)](https://github.com/tdurieux/EnergiBridge/releases)

Energibridge is a cross-platform energy measurement utility that provides support for Linux, Windows, and MacOS, as well as Intel, AMD, and Apple ARM CPU architectures.

This tool is designed to collect resource usage data for a command to execute and to output the data in a CSV format.

| OS      | Intel CPU | AMD CPU | M1 CPU | Intel GPU | Nvidia GPU | AMD GPU | M1 GPU |
| ------- | --------- | ------- | ------ | --------- | ---------- | ------- | ------ |
| Linux   | ✅        | ✅      |        |           | ✅         |         |        |
| Windows | ✅        | ✅      |        |           | ✅         |         |        |
| Mac     | ✅        |         | ✅     | ✅        |            | ✅      | ✅     |

## Requirements

Depending on your hardware you need different dependencies.

### NVIDIA

- nvml

## Install

### Windows

Install LibreHardwareMonitor to access the CPU registry.

In an elevated (Administrator) command line (e.g. cmd.exe):

```
Create:
sc create rapl type=kernel binPath="<absolute_path_to_LibreHardwareMonitor.sys>"

Start:
sc start rapl

Stop:
sc stop rapl

Delete:
sc delete rapl

Build:
cargo build -r
```

> For PowerShell use `sc.exe` instead of `sc`.

### Linux

Change the permission of the msr file to be able to read them without root access.
The permissions are reseted each time your restart the machine.

```
sudo chgrp -R msr /dev/cpu/*/msr;
sudo chmod g+r /dev/cpu/*/msr;
```

Build EnergiBridge

```
cargo build -r;
```

Provide the permission to the binary to read the registry.
Since any non-root program accessing the msr also needs the rawio capability, if you move the binary you should eecute this line again

```
sudo setcap cap_sys_rawio=ep target/release/energibridge;
```

## Usage

To run the script, use the following command:

```
Usage: energibridge[.exe] [OPTIONS] [COMMAND]...

Arguments:
  [COMMAND]...

Options:
  -o, --output <OUTPUT>

  -s, --separator <SEPARATOR>
          [default: ,]
  -c, --command-output <COMMAND_OUTPUT>

  -i, --interval <INTERVAL>
          Duration of the interval between two measurements in micoseconds [default: 100]
  -m, --max-execution <MAX_EXECUTION>
          Define the maximum duration of the execution of the command in seconds, set to -1 to disable [default: 0]
  -g, --gpu
          Get GPU usage data
      --summary
          Provide a summary of the total energy consumption of running the command
  -h, --help
          Print help
  -V, --version
          Print version
```

## Output Example

```csv
Delta,Time,CPU_FREQUENCY_0,CPU_FREQUENCY_1,CPU_FREQUENCY_2,CPU_FREQUENCY_3,CPU_FREQUENCY_4,CPU_FREQUENCY_5,CPU_FREQUENCY_6,CPU_FREQUENCY_7,CPU_FREQUENCY_8,CPU_FREQUENCY_9,CPU_TEMP_0,CPU_TEMP_1,CPU_TEMP_2,CPU_TEMP_3,CPU_TEMP_4,CPU_TEMP_5,CPU_TEMP_6,CPU_TEMP_7,CPU_TEMP_8,CPU_TEMP_9,CPU_USAGE_0,CPU_USAGE_1,CPU_USAGE_2,CPU_USAGE_3,CPU_USAGE_4,CPU_USAGE_5,CPU_USAGE_6,CPU_USAGE_7,CPU_USAGE_8,CPU_USAGE_9,SYSTEM_POWER (Watts),TOTAL_MEMORY,TOTAL_SWAP,USED_MEMORY,USED_SWAP
0,1697704464320,0,0,0,0,0,0,0,0,0,0,46.529457092285156,44.31881332397461,43.83422088623047,47.03656005859375,44.67115783691406,43.856910705566406,41.333412170410156,41.268951416015625,44.348262786865234,43.08387756347656,46.37215805053711,45.429779052734375,15.021618843078613,8.819367408752441,5.0954484939575195,3.514699935913086,2.9715969562530518,1.5818228721618652,1.1069598197937012,0.9475208520889282,11.58033275604248,34359738368,0,10188488704,0
104,1697704464321,0,0,0,0,0,0,0,0,0,0,46.529457092285156,44.31881332397461,43.83422088623047,47.03656005859375,44.67115783691406,43.856910705566406,41.333412170410156,41.268951416015625,44.348262786865234,43.08387756347656,46.37215042114258,45.429771423339844,15.021615982055664,8.819366455078125,5.095447063446045,3.514699697494507,2.9715967178344727,1.5818227529525757,1.1069598197937012,0.9475207924842834,11.58033275604248,34359738368,0,10189275136,0
```


# Jupyter Energibridge extension

`jupyter_energi` is a Jupyter extension that allows you to seamlessly integrate the EnergiBridge tool into your Jupyter notebooks.
This extension provides a simple interface to run code from cells and collect energy consumption data over multiple runs. 
The collected data is then returned as a Pandas DataFrame, which can be used for further analysis and visualization. 
`jupyter_energi` also provides bare-bones visualization capabilities in the form of time series plots and violin plots.

## Installation
`jupyter_energi` comes contained within EnergiBridge, so you do not need to install it separately.
Don't forget to install EnergiBridge as described in the previous section.

## Usage
> [!NOTE]
see Demo notebook in `jupyter_energi` for an easy-to-follow example.


To use `jupyter_energi` simply import it into a Jupyter notebook.
> [!IMPORTANT]
Code you want to measure the energy consumption of should be wholly self-contained when passed to `jupyter_energi`.
This means that any import statements needed should also be contained.
Furthermore, as EnergiBridge needs to be run as admin, Jupyter Notebook should also be opened as admin.

Code of which you want to measure the energy consumption can be specified in two ways:

1. By using the #EnergiBridgeStart and #EnergiBridgeStop tags with the code contained between the tags.
2. By defining the code as a string and directly passing it to the `run` function.

In the following example, we will show both methods.
```python
import jupyter_energi

# Method 1
#EnergiBridgeStart
for i in range(1000000):
    pass
#EnergiBridgeStop

jupyter_energi.run()

# Method 2
code = """ 
for i in range(1000000):
    pass
"""
jupyter_energi.run(program=code)
```

## Functions

The following functions and accompanying arguments are available:

- `run`: Run the code and collect energy consumption data.
  - `program`: The code to run. If left empty `jupyter_energi` will look for the #EnergiBridgeStart and #EnergiBridgeStop tags in any cell in the current notebook.
  - `no_runs`: The number of times to run the code, defaults to 1.
  - returns: A List of Pandas DataFrame containing the collected data, one for every run.

- `extract_time_and_power`: Extract time and power variables from the collected data.
    - `dataset`: A list of Pandas DataFrames containing the collected data returned by the `run` function.
    - `cumulative`: A boolean indicating whether to return the cumulative power consumption or the power consumption per interval, defaults to False.
    - returns: A python list with a numpy array containing the time and power data for every run.

- `make_time_series_plot`: Plot the time series of the collected data.
    - `time_and_power`: A python list with a numpy array containing the time and power data for every run returned by the `extract_time_and_power` function.
    - `cumulative`: A boolean indicating whether to return the cumulative power consumption or the power consumption per interval, defaults to False.
    - returns: A matplotlib plot of the time series data.

- `make_violin_plot`: Plot a violin plot of the collected data.
    - `time_and_power`: A python list with a numpy array containing the time and power data for every run returned by the `extract_time_and_power` function.
    - `cumulative`: A boolean indicating whether to return the cumulative power consumption or the power consumption per interval, defaults to False.
    - returns: A matplotlib plot of the violin plot data.

## Example
```python
import jupyter_energi

# Method 1
#EnergiBridgeStart
for i in range(1000000):
    pass
#EnergiBridgeStop

data = jupyter_energi.run(no_runs=5)

cumulative = True
time_and_power = jupyter_energi.extract_time_and_power(data, cumulative=cumulative)
jupyter_energi.make_time_series_plot(time_and_power, cumulative=cumulative)
jupyter_energi.make_violin_plot(time_and_power, cumulative=cumulative)
```

## Recommendation to collect unbiased energy data

To minimise the confounding factors that affect the energy measurements of your software program , we recommmend some strategies:
- remove uncessary services running in the background.
- Turn off notifications and Bluetooth.
- Avoid connecting to external hardware if not required.
- To see how changes in the code affect the energy coonsumption, freeze your settings. For e.g the brightness and resolution of your screen should be fixed.  

