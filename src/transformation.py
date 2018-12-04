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
import regex as re
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


liste_quartiers = ["prébendes", "beaujardin", "conservatoire", "cathédrale", 
        "fontaines", "2 lions", "halles", "heurteloup", "rotonde", "cher", "velpeau",
        "strasbourg", "paul bert", "febvotte", "eloi", "tranchée", "montjoyeux", "gare",
        "michelet"  "rabelais", "mairie", "portes", "cluzel", "béranger", "radegonde", "sud",
        "nord", "centre"]
def transformation_desc(annonce):
    """On garde la première de la description et on cherche des mots clefs pour les quartiers"""
    annonce["desc"] = annonce["desc"].splitlines()[0]
    if len(annonce["Quartier"]) > 0:
        return annonce
    en_minuscule = annonce["desc"].lower() 
    for quartier in liste_quartiers:
        if quartier in en_minuscule:
            annonce["Quartier"].append(quartier)

    if annonce["Quartier"] == []:
        annonce["Quartier"] = "NaN"
    else:
        annonce["Quartier"] = annonce["Quartier"][0]
    return annonce


motif = re.compile("tours-?37/([a-z])/.*")
def transformation_lien(annonce):
    """Utilisation du lien pour identifier certains quartiers"""
    res = motif.search(annonce["lien"])
    annonce["Quartier"] = []
    try:
        qu, *_ = res.groups()
    except AttributeError:
        pass
    else:
        annonce["Quartier"].append(qu)
    return annonce

def transformation_prix(annonce):
    """Conversion du prix en entier"""
    try:
        annonce["prix"] = int(re.sub("\D","",annonce["prix"]))
    except ValueError:
        annonce["prix"] = "NaN"
    return annonce

def suppression_lien_desc(annonce):
    """Enlevement des clefs inutiles"""
    annonce.pop("desc", None)
    annonce.pop("lien", None)
    return annonce

def main():
    totalites = chargement("./donnees/brute.json")
    mod_prix = (transformation_prix(annonce) for annonce in totalites)
    logements = (transformation_logement(annonce) for annonce in mod_prix 
                 if filtre_logement(annonce))
    avec_pc = (transformation_pcs(annonce) for annonce in logements)
    avec_quartiers = (transformation_lien(annonce) for annonce in avec_pc)
    avec_quartiers_bis = (transformation_desc(annonce) for annonce in avec_quartiers)
    return (suppression_lien_desc(annonce) for annonce in avec_quartiers_bis)


if __name__ == "__main__":
    annonces = list(main())
    with open("./donnees/data.csv", "w") as fichier:
        fichier.write("Id ; Genre ; Neuf ; Surface ; Pieces ; Quartier ; Prix\n")
        for ann in annonces:
            fichier.write("{id} ; {genre} ; {Neuf}; {Surface}; {Nombre_pieces} ; {Quartier} ; {prix}\n".format(**ann))
