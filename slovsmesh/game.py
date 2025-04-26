import xml.etree.ElementTree as ET
from flask import Response


class Game:
    def __init__(self, db, wordlist):
        self.__db = db
        self.__wordlist = wordlist

    def get_scores(self):
        root = ET.Element('root')
        for score in self.__db.get_scores():
            record = ET.SubElement(root, 'record')
            record.set('user_name', score['user_name'])
            record.set('scores', str(score['score']))
        
        data = ET.tostring(root, encoding='utf-8', method='xml')
        return Response(data, mimetype='application/xml; charset=utf-8')

    def put_score(self, user_name, score):
        self.__db.put_score(user_name, score)
        return Response(status=200)

    def validate_word(self, word):
        response = Response(mimetype='text/plain', status=200)

        if self.__wordlist.validate_word(word):
            response.data = "rezult=true"
        else:
            response.data = "rezult=false"

        return response
