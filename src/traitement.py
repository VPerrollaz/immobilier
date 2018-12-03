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
import json


motif = re.compile("(\d+)\sp\s(\d+)\sch\s(\d+).*")
def pcs_conv(pcs):
    """De la chaine pcs renvoit le triplet pièces, chambres, surface."""
    s = motif.search(pcs)
    return s.groups()


def get_genres(nom_fichier):
    """Renvoit l'ensemble de tous les genres contenu dans le fichier codé en json"""
    genres = set()
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            d = json.loads(ligne)
            genres.add(d["genre"])

    return genres




