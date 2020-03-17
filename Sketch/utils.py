
class UtilMethods:
    @staticmethod
    def text_from_file(file_path: str):
        f = open(file_path, 'r')
        file_text = f.read()
        f.close()
        return file_text

    @staticmethod
    def write_text_to_file(file_path: str, text: str):
        file = open(file_path, 'w')
        file.write(text)
        file.close()