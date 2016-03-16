#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Class that provides use cases of BiD SID WebApp, methods that uses them,
and the heuristic of use cases.
"""

# Entrypoints of use cases by order of main menu
case1 = "library-quick-search.jsp"
case2 = "library-advanced-search.jsp"
case3 = "library-build-bibtex.jsp"
case4 = "library-show-publications-bibtex.jsp?id=*"
case5 = "library-edit-search.jsp"
# Considering both options of inserting as same use case
case6 = "library-edit-reference.jsp?mode=insert"
# Extra 'static' use cases
case7 = "library-help.html"
case8 = "library-pending-tasks.html"