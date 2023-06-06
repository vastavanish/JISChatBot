from database import DatabaseConnection

from spacy_utils import preprocess_input_sentence

import pandas as pd

import csv

#db = DatabaseConnection()


def update_chatbot(sentence) -> str:
    try:
        _, words, __ = preprocess_input_sentence(sentence)

        print(words)

        df = pd.read_csv('notfound.csv')

        csv_cols = df.columns.to_list()

        for word in words:
            with open(r'notfound.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
                writer.writerow({'pattern': word})

        return 'ok'
    except Exception as e:

        return str(e)


"""
// With database
def update_chatbot(sentence) -> str:
    try:
        _, words, __ = preprocess_input_sentence(sentence)

        print(words)
        for word in words:
            print(word)
            db.command = "SELECT COUNT(*) as Count FROM Vocabulary WHERE vocabulary='" + word + "'"
            db.cursor.execute(db.command)

            row = db.cursor.fetchone()

            count = row.Count

            if count == 0:
                db.command = '''
                INSERT INTO Vocabulary(vocabulary)
                VALUES(?)
                '''

                db.cursor.execute(db.command, (word))

                db.cursor.commit()

        return 'ok'
    except Exception as e:
        db.cursor.rollback()
        return str(e)

"""
