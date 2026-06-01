T-AIA-600-MAR_7/

README.md               -> Documentation du projet
requirements.txt        -> Dépendances Python

bookworm.py             -> Point d'entrée CLI

data/
├── books/              -> Livres téléchargés depuis Gutenberg
└── cache/              -> Résultats déjà calculés

modules/
├── lexdiv.py           -> Diversité lexicale (tok, typ, hap, ttr, mwl, mwf)
├── topics.py           -> Extraction des thèmes principaux
├── entities.py         -> Extraction personnages et lieux
├── summarize.py        -> Résumé automatique du livre
└── card.py             -> Construction de la Book Card finale

utils/
├── gutenberg.py        -> Téléchargement et chargement des livres
├── text_processing.py  -> Nettoyage, tokenisation, sections, phrases
└── cache.py            -> Sauvegarde / chargement du cache




utilisation librairie request 
=> plus simple d'ecriture, detecte l'encodage pas besoin de décoder les bytes en utf-8 contrairement à urlib, gestion erreur simplifier. Request > urlib.





















               +----------------+
               |  bookworm.py   |
               +--------+-------+
                        |
                        v
               +----------------+
               | gutenberg.py   |
               +--------+-------+
                        |
                        v
               +----------------+
               | Livre brut     |
               +--------+-------+
                        |
                        v
               +--------------------+
               | text_processing.py |
               +--------+-----------+
                        |
         +--------------+--------------+
         |              |              |
         v              v              v
 +--------------+ +-------------+ +-------------+
 |  lexdiv.py   | |  topics.py  | | entities.py |
 +--------------+ +-------------+ +-------------+
         |              |              |
         +--------------+--------------+
                        |
                        v
               +----------------+
               | summarize.py   |
               +--------+-------+
                        |
                        v
                 +------------+
                 |  card.py   |
                 +------+-----+
                        |
                        v
                 +------------+
                 | Book Card  |
                 +------------+

           (cache.py peut être utilisé
            par tous les modules)