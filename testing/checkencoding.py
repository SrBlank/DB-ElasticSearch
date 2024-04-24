import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        return chardet.detect(file.read())['encoding']

csv_encoding = detect_encoding('./lyrics.csv')
print(csv_encoding)
