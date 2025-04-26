from logging import getLogger
import os.path


class Wordlist:
    def __init__(self, path):
        self.__logger = getLogger(__name__)
        self.__path = path
        self.__last_modified = 0
        self.__words = self.__load_words(self.__path)
        self.__logger.info(f"Загрузил {self.get_word_count()} слов из {path}")
    
    def __get_file_mtime(self):
        self.__raise_if_not_exists(self.__path)
        return os.path.getmtime(self.__path)
    
    def __raise_if_not_exists(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File {path} is not a file")
    
    def __load_words(self, path):
        self.__raise_if_not_exists(path)
        with open(path, "r", encoding="utf-8") as f:
            return [word.lower().strip() for word in f.read().splitlines()]
    
    def reload(self):
        try:
            current_mtime = self.__get_file_mtime()
            if current_mtime > self.__last_modified:
                new_words = self.__load_words(self.__path)
                self.__words = new_words
                self.__last_modified = current_mtime
                self.__logger.info(f"Обновил словарь. Теперь {self.get_word_count()} слов")
                return True
            return False
        except Exception as e:
            self.__logger.error(f"Ошибка при обновлении словаря: {e}")
            return False
    
    def get_word_count(self):
        return len(self.__words)
    
    def validate_word(self, word):
        return word.lower() in self.__words
