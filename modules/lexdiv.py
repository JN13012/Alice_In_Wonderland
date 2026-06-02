def total_number_of_words(words):
    total = len(words)
    return total


def total_number_of_unique_words(words):
    unique_words = []
    for x in words:
        if x not in unique_words:
            unique_words.append(x)
    return len(unique_words)


def number_of_word_occuring_only_once(words):
    word_count = {}
    for x in words:
        if x not in word_count:
            word_count[x] = 1
        else:
            word_count[x] += 1
                 
    hap = 0
    for x in word_count.values():
        if x == 1:
            hap += 1
    return hap


def lexical_diversity(words):
    if total_number_of_words(words) == 0 :
        return 0
    lexical_diversity = total_number_of_unique_words(words) / total_number_of_words (words)
    return lexical_diversity

def mean_word_length(words):
    if total_number_of_words(words) == 0:
        return 0
    
    total_letters = 0
    for x in words:
        total_letters += len(x)
    
    return total_letters / total_number_of_words(words)

def mean_word_frequency(words):
    if total_number_of_unique_words(words) ==0:
        return 0
    return total_number_of_words (words) / total_number_of_unique_words(words)


def get_lexdiv_metrics(words):
    tok = total_number_of_words(words)
    typ = total_number_of_unique_words(words)
    hap = number_of_word_occuring_only_once(words)
    ttr = lexical_diversity(words)
    mwl = mean_word_length(words)
    mwf = mean_word_frequency(words)
    return {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": ttr,
        "mwl": mwl,
        "mwf": mwf
    }