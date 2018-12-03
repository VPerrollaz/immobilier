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


def get_genres(ds):
    """Renvoit l'ensemble des genres à partir de la liste des dictionnaires codant les
    annonces"""
    genres = set()
    for d in ds:
        genres.add(d["genre"])

    return genres


def chargement(nom_fichier):
    """Retourne la liste des dictionnaires correspondant aux annonces"""
    resultat = list()
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            resultat.append(json.loads(ligne))

    return resultat

if __name__ == "__main__":
    annonces = chargement("./donnees/brute.json")

