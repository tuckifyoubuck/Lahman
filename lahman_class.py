from bs4 import BeautifulSoup as bs
import requests

class Lahman:
    def __init__(self):
        self.master_url = "https://github.com/chadwickbureau/baseballdatabank/tree/master"

    def get_directories(self) -> list:
        """
        Finds all the directories listed under Lahman master branch
        located on chadwickbureau GitHub page
        :return: list
        """
        res = requests.get(self.master_url)
        soup = bs(res.text, 'lxml')
        file = soup.find_all('a', class_="js-navigation-open")
        substring_ignore_list = ['.', '\n']
        folder_list = []
        for i in file:
            if not any(substring in i.text for substring in substring_ignore_list):
                folder_list.append(i.text)
        return folder_list

    def get_filenames_in_directories(self, dir_list=['core']) -> dict:
        """
        Returns a dictionary containing each directory and filenames in it
        defaults to returning all directories returned by get_directories method
        :param dir_list: directories to pull filenames for
        :return: dict
        """
        dir_files_dict = {}
        for d in dir_list:
            res = requests.get(self.master_url + '/' + d)
            soup = bs(res.text, 'lxml')
            file = soup.find_all('a', class_="js-navigation-open")
            dir_files_list = []
            for i in file:
                if '.csv' in i.text:
                    dir_files_list.append(i.text)
            dir_files_dict[d] = dir_files_list
        return dir_files_dict





