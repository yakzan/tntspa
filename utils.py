import tensorflow as tf
import io
import pandas as pd
import csv
import json

from preprocessing import preprocess_sentence

def load_vectors(fname):
    """
    Load word embeddings from a pre-trained vector file using local python 
    """
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    # number of words and dimensions
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return n, d, data

def read_qald_json(file_path, lang='en', written_to_file=True):
    """
    Read json file from QALD challenges and return a list of question (given language) to sparql query pairs
    """
    with open(file_path, 'r') as json_file:
        # json_object should have one dataset field and a questions array field,
        # each question contains id, answertype, aggregation, onlydbo, hybrid, question, query, answers, etc.
        json_object = json.load(json_file)
        dataset_id = json_object["dataset"]["id"]
        questions = json_object["questions"]
        result = []
        for item in questions:
            query_sparql = item["query"]["sparql"]
            for question in item["question"]:
                if question["language"] == lang:
                    result.append((question["string"], query_sparql))
                    break
        data = pd.DataFrame(data=result, columns=["question", "sparql"])

        if written_to_file:
            base_file_path = file_path[0:file_path.rfind('.')]
            question_file = open(base_file_path+'.'+lang, 'w')
            sparql_file = open(base_file_path+'.sparql', 'w')
            for i in range(len(data)):
                question_file.write(data["question"][i])
                question_file.write('\n')
                sparql_file.write(data["sparql"][i])
                sparql_file.write('\n')
            question_file.close()
            sparql_file.close()

        return data

def read_qald_csv(file_path, written_to_file=True):
    """
    Read csv file from QALD challenges and return a pandas DataFrame containing its data
    """
    data = pd.read_csv(file_path, sep=';', names=["type", "question", "sparql", "other1", "other2"])

    if written_to_file:
            base_file_path = file_path[0:file_path.rfind('.')]
            question_file = open(base_file_path+'.en', 'w')
            sparql_file = open(base_file_path+'.sparql', 'w')
            for i in range(len(data)):
                question_file.write(data["question"][i])
                question_file.write('\n')
                sparql_file.write(data["sparql"][i])
                sparql_file.write('\n')
            question_file.close()
            sparql_file.close()

    return data

def tokenize(sentence):
    """Split the given sentence into a list of tokens"""
    return sentence.split('')

def build_vocabulary(file_path):
    """
    Build a vocabulary from given file path, and output a vocabulary file?
    """
    vocabulary = set()
    file = open(file_path)

    # Simple version, split lines into words using space as delimiter
    # maybe works, maybe not because many words in sparql are combined like functions
    for line in file:
        for word in line.split(' '):
            vocabulary.add(word)

    return vocabulary

def read_dbpedia_prefix(file_path="data/prefixes.csv"):
    """
    Read prefixes from DBpedia
    """
    result = {}
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            result[row[0]] = row[1]

    # Or we can use pandas to read csv into a DataFrame object
    # data = pd.read_csv("data/prefixes.csv", sep='\t')
    # return data

    return result

def read_lines(file_path):
    input_texts = []
    with open(file_path) as file:
        for line in file:
            input_texts.append(line)
    return input_texts

def build_vocabulary_from_texts(texts):
    vocab = set()
    for text in texts:
        vocab.update(text.split())
    return vocab

def write_history(history, file_location):
    file = open(file_location, 'w')
    json.dump({
        "history": history.history,
        "params": history.params,
        "epoch": history.epoch
    }, file)

def read_history(file_location):
    file = open(file_location, 'r')
    history = json.load(file)
    return history