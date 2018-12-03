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
import regex as re

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


def get_genres(annonces):
    """Retourne l'ensemble des genres."""
    resultat = set()
    for annonce in annonces:
        resultat.add(annonce["genre"])

    return resultat


def compte_genres(annonces):
    """Renvoit le nombre d'annonces par genre."""
    compteur = dict()
    for annonce in annonces:
        compteur[annonce["genre"]] = compteur.get(annonce["genre"], 0) + 1

    return compteur


def echantillon_pcs(annonces):
    """Fournit un échantillon des chaines pcs par genre"""
    resultat = dict()
    for annonce in annonces:
        if annonce["genre"] not in resultat:
            resultat[annonce["genre"]] = annonce["pcs"]

    return resultat

def nb_ligne_desc(annonce):
    return len(annonce["desc"].splitlines())


motif = re.compile("(\p{Lu}+(\s\p{Lu}+)?)", re.UNICODE)
def quartier(annonce):
    annonce["desc"], *_ = annonce["desc"].splitlines()
    return motif.findall(annonce["desc"])[0][0]


def main():
    annonces = chargement("./donnees/brute.json")
    print("Genres présents : ")
    print(get_genres(annonces))

    print("\nNombres d'annonces par genres : ")
    pprint(compte_genres(annonces))

    print("\nechantillon de la chaine pcs :")
    pprint(echantillon_pcs(annonces))


if __name__ == "__main__":
    main()
