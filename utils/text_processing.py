def remove_header(text):
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
