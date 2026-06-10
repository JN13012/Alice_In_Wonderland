import re #regex permet de sub(substituer)/split(découper) avec plusieurs séparateurs

def remove_header_footer(text):
    header = "*** START OF THE PROJECT GUTENBERG EBOOK"
    footer = "*** END OF THE PROJECT GUTENBERG EBOOK"
    
    start_index = text.find(header)
    end_index = text.find(footer)
    
    # No header
    if start_index == -1:
        return text

    # Header start after \n
    cut_header = text.find("\n", start_index)
    if cut_header == -1:
        return text
    cut_header += 1
        
    # Len text without Footer
    if end_index == -1:
       end_index = len(text)
       
    return text[cut_header:end_index].strip() #strip supprime les espaces en trop au debut et à la fin.

# Remove \n, extra space and all lower
def normalize_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = " ".join(text.split())
    
    return text

# Renvoi une liste de mots avec .split
def tokenize_words(text):
    normalized_text = normalize_text(text)
    words = normalized_text.split()
    
    return words

# Découpe en chapter en fonction du pattern regex [ivxlcdm\d]
def split_chapters(text):
    pattern = r"(chapter\s+[ivxlcdm\d]+)"
    parts = re.split(pattern, text, flags=re.IGNORECASE) # re.split = regex of separators, stringToCut, maxsplit=0 (unlimited), flags=(ignore Maj+min) => renvoi toujours index0=texte avant le chapitre sinon "" et commence à index1.

    chapters = []

    for i in range (1, len(parts) - 1, 2):
        content = parts[i + 1].strip()

        if content:
            chapters.append(content)
    
    return chapters

# Rend 4 listes de sections
def split_artificial_chapters(text, number_of_sections=4):
    words = text.split()
    section_size = len(words) // number_of_sections

    sections = []

    for i in range (number_of_sections):
        start = i * section_size
        
        if i == number_of_sections - 1:
            end = len(words)

        else:
            end = (i + 1) * section_size
        
        section_words = words[start:end]
        sections.append(" ".join(section_words))

    return sections

# Décision de quel sections return
def split_sections(text, number_of_sections=4):
    chapters = split_chapters(text)

    if chapters:
        return chapters

    return split_artificial_chapters(text, number_of_sections)

# Découpe les phrase en fonction du pattern regex "(?<=[.!?])\s+"
def split_sentences(text):
    pattern = r"(?<=[.!?])\s+"
    sentences = re.split(pattern, text, flags=re.IGNORECASE)

    cleaned_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            cleaned_sentences.append(sentence)

    return cleaned_sentences

