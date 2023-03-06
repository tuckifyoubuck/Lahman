from lahman_class import Lahman
from postgresql_class import PSQL


def main():
    # Get lahman GitHub repository layout
    lahman_github = Lahman()
    schemas = lahman_github.get_directories()
    layout = lahman_github.get_tbl_names_in_dirs(dir_list=schemas)

    # Create new DB named 'lahman
    new_db_name = 'lahman'
    username = 'postgres'
    print('password:')
    password = input()
    temp_db_engine = PSQL(user=username, password=password)
    temp_db_engine.create_new_db(new_db_name)

    # Connect to new DB
    new_db_engine = PSQL(user=username, password=password, database=new_db_name)

    # Create schemas in new DB named after directories in lahman GitHub repository
    new_db_engine.create_schemas(schemas)

    # Loop through lahman GitHub layout, create tables and load data while looping
    # through table/csv names and dataframes returned from GitHub raw csv links
    for schema, tables in layout.items():
        temp_dict = lahman_github.get_tbls_from_dir(tables=tables, directory=schema)
        for tbl_name, dataframe in temp_dict.items():
            new_db_engine.create_tbl(dataframe=dataframe, tbl_name=tbl_name, schema=schema)
            new_db_engine.insert_into_tbl(dataframe=dataframe, tbl_name=tbl_name, schema=schema)

    print('\nlahman database complete!')


if __name__ == "__main__":
    main()
