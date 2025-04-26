from flask import Flask, Response, request
from threading import Timer
from .wordlist import Wordlist
from .database import Database
from .game import Game
import logging
import time

ID_GAME = '9'

def create_app():
    app = Flask(__name__)
    app.config.from_object('slovsmesh.config.Config')

    logger = logging.getLogger('app')

    try:
        db = Database(app.config['DB_PATH'])
    except Exception as e:
        logger.error(f"Не могу открыть базу данных игры: {e}.")
        exit(1)

    try:
        wordlist_path = app.config['WORDLIST_PATH']
        wordlist = Wordlist(wordlist_path)
    except:
        logger.error(f"Отсутствуют слова для игры! Заполните файл {wordlist_path} и перезапустите сервер.")
        exit(2)

    def wordlist_watcher():
        try:
            wordlist.reload()
        except Exception as e:
            logger.error(f"Ошибка в watcher: {e}")
        finally:
            Timer(60, wordlist_watcher).start()
    
    wordlist_watcher()
    game = Game(db, wordlist)

    @app.get('/game/read.php')
    def get_leaderboard():
        if request.args.get('id_game') != ID_GAME:
            return Response(status=418)

        return game.get_scores()

    @app.get('/game/write.php')
    def put_score():
        if request.args.get('id_game') != ID_GAME:
            return Response(status=418)

        user_name = request.args.get('user_name')
        score = request.args.get('scores')

        if not user_name and not score:
            return Response(status=400)

        try:
            score = int(score)

            if len(user_name) > 12:
                logger.warning("Превышены лимиты user_name")
                return Response(status=400)
            if score > 65535:
                logger.warning("Превышены лимиты score")
                return Response(status=400)

            return game.put_score(user_name, score)
        except ValueError as e:
            logger.error(f"Неверный формат счета: {score}")
            return Response(status=400)
        except Exception as e:
            logger.error(f"Не могу записать результат игры: {e}")
            return Response(status=500)

    @app.get('/game/words.php')
    def validate_word():
        word = request.args.get('word')

        if not word:
            logger.debug(f"Отсутствует слово для проверки")
            return Response(status=400)
        
        return game.validate_word(word)

    return app