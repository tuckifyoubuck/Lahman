import pandas as pd
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
        defaults to returning all directories for the 'core' lahman directory
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

    def get_tables_from_dir(self, tables=None, directory='core'):
        """

        :param tables: list of tables to return df for
        :param directory: github directory/folder to pull table/tables from
        :return: dictionary containing tablename/filename as key and a pandas df with csv data
        """
        github_raw_link = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/'
        tables_dict = {}
        for csv in tables:
            tbl_name = csv[:-4]
            tables_dict[tbl_name] = pd.read_csv(github_raw_link+directory+'/'+csv)
        return tables_dict







