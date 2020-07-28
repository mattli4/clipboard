import codecs
import os


class ControlCV:
    CLIPBOARD = []
    DEFAULT_FILE = 'clipboardDefault.txt'

    def __init__(self):
        self.cwd = os.getcwd()
        if os.path.exists(self.DEFAULT_FILE):
            self.load_from_file(self.DEFAULT_FILE)

    def dump_to_file(self, file):
        with codecs.open(file, 'w', encoding='utf-8') as fp:
            all_items = '#!'.join(self.CLIPBOARD)
            fp.write(all_items)
            fp.close()

    def load_from_file(self, file):
        with codecs.open(file, 'r', encoding='utf-8') as fp:
            all_items = fp.read()
            self.CLIPBOARD = all_items.split('#!')
            fp.close()

    def load_from_file_by_line(self, file):
        with codecs.open(file, 'r', encoding='utf-8') as fp:
            for item in fp.readlines():
                self.CLIPBOARD.append(item)
            fp.close()
