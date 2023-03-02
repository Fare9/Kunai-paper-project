#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Generate two box plot for each one of the datasets
these box plots will show the improvement of Kunai
respecting the information extracted from the APK
files.

|         _________
|   |----|     |   |----|
|         ¯¯¯¯¯¯¯¯¯
|
|
|
|_______________________________________
'''

import numpy
import pandas as pd
import plotly.graph_objects as go


def DELTA(str):
    return "delta_%s" % (str)


def DELTA_DIV(str):
    return "delta_%s_div" % (str)


def trim_data(DATA: pd.DataFrame, size, minor_size) -> pd.DataFrame:
    return DATA[
        # high pass filter
        (DATA[DELTA('method_xref_read')] <= size) &
        (DATA[DELTA('field_xref_read')] <= size) 
        # low-pass filter
        #(DATA[DELTA('classes_xref_from')] > minor_size) &
        #(DATA[DELTA('classes_xref_to')] > minor_size) &
        #(DATA[DELTA('classes_xref_const_class')] > minor_size) &
        #(DATA[DELTA('class_xref_new_instance')] > minor_size) &
        #(DATA[DELTA('method_xref_const_class')] > minor_size) &
        #(DATA[DELTA('method_xref_from')] > minor_size) &
        #(DATA[DELTA('method_xref_new_instance')] > minor_size) &
        #(DATA[DELTA('method_xref_read')] > minor_size) &
        #(DATA[DELTA('method_xref_to')] > minor_size) &
        #(DATA[DELTA('method_xref_write')] > minor_size) &
        #(DATA[DELTA('field_xref_read')] > minor_size) &
        #(DATA[DELTA('field_xref_write')] > minor_size) &
        #(DATA[DELTA('str_xref_from')] > minor_size) &
        #(DATA[DELTA('stringanalysis')] > minor_size)
    ]


DATA_GOOGLEPLAY = pd.read_csv('information_googleplay.csv')
DATA_MALWARE = pd.read_csv('information_malware.csv')

original_length_gp = len(DATA_GOOGLEPLAY)
original_length_malware = len(DATA_MALWARE)

# remove for google play those cases greater than 75KB
DATA_GOOGLEPLAY = trim_data(DATA_GOOGLEPLAY, 75*1000, -2*1000).reset_index()

DATA_MALWARE = trim_data(DATA_MALWARE, 20*1000, -2*1000).reset_index()

print(f"Original Length Google Play: {original_length_gp}, current length: {len(DATA_GOOGLEPLAY)}, removed: {original_length_gp-len(DATA_GOOGLEPLAY)}")
print(f"Original Length Malware: {original_length_malware}, current length: {len(DATA_MALWARE)}, removed: {original_length_malware-len(DATA_MALWARE)}")

fig = go.Figure()


def get_list_not_inf(df: pd.DataFrame, key) -> list:
    key_div = key + '_div'
    return list(df.loc[df[key_div] != numpy.inf][key])


def add_boxplot(fig, x, name):
    fig.add_trace(go.Box(
        x=x,
        y=[name]*len(x),
        name=name,
        width=0.8,
        showlegend=False
    ))

# for google play information


deltas_str = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_strings')
add_boxplot(fig, deltas_str, "string")

deltas_types = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_types')
add_boxplot(fig, deltas_types, "type")

deltas_protos = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_protos')
add_boxplot(fig, deltas_protos, "proto")

deltas_fields = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_fields')
add_boxplot(fig, deltas_fields, "field")

deltas_methods = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_methods')
add_boxplot(fig, deltas_methods, "method")

deltas_classes = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_classes')
add_boxplot(fig, deltas_classes, "classes")

delta_instructions = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_instructions')
add_boxplot(fig, delta_instructions, "instructions")

delta_classanalysis = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_classanalysis')
add_boxplot(fig, delta_classanalysis, "classanalysis")

delta_classes_xref_from = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_classes_xref_from')
add_boxplot(fig, delta_classes_xref_from, "classes_xref_from")

delta_classes_xref_to = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_classes_xref_to')
add_boxplot(fig, delta_classes_xref_to, "classes_xref_to")

delta_classes_xref_const_class = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_classes_xref_const_class')
add_boxplot(fig, delta_classes_xref_const_class, "classes_xref_const_class")

delta_class_xref_new_instance = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_class_xref_new_instance')
add_boxplot(fig, delta_class_xref_new_instance, "class_xref_new_instance")

delta_methodanalysis = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_methodanalysis')
add_boxplot(fig, delta_methodanalysis, "methodanalysis")

delta_method_xref_const_class = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_method_xref_const_class')
add_boxplot(fig, delta_method_xref_const_class, "method_xref_const_class")

delta_method_xref_from = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_method_xref_from')
add_boxplot(fig, delta_method_xref_from, "method_xref_from")

delta_method_xref_new_instance = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_method_xref_new_instance')
add_boxplot(fig, delta_method_xref_new_instance, "method_xref_new_instance")

delta_method_xref_read = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_method_xref_read')
add_boxplot(fig, delta_method_xref_read, "method_xref_read")

delta_method_xref_to = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_method_xref_to')
add_boxplot(fig, delta_method_xref_to, "method_xref_to")

delta_method_xref_write = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_method_xref_write')
add_boxplot(fig, delta_method_xref_write, "method_xref_write")

delta_fieldanalysis = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_fieldanalysis')
add_boxplot(fig, delta_fieldanalysis, "fieldanalysis")

delta_field_xref_read = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_field_xref_read')
add_boxplot(fig, delta_field_xref_read, "field_xref_read")

delta_field_xref_write = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_field_xref_write')
add_boxplot(fig, delta_field_xref_write, "field_xref_write")

delta_stringanalysis = get_list_not_inf(
    DATA_GOOGLEPLAY, 'delta_stringanalysis')
add_boxplot(fig, delta_stringanalysis, "stringanalysis")

delta_str_xref_from = get_list_not_inf(DATA_GOOGLEPLAY, 'delta_str_xref_from')
add_boxplot(fig, delta_str_xref_from, "str_xref_from")


fig.update_layout(
    xaxis=dict(zeroline=False),
    xaxis_title="Improvement Factor",
    boxmode='group',
    boxgap=0,
    boxgroupgap=0,
    margin=dict(l=0, r=0, t=0, b=0),
)

fig.update_traces(orientation='h')  # horizontal box plots
#fig.show()
fig.write_image("/tmp/test.pdf")
fig.write_image("information-improvement-gplay.pdf", engine="kaleido")

# for malware information

fig = go.Figure()

deltas_str = get_list_not_inf(DATA_MALWARE, 'delta_strings')
add_boxplot(fig, deltas_str, "string")

deltas_types = get_list_not_inf(DATA_MALWARE, 'delta_types')
add_boxplot(fig, deltas_types, "type")

deltas_protos = get_list_not_inf(DATA_MALWARE, 'delta_protos')
add_boxplot(fig, deltas_protos, "proto")

deltas_fields = get_list_not_inf(DATA_MALWARE, 'delta_fields')
add_boxplot(fig, deltas_fields, "field")

deltas_methods = get_list_not_inf(DATA_MALWARE, 'delta_methods')
add_boxplot(fig, deltas_methods, "method")

deltas_classes = get_list_not_inf(DATA_MALWARE, 'delta_classes')
add_boxplot(fig, deltas_classes, "classes")

delta_instructions = get_list_not_inf(DATA_MALWARE, 'delta_instructions')
add_boxplot(fig, delta_instructions, "instructions")

delta_classanalysis = get_list_not_inf(DATA_MALWARE, 'delta_classanalysis')
add_boxplot(fig, delta_classanalysis, "classanalysis")

delta_classes_xref_from = get_list_not_inf(
    DATA_MALWARE, 'delta_classes_xref_from')
add_boxplot(fig, delta_classes_xref_from, "classes_xref_from")

delta_classes_xref_to = get_list_not_inf(DATA_MALWARE, 'delta_classes_xref_to')
add_boxplot(fig, delta_classes_xref_to, "classes_xref_to")

delta_classes_xref_const_class = get_list_not_inf(
    DATA_MALWARE, 'delta_classes_xref_const_class')
add_boxplot(fig, delta_classes_xref_const_class, "classes_xref_const_class")

delta_class_xref_new_instance = get_list_not_inf(
    DATA_MALWARE, 'delta_class_xref_new_instance')
add_boxplot(fig, delta_class_xref_new_instance, "class_xref_new_instance")

delta_methodanalysis = get_list_not_inf(DATA_MALWARE, 'delta_methodanalysis')
add_boxplot(fig, delta_methodanalysis, "methodanalysis")

delta_method_xref_const_class = get_list_not_inf(
    DATA_MALWARE, 'delta_method_xref_const_class')
add_boxplot(fig, delta_method_xref_const_class, "method_xref_const_class")

delta_method_xref_from = get_list_not_inf(
    DATA_MALWARE, 'delta_method_xref_from')
add_boxplot(fig, delta_method_xref_from, "method_xref_from")

delta_method_xref_new_instance = get_list_not_inf(
    DATA_MALWARE, 'delta_method_xref_new_instance')
add_boxplot(fig, delta_method_xref_new_instance, "method_xref_new_instance")

delta_method_xref_read = get_list_not_inf(
    DATA_MALWARE, 'delta_method_xref_read')
add_boxplot(fig, delta_method_xref_read, "method_xref_read")

delta_method_xref_to = get_list_not_inf(DATA_MALWARE, 'delta_method_xref_to')
add_boxplot(fig, delta_method_xref_to, "method_xref_to")

delta_method_xref_write = get_list_not_inf(
    DATA_MALWARE, 'delta_method_xref_write')
add_boxplot(fig, delta_method_xref_write, "method_xref_write")

delta_fieldanalysis = get_list_not_inf(DATA_MALWARE, 'delta_fieldanalysis')
add_boxplot(fig, delta_fieldanalysis, "fieldanalysis")

delta_field_xref_read = get_list_not_inf(DATA_MALWARE, 'delta_field_xref_read')
add_boxplot(fig, delta_field_xref_read, "field_xref_read")

delta_field_xref_write = get_list_not_inf(
    DATA_MALWARE, 'delta_field_xref_write')
add_boxplot(fig, delta_field_xref_write, "field_xref_write")

delta_stringanalysis = get_list_not_inf(DATA_MALWARE, 'delta_stringanalysis')
add_boxplot(fig, delta_stringanalysis, "stringanalysis")

delta_str_xref_from = get_list_not_inf(DATA_MALWARE, 'delta_str_xref_from')
add_boxplot(fig, delta_str_xref_from, "str_xref_from")

fig.update_layout(
    xaxis=dict(zeroline=False),
    xaxis_title="Improvement Factor",
    boxmode='group',
    boxgap=0,
    boxgroupgap=0,
    margin=dict(l=0, r=0, t=0, b=0)
)

fig.update_traces(orientation='h')  # horizontal box plots
#fig.show()
fig.write_image("information-improvement-malware.pdf", engine="kaleido")