
def read_cipher_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            result = ""
            s = file.readlines()
            for i in s:
                result += i.replace("\n", " ").lower()
            return result
    except FileNotFoundError:
        print("Невозможно считать файл")

print(read_cipher_from_file("text_files/encV_source_text.txt"))