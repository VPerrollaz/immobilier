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
ROOT = Path(".").resolve()

def main():
    navigateur = webdriver.Firefox()
    navigateur.get(DEPART)
    sleep(5)
    fichier_courant = ROOT / "sauvegarde" / "test.html"
    fichier_courant.write_text(navigateur.page_source)



if __name__ == "__main__":
    main()

