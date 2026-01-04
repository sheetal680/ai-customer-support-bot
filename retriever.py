def retrieve_best_faq(user_question, faqs):
    user_question = user_question.lower()

    best_score = 0
    best_faq = None

    for faq in faqs:
        overlap = sum(
            1 for word in faq["question"].split()
            if word in user_question
        )
        score = overlap / max(len(faq["question"].split()), 1)

        if score > best_score:
            best_score = score
            best_faq = faq

    return best_faq, best_score
