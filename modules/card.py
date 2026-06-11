def build_card(info, lexdiv, topics, entities, summary, similar):
    return {
        "info": build_info(info),
        "lexdiv": lexdiv,
        "topics": topics,
        "entities": entities,
        "summary": summary,
        "similar": similar,
    }


def build_info(info):
    return {
        "id": str(info.get("id", "Unknown")),
        "authors": info.get("authors", "Unknown"),
        "bookshelves": info.get("bookshelves", "Unknown"),
    }
