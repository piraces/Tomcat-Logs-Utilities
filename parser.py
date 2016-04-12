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
from identification import Identification
import cases_heuristic

# Main pages of possible events. Used for replacing and identifying events.
pages = ["/attachedFiles/", "library-advanced-search.jsp", "library-build-bibtex.jsp", "library-edit-configuration.jsp",
    "library-edit-reference.jsp", "library-edit-search.jsp", "library-error.jsp", "library-help.html",
    "library-pending-tasks.html", "library-quick-search.jsp", "library-save-configuration.jsp",
    "library-show-publications-bibtex.jsp", "library-show-publications-raw-bibtex.jsp", "library-show-publications.jsp",
    "library-update-db.jsp"]

# Possible names of events known as "index".
index = ["GET /PUBLICATIONS HTTP/1",  "GET /PUBLICATIONS/ HTTP/1", "GET / HTTP/1"]

# Header lines of the output CSV
lineCustom = "User Session ID; Host; User Auth; Date & Time; Request; HTTPStatusCode; Bytes Sent (-headers); " \
       "Request Method; Query String; Referer (header); User Agent; Session; Case; Case-id\n"

linePerfect = "CaseId; XForwardedFor; IP; User; Timestamp; Event; Tipo; Bytes; User Agent; Referer (header); " \
              "Session; Case; Case-id\n"

line = "IP; Unknown; User; Timestamp; Event; Tipo; Bytes; Session; Case; Case-id\n"

# Temporary files to make CSV conversion.
tempFile = "temp.csv"
tempFile2 = "temp2.csv"

# Output
finalOutput = ""

# Numbers of certain rows of the CSV. Useful for not touching the code. Changes between different headers.
ip_row = 0
user_row = 2
date_row = 3
event_row = 4
status_row = 5
# session_row = 6

# Custom time for session heuristic.
session_time = 30

# List of identifications (certain different entries of logs)
identifications = []

# Performance
last_timestamp = ""
last_use_case = 1

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
        line = line.encode("utf-8")
        sys.stdout.write(line)
    fileinput.close()

# CSV Parser. Applies user session & use cases heuristics (default Tomcat logging version).
def default_csv_parser(filename, output, heuristic):
    # Corrects the CSV in first place
    correct_csv(filename)
    print ("--> Changing format of CSV (delimiters)")
    with open(filename, mode="rb") as infile:
        reader = csv.reader(infile, delimiter=" ")
        with open(tempFile, mode="w") as outfile:
            writer = csv.writer(outfile, delimiter=';')
            for row in reader:
                # Ignore one column (offset - 4)
                row[5] = "\"" + row[5] + "\""
                writer.writerow((row[0], row[1], row[2], row[3], row[5], row[6], row[7]))
    # Goes to main parser
    csv_parser(tempFile, tempFile2, 1, heuristic)


# CSV Parser. Applies user session & use cases heuristics.
def csv_parser(filename, output, date, heuristic):
    print ("--> Applying heuristics & parsing CSV")
    with open(filename, "rb") as file_a:
        r = csv.reader(file_a, delimiter=';')
        file_b = open(output, "w")
        w = csv.writer(file_b,  delimiter=';')
        # Writes the CSV header
        file_b.writelines(line)
        # Reads the entire input file
        for row in r:
            # Format timestamp for best further treatment
            if date:
                row[date_row] = date_time_format(row[date_row])
            # Sets last timestamp
            global last_timestamp
            global last_use_case
            last_timestamp = row[date_row]
            id = Identification(row[ip_row], row[date_row], row[user_row], row[status_row], last_use_case)
            identifications.append(id)
            # Attempt to apply user session heuristic
            session = change_session(id, identifications)
            # Attempt to apply use cases heuristic
            if heuristic.lower() == "h1":
                case = cases_heuristic.set_use_case_h1(id, row[event_row])
            elif heuristic.lower() == "h2":
                case = cases_heuristic.set_use_case_h2(id, row[event_row])
            elif heuristic.lower() == "h3":
                case = cases_heuristic.set_use_case_h3(id, row[event_row])
            elif heuristic.lower() == "h4":
                case = cases_heuristic.set_use_case_h4(id, row[event_row], identifications)
            else:
                # By default, applies the H3 heuristic
                case = cases_heuristic.set_use_case_h3(id, row[event_row])
            last_use_case = case
            # Append 'case id' column (and others)
            row.append(str(session))
            row.append(case)
            caseid = str(session) + str(case)
            row.append(caseid)
            # Temporal restriction
            if case != 0:
                w.writerow(row)
        file_a.close()
        file_b.close()
        # Deletes extra parameters from events
        delete_extra_parameters(output, finalOutput)

# CSV Parser. Replace event names with other more "legible" and short".
def replace_event_names(filename, output):
    print ("--> Replacing event names with legible ones")
    with open(filename, "rb") as file_a:
        r = csv.reader(file_a, delimiter=';')
        file_b = open(output, "w")
        w = csv.writer(file_b, delimiter=';')
        file_b.writelines(line)
        # Reads the entire input file
        for row in r:
            for thing in pages:
                if thing in row[event_row]:
                    row[event_row] = thing
                elif index[0] in row[event_row] or index[1] in row[event_row] or index[2] in row[event_row]:
                    row[event_row] = "index"
                w.writerow(row)
        file_a.close()
        file_b.close()

# Events parser. Deletes parameters that doesn't identify use cases.
def delete_extra_parameters(filename, output):
    print ("--> Replacing event parameters that are not useful")
    with open(filename, "rb") as file_a:
        r = csv.reader(file_a, delimiter=';')
        file_b = open(output, "w")
        w = csv.writer(file_b, delimiter=';')
        # Reads the entire input file
        # Skips first row (header)
        header = r.next()
        w.writerow(header)
        for row in r:
            event = str(row[event_row])
            # Deletes type of event
            eventSplit = event.split(' ', 1)
            eventSplit1 = eventSplit[1]
            # Splits page from parameters
            eventSplit2 = eventSplit1.split('?', 1)
            page = eventSplit2[0]
            # Checks for parameters that identifies use cases
            if len(eventSplit2) >= 2:
                parameters = eventSplit2[1]
                if "library-edit-reference.jsp" in page and "mode=insert&view=bibtex" in parameters:
                    page += "?" + "mode=insert&view=bibtex"
                elif "library-edit-reference.jsp" in page and "mode=insert&view=field" in parameters:
                    page += "?" + "mode=insert&view=field"
                elif "library-edit-reference.jsp" in page and "mode=query" in parameters:
                    page += "?" + "mode=query"
                elif "library-show-publications-bibtex.jsp" in page and "id=*" in parameters:
                    page += "?" + "id=*"
            # Checks for static pages
            if "/attachedFiles/" in page:
                page = "/PUBLICATIONS/attachedFiles"
            elif "/images/" in page:
                page = "/PUBLICATIONS/images"
            elif "/styles/" in page:
                page = "/PUBLICATIONS/styles"
            elif "/scripts/" in page:
                page = "/PUBLICATIONS/scripts"
            elif "/applets/" in page:
                page = "/PUBLICATIONS/applets"
            elif "/PATCHES/" in page:
                page = "/PUBLICATIONS/PATCHES"
            elif "/config/" in page:
                page = "/PUBLICATIONS/config"
            # Deletes possible HTTP info in the event
            if " HTTP" in eventSplit2[0]:
                page = page.split(' ', 1)[0]

            # Correct multiple slashes
            page = page.replace("//", "/")
            page = page.replace("///", "/")
            # Close the string to ignore possible CSV delimiters
            row[event_row] = "\"" + page + "\""
            # Write the event (page)
            w.writerow(row)
        file_a.close()
        file_b.close()

# Main method. Applies heuristics and creates a new CSV for data & process mining.
def main():
    if len(sys.argv) > 4:
        if sys.argv[3].lower() == "default":
            print ("\n--> Using CSV header (default): \n" + line + "\n")
            global finalOutput
            finalOutput = sys.argv[2]
            default_csv_parser(sys.argv[1], sys.argv[2], sys.argv[4])
        elif sys.argv[3].lower() == "custom":
            print ("\nUsing CSV header (custom): \n" + line + "\n")
            csv_parser(sys.argv[1], sys.argv[2], 0, sys.argv[4])

        result = 100.0 - ((float(cases_heuristic.identifiedAttacks) / float(cases_heuristic.strangeEvents)) * 100.0)
        result2 = 100.0 - ((float(cases_heuristic.strangeEvents) / float(cases_heuristic.totalEvents)) * 100.0)
        print ("\n\nAccuracy (strange): " + str(result2) + " %")
        print ("Accuracy (strange + not OK): " + str(result) + " %")
        print ("Total events: " + str(cases_heuristic.totalEvents))
        print ("Strange events: " + str(cases_heuristic.strangeEvents))
        print ("Identified attack events: " + str(cases_heuristic.identifiedAttacks))
        print ("Done! Results available in: " + sys.argv[2] + "\n")
    else:
        print "Enter as arguments the name of the log file, the output file and the parser type (default | custom). " \
              "In this order."

# Execution of main method
if __name__ == '__main__':
    main()
