#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Analysis of data from kunai-benchmark-results

Create two big dot plots with the comparison between Androguard and
Kunai analysis, one of the Plots will be for comparing between
size of dex - real time of analysis:


    time of     |
    analysis    |
                |
                |
                |
                |
                -----------------------------
                size of
                dex

And the other will represent the size of dex - memory consumed.

    memory      |
    consumed    |
                |
                |
                |
                |
                -----------------------------
                size of
                dex

With these two plots we will get an idea of the differences between
Kunai and androguard.
'''

import os
import csv
import sys
import pprint
import math
import statistics
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from database_connector import DatabaseConnector
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


SHOW_LATEX = True


def print_numbers(key, number):
    global SHOW_LATEX
    if SHOW_LATEX:
        print(f"lx.safe_full_number('{key}', {number})")
    else:
        print(f"{key}={number}")


def create_dot_plot(sizes: list, times_androguard: list, times_kunai: list, memory_androguard: list, memory_kunai: list) -> tuple:
    '''
    Create two dot plots one for size-time and other
    for size-memory.
    '''
    time_difference = list()
    memory_difference = list()

    for i in range(len(times_androguard)):
        time_difference.append(times_androguard[i] - times_kunai[i])
    
    for i in range(len(memory_androguard)):
        memory_difference.append(memory_androguard[i] - memory_kunai[i])
    

    size_time_fig = go.Figure()
    size_time_fig.add_trace(go.Scatter(
        x=sizes,
        y=times_androguard,
        marker=dict(color='crimson', size=12),
        mode="markers",
        name="Androguard"
    ))

    size_time_fig.add_trace(go.Scatter(
        x=sizes,
        y=times_kunai,
        marker=dict(color='blue', size=12),
        mode="markers",
        name="Kunai"
    ))
    '''
    size_time_fig.add_trace(go.Scatter(
        x=sizes,
        y=time_difference,
        marker=dict(color='gold', size=12),
        mode="markers",
        name="Diff"
    ))
    '''

    size_time_fig.update_layout(xaxis_title="DEX file size (bytes)",
                                yaxis_title="Time of analysis (seconds)")

    size_memory_fig = go.Figure()
    size_memory_fig.add_trace(go.Scatter(
        x=sizes,
        y=memory_androguard,
        marker=dict(color='crimson', size=12),
        mode="markers",
        name="Androguard"
    ))

    size_memory_fig.add_trace(go.Scatter(
        x=sizes,
        y=memory_kunai,
        marker=dict(color='blue', size=12),
        mode="markers",
        name="Kunai"
    ))

    '''
    size_memory_fig.add_trace(go.Scatter(
        x=sizes,
        y=memory_difference,
        marker=dict(color='gold', size=12),
        mode="markers",
        name="Diff"
    ))
    '''

    size_memory_fig.update_layout(xaxis_title="DEX file size (bytes)",
                                  yaxis_title="Memory consumed (bytes)")

    return size_time_fig, size_memory_fig


def flip_index(l: list, i: int, j: int) -> list:
    '''
    Simply flip two index from a list.

    :param l: list where to flip the data.
    :param i: first index.
    :param j: second index.
    '''
    temp = l[i]
    l[i] = l[j]
    l[j] = temp
    return l


def create_plot_line(sizes: list, times_androguard: list, times_kunai: list, memory_androguard: list, memory_kunai: list) -> tuple:
    '''
    Create a plot with a line that represents how it
    grows time and memory usage with the size of the
    DEX, this representation it is similar to previous
    dot plot, but it is easier to visualize, we must
    apply some kind of heuristic (typical deviation
    or the mean) in order to normalize data and avoid
    cases where some data grows a lot or finishes very
    early.

    :param sizes: size of the analyzed files.
    :param times_androguard: time of analysis for androguard.
    :param times_kunai: time of analysis for kunai.
    :param memory_androguard: memory used by androguard for the analysis.
    :param memory_kunai: memory used by kunai for the analysis.
    '''
    global SHOW_PLOT

    df = pd.read_csv('analysis_googleplay.csv')

    # code by Aymar Cublier

    # Get array of DEX sizes (in bytes)
    X = df.iloc[:, 0].values.reshape(-1, 1) / 1024
    # Get array of execution times Androguard
    T1 = df.iloc[:, 1].values.reshape(-1, 1)
    # Get array of execution times KUNAI
    T2 = df.iloc[:, 2].values.reshape(-1, 1)
    # Get array of memory usage Androguard
    M1 = df.iloc[:, 3].values.reshape(-1, 1) / 1024
    # Get array of memory usage KUNAI
    M2 = df.iloc[:, 4].values.reshape(-1, 1) / 1024
    
    # Get means and std deviation
    muta, sdta = np.mean(T1), np.std(T1)
    mutm, sdtm = np.mean(T2), np.std(T2)
    muma, sdma = np.mean(M1), np.std(M1)
    mumm, sdmm = np.mean(M2), np.std(M2)

    # Create LinearRegression for series
    lrta = LinearRegression() # Time Androguard
    lrtm = LinearRegression() # Time KUNAI
    lrma = LinearRegression() # Memory Androguard
    lrmm = LinearRegression() # Memory KUNAI

    # Fit and predict times
    lrta.fit(X, T1)           
    lrtm.fit(X, T2)
    T1P = lrta.predict(X)     # predict a linear regresion for androguard time
    T2P = lrtm.predict(X)     # predict a linear regresion for kunai time

    # Fit and predict memory
    lrma.fit(X, M1)
    lrmm.fit(X, M2)
    M1P = lrma.predict(X)     
    M2P = lrmm.predict(X)

    plt.scatter(X, T1, label="Time Androguard ($\mu = %.2f$)" % muta)
    plt.scatter(X, T2, label="Time KUNAI ($\mu = %.2f$)" % mutm)
    plt.plot(X, T1P, label="Fit Androguard: $R^2 = %.3f$" % lrta.score(X, T1), linewidth=3)
    plt.plot(X, T2P, label="Fit KUNAI: $R^2 = %.3f$" % lrtm.score(X, T2), linewidth=3)
    plt.xlabel("DEX size (in KB)", fontsize=14)
    plt.ylabel("Execution time (in s)", fontsize=14)

    plt.legend(fontsize=14)
    plt.xticks(range(0, 20000, 2500), fontsize=14)
    plt.yticks(fontsize=14)

    plt.grid()
    plt.savefig("output_plots/Time-Analysis-Google500.png", dpi=400, bbox_inches='tight', pad_inches=0.4, format='png')
    if SHOW_PLOT:
        plt.show()

    plt.scatter(X, M1, label="Memory Androguard ($\mu = %.0f$ KB)" % (muma))
    plt.scatter(X, M2, label="Memory KUNAI ($\mu = %.0f$ KB)" % (mumm))
    plt.plot(X, M1P, label="Fit Androguard: $R^2 = %.3f$" % lrma.score(X, M1), linewidth=3)
    plt.plot(X, M2P, label="Fit KUNAI: $R^2 = %.3f$" % lrmm.score(X, M2), linewidth=3)
    plt.xlabel("DEX size (in KB)", fontsize=14)
    plt.ylabel("Memory usage (in KB)", fontsize=14)

    plt.legend(fontsize=14)
    plt.xticks(range(0, 20000, 2500), fontsize=14)
    plt.yticks(range(0, 2000, 250), fontsize=14) 
    
    plt.grid()
    plt.savefig("output_plots/Memory-Analysis-Google500.png", dpi=400,pad_inches=0.4, format='png')

    if SHOW_PLOT:
        plt.show()


class InterestingDexFile(object):

    def __init__(self) -> None:
        self.size = 0
        self.package = ""
        self.file = ""
        self.time_androguard = 0
        self.time_kunai = 0
        self.memory_androguard = 0
        self.memory_kunai = 0

    def __str__(self) -> str:
        global SHOW_LATEX

        return "File package: %s, file name: %s, size: %d, time androguard: %f, time kunai: %f, memory androguard: %d, memory kunai: %d" % (
            self.package,
            self.file,
            self.size,
            self.time_androguard,
            self.time_kunai,
            self.memory_androguard,
            self.memory_kunai
        )

# Main code goes here

SHOW_PLOT = False

if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        SHOW_PLOT = True
    



databaseconnector = DatabaseConnector()

databaseconnector.config()

##########################################################################################
# get results in here!!!

total_apks = databaseconnector.get_number_of_values_by_query(
    {"analysis": {'$exists': True}})

total_apks_downloaded = databaseconnector.get_number_of_values_by_query({
    'analysis.path_apk': {
        '$ne': None
    }
})

total_apks_analyzed = databaseconnector.get_number_of_values_by_query({
    'analysis.benchmark': {
        '$exists': True
    }
})

analysis_of_apks_androguard = databaseconnector.get_number_of_values_by_query({
    'analysis.benchmark.base_apk.Androguard.exit_code': {
        '$eq': 0
    }
})

analysis_of_apks_kunai = databaseconnector.get_number_of_values_by_query({
    'analysis.benchmark.base_apk.Kunai.exit_code': {
        '$eq': 0
    }
})

complete_analysis_cursor = databaseconnector.retrieve_all_the_documents_from_collection()

# total dex files
total_dex_files = 0
# correctly analyzed dex by both tools
correctly_analyzed_dex_files = 0
packages = list()
sizes = list()
# comparison size_time androguard (use a list to keep repetitions)
size_time_androguard = list()
# comparison size_time kunai
size_time_kunai = list()

# comparison size_memory androguard
size_memory_androguard = list()
# comparison size_memory kunai
size_memory_kunai = list()

biggest_file = InterestingDexFile()
smallest_file = InterestingDexFile()


kunai_faster_androguard = 0
kunai_slower_androguard = 0
kunai_same_time_androguard = 0
kunai_bigger_androguard = 0
kunai_smaller_androguard = 0
kunai_same_memory_androguard = 0


for doc in complete_analysis_cursor:
    
    if 'benchmark' not in doc['analysis'].keys():
        continue

    for key in doc['analysis']['benchmark'].keys():
        if key == 'base_apk':
            continue

        analysis_androguard_kunai = doc['analysis']['benchmark'][key]
        total_dex_files += 1
        # fair comparison must be both analysis are okay
        if analysis_androguard_kunai['Androguard']['exit_code'] != 0 or \
                analysis_androguard_kunai['Kunai']['exit_code'] != 0:
            print(
                f"Not correctly analyzed DEX file: pkg_name={doc['package']}, dex file={key}, androguard={analysis_androguard_kunai['Androguard']['exit_code']}, Kunai={analysis_androguard_kunai['Kunai']['exit_code']}")
            continue

        correctly_analyzed_dex_files += 1
        
        size = analysis_androguard_kunai['Androguard']['file_size']
        time_androguard = analysis_androguard_kunai['Androguard']['analysis_time']
        memory_androguard = analysis_androguard_kunai['Androguard']['memory']

        time_kunai = analysis_androguard_kunai['Kunai']['analysis_time']
        memory_kunai = analysis_androguard_kunai['Kunai']['memory']

        packages.append(doc['package'])
        sizes.append(size)

        size_time_androguard.append(time_androguard)
        size_time_kunai.append(time_kunai)

        if time_kunai > time_androguard:
            kunai_slower_androguard += 1
        elif time_kunai < time_androguard:
            kunai_faster_androguard += 1
        else:
            kunai_same_time_androguard += 1


        size_memory_androguard.append(memory_androguard)
        size_memory_kunai.append(memory_kunai)

        if memory_kunai < memory_androguard:
            kunai_smaller_androguard += 1
        elif memory_kunai > memory_androguard:
            kunai_bigger_androguard += 1
        else:
            kunai_same_memory_androguard += 1

        if size > biggest_file.size:
            biggest_file.size = size
            biggest_file.package = doc['package']
            biggest_file.file = key
            biggest_file.time_androguard = time_androguard
            biggest_file.time_kunai = time_kunai
            biggest_file.memory_androguard = memory_androguard
            biggest_file.memory_kunai = memory_kunai

        if smallest_file.size == 0 or size < smallest_file.size:
            smallest_file.size = size
            smallest_file.package = doc['package']
            smallest_file.file = key
            smallest_file.time_androguard = time_androguard
            smallest_file.time_kunai = time_kunai
            smallest_file.memory_androguard = memory_androguard
            smallest_file.memory_kunai = memory_kunai


n_analyzed_files = len(sizes)

for i in range(n_analyzed_files):
    for j in range(0, n_analyzed_files-i-1):
        if sizes[j] > sizes[j+1]:
            sizes = flip_index(sizes, j, j+1)
            packages = flip_index(packages, j, j+1)
            size_time_androguard = flip_index(size_time_androguard, j, j+1)
            size_time_kunai = flip_index(size_time_kunai, j, j+1)
            size_memory_androguard = flip_index(size_memory_androguard, j, j+1)
            size_memory_kunai = flip_index(size_memory_kunai, j, j+1)

with open('analysis_googleplay.csv', 'w', newline='') as csvfile:
    fieldnames = ['size', 'time_androguard', 'time_kunai', 'memory_androguard', 'memory_kunai', 'time_improve_factor', 'memory_improve_factor', 'package']
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)
    for i in range(n_analyzed_files):
        writer.writerow([sizes[i], size_time_androguard[i], size_time_kunai[i], size_memory_androguard[i], size_memory_kunai[i], size_time_androguard[i]/size_time_kunai[i], size_memory_androguard[i]/size_memory_kunai[i], packages[i]])


fig_size_time, fig_size_mem = create_dot_plot(
    sizes, size_time_androguard, size_time_kunai, size_memory_androguard, size_memory_kunai)

create_plot_line(
    sizes, size_time_androguard, size_time_kunai, size_memory_androguard, size_memory_kunai)

##########################################################################################
# Print results in here!

print_numbers('totalApks', total_apks)
print_numbers('totalApksDownloaded', total_apks_downloaded)
print_numbers('totalApksAnalyzed', total_apks_analyzed)
print_numbers('totalApksCorrectlyAnalyzedAndroguard',
              analysis_of_apks_androguard)
print_numbers('totalApksCorrectlyAnalyzedKunai', analysis_of_apks_kunai)
print_numbers('totalDexFiles', total_dex_files)
print_numbers('totalDexFilesCorrectlyAnalyzed', correctly_analyzed_dex_files)

print_numbers('androguardMedianSizeTime', statistics.median(size_time_androguard))
print_numbers('kunaiMedianSizeTime', statistics.median(size_time_kunai))

print_numbers('androguardMedianSizeMemory', statistics.median(size_memory_androguard))
print_numbers('kunaiMedianSizeMemory', statistics.median(size_memory_kunai))

print_numbers('kunaiFasterAndroguard', kunai_faster_androguard)
print_numbers('kunaiSlowerAndroguard', kunai_slower_androguard)
print_numbers('kunaiSameTimeAndroguard', kunai_same_time_androguard)

print_numbers('kunaiSmallerAndroguard', kunai_smaller_androguard)
print_numbers('kunaiBiggerAndroguard', kunai_bigger_androguard)
print_numbers('kunaiSameSizeAndroguard', kunai_same_memory_androguard)


print("Biggest DEX file: %s" % (str(biggest_file)))
print("Smallest DEX file: %s" % (str(smallest_file)))

if SHOW_PLOT:
    fig_size_time.show()
    fig_size_mem.show()

fig_size_time.write_image("output_plots/size-time-Google500.png")
fig_size_mem.write_image("output_plots/size-memory-Google500.png")
