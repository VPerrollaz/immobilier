#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 vincent <vincent@vincent-U36SG>
#
# Distributed under terms of the MIT license.

"""
Fonctions pour la création du jeu de données.
"""

from selenium import webdriver
from time import sleep
from pathlib import Path

DEPART = "https://www.seloger.com/immobilier/achat/immo-tours-37/"
REP_INI = Path(".").resolve()

def get_annonces(navigateur):
    """Retourne la liste des annonces dans une page"""
    liste = navigateur.find_elements_by_class_name("c-pa-list")
    return liste


def get_page_suivante(navigateur):
    """Retourne le tag pour passer à la page suivante."""
    return navigateur.find_element_by_link_text("Suivant")


def lancement():
    navigateur = webdriver.Firefox()
    navigateur.get(DEPART)
    sleep(5)
    return navigateur


if __name__ == "__main__":
    nav = lancement()

