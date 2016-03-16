#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey
# Execution: python parser.py inputFile outputFile (default|custom)

"""
Program to parse and modify logs from Tomcat (v7) with default logging configuration.
Includes a line at the beginning of the document, in order to obtain the header of the resultant CSV.
The program attempts to provide a "case id" column, that makes reference with an use case inside a
HTTP user session.
"""

import sys
import csv
import fileinput
import datetime
import time
from heuristic import Identification

# Header line of the output CSV
lineComplete = "User Session ID; Host; User Auth; Date & Time; Request; HTTPStatusCode; Bytes Sent (-headers); " \
       "Request Method; Query String; Referer (header); User Agent\n"

lineCustom = "XForwardedFor; IP; User; Timestamp; Event; Tipo; Bytes; Session\n"
line = "IP; Unknown; User; Timestamp; Event; Tipo; Bytes; Session\n"

# Temporary file to make CSV conversion.
tempFile = "temp.csv"

# Numbers of certain rows of the CSV. Useful for not touching the code.
ip_row = 0
date_row = 3
user_row = 2
session_row = 6

# Custom time for session heuristic.
session_time = 30

# List of identifications (certain different entries of logs)
identifications = []

# Performance
last_timestamp = ""

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

    # Convert to unix timestamp
    d1_ts = time.mktime(t1.timetuple())
    d2_ts = time.mktime(t2.timetuple())

    # Now in seconds, division to get minutes.

    difference = (d1_ts-d2_ts) / 60

    return difference

# Session changer. Applies an heuristic for identifying HTTP user sessions.
def change_session(change, list):
    session = change.session
    for ident in list:
        if ident.ip == change.ip and ident.user != change.user:
            # If the entries have the same IP address, and differs in user
            hex_dig = Identification.get_hash(change)
            identifications.remove(change)
            change.session = hex_dig
            identifications.remove(ident)
            identifications.append(change)
        elif ident.ip == change.ip and (compare_timestamp(ident.timestamp, change.timestamp) > session_time):
            # If the entries have the same IP address, and timestamp difference are "big" enough
            hex_dig = Identification.get_hash(change)
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
        elif compare_timestamp(last_timestamp, ident.timestamp) > session_time:
            # If IP has been out for a long time
            identifications.remove(ident)
    return session

# CSV correction. For Null bytes and other problems.
def correct_csv(filename):
    # Corrects the CSV "inplace"
    print ("--> Correcting CSV (for bad characters)")
    for line in fileinput.FileInput(filename, inplace=1):
        line = line.replace('\0', '')
        sys.stdout.write(line)
    fileinput.close()

# CSV Parser. Applies user session heuristic (default Tomcat logging version).
def default_csv_parser(filename, output):
    # Corrects the CSV in first place
    correct_csv(filename)
    print ("--> Changing format of CSV (delimiters)")
    with open(filename, mode="rb") as infile:
        reader = csv.reader(infile, delimiter=" ")
        with open(tempFile, mode="w") as outfile:
            writer = csv.writer(outfile, delimiter=';')
            for row in reader:
                # Ignore one column (offset)
                writer.writerow((row[0], row[1], row[2], row[3], row[5], row[6], row[7]))
    # Goes to main parser
    csv_parser(tempFile, output, 1)

# CSV Parser. Applies user session heuristic.
def csv_parser(filename, output, date):
    print ("--> Applying heuristics & parsing CSV")
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

            # Format timestamp for best further treatment
            if date:
                row[date_row] = date_time_format(row[date_row])
            # Sets last timestamp
            global last_timestamp
            last_timestamp = row[date_row]
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
    if len(sys.argv) > 3:
        if sys.argv[3].lower() == "default":
            print ("\n--> Using CSV header (default): \n" + line + "\n")
            default_csv_parser(sys.argv[1], sys.argv[2])
            print ("\nDone! Results available in: " + sys.argv[2] + "\n")
        elif sys.argv[3].lower() == "custom":
            print ("Using CSV header (custom): \n" + line + "\n")
            csv_parser(sys.argv[1], sys.argv[2], 0)
            print ("Done! Results available in: " + sys.argv[2] + "\n")
    else:
        print "Enter as arguments the name of the log file, the output file and the parser type (default | custom). " \
              "In this order."

# Execution of main method
if __name__ == '__main__':
    main()
