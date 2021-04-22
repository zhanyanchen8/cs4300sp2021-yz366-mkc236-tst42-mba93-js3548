import json,pandas as pd, numpy as np, matplotlib.pyplot as plt,os
from data_summary.course_data_summary import get_data,get_terms_and_TFs
from sklearn.feature_extraction.text import TfidfTransformer
from machine_learning.keyword_extractor_summarizer import keyword_extractor
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize

def loadData():
    path_course = r'C:\Users\Mads-\Documents\Universitet\6. Semester\INFO4300 Language and Information\course_data'
    path_rmp = r'C:\Users\Mads-\Documents\Universitet\6. Semester\INFO4300 Language and Information\rate_my_professor.csv'
    course_data = get_data(path=path_course)
    rmp_data = get_data(path=path_rmp, filetype="csv")
    return course_data, rmp_data

def load_course_descriptions():
    course_data, _ = loadData()
    course_desc = course_data[["description"]]
    return course_data,course_desc

def text_extractor(course_desc,query,doc_term_TF_matrix,terms,vectorizer):
    """
    Get sentences
    For each sentence find a similarity score
    Find the sentence with largest score. Add that and the next 2-3 sentences.
    """
    query = query.lower()
    query_vec = vectorizer.transform(pd.Series(query))
    sentences = sent_tokenize(course_desc)
    sentences_vec = [vectorizer.transform(pd.Series(sentence)) for sentence in sentences]

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(doc_term_TF_matrix)

    tf_idf_desc = tfidf_transformer.transform(query_vec)
    tf_idf_sentences = [tfidf_transformer.transform(sentence) for sentence in sentences_vec]

    sim_array = np.zeros(len(sentences_vec))  # array of similarity scores

    array_1 = tf_idf_desc
    for i in range(len(sentences_vec)):
        array_2 = tf_idf_sentences[i]
        sim_array[i] = cosine_similarity(array_1, array_2)
    print(course_desc)
    print("Most:",sentences[np.argmax(sim_array)])

   #### DECICE WHAT DATA TO RETURN ###
   return 0

if __name__ == "__main__":
    course_data, course_desc = load_course_descriptions()
    terms, terms_TF,doc_term_TF_matrix,vectorizer  = get_terms_and_TFs(course_data,max_dfq=.5)

    i = 1189
    print(course_data.iloc[i][["titleLong"]])
    desc_example = course_desc.iloc[i]
    a = vectorizer.transform(desc_example)
    keyword_extractor(doc_term_TF_matrix,terms,vectorizer,desc_example,n=3)
    print("#####")
    print("Query: Information retrieval")
    query = "Information retrieval"
    print(desc_example[0])
    test_str = desc_example[0]
    summarized_text = text_extractor(test_str,query,doc_term_TF_matrix,terms,vectorizer)