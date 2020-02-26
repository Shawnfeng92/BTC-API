# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 8:44:31 2020

@author: Shawn
"""


from datetime import datetime


def isotoepochms(t8601="2020-02-02T18:56:01.785Z"):
    if len(t8601) > 20:
        t8601 = datetime.strptime(t8601, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        t8601 = datetime.strptime(t8601, "%Y-%m-%dT%H:%M:%SZ")

    delta = t8601 - datetime(1970, 1, 1)
    return int(delta.total_seconds()) * 1000 + int(delta.microseconds / 1000)


def epochmstoiso(timestamp=1582335222):
    return datetime.utcfromtimestamp(timestamp / 1000).isoformat()[:-3] + "Z"
