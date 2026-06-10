def build_card(book_id, lexdiv, topics, entities, summary, similar, info):
    return {
        "info": info,
        "lexdiv": lexdiv,
        "topics": topics,
        "entities": entities,
        "summary": summary,
        "similar": similar,
    }
