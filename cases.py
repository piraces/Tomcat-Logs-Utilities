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
,["library-pending-tasks.html"]]

# Id for use case of attack or unrecognized
strange = 0

# Checks the actual event and use case, and sets the new use case.
def set_use_case(id, event):
    case = id.case
    new_case = case
    found = 0
    for thing in cases[case]:
        if thing in event:
            found = 1
    if not found:
        i = 0
        while i < 10:
            if cases[i][0] in event:
                new_case = i
                id.set_case(i)
                found = 1
            i += 1
    if not found:
        new_case = strange
        id.set_case(strange)
    return new_case
