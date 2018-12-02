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

class Session:
    """
    Classe permettant de parcourir le site seloger pour récupérer les annonces de la ville
    de Tours
    """
    DEPART = "https://www.seloger.com/immobilier/achat/immo-tours-37/"
    REP_INI = Path(".").resolve()

    def __init__(self):
        self.navigateur = webdriver.Firefox()
        self.navigateur.get(Session.DEPART)
        sleep(5)

    def get_annonces(self):
        """Retourne la liste des annonces dans une page"""
        return self.navigateur.find_elements_by_class_name("c-pa-list")


    def page_suivante(self):
        """Passe à la page suivante"""
        self.navigateur.find_element_by_link_text("Suivant").click()


if __name__ == "__main__":
    nav = Session()

