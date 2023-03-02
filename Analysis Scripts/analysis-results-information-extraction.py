#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
Analysis script that will read the information obtained
by Androguard and Kunai from the database, with this
information, we will generate two CSVs (one for googleplay
datasets and one for malware dataset) the CSV will contain
the improvements from the analysis, two ways for calculate
them:

        info kunai - info androguard
        info kunai/info androguard
'''

import sys
import csv
import pprint
from database_connector import DatabaseConnector


def DELTA(str):
    return "delta_%s" % (str)


def DELTA_DIV(str):
    return "delta_%s_div" % (str)

total_row_per_field = {}
infs_per_field = {}


def operate(Kunai, Androguard, field):
    global infs_per_field
    global total_row_per_field

    if field not in total_row_per_field.keys():
        total_row_per_field[field] = 1
    else:
        total_row_per_field[field] += 1

    if Androguard[field] == 0:
        if field not in infs_per_field.keys():
            infs_per_field[field] = 1
        else:
            infs_per_field[field] += 1
        return Kunai[field] - Androguard[field],"INF"
    return Kunai[field] - Androguard[field], Kunai[field] / Androguard[field]


def get_improvement(Androguard, Kunai):
    delta_str, delta_str_div = operate(Kunai, Androguard, 'strings')
    delta_types, delta_types_div = operate(Kunai, Androguard, 'types')
    delta_protos, delta_protos_div = operate(Kunai, Androguard, 'protos')
    delta_fields, delta_fields_div = operate(Kunai, Androguard, 'fields')
    delta_methods, delta_methods_div = operate(Kunai, Androguard, 'methods')
    delta_classes, delta_classes_div = operate(Kunai, Androguard, 'classes')
    delta_instructions, delta_instructions_div = operate(
        Kunai, Androguard, 'instructions')
    delta_classanalysis, delta_classanalysis_div = operate(
        Kunai, Androguard, 'classanalysis')
    delta_classes_xref_from, delta_classes_xref_from_div = operate(
        Kunai, Androguard, 'classes_xref_from')
    delta_classes_xref_to, delta_classes_xref_to_div = operate(
        Kunai, Androguard, 'classes_xref_to')
    delta_classes_xref_const_class, delta_classes_xref_const_class_div = operate(
        Kunai, Androguard, 'classes_xref_const_class')
    delta_class_xref_new_instance, delta_class_xref_new_instance_div = operate(
        Kunai, Androguard, 'class_xref_new_instance')
    delta_methodanalysis, delta_methodanalysis_div = operate(
        Kunai, Androguard, 'methodanalysis')
    delta_method_xref_const_class, delta_method_xref_const_class_div = operate(
        Kunai, Androguard, 'method_xref_const_class')
    delta_method_xref_from, delta_method_xref_from_div = operate(
        Kunai, Androguard, 'method_xref_from')
    delta_method_xref_new_instance, delta_method_xref_new_instance_div = operate(
        Kunai, Androguard, 'method_xref_new_instance')
    delta_method_xref_read, delta_method_xref_read_div = operate(
        Kunai, Androguard, 'method_xref_read')
    delta_method_xref_to, delta_method_xref_to_div = operate(
        Kunai, Androguard, 'method_xref_to')
    delta_method_xref_write, delta_method_xref_write_div = operate(
        Kunai, Androguard, 'method_xref_write')
    delta_fieldanalysis, delta_fieldanalysis_div = operate(
        Kunai, Androguard, 'fieldanalysis')
    delta_field_xref_read, delta_field_xref_read_div = operate(
        Kunai, Androguard, 'field_xref_read')
    delta_field_xref_write, delta_field_xref_write_div = operate(
        Kunai, Androguard, 'field_xref_write')
    delta_stringanalysis, delta_stringanalysis_div = operate(
        Kunai, Androguard, 'stringanalysis')
    delta_str_xref_from, delta_str_xref_from_div = operate(
        Kunai, Androguard, 'str_xref_from')

    return [delta_str, delta_str_div,
            delta_types, delta_types_div,
            delta_protos, delta_protos_div,
            delta_fields, delta_fields_div,
            delta_methods, delta_methods_div,
            delta_classes, delta_classes_div,
            delta_instructions, delta_instructions_div,
            delta_classanalysis, delta_classanalysis_div,
            delta_classes_xref_from, delta_classes_xref_from_div,
            delta_classes_xref_to, delta_classes_xref_to_div,
            delta_classes_xref_const_class, delta_classes_xref_const_class_div,
            delta_class_xref_new_instance, delta_class_xref_new_instance_div,
            delta_methodanalysis, delta_methodanalysis_div,
            delta_method_xref_const_class, delta_method_xref_const_class_div,
            delta_method_xref_from, delta_method_xref_from_div,
            delta_method_xref_new_instance, delta_method_xref_new_instance_div,
            delta_method_xref_read, delta_method_xref_read_div,
            delta_method_xref_to, delta_method_xref_to_div,
            delta_method_xref_write, delta_method_xref_write_div,
            delta_fieldanalysis, delta_fieldanalysis_div,
            delta_field_xref_read, delta_field_xref_read_div,
            delta_field_xref_write, delta_field_xref_write_div,
            delta_stringanalysis, delta_stringanalysis_div,
            delta_str_xref_from, delta_str_xref_from_div]


header_info_google_play = [
    'package_name',
    'file',
    DELTA('strings'),
    DELTA_DIV('strings'),
    DELTA('types'),
    DELTA_DIV('types'),
    DELTA('protos'),
    DELTA_DIV('protos'),
    DELTA('fields'),
    DELTA_DIV('fields'),
    DELTA('methods'),
    DELTA_DIV('methods'),
    DELTA('classes'),
    DELTA_DIV('classes'),
    DELTA('instructions'),
    DELTA_DIV('instructions'),
    DELTA('classanalysis'),
    DELTA_DIV('classanalysis'),
    DELTA('classes_xref_from'),
    DELTA_DIV('classes_xref_from'),
    DELTA('classes_xref_to'),
    DELTA_DIV('classes_xref_to'),
    DELTA('classes_xref_const_class'),
    DELTA_DIV('classes_xref_const_class'),
    DELTA('class_xref_new_instance'),
    DELTA_DIV('class_xref_new_instance'),
    DELTA('methodanalysis'),
    DELTA_DIV('methodanalysis'),
    DELTA('method_xref_const_class'),
    DELTA_DIV('method_xref_const_class'),
    DELTA('method_xref_from'),
    DELTA_DIV('method_xref_from'),
    DELTA('method_xref_new_instance'),
    DELTA_DIV('method_xref_new_instance'),
    DELTA('method_xref_read'),
    DELTA_DIV('method_xref_read'),
    DELTA('method_xref_to'),
    DELTA_DIV('method_xref_to'),
    DELTA('method_xref_write'),
    DELTA_DIV('method_xref_write'),
    DELTA('fieldanalysis'),
    DELTA_DIV('fieldanalysis'),
    DELTA('field_xref_read'),
    DELTA_DIV('field_xref_read'),
    DELTA('field_xref_write'),
    DELTA_DIV('field_xref_write'),
    DELTA('stringanalysis'),
    DELTA_DIV('stringanalysis'),
    DELTA('str_xref_from'),
    DELTA_DIV('str_xref_from'),
]

header_info_malware = [
    'MD5',
    'Family',
    'File',
    DELTA('strings'),
    DELTA_DIV('strings'),
    DELTA('types'),
    DELTA_DIV('types'),
    DELTA('protos'),
    DELTA_DIV('protos'),
    DELTA('fields'),
    DELTA_DIV('fields'),
    DELTA('methods'),
    DELTA_DIV('methods'),
    DELTA('classes'),
    DELTA_DIV('classes'),
    DELTA('instructions'),
    DELTA_DIV('instructions'),
    DELTA('classanalysis'),
    DELTA_DIV('classanalysis'),
    DELTA('classes_xref_from'),
    DELTA_DIV('classes_xref_from'),
    DELTA('classes_xref_to'),
    DELTA_DIV('classes_xref_to'),
    DELTA('classes_xref_const_class'),
    DELTA_DIV('classes_xref_const_class'),
    DELTA('class_xref_new_instance'),
    DELTA_DIV('class_xref_new_instance'),
    DELTA('methodanalysis'),
    DELTA_DIV('methodanalysis'),
    DELTA('method_xref_const_class'),
    DELTA_DIV('method_xref_const_class'),
    DELTA('method_xref_from'),
    DELTA_DIV('method_xref_from'),
    DELTA('method_xref_new_instance'),
    DELTA_DIV('method_xref_new_instance'),
    DELTA('method_xref_read'),
    DELTA_DIV('method_xref_read'),
    DELTA('method_xref_to'),
    DELTA_DIV('method_xref_to'),
    DELTA('method_xref_write'),
    DELTA_DIV('method_xref_write'),
    DELTA('fieldanalysis'),
    DELTA_DIV('fieldanalysis'),
    DELTA('field_xref_read'),
    DELTA_DIV('field_xref_read'),
    DELTA('field_xref_write'),
    DELTA_DIV('field_xref_write'),
    DELTA('stringanalysis'),
    DELTA_DIV('stringanalysis'),
    DELTA('str_xref_from'),
    DELTA_DIV('str_xref_from'),
]

db_connector = DatabaseConnector()

db_connector.config(database='INFORMATION',
                    collection='APKs', malware_collection='MALWARE')

all_googleplay_info = db_connector.retrieve_all_the_documents_from_collection()

all_malware_info = db_connector.retrieve_all_documents_from_malware_collection()

androguard_errors = 0
kunai_errors = 0

with open('information_googleplay.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header_info_google_play)
    for row in all_googleplay_info:
        package_name = row['package']
        analysis_benchmark = row['analysis']['benchmark']
        for file in analysis_benchmark:
            file_name = file
            androguard_results = analysis_benchmark[file_name]['Androguard']
            kunai_results = analysis_benchmark[file_name]['Kunai']
            if androguard_results['exit_code'] != 0:
                androguard_errors += 1
            if kunai_results['exit_code'] != 0:
                kunai_errors += 1
            if androguard_results['exit_code'] != 0 or kunai_results['exit_code'] != 0:
                continue
            values = get_improvement(androguard_results, kunai_results)

            if values[0] < 0:
                print(f"Error with string in package name {package_name}, file name {file_name}")

            writer.writerow([package_name, file_name] + values)

print("Number of errors in Google Play")
print(f"Androguard:{androguard_errors}")
print(f"Kunai:{kunai_errors}")

androguard_errors = 0
kunai_errors = 0

with open('information_malware.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header_info_malware)
    for row in all_malware_info:
        md5 = row['md5']
        malware_family = row['malware_family']
        analysis_benchmark = row['analysis']['benchmark']
        for file in analysis_benchmark:
            file_name = file
            androguard_results = analysis_benchmark[file_name]['Androguard']
            kunai_results = analysis_benchmark[file_name]['Kunai']
            if androguard_results['exit_code'] != 0:
                androguard_errors += 1
            if kunai_results['exit_code'] != 0:
                kunai_errors += 1
            if androguard_results['exit_code'] != 0 or kunai_results['exit_code'] != 0:
                continue
            values = get_improvement(androguard_results, kunai_results)

            if values[0] < 0:
                print(f"Error with string in md5 {md5}, malware family {malware_family}, file name {file_name}")

            writer.writerow([md5, malware_family, file_name] + values)

print("Number of errors in Malware")
print(f"Androguard:{androguard_errors}")
print(f"Kunai:{kunai_errors}")

print("Total rows per field:")
pprint.pprint(total_row_per_field)
print("Total INF per field (%):")
for field in infs_per_field.keys():
    percentage = (infs_per_field[field]/total_row_per_field[field])*100
    print(f"{field} = {percentage}%")