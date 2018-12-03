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


valides = {"Appartement" : ("Appartement", 0),
          "Maison / Villa" : ("Maison", 0),
          "Appartement neuf" : ("Appartement", 1),
          "Maison / Villa neuve" : ("Maison", 1)}


def filtre_logement(annonce):
    """Ne garde que les logements"""
    return annonce["genre"] in valides


def transformation_logement(annonce):
    """Assainit l'entrée genre en ajoutant une entrée Neuf"""
    annonce["genre"], annonce["Neuf"] = valides[annonce["genre"]]
    return annonce


surface = re.compile("(\d+(,\d+)?)\s?m")
pieces = re.compile("(\d+)\sp")
def transformation_pcs(annonce):
    """De la chaine pcs renvoit le triplet pièces, chambres, surface."""
    pcs = annonce["pcs"]
    res = surface.search(pcs)
    try:
        annonce["Surface"] = float(res.group().replace(",",".")[:-2])
    except:
        annonce["Surface"] = "NaN"

    res = pieces.search(pcs)
    try:
        annonce["Nombre_pieces"] = int(res.group()[:-2])
    except:
        annonce["Nombre_pieces"] = "NaN"
    annonce.pop("pcs", None)
    return annonce


def main():
    totalites = chargement("./donnees/brute.json")
    logements = (transformation_logement(annonce) for annonce in totalites 
                 if filtre_logement(annonce))
    avec_pc = (transformation_pcs(annonce) for annonce in logements)
    return avec_pc


if __name__ == "__main__":
    annonces = list(main())

