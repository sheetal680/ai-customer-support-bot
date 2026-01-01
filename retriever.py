from sklearn.metrics.pairwise import cosine_similarity

def retrieve_best_faq(question_vec, faq_vecs, faqs):
    scores = cosine_similarity([question_vec], faq_vecs)[0]
    best_index = scores.argmax()
    best_score = scores[best_index]
    return faqs[best_index], best_score
