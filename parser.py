#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Program to parse and modify logs from Tomcat (v7) with default logging configuration.
Includes a line at the beginning of the document, in order to obtain the header of the resultant CSV.
The program attempts to provide a "case id" column, that makes reference with an use case inside a
HTTP user session.
"""

import sys
import csv
import datetime
from heuristic import Identification

# Header line of the output CSV
#line = "User Session ID; Host; User Auth; Date & Time; Request; HTTPStatusCode; Bytes Sent (-headers); " \
#       "Request Method; Query String; Referer (header); User Agent\n"

line = "XForwardedFor; IP; User; Timestamp; Event; Tipo; Bytes; Session\n"

# Numbers of certain rows of the CSV. Useful for not touching the code.
ip_row = 1
date_row = 3
user_row = 2
session_row = 6

# Custom time for session heuristic.
session_time = 30

# List of identifications (certain different entries of logs)
identifications = []

# Date and Time formatter (DD/MM/YYYY HH:MM:SS)
def date_time_format(row):
    row = row.replace("Jan", "01")
    row = row.replace("Feb", "02")
    row = row.replace("Mar", "03")
    row = row.replace("Apr", "04")
    row = row.replace("May", "05")
    row = row.replace("Jun", "06")
    row = row.replace("Jul", "07")
    row = row.replace("Aug", "08")
    row = row.replace("Sep", "09")
    row = row.replace("Oct", "10")
    row = row.replace("Nov", "11")
    row = row.replace("Dec", "12")
    row = row.replace(" +0000", "")
    row = row.replace("[", "")
    row = row.replace("]", "")
    row = row.replace(":", " ", 1)
    return row


# Compare two timestamps in custom timestamp format, returns minutes of difference.
def compare_timestamp(timestamp1, timestamp2):

    t1 = datetime.datetime.strptime(timestamp1.strip(), '%d/%m/%Y %H:%M:%S')
    t2 = datetime.datetime.strptime(timestamp2.strip(), '%d/%m/%Y %H:%M:%S')

    difference = t1 - t2

    difference = difference.days * 24 * 60
    return difference


# Session changer. Applies an heuristic for identifying HTTP user sessions.
def change_session(change, list):
    session = change.session
    for ident in list:
        if ident.ip == change.ip and ident.user != change.user:
            # If the entries have the same IP address, and differs in user
            hex_dig = hash(Identification.get_hash(change))
            identifications.remove(change)
            change.session = hex_dig
            identifications.remove(ident)
            identifications.append(change)
        elif ident.ip == change.ip and (compare_timestamp(ident.timestamp, change.timestamp) > session_time):
            # If the entries have the same IP address, and timestamp difference are "big" enough
            hex_dig = hash(Identification.get_hash(change))
            identifications.remove(change)
            change.session = hex_dig
            identifications.remove(ident)
            identifications.append(change)
        elif ident.ip == change.ip and not ident == change:
            # If the entries have the same IP address, and they're not the same object
            session = ident.session
            identifications.remove(change)
            change.session = session
            identifications.remove(ident)
            identifications.append(change)
    return session


# CSV Parser. Applies user session heuristic.
def csv_parser(filename, output):
    with open(filename, "rb") as file_a:
        r = csv.reader(file_a, delimiter=';')
        file_b = open(output, "w")
        w = csv.writer(file_b,  delimiter=';')
        # Writes the CSV header
        file_b.writelines(line)
        # Reads the entire input file
        for row in r:
            # If HTTP SESSION is not available, the row is ignored
            #if "-" not in row[0]:

            # Format timestamp for best further reatment
            #row[date_row] = date_time_format(row[date_row])
            id = Identification(row[ip_row], row[date_row], row[user_row])
            identifications.append(id)
            # Attempt to apply user session heuristic
            session = change_session(id, identifications)
            row.append(session)
            w.writerow(row)
        file_a.close()
        file_b.close()


# Main method. Applies heuristics and creates a new CSV for data & process mining.
def main():
    if len(sys.argv) > 1:
        csv_parser(sys.argv[1], sys.argv[2])
    else:
        print "Introduzca como argumentos el nombre del fichero de log y el fichero de salida"

# Execution of main method
if __name__ == '__main__':
    main()
