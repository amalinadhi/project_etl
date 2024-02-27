
from tqdm import tqdm

from src._query import execute_command
from src._utils import load_spreadsheet, pickle_load 

# UPDATE CLASS
class BaseCommand:
    def __init__(self, config):
        # Extract configuration
        self.spreadsheet_id = config['spreadsheet_id']
        self.sheet_name = config['sheet_name']
        self.dump_path = config['dump_path']
        self.table_data_name = config['table_data_name']
        self.table_last_read_name = config['table_last_read_name']

    # FOR CREATING BASIC TABLES
    # ==========================
    def _is_data_table_exists(self):
        """
        Return true if the data table exists
        """
        # Write command
        command = f"""
            SELECT EXISTS (
                SELECT * FROM
                    pg_tables
                WHERE
                    schemaname = 'public'
                    AND tablename = '{self.table_data_name}'
            )
        """
        return execute_command(command = command,
                               fetch_results = True)[0]
    
    def _is_last_read_table_exists(self):
        """
        Return true if the data table exists
        """
        # Write command
        command = f"""
            SELECT EXISTS (
                SELECT * FROM
                    pg_tables
                WHERE
                    schemaname = 'public'
                    AND tablename = '{self.table_last_read_name}'
            )
        """
        return execute_command(command = command,
                               fetch_results = True)[0]

    def create_data_table(self):
        """
        Create table in the PostgreSQL database if exist
        """
        # Check
        if not self._is_data_table_exists():
            print('Data table is not exist!')
            print(f'>> Create data table with table-name: {self.table_data_name}')
            execute_command(command = self.data_table_command)
            print(f'>> Success!')
        else:
            print('Data table is exist!')

    def create_last_read_table(self):
        # Check
        if not self._is_last_read_table_exists():
            print('Last read info table is not exist!')
            print(f'>> Create last read info table with table-name: {self.table_last_read_name}')
            execute_command(command = self.last_read_table_command)
            print(f'>> Success!')
        else:
            print('Last read info table is exist!')


    # FOR UPDATING DATA
    # ==================
    def _get_latest_read(self):
        """Get the latest read data"""
        # Check if the last_read_table_exists
        if not self._is_last_read_table_exists():
            self.last_update_id = 0
            self.last_row = 0
        
        # Kalau table last read ada,
        else:
            # Check if we already load the data
            command = f"""
                SELECT COUNT(update_id)
                FROM {self.table_last_read_name}
                WHERE table_name = '{self.table_data_name}'
            """
            res = execute_command(command = command, fetch_results=True)[0]

            # Kalau belum di update
            if res == 0:
                self.last_row = 0
                self.last_update_id = 0

            # Kalau sudah di read
            else:
                # Query untuk dapatkan yang last_read yang paling akhir
                command = f"""
                    SELECT last_row, created_at
                    FROM {self.table_last_read_name}
                    WHERE table_name = '{self.table_data_name}'
                    ORDER BY created_at DESC
                    LIMIT 1
                """
                res = execute_command(command = command, fetch_results=True)
                self.last_row, self.last_update = res

                # Query untuk dapatkan last_update_id
                command = f"""
                    SELECT MAX(update_id)
                    FROM {self.table_last_read_name}
                """
                res = execute_command(command = command, fetch_results=True)[0]
                self.last_update_id = res

    def _load_data(self):
        """Load data & dump it to spreadsheet"""
        load_spreadsheet(sheet_id = self.spreadsheet_id,
                         sheet_name = self.sheet_name,
                         dump_path = self.dump_path)

    def _add_record(self, id, value):
        """add record to data table"""
        # Get value clean
        value_clean = self._get_value_clean(id = id,
                                            value = value)
        # Execute
        command = f"INSERT INTO {self.table_data_name} VALUES ({value_clean})"
        execute_command(command = command)

    def update_data(self):
        """
        Get command to write data to table
        """
        # Get latest read data
        self._load_data()
        self._get_latest_read()
        
        # Open data
        values = pickle_load(file_path = self.dump_path)
        values_to_update = values[self.last_row+1:]
        number_of_update = len(values_to_update)

        if number_of_update == 0:
            print(f"Data is already up to date! Last update on: {self.last_update}")
        else:
            print(f"Start updating the {number_of_update} data!")
            # Write commands
            for i, value in enumerate(tqdm(values_to_update)):
                # Get id
                id = self.last_row + i + 1

                # Add data record
                self._add_record(id = id,
                                value = value)
                
            # Write latest row to last_read table
            command = f"""
                INSERT INTO {self.table_last_read_name} VALUES (
                    {str(int(self.last_update_id)+1)}, 
                    {self.last_row + number_of_update}, 
                    '{self.table_data_name}'
                )
            """
            execute_command(command = command)

            print(f"Finish updating {number_of_update} data!")
