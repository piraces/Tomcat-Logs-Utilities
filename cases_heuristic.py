#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Class that provides use cases of BiD SID WebApp, methods that uses them,
and the heuristic of use cases.
"""

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
# 10 - Index

# Matrix of use cases and keywords of each one (H1)
cases1 = [["admin"]
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
    ,["GET /PUBLICATIONS HTTP/1",  "GET /PUBLICATIONS/ HTTP/1", "GET / HTTP/1"]]

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

# Matrix of use cases and keywords of each one (H1)
cases2 = [["admin"]
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
# 20 - Show publications directly
# 21 - Show publications in BibTeX directly
# 22 - Show publications in BibTeX directly (raw)
# 23 - Edit / Update directly

# Matrix of use cases and keywords of each one (H1)
cases3 = [["admin"]
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
    ,["GET /PUBLICATIONS HTTP/1",  "GET /PUBLICATIONS/ HTTP/1", "GET / HTTP/1"]
    ,["library-show-publications.jsp", "library-show-publications-bibtex.jsp",
      "library-show-publications-raw-bibtex.jsp", "library-edit-configuration.jsp", "library-save-configuration.jsp",
      "library-edit-reference.jsp", "library-update-db.jsp"]
    ,["library-show-publications-bibtex.jsp"]
    ,["library-show-publications-raw-bibtex.jsp"]
    ,["library-edit-reference.jsp", "library-update-db.jsp"]]

# Id for use case of attack or unrecognized
strange = 0

# Id for use case of index
indexH1 = 10
index = 19

# Number of events (total)
totalEvents = 0

# Number of events (strange)
strangeEvents = 0

# Number of events (strange & not 200)
identifiedAttacks = 0

# Name for strange events file
eventsFile = "strange.txt"

# Checks the actual event and use case, and sets the new use case. Based on H1 heuristic.
# H1 heuristic checks the "entrypoint" of use cases to determine a new use case, and a list of common use case pages to
# check the current use case.
def set_use_case_h1(id, event):
    case = id.case
    new_case = case
    found = 0
    for thing in cases1[case]:
        if thing in event:
            found = 1
    if not found:
        i = 0
        while i < 11:
            if cases1[i][0] in event:
                new_case = i
                id.set_case(i)
                found = 1
            i += 1
    if not found:
        if cases1[indexH1][0] in event or cases1[indexH1][1] in event or cases1[indexH1][2] in event:
            new_case = indexH1
            id.set_case(indexH1)
        else:
            new_case = strange
            id.set_case(strange)
            # Logs event to test the efficiency of the heuristic
            write_strange_behaviour(id.ip + " || " + id.timestamp + " || " + event + " || " + id.status)
            global strangeEvents
            strangeEvents += 1
            if id.status != '200':
                global identifiedAttacks
                identifiedAttacks += 1
    global totalEvents
    totalEvents += 1
    return new_case

# Checks the actual event and use case, and sets the new use case. Based on H2 heuristic.
# H2 heuristic checks the "entrypoint" of use cases to determine a new use case, and a list of common use case pages to
# check the current use case. Furthermore, it considers static behaviors.
def set_use_case_h2(id, event):
    case = id.case
    new_case = case
    found = 0
    for thing in cases2[case]:
        if thing in event:
            found = 1
    if not found:
        i = 0
        while i < 20:
            if cases2[i][0] in event:
                new_case = i
                id.set_case(i)
                found = 1
            i += 1
    if not found:
        if cases2[index][0] in event or cases2[index][1] in event or cases2[index][2] in event:
            new_case = index
            id.set_case(index)
        else:
            new_case = strange
            id.set_case(strange)
            # Logs event to test the efficiency of the heuristic
            write_strange_behaviour(id.ip + " || " + id.timestamp + " || " + event + " || " + id.status)
            global strangeEvents
            strangeEvents += 1
            if id.status != '200':
                global identifiedAttacks
                identifiedAttacks += 1
    global totalEvents
    totalEvents += 1
    return new_case

# Checks the actual event and use case, and sets the new use case. Based on H3 heuristic.
# H3 heuristic checks the "entrypoint" of use cases to determine a new use case, and a list of common use case pages to
# check the current use case. Furthermore, it considers extra behaviors (from bots and other strange and correct cases).
def set_use_case_h3(id, event):
    case = id.case
    new_case = case
    found = 0
    for thing in cases3[case]:
        if thing in event:
            found = 1
    if not found:
        i = 0
        while i < 24:
            if cases3[i][0] in event:
                new_case = i
                id.set_case(i)
                found = 1
            i += 1
    if not found:
        if cases3[index][0] in event or cases3[index][1] in event or cases3[index][2] in event:
            new_case = index
            id.set_case(index)
        else:
            new_case = strange
            id.set_case(strange)
            # Logs event to test the efficiency of the heuristic
            write_strange_behaviour(id.ip + " || " + id.timestamp + " || " + event + " || " + id.status)
            global strangeEvents
            strangeEvents += 1
            if id.status != '200':
                global identifiedAttacks
                identifiedAttacks += 1
    global totalEvents
    totalEvents += 1
    return new_case

# Writes in an output info file, the strange events detected in heuristics (for posterior analysis)
def write_strange_behaviour(event):
    # Open a file, for writing appending lines
    fo = open(eventsFile, "ab")
    fo.write(event + "\n")
    # Close opened file
    fo.close()
