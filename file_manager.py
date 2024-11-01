import os



class Filemanager:
    def __init__(self, file_name=None, folder='store'):
        self.__file_name = file_name
        self.__folder = folder

    @property
    def file_name(self):
        return self.__file_name
    
    @file_name.setter
    def file_name(self, file_name):
        self.__file_name = file_name
    
    @property
    def folder(self):
        return self.__folder
    
    @folder.setter
    def folder(self, folder):
        self.__folder = folder

    def read_file(self, lines=False):
        content = None

        try:
            with open(f"{self.folder}/{self.file_name}", 'r', encoding="utf-8") as file:
                if lines:
                    content = file.readlines()
                else:
                    content = file.read()
                
        except Exception as e:
            print("Unable to read file")
            print(e)
        
        return content
    
    def write_file(self, content, mode='w'):
        try:
            with open(f"{self.folder}/{self.file_name}", mode, encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            print("Unable to write file")
            print(e)

    def delete_file(self):
        try:
            os.remove(f"{self.folder}/{self.file_name}")
        except Exception as e:
            print("Unable to delete file")
            print(e)
        

