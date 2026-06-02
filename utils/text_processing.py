import re

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
       
    return text[cut_header:end_index].strip()

# Remove \n, extra space and all lower
def normalize_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = " ".join(text.split())
    
    return text

def tokenize_words(text):
    normalized_text = normalize_text(text)
    words = normalized_text.split()
    
    return words