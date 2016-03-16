#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Class that provides use cases of BiD SID WebApp, methods that uses them,
and the heuristic of use cases.
"""

from heuristic import Identification

# Entrypoints and intermediate keywords of use cases, by order of main menu

# 0 - Default entrypoint
case0 = ["/PUBLICATIONS"]
# 1 - Quick search
case1 = ["library-quick-search.jsp", "/attachedFiles/", "library-error.jsp"]
# 2 - Advanced search
case2 = ["library-advanced-search.jsp", "library-show-publications.jsp", "library-show-publications-bibtex.jsp",
         "/attachedFiles/", "library-show-publications-raw-bibtex.jsp", "library-error.jsp"]
# 3 - Build bibtex
case3 = ["library-build-bibtex.jsp"]
# 4 - Get all entries in bibtex
case4 = ["library-show-publications-bibtex.jsp?id=*"]
# 5 - Edit entries
case5 = ["library-edit-search.jsp", "library-show-publications.jsp", "library-show-publications-bibtex.jsp",
         "library-edit-reference.jsp", "library-update-db.jsp", "library-show-publications-raw-bibtex.jsp",
         "library-edit-configuration.jsp", "library-save-configuration.jsp", "library-error.jsp"]
# 6 - Considering both options of inserting as same use case
case6 = ["library-edit-reference.jsp?mode=insert", "library-update-db.jsp", "library-show-publications.jsp",
         "library-show-publications-bibtex.jsp", "library-edit-configuration.jsp", "library-save-configuration.jsp",
         "library-show-publications-raw-bibtex.jsp", "library-edit-reference.jsp", "library-error.jsp"]
# Extra 'static' use cases
# 7 - Help of the library
case7 = ["library-help.html"]
# 8 - Pending tasks of the library
case8 = ["library-pending-tasks.html"]

# 9 -> Attacks or bad/strange requests

# Checks the actual event and use case, and sets the new use case.
def set_use_case(id, event):
    case = id.case
    new_case = case
    changed = 0
    if any(event in case0 for event in case0):
        if case == 0 or (event in case0[0]):
            id.set_case(0)
            new_case = 0
            changed = 1
    if any(event in case1 for event in case1):
        if case == 1 or (event in case1[0]):
            id.set_case(1)
            new_case = 1
            changed = 1
    if any(event in case2 for event in case2):
        if case == 2 or (event in case2[0]):
            id.set_case(2)
            new_case = 2
            changed = 1
    if any(event in case3 for event in case3):
        if case == 3 or (event in case3[0]):
            id.set_case(3)
            new_case = 3
            changed = 1
    if any(event in case4 for event in case4):
        if case == 4 or (event in case4[0]):
            id.set_case(4)
            new_case = 4
            changed = 1
    if any(event in case5 for event in case5):
        if case == 5 or (event in case5[0]):
            id.set_case(5)
            new_case = 5
            changed = 1
    if any(event in case6 for event in case6):
        if case == 6 or (event in case6[0]):
            id.set_case(6)
            new_case = 6
            changed = 1
    if any(event in case7 for event in case7):
        if case == 7 or (event in case7[0]):
            id.set_case(7)
            new_case = 7
            changed = 1
    if any(event in case8 for event in case8):
        if case == 8 or (event in case8[0]):
            id.set_case(8)
            changed = 1
    if not changed:
        id.set_case(9)
    return new_case
