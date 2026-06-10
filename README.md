# Alice In Wonderland - Bookworm

Projet T-AIA-600-MAR_7.

Bookworm est un outil CLI qui analyse des livres depuis Project Gutenberg pour produire des informations utiles sous forme de "book card".

Le but du projet est de transformer un texte brut en informations structurées :

- diversité lexicale
- topics par section
- personnages et lieux
- résumé court
- similarité entre livres
- fiche finale du livre

## Structure du projet

```text
README.md               -> Documentation du projet
requirements.txt        -> Dépendances Python
bookworm.py             -> Point d'entrée CLI

data/
├── books/              -> Livres téléchargés depuis Gutenberg
└── cache/              -> Résultats déjà calculés

modules/
├── lexdiv.py           -> Diversité lexicale
├── topics.py           -> Extraction des thèmes principaux
├── entities.py         -> Extraction personnages et lieux
├── summarize.py        -> Résumé du livre
├── similarity.py       -> Similarité entre livres
└── card.py             -> Construction de la Book Card finale

utils/
├── gutenberg.py        -> Téléchargement et chargement des livres
├── text_processing.py  -> Nettoyage, tokenisation, sections, phrases
└── cache.py            -> Sauvegarde / chargement du cache
```

## Installation

Créer et activer l'environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Le modèle anglais de SpaCy est nécessaire pour la reconnaissance d'entités :

```bash
python -m spacy download en_core_web_sm
```

Le modèle est aussi listé dans `requirements.txt` via son URL, mais la commande ci-dessus reste utile à connaître et à documenter.

## Utilisation

Afficher l'aide :

```bash
python3 bookworm.py --help
```

Diversité lexicale :

```bash
python3 bookworm.py --lexdiv 11
```

Topics :

```bash
python3 bookworm.py --topics 11
```

Entités :

```bash
python3 bookworm.py --entities 11
```

Résumé :

```bash
python3 bookworm.py --summarize 11
```

## Cache

Le projet utilise deux niveaux de cache.

`data/books/` stocke les textes des livres déjà téléchargés.  
Cela évite de refaire une requête à Project Gutenberg à chaque commande.

`data/cache/` stocke les résultats déjà calculés, par exemple :

```text
1_lexdiv.json
2_topics_v2.json
11_summary_hybrid_v3.json
```

Cela évite de recalculer des traitements plus coûteux comme les topics, les entités ou le résumé.

## Choix techniques

### Requests

`requests` est utilisé pour télécharger les livres depuis Project Gutenberg.

Pourquoi :

- écriture plus simple que `urllib`
- gestion des erreurs HTTP avec `raise_for_status()`
- détection de l'encodage plus pratique

### Pathlib

`pathlib` est utilisé pour gérer les chemins de fichiers.

Pourquoi :

- plus lisible que construire des chemins avec des chaînes
- facilite la création de chemins comme `data/books/11.txt`

### sys.argv

Le projet utilise `sys.argv` pour lire les options CLI.

Pourquoi :

- solution native Python
- simple pour comprendre le fonctionnement d'une ligne de commande
- suffisant pour une première version du projet

Limite :

- `argparse` serait plus propre pour gérer automatiquement l'aide, les erreurs et les options

## Lexical diversity

La commande `--lexdiv <ID>` retourne :

```python
{
    "tok": int,
    "typ": int,
    "hap": int,
    "ttr": float,
    "mwl": float,
    "mwf": float
}
```

Méthode :

- `tok` : nombre total de mots
- `typ` : nombre de mots uniques
- `hap` : mots qui apparaissent une seule fois
- `ttr` : mots uniques / mots totaux
- `mwl` : longueur moyenne des mots
- `mwf` : fréquence moyenne des mots

## Topics

La commande `--topics <ID>` retourne :

```python
{1: list[str], 2: list[str], ...}
```

Méthode choisie : TF-IDF avec Scikit-learn.

TF-IDF signifie `Term Frequency - Inverse Document Frequency`.

L'idée :

- un mot est important s'il apparaît souvent dans une section
- mais il est moins important s'il apparaît dans toutes les sections

Pourquoi Scikit-learn :

- fournit `TfidfVectorizer`
- fiable et utilisé en NLP classique
- plus pertinent qu'un simple compteur de mots

Pourquoi pas seulement `Counter` :

- `Counter` donne les mots les plus fréquents
- mais un mot fréquent n'est pas forcément représentatif
- TF-IDF donne des mots plus spécifiques à chaque section

Découpage :

- si le livre contient des chapitres avec le pattern `CHAPTER I`, `CHAPTER II`, etc., ces chapitres sont utilisés comme sections
- sinon le texte est découpé artificiellement en 4 sections

## Entities

La commande `--entities <ID>` retourne :

```python
{
    "characters": list[str],
    "locations": list[str]
}
```

Méthode choisie : SpaCy + Counter.

SpaCy détecte les entités nommées du texte.

On garde :

- `PERSON` pour les personnages
- `GPE` et `LOC` pour les lieux

`Counter` permet :

- de supprimer les doublons
- de trier les entités par fréquence

Limite :

- SpaCy peut faire des erreurs sur les textes littéraires
- certains titres ou mots peuvent être mal classés comme personnages ou lieux

## en_core_web_sm

`en_core_web_sm` est le modèle anglais utilisé par SpaCy.

SpaCy est la bibliothèque, mais le modèle contient les données entraînées pour reconnaître :

- `PERSON`
- `GPE`
- `LOC`
- autres labels d'entités

Sans ce modèle, cette ligne ne peut pas fonctionner :

```python
spacy.load("en_core_web_sm")
```

## Click

`click` est une dépendance utilisée par SpaCy/Typer pour certaines commandes internes.

Le projet ne l'utilise pas directement, mais SpaCy en a besoin dans notre environnement.

Sans `click`, l'import de SpaCy peut provoquer :

```text
ModuleNotFoundError: No module named 'click'
```

## Summarize

La commande `--summarize <ID>` retourne une chaîne courte de quelques phrases.

Nous avons testé deux méthodes.

### Méthode 1 : résumé extractif

Principe :

- découper le texte en phrases
- compter les mots importants
- donner un score à chaque phrase
- sélectionner les meilleures phrases

Problème rencontré :

- les phrases Gutenberg peuvent être très longues
- certains blocs contiennent des citations, poèmes ou dialogues
- le résumé obtenu était trop long et parfois imprécis
- la méthode ne reformule pas et ne comprend pas vraiment le sens

Conclusion :

Cette méthode était légère et conforme aux contraintes, mais le résultat était trop imprécis pour notre usage.

### Méthode 2 : résumé hybride par template

Méthode retenue.

Principe :

- utiliser les personnages trouvés par `entities`
- utiliser les lieux trouvés par `entities`
- utiliser les mots importants trouvés par `topics`
- générer un court texte en 3 phrases

Exemple :

```text
This book focuses on Alice, Hatter, and Mouse.
Important locations include King, Duchess, and Dinah.
Main topics include alice, said, little, rabbit, and queen.
```

Pourquoi ce choix :

- très léger
- pas de modèle lourd
- pas d'API
- résultat court et stable
- adapté à une description de catalogue ou de book card

Limite :

- ce n'est pas un résumé narratif complet
- il ne raconte pas toute l'intrigue
- la qualité dépend de `topics` et `entities`

## Schéma général

```text
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

           cache.py peut être utilisé
           par tous les modules
```

## Limites actuelles

- `--similar` n'est pas encore terminé
- `--card` n'est pas encore terminé
- les entités peuvent contenir des faux positifs
- les topics dépendent beaucoup de la qualité du découpage en sections
- le résumé hybride est une description courte, pas un résumé narratif détaillé
