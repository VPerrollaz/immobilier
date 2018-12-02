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
import re


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


class Annonce:
    """
    Classe pour la gestion d'une annonce. Le tag de l'annonce ayant une durée de vie limite à
    celle de la page dans le nagivateur n'est pas stocké dans l'élément.
    """

    motif = re.compile("(\d+)\sp\s(\d+)\sch\s(\d+).*")

    def __init__(self, annonce):
        self.set_id(annonce)
        self.set_genre(annonce)
        self.set_prix(annonce)
        self.set_pcs(annonce)


    def set_genre(self, annonce):
        """Affecte le style de l'annonce"""
        l = annonce.find_element_by_class_name("c-pa-link")
        self.genre = l.text


    def set_id(self, annonce):
        """Affecte l'identifiant unique de l'annonce"""
        self.id = annonce.get_attribute("id")


    def set_prix(self, annonce):
        """Affecte le prix sous la forme d'une chaine de caractères"""
        t = annonce.find_element_by_class_name("c-pa-price")
        self.prix = t.text


    def set_pcs(self, annonce):
        """Affecte pieces chambres surface"""
        c = annonce.find_element_by_class_name("c-pa-criterion")
        se = Annonce.motif.search(c.text)
        self.pieces, self.chambres, self.surface = se.groups()


    def voir_detail(self, annonce):
        """Clique le lien vers la page détaillée"""
        b = annonce.find_element_by_class_name("button")
        l = b.find_element_by_tag_name("a")
        l.click()


if __name__ == "__main__":
    nav = Session()

