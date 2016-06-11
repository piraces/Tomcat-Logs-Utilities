# Tomcat Logs Utilities

This repository contains an extensible Python script, for parsing Apache Tomcat logs with several purposes.

This tool has been used for tests with ["Process Mining for Security" metodology](http://sid.cps.unizar.es/PMS/).

## Functions

This pre-processing tool, allows to do the following with Tomcat Web server (access) logs:
  - Convert raw logs to csv, with custom or default header (obtained from Tomcat logging configuration).
  - Apply a session heuristic to determine different sessions in given log, if these are not present.
  - Apply multiple use cases heuristics to determine the possibles use cases given in a session.

The tool, does also this tasks in background:
  - Search and remove bad characters from raw logs.
  - Register (output to one file) "strange" events identified in the pre-processing of logs.
  - Choosing and applying the desired delimiter for resultant CSV file.
  - Extract statistics from the pre-processing process.

The main purpose of the tool is the validation of heuristics proposed in ["Process Mining for Security" metodology](http://sid.cps.unizar.es/PMS/), and for allowing to do several process mining tasks from raw Tomcat logs.

## Important Notes

Note that the use cases heuristics, only works on custom system logs, their have to be changed to pre-process diferent web information systems. To do these changes, you'll have to modify "cases" and "paths" arrays in cases_heuristic.py, to reflect the main behaviour of your web information system.

Also, if you want to use a custom header, you'll have to modify the global variables in parser.py.

## Installation

This tool requires [Python 2.x](https://www.python.org) to run. It does not work with Python 3.

It does not require additional packages.

## Execution
Execution has to follow the format: python parser.py inputFile outputFile (default|custom) [heuristicName].

An example of use, could be the following:
```sh
$ python parser.py log.txt output.csv default h1_3
```

The above example, will take "log.txt", pre-process it, apply specified heuristic (and session heuristic), and output the CSV needed for following tasks.

## Available heuristics

**The list of available heuristics is the following:** h1_0, h1_1, h1_2, h1_3, h2.

- **H1_x** heuristics, checks the "entrypoint" of use cases to determine a new use case, and a list of common use case pages to check the current use case. Different versions are provided, with different levels of "granularity" (extra behaviors detected).
- **H2** heuristic, checks the longest path possible of use cases to determine a new use case, and a list of common use case pages to check the current use case. Furthermore, it considers extra behaviors (from bots and other strange and correct cases).


License
----

GPLv3


