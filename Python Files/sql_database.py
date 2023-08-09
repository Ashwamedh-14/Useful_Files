from mysql.connector import cursor, cursor_cext, errors
import datetime as dt

def exists(curr: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str, primary_key: str | int | float,
        primary_col: str) -> bool:
    
    if type(curr) not in (cursor.MySQLCursor, cursor_cext.CMySQLCursor):
        raise TypeError("Cursor should either be cursor.MySQLCursor or cursor_cext.CMySQLCursor")
    elif type(tablename) != str:
        raise TypeError("Tablename should be a string type")
    elif type(primary_key) not in (str, int, float):
        raise TypeError("Primary key should either be a string, float, or integer")
    elif type(primary_col) != str:
        raise TypeError("Primary column needs to be a string type")
    else:
        query = f"select * from {tablename.upper()} where {primary_col} = "
        query += "%s"
        curr.execute(query, (primary_key,))
        if curr.fetchone() == None:
            return False
        return True

def create_new_row(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str, *values: int | float | str) -> None:
    '''
    Cursor: Cursor object of the connected database
    Tablename: Name of table in which data is to be stored
    Values: Values you want to store

    This function assumes you know the structure of the table as well as its constraints
    If you have no value to pass in a particular column, pass None

    Raises TypeError if Correct type not passed
    '''
    if type(cursor_obj) != cursor.MySQLCursor and type(cursor_obj) != cursor_cext.CMySQLCursor:
        raise TypeError("Not the correct mysql cursor. It needs to be of type cursor.MySQLCursor")
    elif type(tablename) != str:
        raise TypeError("Tablename needs to be of type string")
    
    query = f"insert into {tablename.upper()} values("

    for i in values:
        print(i)
        if type(i) == int or type(i) == float or type(i) == str or i == None:
            query += "%s, "
        else:
            raise TypeError("The values should be either an integer, float or string")
    
    query = query[:-2] + ')'
    cursor_obj.execute(query, (*values,))


def create_new_row_colwise(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str,
                           cols: list[str], vals: list[int | float | str]):
    '''
    Cursor_Obj: Cursor Object for your mysql server
    Tablename: Name of table
    cols: Array of Columns in which data is to be inserted
    vals: Array of Values to be inserted (Pass dates as YYYY-MM-DD)

    ***NOTE :- values will added respective to the order of columns***

    Errors:
    TypeError if incorrect type is passed
    errors.ProgramingError if value passed in incorrect order, possible sql injection or server is not on
    errors.IntegrityError if primary key is not passed
    '''
    query = "insert into "
    if type(cursor_obj) not in (cursor.MySQLCursor, cursor_cext.CMySQLCursor):
        raise TypeError("Incorrect cursor type.")
    elif type(tablename) != str:
        raise TypeError("Tablename should be a string")
    elif type(cols) != list:
        raise TypeError("Cols should be an Array of columns in which data is to be inserted")
    elif type(vals) != list:
        raise TypeError("Vals should be an Array of values")
    else:
        query += tablename.upper() + '('
        for i in cols:
            if type(i) != str:
                raise TypeError("Column names should be strings")
            query += f"{i}, "
        
        query = query[0:-2] + ") values("

        for i in vals:
            if type(i) not in (int, float, str) and i != None:
                raise TypeError("Values should be either strings, floats or integeres")
            query += "%s, "
        query = query[0:-2] + ')'

        cursor_obj.execute(query, tuple(vals))


def number_of_rows(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str) -> int:
    '''
    Cursor_Obj: Cursor Object for your mysql server
    Tablename: Name of table

    Errors:
    TypeError if incorrect type is passed
    errors.ProgramingError if value passed in incorrect order, possible sql injection or server is not on
    '''
    if type(cursor_obj) not in (cursor.MySQLCursor, cursor_cext.CMySQLCursor):
        raise TypeError("Incorrect cursor type.")
    elif type(tablename) != str:
        raise TypeError("Tablename should be a string")
    else:
        count = cursor_obj.execute(f"select count(*) from {tablename.upper()}")
        return count[0]

def get_all(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str, *cols: str, condition: str | None = None) -> list[tuple[int | float | str | dt.datetime]]:
    '''
    Cursor_Obj: Cursor Object for your mysql server
    Tablename: Name of table
    cols: Column names of which you want the data\n
    Condition:- takes sql where condition. For example\n
                If you want to have data according to null vales in a column, you will pass in string:\n
                "column = null"\n
                If you want to have data according to not null values in a column, you will pass:\n
                "column != null"\n

    ***NOTE :- If you want all the columns just place '*'***

    Raises Following errors
    TypeError: Incorrect datatype passed
    ProgrammingError: Column not in the table mentioned
    ''' 
    query = "select "
    if type(cursor_obj) not in (cursor.MySQLCursor, cursor_cext.CMySQLCursor):
        raise TypeError("Incorrect cursor type.")
    elif type(tablename) != str:
        raise TypeError("Tablename should be a string")
    elif type(condition) != str and condition != None:
        raise TypeError("Condition should be either string type or NoneType")
    for i in cols:
        if type(i) != str:
            raise TypeError("Column names should be strings")
        query += f"{i}, "
    else:
        query = query[0:-2] + f" from {tablename.upper()}"
        if condition:
            query += f" where {condition}"
        cursor_obj.execute(query)
        return cursor_obj.fetchall()


def get_data(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor,tablename:str, primary_col: str,
            primary_key: str | int | float, *columns: str) -> tuple[str | int | float | dt.datetime, ...]:
    '''
    Cursor: Cursor object of the connected database
    Tablename: Name of table in which data is to be stored
    Primary_col: The primary column name
    primary_key: The value whose row data you want
    columns: The name of the columns whose data you want

    The data is returned in the order of columns passed

    Raises TypeError if incorrect type is passed
    '''

    query = "select "

    if type(cursor_obj) != cursor.MySQLCursor and type(cursor_obj) != cursor_cext.CMySQLCursor:
        raise TypeError("Not the correct mysql cursor. It needs to be of type cursor.MySQLCursor")
    elif type(tablename) != str:
        raise TypeError("Tablename needs to be of type string")
    elif type(primary_col) != str:
        raise TypeError("Primary column needs to be string")

    for i in columns:
        if type(i) == str:
            query += f"{i}"
        else:
            raise TypeError("All columns should be of string type")
        query += ", "

    query = query[:-2] + f" from {tablename.upper()} where {primary_col} = "
    
    if type(primary_key) == str or type(primary_key) == int or type(primary_key) == float:
        query += "%s"
    else:
        raise TypeError("Primary key needs to be either a string, float, or integer")
    
    cursor_obj.execute(query, (primary_key,))
    return cursor_obj.fetchone()


def update_data(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str, primary_col: str,
                primary_key: str | int | float, columns: list[str], values: list[str | float | int]) -> None:
    '''
    Cursor: Cursor object of the connected database
    Tablename: Name of table in which data is to be stored
    Primary_col: The primary column name
    primary_key: The value whose row data you want
    Columns: The name of columns where data is to be updated
    values: Values to be enterred

    ***
    NOTE: Values to be provided in the same order as columns provided
    ***
    '''

    if type(cursor_obj) != cursor.MySQLCursor and type(cursor_obj) != cursor_cext.CMySQLCursor:
        raise TypeError("Not the correct mysql cursor. It needs to be of type cursor.MySQLCursor")
    elif type(tablename) != str:
        raise TypeError("Tablename needs to be of type string")
    elif type(primary_col) != str:
        raise TypeError("Primary column needs to be a string")
    
    query = f"update {tablename.upper()} set "

    col = enumerate(columns)
    data_set = tuple()

    for i, j in col:
        if type(j) != str:
            raise TypeError("Column names should be of type string")
        else:
            query += f"{j} = "
        
        if type(values[i]) == str or values[i] == None or type(values[i]) == int or type(values[i]) == float:
            query += "%s, "
        else:
            raise TypeError("Values should be either a string, float or integer")
        data_set += (values[i],)

    query = query[:-2] + f" where {primary_col} = "
    if type(primary_key) == str or type(primary_key) == int or type(primary_key) == float:
        query += "%s"
    else:
        raise TypeError("Only string, integer or float values expected in Primary key")
    
    cursor_obj.execute(query, (*data_set, primary_key))



def delete_row(cursor_obj: cursor.MySQLCursor | cursor_cext.CMySQLCursor, tablename: str,
            primary_col: str, primary_key: str | int | float) -> None:
    '''
    Cursor: Cursor object of the connected database
    Tablename: Name of table in which data is to be stored
    Primary_col: The primary column name
    primary_key: The value of primary column whose row you want to delete
    '''

    
    if type(cursor_obj) != cursor.MySQLCursor and type(cursor_obj) != cursor_cext.CMySQLCursor:
        raise TypeError("Not the correct mysql cursor. It needs to be of type cursor.MySQLCursor")
    elif type(tablename) != str:
        raise TypeError("Tablename needs to be of type string")
    elif type(primary_col) != str:
        raise TypeError("Primary column needs to be string")
    if type(primary_key) == str or type(primary_key) == float or type(primary_key) == int:
        query = f"delete from {tablename.upper()} where {primary_col} = "
        query += "%s"
        cursor_obj.execute(query, (primary_key,))
    else:
        raise TypeError("Primary key needs to be a string, integer or a float")