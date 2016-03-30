#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Class that provides use cases of BiD SID WebApp, methods that uses them,
and the heuristic of use cases.
"""

# Entrypoints and intermediate keywords of use cases, by order of main menu

# 0 - Attacks or bad/strange requests
# 1 - Quick search
# 2 - Advanced search
# 3 - Build bibtex
# 4 - Get all entries in bibtex
# 5 - Edit entries
# 6 - Insert view fields
# 7 - Insert view bibtex
# Extra 'static' use cases
# 8 - Help of the library
# 9 - Pending tasks of the library
# 10 - Images
# 11 - Styles
# 12 - JavaScript files
# 13 - Applets
# 14 - Patches
# 15 - Config
# 16 - Attached Files
# 17 - Robots
# 18 - Favicon
# 19 - Index

'''
cases = [["library-quick-search.jsp", "/attachedFiles/", "library-error.jsp"]
,["library-advanced-search.jsp", "library-show-publications.jsp", "library-show-publications-bibtex.jsp",
         "/attachedFiles/", "library-show-publications-raw-bibtex.jsp", "library-error.jsp"]
,["library-build-bibtex.jsp"]
,["library-show-publications-bibtex.jsp?id=*"]
,["library-edit-search.jsp", "library-show-publications.jsp", "library-show-publications-bibtex.jsp",
         "library-edit-reference.jsp", "library-update-db.jsp", "library-show-publications-raw-bibtex.jsp",
         "library-edit-configuration.jsp", "library-save-configuration.jsp", "library-error.jsp"]
,["library-edit-reference.jsp?mode=insert", "library-update-db.jsp", "library-show-publications.jsp",
         "library-show-publications-bibtex.jsp", "library-edit-configuration.jsp", "library-save-configuration.jsp",
         "library-show-publications-raw-bibtex.jsp", "library-edit-reference.jsp", "library-error.jsp"]
,["library-help.html"]
,["library-pending-tasks.html"]]
'''

# Matrix of use cases and keywords of each one
cases = [["admin"]
,["library-quick-search.jsp", "/attachedFiles/", "library-error.jsp"]
,["library-advanced-search.jsp", "library-show-publications.jsp", "library-show-publications-bibtex.jsp",
         "/attachedFiles/", "library-show-publications-raw-bibtex.jsp", "library-error.jsp"]
,["library-build-bibtex.jsp"]
,["library-show-publications-bibtex.jsp?id=*"]
,["library-edit-search.jsp", "library-show-publications.jsp", "library-show-publications-bibtex.jsp",
         "library-edit-reference.jsp?id=", "library-update-db.jsp", "library-show-publications-raw-bibtex.jsp",
         "library-edit-configuration.jsp", "library-save-configuration.jsp", "library-error.jsp"]
,["library-edit-reference.jsp?mode=insert&view=field", "library-update-db.jsp", "library-show-publications.jsp",
         "library-show-publications-bibtex.jsp", "library-edit-configuration.jsp", "library-save-configuration.jsp",
         "library-show-publications-raw-bibtex.jsp", "library-edit-reference.jsp?id=", "library-error.jsp",
         "library-edit-reference.jsp?idOld="]
,["library-edit-reference.jsp?mode=insert&view=bibtex", "library-update-db.jsp", "library-show-publications.jsp",
         "library-show-publications-bibtex.jsp", "library-edit-configuration.jsp", "library-save-configuration.jsp",
         "library-show-publications-raw-bibtex.jsp", "library-edit-reference.jsp?id=", "library-error.jsp",
         "library-edit-reference.jsp?idOld="]
,["library-help.html"]
,["library-pending-tasks.html"]
,["/images/"]
,["/styles/"]
,["/scripts/"]
,["/applets/"]
,["/PATCHES/"]
,["/config/"]
,["/attachedFiles"]
,["/robots.txt"]
,["/favicon.ico"]
,["GET /PUBLICATIONS HTTP/1",  "GET /PUBLICATIONS/ HTTP/1", "GET / HTTP/1"]]

# Id for use case of attack or unrecognized
strange = 0

# Id for use case of index
index = 19

# Name for strange events file
eventsFile = "strange.txt"

# Checks the actual event and use case, and sets the new use case. Based on H1 heuristic.
# H1 heuristic checks the "entrypoint" of use cases to determine a new use case, and a list of common use case pages to
# check the current use case.
def set_use_case_h1(id, event):
    case = id.case
    new_case = case
    found = 0
    for thing in cases[case]:
        if thing in event:
            found = 1
    if not found:
        i = 0
        while i < 20:
            if cases[i][0] in event:
                new_case = i
                id.set_case(i)
                found = 1
            i += 1
    if not found:
        if cases[index][0] in event or cases[index][1] in event or cases[index][2] in event:
            new_case = index
            id.set_case(index)
        else:
            new_case = strange
            id.set_case(strange)
            # Logs event to test the efficiency of the heuristic
            write_strange_behaviour(id.ip + " || " + id.timestamp + " || " + event + " || " + id.status)
    return new_case

# Writes in an output info file, the strange events detected in heuristics (for posterior analysis)
def write_strange_behaviour(event):
    # Open a file, for writing appending lines
    fo = open(eventsFile, "ab")
    fo.write(event + "\n")
    # Close opened file
    fo.close()
