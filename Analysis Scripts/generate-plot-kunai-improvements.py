#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

'''
Obtain the improvements from each of the analysis for memory
and for time, for both datasets. Then print two plots that joins
the datasets.

The improvements is represented by an improvement factor that
is calculated as:

    result_androguard / result_kunai

For the next fields:
    - size-time
    - size-memory
'''
SHOW_LATEX = True


def print_numbers(key, number):
    global SHOW_LATEX
    if SHOW_LATEX:
        print(f"lx.safe_full_number('{key}', {number})")
    else:
        print(f"{key}={number}")


CSV_GOOGLEPLAY = './analysis_googleplay.csv'
CSV_MALWARE = './analysis_malware.csv'

# read in dataframe
DATA_GOOGLEPLAY = pd.read_csv(CSV_GOOGLEPLAY)
DATA_MALWARE = pd.read_csv(CSV_MALWARE)

# remove those cases greater to 15MB
DATA_GOOGLEPLAY = DATA_GOOGLEPLAY[DATA_GOOGLEPLAY['size'] <= 15000000]
DATA_MALWARE = DATA_MALWARE[DATA_MALWARE['size'] <= 15000000]


# represent the time improvement
size_time_fig = go.Figure()

size_time_fig.add_trace(go.Scatter(
    x=list(DATA_GOOGLEPLAY['size']),
    y=list(DATA_GOOGLEPLAY['time_improve_factor']),
    name="Time improvement Googleplay",
    marker=dict(color='crimson', size=8),
    mode="markers"
))


size_time_fig.add_trace(go.Scatter(
    x=list(DATA_MALWARE['size']),
    y=list(DATA_MALWARE['time_improve_factor']),
    name="Time improvement Malware",
    marker=dict(color='blue', size=8),
    mode="markers"
))

size_time_fig.update_layout(yaxis_type="log",
                            yaxis_title="Speedup factor (log scale)",
                            xaxis_title="DEX size",
                            font=dict(
                                family="Courier New, monospace",
                                size=20,
                            ),
                            legend=dict(
                                x=0.785,
                                y=1,
                                traceorder="reversed",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Courier",
                                    size=20,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                            )

size_mem_fig = go.Figure()

size_mem_fig.add_trace(go.Scatter(
    x=list(DATA_GOOGLEPLAY['size']),
    y=list(DATA_GOOGLEPLAY['memory_improve_factor']),
    name="Memory improvement Googleplay",
    marker=dict(color='crimson', size=8),
    mode="markers"
))

size_mem_fig.add_trace(go.Scatter(
    x=list(DATA_MALWARE['size']),
    y=list(DATA_MALWARE['memory_improve_factor']),
    name='Memory improvement Malware',
    marker=dict(color='blue', size=8),
    mode="markers"
))

size_mem_fig.update_layout(yaxis_type="log",
                           yaxis_title="Memory reduction factor (log scale)",
                           xaxis_title="DEX size",
                           font=dict(
                               family="Courier New, monospace",
                               size=20,
                           ),
                           legend=dict(
                               x=0.77,
                               y=1,
                               traceorder="reversed",
                               title_font_family="Times New Roman",
                               font=dict(
                                   family="Courier",
                                   size=20,
                                   color="black"
                               ),
                               bgcolor="LightSteelBlue",
                               bordercolor="Black",
                               borderwidth=2
                           )
                           )

# size_time_fig.write_image('./test1.png')
size_time_fig.show()
size_mem_fig.show()


print_numbers('GooglePlayTimeSpeedUpAverage', round(
    DATA_GOOGLEPLAY['time_improve_factor'].mean(), 1))
print_numbers('MalwareTimeSpeedUpAverage', round(
    DATA_MALWARE['time_improve_factor'].mean(), 1))
print_numbers('GooglePlayMemoryReductionAverage', round(
    DATA_GOOGLEPLAY['memory_improve_factor'].mean(), 1))
print_numbers('MalwareMemoryReductionAverage', round(
    DATA_MALWARE['memory_improve_factor'].mean(), 1))
