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
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
from pathlib import Path
import json


class Session:
    """
    Classe permettant de parcourir le site seloger pour récupérer les annonces de la ville
    de Tours
    """

    def __init__(self, depart):
        self.navigateur = webdriver.Firefox()
        self.navigateur.get(depart)
        sleep(5)

    def traitement_page_courante(self, path):
        """sauvegarde les annonces dans le fichier fournit par path au format json, renvoit la
        durée d'exécution""" 
        debut = time()
        with open(path, 'a') as f:
            for a in self.navigateur.find_elements_by_class_name("c-pa-list"):
                ann = Annonce(a)
                f.write(ann.to_json())

        return time() - debut


    def page_suivante(self):
        """Passe à la page suivante"""
        self.navigateur.find_element_by_link_text("Suivant").click()


class Annonce:
    """
    Classe pour la gestion d'une annonce. Le tag de l'annonce ayant une durée de vie limite à
    celle de la page dans le nagivateur n'est pas stocké dans l'élément.
    """

    def __init__(self, annonce):
        self.set_id(annonce)
        self.set_genre(annonce)
        self.set_prix(annonce)
        self.set_pcs(annonce)
        self.set_desc(annonce)
        self.set_lien(annonce)


    def __str__(self):
        return f"""
id          : {self.id}
genre       : {self.genre}
pcs         : {self.pcs}
lien        : {self.lien}
prix        : {self.prix}
description : {self.desc}
"""


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
        self.pcs = c.text


    def set_desc(self, annonce):
        """Récupère la description"""
        d = annonce.find_element_by_class_name("description")
        self.desc = d.text


    def set_lien(self, annonce):
        """Affecte le lien vers la page détaillée"""
        b = annonce.find_element_by_class_name("button")
        l = b.find_element_by_tag_name("a")
        self.lien = l.get_attribute("href")
        # l.click si jamais on veut le détail

    
    def to_json(self):
        """Renvoit une chaine pour stocker le résultat en json."""
        return json.dumps(self.__dict__)


def main():
    depart = "https://www.seloger.com/immobilier/achat/immo-tours-37/"
    fichier = Path(".").resolve() / "sauvegarde/res.json"
    nav = Session(depart)
    while True:
        duree = nav.traitement_page_courante(fichier)
        print("page {} traitée".format(nav.navigateur.current_url))
        if duree < 5:
            sleep(6 - int(duree))
        try:
            nav.page_suivante()
        except NoSuchElementException:
            break
        sleep(5)
    nav.navigateur.quit()


if __name__ == "__main__":
    main()
