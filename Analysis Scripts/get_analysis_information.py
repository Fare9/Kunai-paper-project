#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
Get data from kunai-benchmark-results

It needs a specific format, for that reason cannot
be used for other files.
'''

import os
import sys
from os.path import basename
from database_connector import DatabaseConnector
from scanf import scanf

size_of_files = dict()
database_connector = DatabaseConnector()

def retrieve_variables_from_line(line: str) -> tuple:
    '''
    Use scanf function in order to retrieve the different variables
    from the line of the CSV scanned.

    :param line: line to analyze with scanf and extract data.
    :return: tuple with variables of different data types
    '''
    return scanf("%s;%s;cmd:%s %s;real:%f:user:%f;sys:%f;memory:%d;cpu:%d%;exit-code:%d", line)

def retrieve_variables_from_line_with_analysis_time(line: str) -> tuple:
    '''
    Use scanf function in order to retrieve the different variables
    from the line of the CSV scanned.

    :param line: line to analyze with scanf and extract data.
    :return: tuple with variables of different data types
    '''
    return scanf("%s;%s;analysis_time:%f;cmd:%s %s;real:%f:user:%f;sys:%f;memory:%d;cpu:%d%;exit-code:%d", line)


def extract_variables_analysis_line(lines: list) -> dict:
    '''
    Extract all the variables from a list of string lines
    with the information from the analysis, create a dictionary
    with the results from the analysis, and finish it.
    '''
    results = {'benchmark':dict()}

    tool = None
    file = None
    analysis_time = 0.0
    analysis_command = None
    path_command = None
    real_time = 0.0
    user_time = 0.0
    sys_time = 0.0
    memory = 0
    cpu = 0
    exit_code = 0

    for line in lines:
        line = line.strip()
        if 'analysis_time:' in line:
            (tool, file, analysis_time, analysis_command, path_command, real_time, user_time, sys_time, memory, cpu, exit_code) = retrieve_variables_from_line_with_analysis_time(line)
        else:
            (tool, file, analysis_command, path_command, real_time, user_time, sys_time, memory, cpu, exit_code) = retrieve_variables_from_line(line)

        analyzed_file_name = basename(file).replace(".","_")

        if analyzed_file_name not in results['benchmark']:
            results['benchmark'][analyzed_file_name] = dict()

        if tool not in results['benchmark'][analyzed_file_name].keys():
            results['benchmark'][analyzed_file_name][tool] = {
                'analysis_time':analysis_time,
                'real_time':real_time,
                'user_time':user_time,
                'sys_time':sys_time,
                'memory':memory,
                'exit_code':exit_code,
                'file_size':size_of_files[path_command]
            }

    return results
        
def read_all_paths_and_sizes(lines: str):
    global size_of_files

    path = ""
    size = 0
    for line in lines:
        line = line.strip()
        (path, size) = scanf("%s:%d", line)
        size_of_files[path] = size


def main():
    global database_connector

    database_connector.config()

    with open('./kunai-benchmark-results/file_sizes.csv', 'r') as f_:
        lines = f_.readlines()
        read_all_paths_and_sizes(lines)
    
    for root, dirs, files in os.walk('./kunai-benchmark-results/'):
        for filename in files:
            if filename == 'file_sizes.csv':
                continue
            path = os.path.join(root, filename)
            with open(path, 'r') as f_:
                lines = f_.readlines()
                result = extract_variables_analysis_line(lines)

                current_data = database_connector.retrieve_analysis_apk(filename.replace('.csv',''))
                if current_data is None:
                    print(f"Error for packagename {filename.replace('.csv','')}")
                    sys.exit(1)
                
                current_data['analysis']['benchmark'] = result['benchmark']
                
                database_connector.insert_analysis_apk(filename.replace('.csv',''), dict(current_data['analysis']))

if __name__ == '__main__':
    main()
                