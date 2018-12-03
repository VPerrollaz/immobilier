#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 vincent <vincent@vincent-U36SG>
#
# Distributed under terms of the MIT license.

"""
Transformation des données brutes.
"""
import re


motif = re.compile("(\d+)\sp\s(\d+)\sch\s(\d+).*")
def pcs_conv(pcs):
    """De la chaine pcs renvoit le triplet pièces, chambres, surface."""
    s = motif.search(pcs)
    return s.groups()



