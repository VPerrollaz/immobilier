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

def chargement(nom_fichier):
    """Retourne la liste des dictionnaires correspondant aux annonces"""
    resultat = list()
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            resultat.append(json.loads(ligne))

    return resultat


def filtre_logement(annonces):
    """Ne garde que les maisons et appartements et assénit l'entrée genre en ajoutant une
    entrée neuf"""
    resultat = list()
    valide = {"Appartement" : ("Appartement", False),
              "Maison / Villa" : ("Maison", False),
              "Appartement neuf" : ("Appartement", True),
              "Maison / Villa neuve" : ("Maison", True)}
    for annonce in annonces:
        if annonce["genre"] in valide: 
            annonce["genre"], annonce["Neuf"] = valide[annonce["genre"]]
            resultat.append(annonce)

    return resultat


motif = re.compile("(\d+)\sp\s(\d+)\sch\s(\d+).*")
def pcs_conv(pcs):
    """De la chaine pcs renvoit le triplet pièces, chambres, surface."""
    s = motif.search(pcs)
    return s.groups()


def main():
    totalites = chargement("./donnees/brute.json")
    pertinentes = filtre_logement(totalites)
    return pertinentes

if __name__ == "__main__":
    annonces = main()
    print(len(annonces))


