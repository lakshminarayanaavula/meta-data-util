import os
import json


directory_path = "../meta_input_files"
file_list = os.listdir(directory_path)


def create_schema():
    for filename in file_list:
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                table_name = json_data.get("dbTable")
                fields = json_data.get("fields", [])
                columns = []
                for field in fields:
                    column_name = field.get("dbName")
                    data_type = field.get("dataType")
                    is_required = field.get("required", False)
                    is_foreign_key = field.get("foreignKey", False)
                    foreign_key_info = field.get("foreignKeyInfo")
                    if is_foreign_key and foreign_key_info:
                        reference_table = foreign_key_info.get("parentObjectDbName")
                        reference_column = foreign_key_info.get("primaryKeyDbName")
                        if column_name == 'created_by' or column_name == 'modified_by' or column_name == 'org_id':
                            columns.append(f"{column_name} {data_type} NOT NULL")
                        else:
                            columns.append(f"{column_name} {data_type} NOT NULL REFERENCES {reference_table}({reference_column})")
                    else:
                        constraint = "NOT NULL" if is_required else ""
                        if column_name == "id":
                            constraint = " PRIMARY KEY"
                        if data_type == "PICKLIST":
                            data_type = 'UUID'
                        if data_type == 'STRING':
                            data_type = 'VARCHAR(255)'
                        if data_type == 'NUMBER':
                            data_type = 'NUMERIC'
                        if column_name == 'created_date' or column_name == 'modified_date':
                            data_type = "TIMESTAMP WITHOUT TIME ZONE"
                        columns.append(f"{column_name} {data_type} {constraint}")
                columns.append(f"deleted boolean default false")
                columns_str = ",\n    ".join(columns)
                sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n);"
                file_name = f"../sql-script/{table_name}.sql"
                directory = os.path.dirname(file_name)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(file_name,'w') as f:
                    f.write(sql_query)
                print(f"SQL Query for {table_name}:\n{sql_query}\n\n")


def generate_java_source_code():
    pass


if __name__ == '__main__':
    print("1. Create Schema 2. Generate Java Source Code ")
    choice = input("Enter your choice: ")
    if choice == "1":
        create_schema()
    elif choice == "2":
        generate_java_source_code()
    else:
        print("Invalid choice")
