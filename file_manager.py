import os

    

class Filemanager:       
    """
    A class for managing file operations such as reading, writing, and deleting files.

    Attributes:
        __file_name (str): The name of the file to be managed.
        __folder (str): The folder where the file is located.
        
    methods:
        read_file: Reads the content of the file.
        write_file: Writes content to the file.
        delete_file: Deletes the file.
    """ 
    def __init__(self, file_name=None, folder='store'):
        """
        Initialize the Filemanager with a file name and folder.

        Args:
            file_name (str, optional): The name of the file. Defaults to None.
            folder (str, optional): The folder where the file is located. Defaults to 'store'.
        """
        self.__file_name = file_name
        self.__folder = folder

    @property
    def file_name(self): # getter
        return self.__file_name
    
    @file_name.setter # setter
    def file_name(self, file_name):
        self.__file_name = file_name
    
    @property # getter
    def folder(self):
        return self.__folder
    
    @folder.setter # setter 
    def folder(self, folder):
        self.__folder = folder

    def read_file(self, lines=False):
        """
        Read the contents of the file.

        Args:
            lines (bool, optional): If True, read the file line by line. If False, read the entire content. Defaults to False.

        Returns:
            str or list: The content of the file as a string or a list of lines.

        Raises:
            Exception: If unable to read the file.
        """
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
        """
        Write content to the file.

        Args:
            content (str): The content to be written to the file.
            mode (str, optional): The mode in which the file should be opened ('w' for write, 'a' for append). Defaults to 'w'.

        Raises:
            Exception: If unable to write to the file.
        """
        try:
            with open(f"{self.folder}/{self.file_name}", mode, encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            print("Unable to write file")
            print(e)

    def delete_file(self):
        """
        Delete the file.

        Raises:
            Exception: If unable to delete the file.
        """
        try:
            os.remove(f"{self.folder}/{self.file_name}")
        except Exception as e:
            print("Unable to delete file")
            print(e)
        

