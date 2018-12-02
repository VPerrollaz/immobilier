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

DEPART = "https://www.seloger.com/immobilier/achat/immo-tours-37/"


def main():
    navigateur = webdriver.Firefox()
    navigateur.get(DEPART)
    sleep(3)
    with open("sauvegarde/root.html", "w") as f:
        f.write(navigateur.page_source)


if __name__ == "__main__":
    main()


