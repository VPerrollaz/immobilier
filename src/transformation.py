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


def pprint(dico):
    """Affichage espacé d'un dictionnaire"""
    for clef in dico:
        print("{} : {}".format(clef, dico[clef]))


def chargement(nom_fichier):
    """Retourne la liste des dictionnaires correspondant aux annonces"""
    resultat = list()
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            resultat.append(json.loads(ligne))

    return resultat


def filtre_logement(annonce):
    """Ne garde que les maisons et appartements et assénit l'entrée genre en ajoutant une
    entrée neuf"""
    valide = {"Appartement" : ("Appartement", False),
              "Maison / Villa" : ("Maison", False),
              "Appartement neuf" : ("Appartement", True),
              "Maison / Villa neuve" : ("Maison", True)}
    if annonce["genre"] in valide: 
        annonce["genre"], annonce["Neuf"] = valide[annonce["genre"]]

    return annonce


motif_ancien = re.compile("(\d+)\sp\s(\d+)\sch\s(\d+).*")
motif_neuf = re.compile("(\d+)\sp\s(\d+)\sm.*")
def filtre_pcs(annonce):
    """De la chaine pcs renvoit le triplet pièces, chambres, surface."""
    if annonce["Neuf"]:
        s = motif_neuf.search(annonce["pcs"])
        nb_pieces, surface = s.groups()
    else:
        s = motif_ancien.search(annonce["pcs"])
        nb_pieces, _, surface = s.groups()

    annonce["Surface"] = int(surface)
    annonce["Nombre_pieces"] = int(nb_pieces)
    return annonce


def main():
    totalites = chargement("./donnees/brute.json")
    logements = (filtre_logement(annonce) for annonce in totalites)
    avec_pc = (filtre_pcs(annonce) for annonce in logements)
    return avec_pc


if __name__ == "__main__":
    annonces = list(main())

