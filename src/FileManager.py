import os

class FileManager:
    def __init__(self):
        folder_path = 'vocabulary'
        self.file_paths = []
        self.words_dict = dict()
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.file_paths.append(file_path)
        for file_path in self.file_paths:
            self.get_file_words_list(file_path)

    def get_file_words_list(self, file_path):
        self.words_dict = dict()

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                find_index = line.find('  ')
                if -1 != find_index:
                    e_words = line[:find_index]
                    c_words = line[find_index:-1].strip()
                    self.words_dict[e_words] = c_words

    def get_words_list(self):
        sorted_items = sorted(self.words_dict.items(), key=lambda x: x[0])
        return sorted_items
