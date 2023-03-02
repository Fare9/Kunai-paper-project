#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
Get data extracted both with Androguard and
Kunai, this script will be used for the information
extracted from Google Play apps.

Analyzed folder: extract-information-googleplay
'''

import os
from os.path import basename
from database_connector import DatabaseConnector
from scanf import scanf

database_connector = DatabaseConnector()

def retrieve_variables_androguard(line: str) -> tuple:
    '''
    Extract information from the Androguard analysis line, 
    this is a little bit different to the one on Kunai.

    :param line: line to analyze with scanf and extract data.
    :return: tuple with variables of different data types.
    ''' 
    return scanf("%s;%s;strings:%d;fields:%d;methods:%d; classes:%d;instructions:%d;classanalysis:%d;classes_xref_from:%d,classes_xref_to:%d,classes_xref_const_class:%d,class_xref_new_instance:%d,methodanalysis:%d;method_xref_const_class:%d,method_xref_from:%d,method_xref_new_instance:%d,method_xref_read:%d,method_xref_to:%d,method_xref_write:%d;fieldanalysis:%d;field_xref_read:%d;field_xref_write:%d;stringanalysis:%d,str_xref_from:%d,;exit_code:%d", line)

def retrieve_variables_kunai(line: str) -> tuple:
    '''
    Extract information from the Kunai analysis line.

    :param line: line to analyze with scanf and extract data.
    :return: tuple with variables of different data types.
    '''
    return scanf("%s;%s;strings:%d;types:%d;protos:%d;fields:%d;methods:%d;classes:%d;instructions:%d;classanalysis:%d;classes_xref_from:%d;classes_xref_to:%d;classes_xref_const_class:%d;class_xref_new_instance:%d;methodanalysis:%d;method_xref_const_class:%d;method_xref_from:%d;method_xref_new_instance:%d;method_xref_read:%d;method_xref_to:%d;method_xref_write:%d;fieldanalysis:%d;field_xref_read:%d;field_xref_write:%d;stringanalysis:%d;str_xref_from:%d;exit_code:%d", line)

def retrieve_type_error(line: str) -> tuple:
    '''
    Extract information in case of type error.

    :param line: line to analyze.
    :return: tuple with information.
    '''
    values = line.split(';')
    exit_code = int(values[-1].split(':')[1])
    return (values[0], values[1], exit_code)

def analyze_lines(lines: list):
    '''
    Analyze all the lines from the analysis files,
    generate a results dictionary and return it.

    :param lines: all the lines from the analysis file.
    :result: dictionary with the results from the analysis.
    '''

    results = {'benchmark':dict()}

    tool=""
    analyzed_path=""
    strings=0
    types=0
    protos=0
    fields=0
    methods=0
    classes=0
    instructions=0
    classanalysis=0
    classes_xref_from=0
    classes_xref_to=0
    classes_xref_const_class=0
    class_xref_new_instance=0
    methodanalysis=0
    method_xref_const_class=0
    method_xref_from=0
    method_xref_new_instance=0
    method_xref_read=0
    method_xref_to=0
    method_xref_write=0
    fieldanalysis=0
    field_xref_read=0
    field_xref_write=0
    stringanalysis=0
    str_xref_from=0
    exit_code=0

    for line in lines:
        line = line.strip()

        if line is None or line == "":
            continue

        try:
            if 'Androguard' in line:
                (tool,analyzed_path,strings,fields,methods,classes,instructions,classanalysis,classes_xref_from,classes_xref_to,classes_xref_const_class,class_xref_new_instance,methodanalysis,method_xref_const_class,method_xref_from,method_xref_new_instance,method_xref_read,method_xref_to,method_xref_write,fieldanalysis,field_xref_read,field_xref_write,stringanalysis,str_xref_from,exit_code) = retrieve_variables_androguard(line)
                types = 0
                protos = 0
            elif 'Kunai' in line:
                (tool,analyzed_path,strings,types,protos,fields,methods,classes,instructions,classanalysis,classes_xref_from,classes_xref_to,classes_xref_const_class,class_xref_new_instance,methodanalysis,method_xref_const_class,method_xref_from,method_xref_new_instance,method_xref_read,method_xref_to,method_xref_write,fieldanalysis,field_xref_read,field_xref_write,stringanalysis,str_xref_from,exit_code) = retrieve_variables_kunai(line)
        except:
            (tool, analyzed_path, exit_code) = retrieve_type_error(line)
            strings=0
            types=0
            protos=0
            fields=0
            methods=0
            classes=0
            instructions=0
            classanalysis=0
            classes_xref_from=0
            classes_xref_to=0
            classes_xref_const_class=0
            class_xref_new_instance=0
            methodanalysis=0
            method_xref_const_class=0
            method_xref_from=0
            method_xref_new_instance=0
            method_xref_read=0
            method_xref_to=0
            method_xref_write=0
            fieldanalysis=0
            field_xref_read=0
            field_xref_write=0
            stringanalysis=0
            str_xref_from=0
                
        file_name = basename(analyzed_path).replace('.','_')

        if file_name not in results['benchmark']:
            results['benchmark'][file_name] = dict()
        
        if tool not in results['benchmark'][file_name]:
            results['benchmark'][file_name][tool] = dict()

        results['benchmark'][file_name][tool] = {
            'strings':strings,
            'types':types,
            'protos':protos,
            'fields':fields,
            'methods':methods,
            'classes':classes,
            'instructions':instructions,
            'classanalysis':classanalysis,
            'classes_xref_from':classes_xref_from,
            'classes_xref_to':classes_xref_to,
            'classes_xref_const_class':classes_xref_const_class,
            'class_xref_new_instance':class_xref_new_instance,
            'methodanalysis':methodanalysis,
            'method_xref_const_class':method_xref_const_class,
            'method_xref_from':method_xref_from,
            'method_xref_new_instance':method_xref_new_instance,
            'method_xref_read':method_xref_read,
            'method_xref_to':method_xref_to,
            'method_xref_write':method_xref_write,
            'fieldanalysis':fieldanalysis,
            'field_xref_read':field_xref_read,
            'field_xref_write':field_xref_write,
            'stringanalysis':stringanalysis,
            'str_xref_from':str_xref_from,
            'exit_code':exit_code
        }

    return results

def main():
    global database_connector

    database_connector.config()

    for root, dirs, files in os.walk('./extract-information-googleplay/'):
        for filename in files:
            path = os.path.join(root, filename)
            with open(path, 'r') as f_:
                print(f"Analyzing file '{path}'")
                lines = f_.readlines()
                result = analyze_lines(lines)
                pkg_name = filename.replace('.csv', '')
                database_connector.insert_analysis_apk(pkg_name=pkg_name,analysis_results=result)
            
if __name__ == '__main__':
    main()