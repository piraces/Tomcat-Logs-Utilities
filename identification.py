#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Class that provides an object and methods for identifying log entries and compare each one.
Considers IP address, timestamp of petition, user,
"""


class Identification(object):

    def __init__(self, ip, timestamp, user, status, case):
        self.ip = ip
        self.timestamp = timestamp
        self.user = user
        self.status = status
        # Session (initially) is a simple hash of the object
        self.session = self.get_hash()
        self.case = case

    # Getters and setters of attributes
    def set_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_session(self):
        self.session = id(self)

    def get_session(self):
        return self.session

    def set_custom_session(self, session):
        self.session = session

    def set_case(self, case):
        self.case = case

    def get_case(self):
        return self.case

    # Provides an "unique" hash for this object (considering user, IP and timestamp)
    def get_hash(self):
        # Consider using abs() function, but it increases the probability of collision
        return hash(self.user + self.ip + self.timestamp)


