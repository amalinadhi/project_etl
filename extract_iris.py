from src._base import BaseCommand


# CLASS
class IrisCommand(BaseCommand):
    def __init__(self, config):
        # Initialize parents
        super().__init__(config)

        # Initialize specific methods
        self._create_data_table_command()
        self._create_last_read_table_command()

    # BUAT CUSTOMIZE METHOD DISINI
    def _create_data_table_command(self):
        self.data_table_command = f"""
            CREATE TABLE IF NOT EXISTS {self.table_data_name} (
                flower_id varchar(80) not null,
                sepal_length real,
                sepal_width real,
                petal_length real,
                petal_width real,
                class varchar(80),
                PRIMARY KEY (flower_id)
            )
        """

    def _create_last_read_table_command(self):
        self.last_read_table_command = f"""
            CREATE TABLE IF NOT EXISTS {self.table_last_read_name} (
                update_id varchar(80),
                last_row int,
                table_name varchar(80),
                created_at timestamp not null default current_timestamp,
                PRIMARY KEY (update_id)
            )
        """

    def _get_value_clean(self, id: int, value: list) -> str:
        """clean the value"""
        # Buat flower id 
        flower_id = str(id)

        # Add '' to class_name
        value[-1] = f"'{value[-1]}'"

        # Join all
        value = ', '.join([flower_id] + value)

        return value

 


if __name__ == '__main__':
    # GLOBAL VARIABLE
    CONFIG = {
        'spreadsheet_id': "1E8X7-UJHs9USfJf2cMsKVpcpmwiBzYGsYVI5iTP0agw",
        'sheet_name': "iris",
        'dump_path': "data/interim/iris.pkl",
        'table_data_name': "iris",
        'table_last_read_name': "last_read_info"
    }

    # Initialize
    obj = IrisCommand(config = CONFIG)

    # Execute
    obj.create_data_table()
    obj.create_last_read_table()
    obj.update_data()

    # Untuk drop table
    # from src._query import execute_command
    # execute_command(command = "DROP TABLE iris, last_read_info")
