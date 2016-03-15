#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl Piracés Alastuey

"""
Class that provides an object and methods for identifying log entries and compare each one.
Considers IP address, timestamp of petition, user,
"""


class Identification(object):

    def __init__(self, ip, timestamp, user):
        self.ip = ip
        self.timestamp = timestamp
        self.user = user
        self.session = self.get_hash()

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

    def set_session(self):
        self.session = id(self)

    def get_session(self):
        return self.session

    def set_custom_session(self, session):
        self.session = session

    # Provides an "unique" hash for this object (considering user, IP and timestamp)
    def get_hash(self):
        # Consider using abs() function, but it increases the probability of collision
        return hash(self.user + self.ip + self.timestamp)


