# Alice In Wonderland - Bookworm

Projet T-AIA-600-MAR_7.

Bookworm est un outil en ligne de commande qui analyse des livres venant de Project Gutenberg et produit des informations structurees sous forme de "book card".

L'objectif est de transformer un texte brut en informations utiles :

- diversite lexicale ;
- mots importants par section ;
- personnages et lieux ;
- resume court ;
- livres similaires ;
- fiche finale du livre.

## Installation

Creer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dependances :

```bash
pip install -r requirements.txt
```

Le modele anglais SpaCy est necessaire pour la reconnaissance d'entites :

```bash
python -m spacy download en_core_web_sm
```

Le modele est aussi present dans `requirements.txt` via son URL.

## Utilisation

Afficher l'aide :

```bash
python3 bookworm.py --help
```

Calculer la diversite lexicale :

```bash
python3 bookworm.py --lexdiv 11
```

Extraire les mots importants par section :

```bash
python3 bookworm.py --topics 11
```

Extraire les personnages et lieux :

```bash
python3 bookworm.py --entities 11
```

Generer un resume :

```bash
python3 bookworm.py --summarize 11
```

Trouver les livres similaires :

```bash
python3 bookworm.py --similar 11
```

Generer la book card complete :

```bash
python3 bookworm.py --card 11
```

## Structure Du Projet

```text
README.md               -> Documentation du projet
requirements.txt        -> Dependances Python
bookworm.py             -> Point d'entree CLI

data/
├── books/              -> Livres telecharges depuis Project Gutenberg
└── cache/              -> Resultats sauvegardes

modules/
├── lexdiv.py           -> Diversite lexicale
├── topics.py           -> Mots importants par section
├── entities.py         -> Personnages et lieux
├── summarize.py        -> Resume court
├── similarity.py       -> Similarite entre livres
└── card.py             -> Construction de la book card

utils/
├── gutenberg.py        -> Telechargement et chargement des livres
├── text_processing.py  -> Nettoyage et decoupage du texte
└── cache.py            -> Gestion du cache JSON
```

## Fonctionnement General

```text
bookworm.py
    |
    v
load_book(book_id)
    |
    v
remove_header_footer(text)
    |
    +--> lexdiv
    +--> topics
    +--> entities
    +--> summarize
    +--> similarity
    |
    v
card
```

`bookworm.py` lit l'option CLI avec `sys.argv`, charge le livre, nettoie le texte et appelle le module correspondant.

Les traitements couteux sont sauvegardes dans `data/cache/` pour eviter de recalculer les memes resultats.

## `bookworm.py`

`bookworm.py` est le point d'entree du projet.

Il gere :

- la lecture de l'option CLI ;
- la verification que l'ID du livre est present ;
- le chargement et nettoyage du livre ;
- l'appel aux modules ;
- la sauvegarde et lecture du cache ;
- l'affichage des resultats.

Les constantes de cache sont definies au debut du fichier :

```python
LEXDIV_CACHE = "lexdiv"
TOPICS_CACHE = "topics_v5"
ENTITIES_CACHE = "entities_v11"
SUMMARY_CACHE = "summary_hybrid_v7"
SIMILAR_CACHE = "similar_v2"
CARD_CACHE = "card_v18"
```

Ces noms permettent de changer de version de cache quand une methode evolue.

`get_clean_book()` charge le livre avec `load_book()`, retire le header/footer Gutenberg, puis sauvegarde le texte nettoye dans `data/books/`.

## `utils/gutenberg.py`

Ce fichier gere les livres Project Gutenberg.

Pipeline :

```text
book id
   |
   v
check data/books
   |
   +--> if exists: read local file
   |
   +--> else: download from Gutenberg
               |
               v
            save locally
```

Fonctions :

- `get_book(book_id)` construit l'URL Gutenberg et telecharge le fichier texte ;
- `save_book(book_id, text)` sauvegarde le livre dans `data/books/` ;
- `load_book(book_id)` lit le livre local s'il existe, sinon le telecharge.

Pourquoi ce choix :

- eviter de telecharger plusieurs fois le meme livre ;
- permettre au projet de fonctionner plus vite apres un premier lancement ;
- garder le code de telechargement separe du code NLP.

Limite :

- si Gutenberg est inaccessible et que le livre n'est pas deja local, la commande peut echouer.

## `utils/text_processing.py`

Ce fichier regroupe les operations communes de nettoyage.

Fonctions principales :

- `remove_header_footer()` retire le texte legal de Project Gutenberg ;
- `normalize_text()` met en minuscule, retire la ponctuation et normalise les espaces ;
- `tokenize_words()` transforme le texte en liste de mots ;
- `split_chapters()` detecte les chapitres de type `CHAPTER I` ;
- `split_artificial_chapters()` coupe le texte en 4 sections si aucun chapitre n'est detecte ;
- `split_sections()` choisit entre chapitres reels et sections artificielles ;
- `split_sentences()` decoupe le texte en phrases.

Pipeline de nettoyage :

```text
raw Gutenberg text
   |
   v
remove_header_footer
   |
   v
normalize_text
   |
   v
tokenize_words / split_sections
```

La logique de decoupage des chapitres filtre les sections trop courtes pour eviter de prendre la table des matieres comme de vrais chapitres.

## `utils/cache.py`

Ce fichier gere le cache.

Fonctions :

- `get_cache_path(book_id, task_name)` construit le chemin du cache ;
- `load_cache(book_id, task_name)` lit un resultat sauvegarde ;
- `save_cache(book_id, task_name, data)` sauvegarde un resultat en JSON.

Pipeline :

```text
command
   |
   v
load_cache
   |
   +--> cache found: print result
   |
   +--> no cache: compute result
                  |
                  v
               save_cache
```

Le cache est important parce que certaines operations, comme SpaCy ou la similarite sur plusieurs livres, peuvent prendre du temps.

## `modules/lexdiv.py`

Commande :

```bash
python3 bookworm.py --lexdiv <ID>
```

Sortie attendue :

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

Pipeline :

```text
clean text
   |
   v
tokenize_words
   |
   v
count total words
   |
   v
count unique words
   |
   v
count hapax
   |
   v
compute ratios
```

Logique :

- `tok` : nombre total de tokens ;
- `typ` : nombre de tokens uniques ;
- `hap` : nombre de mots qui apparaissent une seule fois ;
- `ttr` : `typ / tok` ;
- `mwl` : longueur moyenne des mots ;
- `mwf` : `tok / typ`.

La methode est volontairement simple, car ces metriques sont directement definies par le sujet.

## `modules/topics.py`

Commande :

```bash
python3 bookworm.py --topics <ID>
```

Sortie attendue :

```python
{
    1: list[str],
    2: list[str],
    ...
}
```

Pipeline :

```text
clean text
   |
   v
split_sections
   |
   v
filter short sections
   |
   v
remove stop words
   |
   v
TF-IDF
   |
   v
top 10 words per section
```

Logique :

- le texte est separe en chapitres si possible ;
- sinon il est separe en 4 sections artificielles ;
- les sections de moins de 80 mots sont ignorees ;
- `TfidfVectorizer` calcule les scores TF-IDF ;
- les 10 meilleurs mots par section sont retournes.

Pourquoi TF-IDF :

- un simple compteur retourne souvent des mots frequents mais peu representatifs ;
- TF-IDF valorise les mots importants dans une section mais moins communs dans toutes les sections ;
- la methode est legere, classique et explicable.

Stop words :

- SpaCy fournit une liste de stop words anglais ;
- `CUSTOM_STOP_WORDS` ajoute du bruit specifique a Gutenberg ou aux dialogues, comme `gutenberg`, `ebook`, `said`, `chapter`.

Limites :

- TF-IDF retourne des mots, pas des themes abstraits ;
- le resultat depend du decoupage ;
- certains mots parasites peuvent rester.

## `modules/entities.py`

Commande :

```bash
python3 bookworm.py --entities <ID>
```

Sortie attendue :

```python
{
    "characters": list[str],
    "locations": list[str]
}
```

Pipeline :

```text
clean text
   |
   v
remove probable headings
   |
   v
SpaCy NER
   |
   v
keep PERSON / GPE / LOC
   |
   v
clean entity names
   |
   v
count frequency
   |
   v
top characters and locations
```

Logique :

- `load_nlp()` charge `en_core_web_sm` seulement quand il est necessaire ;
- `remove_heading_lines()` retire les titres probables pour reduire les faux positifs ;
- SpaCy detecte les entites nommees ;
- `PERSON` est classe dans `characters` ;
- `GPE` et `LOC` sont classes dans `locations` ;
- `clean_entity_name()` nettoie les espaces, possessifs et ponctuation ;
- `is_valid_entity_name()` retire des entites trop courtes, numeriques ou liees au bruit Gutenberg ;
- `Counter` classe les entites par frequence ;
- les entites deja classees comme personnages sont retirees des lieux.

L'auteur du livre est passe comme nom a exclure depuis `bookworm.py`, pour eviter qu'il apparaisse comme personnage.

Limites :

- SpaCy peut confondre certains titres, objets ou roles avec des personnages ;
- certains lieux peuvent etre faux positifs ;
- la litterature ancienne est plus difficile pour un petit modele generaliste.

## `modules/summarize.py`

Commande :

```bash
python3 bookworm.py --summarize <ID>
```

Sortie attendue :

```python
str
```

Pipeline :

```text
clean text
   |
   +--> get_entities
   |
   +--> get_topics
   |
   +--> get_book_info
          |
          v
theme dictionary
          |
          v
summary template
```

Logique :

- le resume recupere le titre, l'auteur et la categorie du livre ;
- il extrait les personnages principaux avec `entities` ;
- il extrait les mots importants avec `topics` ;
- `THEME_KEYWORDS` associe certains mots a des themes generaux ;
- `get_theme_labels()` compte les themes retrouves dans les mots importants ;
- le resume final est construit avec des phrases templates.

Exemple de sortie :

```text
Alice's Adventures in Wonderland is a book written by Lewis Carroll.
It belongs to the Children / Young Adult category.
It explores themes of animals, authority and society, and adventure.
The text focuses on characters such as Alice, Hatter, and Mouse, with places such as Duchess and Dinah.
Its most distinctive keywords include queen, rabbit, king, door, and bottle.
```

Methodes considerees :

- resume extractif : selectionner les phrases les plus importantes ;
- resume hybride par template : generer un court paragraphe a partir des metadonnees, topics et entites.

Methode retenue :

- le template est stable ;
- il est rapide ;
- il n'utilise pas de LLM, API ou gros modele ;
- il est plus facile a controler pour une book card.

Limites :

- ce n'est pas un resume narratif complet ;
- si les entites ou topics sont bruites, le resume le sera aussi ;
- les themes generaux dependent du dictionnaire `THEME_KEYWORDS`.

## `modules/similarity.py`

Commande :

```bash
python3 bookworm.py --similar <ID>
```

Sortie attendue :

```python
["title1", "title2", "title3", "title4", "title5"]
```

Pipeline :

```text
book id
   |
   v
load collection
   |
   v
clean each book
   |
   v
TF-IDF vectorization
   |
   v
cosine similarity
   |
   v
sort decreasing score
   |
   v
top 5 titles
```

Logique :

- `BOOK_COLLECTION` contient les livres demandes dans le sujet ;
- `get_book_info()` retourne l'id, le titre, l'auteur et la categorie ;
- `get_similar_books()` charge tous les livres de la collection ;
- les textes sont nettoyes avec `remove_header_footer()` ;
- `TfidfVectorizer` transforme chaque livre en vecteur ;
- `cosine_similarity()` compare le livre cible avec les autres ;
- le livre cible est exclu du resultat ;
- les 5 titres les plus proches sont retournes.

Choix technique :

- TF-IDF + cosine similarity est une methode classique pour comparer des documents ;
- elle est legere et ne demande pas de modele lourd ;
- les stop words SpaCy et Gutenberg reduisent le bruit.

Limites :

- la similarite est surtout lexicale ;
- elle ne comprend pas vraiment l'intrigue ;
- un livre peut etre proche par vocabulaire sans etre proche par theme profond.

## `modules/card.py`

Commande :

```bash
python3 bookworm.py --card <ID>
```

Sortie attendue :

```python
{
    "info": {"id": str, "authors": str, "bookshelves": str},
    "lexdiv": {"tok": int, "typ": int, "hap": int, "ttr": float, "mwl": float, "mwf": float},
    "topics": {1: list[str], 2: list[str], ...},
    "entities": {"characters": list[str], "locations": list[str]},
    "summary": str,
    "similar": ["title1", "title2", "title3", "title4", "title5"]
}
```

Pipeline :

```text
book id
   |
   v
clean text
   |
   +--> lexdiv
   +--> topics
   +--> entities
   +--> summarize
   +--> similar
          |
          v
build_card
          |
          v
final dictionary
```

Logique :

- `bookworm.py` calcule ou charge chaque resultat depuis le cache ;
- `build_card()` assemble les resultats ;
- `build_info()` garde seulement les champs demandes par le sujet : `id`, `authors`, `bookshelves` ;
- `print_card()` affiche une ligne par grande section pour garder la sortie lisible.

## Collection De Livres Pour La Similarite

La collection utilisee correspond a celle du sujet :

```text
11     Alice's Adventures in Wonderland
12     Through the Looking-Glass
16     Peter Pan
55     The Wonderful Wizard of Oz
113    The Secret Garden
120    Treasure Island
236    The Jungle Book
108    The Return of Sherlock Holmes
834    The Memoirs of Sherlock Holmes
863    The Mysterious Affair at Styles
1661   The Adventures of Sherlock Holmes
61262  Poirot Investigates
69087  The Murder of Roger Ackroyd
70114  The Big Four
35     The Time Machine
36     The War of the Worlds
84     Frankenstein; Or, The Modern Prometheus
159    The Island of Doctor Moreau
164    Twenty Thousand Leagues under the Sea
345    Dracula
68283  The Call of Cthulhu
```

## Cache

Le cache evite de recalculer les traitements couteux.

```text
data/books/   -> textes telecharges ou nettoyes
data/cache/   -> resultats des modules
```

Exemples :

```text
11_lexdiv.json
11_topics_v5.json
11_entities_v11.json
11_summary_hybrid_v7.json
11_similar_v2.json
11_card_v18.json
```

Les suffixes de version permettent de ne pas reutiliser un ancien cache quand la logique d'un module change.

## Choix Techniques

### `requests`

Utilise pour telecharger les livres depuis Project Gutenberg. Il simplifie les requetes HTTP et permet d'utiliser `raise_for_status()`.

### `pathlib`

Utilise pour construire les chemins de fichiers de maniere lisible.

### `sys.argv`

Utilise pour garder un CLI simple. Une alternative plus complete serait `argparse`.

### SpaCy

Utilise pour la reconnaissance d'entites nommees. Le modele `en_core_web_sm` est leger et suffisant pour un prototype.

### Scikit-learn

Utilise pour `TfidfVectorizer` et `cosine_similarity`.

## Limites Connues

- la gestion d'erreurs reseau peut encore afficher une exception Python ;
- SpaCy peut produire des faux positifs sur les textes litteraires ;
- TF-IDF retourne des mots importants, pas une comprehension semantique complete ;
- le resume est une description courte, pas un resume narratif complet ;
- le projet utilise `sys.argv`, donc le CLI reste basique.

## Conformite Au Sujet

Commandes implementees :

```text
--lexdiv <ID>
--topics <ID>
--entities <ID>
--summarize <ID>
--similar <ID>
--card <ID>
```

Contraintes respectees :

- script principal nomme `bookworm.py` ;
- operations effectuees sur des livres Project Gutenberg ;
- cache pour reutiliser les resultats ;
- pas de LLM, pas d'API externe, pas de gros modele ;
- methodes legeres et explicables ;
- documentation des choix, pipelines, limites et commandes.
