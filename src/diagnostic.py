#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 vincent <vincent@vincent-U36SG>
#
# Distributed under terms of the MIT license.

"""
Fonctions pour diagnostiquer les données brutes.
"""
import json


def chargement(nom_fichier):
    """Retourne la liste des dictionnaires correspondant aux annonces"""
    resultat = list()
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            resultat.append(json.loads(ligne))

    return resultat


def compte_genres(ds):
    """Renvoit le nombre d'annonces par genre."""
    compteur = dict()
    for d in ds:
        compteur[d["genre"]] = compteur.get(d["genre"], 0) + 1

    return compteur


if __name__ == "__main__":
    annonces = chargement("./donnees/brute.json")
