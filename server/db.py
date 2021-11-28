import aiosqlite


class Database:
    INSTANCE = None
    DATABASE_URL = 'shop.db'

    SELECT_ID = 'SELECT * FROM {table_name} WHERE {pk_name} = ?'
    SELECT_LIST = 'SELECT * FROM {table_name} {limit}'
    SELECT_COUNT = 'SELECT count(*) FROM ({subquery}) t'
    SELECT_SEARCH = '''
    WITH exact_match AS (
        SELECT *, 1 AS priority
        FROM {table_name}
        WHERE {search_field} = ?
    )
    SELECT * FROM exact_match
    UNION
    SELECT *, 2 AS priority
    FROM {table_name}
    WHERE
        {search_field} LIKE ?
        AND {pk_name} NOT IN (SELECT {pk_name} FROM exact_match)
    ORDER BY priority
    {limit}
    '''

    INSERT = 'INSERT INTO {table_name} ({field_list}) VALUES ({data_list})'
    UPDATE = 'UPDATE {table_name} SET {set_query} WHERE {pk_name} = ?'
    DELETE = 'DELETE FROM {table_name} WHERE {pk_name} = ?'

    def __new__(cls, *args, **kwargs):
        if not cls.INSTANCE:
            cls.INSTANCE = super().__new__(cls, *args, **kwargs)
        return cls.INSTANCE

    @staticmethod
    def dict_factory(cursor, row):
        result = {}
        for index, col in enumerate(cursor.description):
            result[col[0]] = row[index]
        return result

    @classmethod
    def get_select_query(cls, table_name, search_field, pk_name, search_string, limit, offset):
        limit_query = ''
        if limit:
            limit_query += f'LIMIT {limit} '
        if offset:
            limit_query += f'OFFSET {offset}'

        if search_string:
            query_text = cls.SELECT_SEARCH.format(
                table_name=table_name, search_field=search_field, limit=limit_query, pk_name=pk_name)
            search_string = search_string.lower()
            params = (search_string, f'%{search_string}%')
        else:
            query_text = cls.SELECT_LIST.format(table_name=table_name, limit=limit_query, pk_name=pk_name)
            params = tuple()
        return query_text, params

    async def read_record(self, table_name, pk_name, record_id):
        async with aiosqlite.connect(self.DATABASE_URL) as connect:
            connect.row_factory = self.dict_factory
            query_text = self.SELECT_ID.format(table_name=table_name, pk_name=pk_name)
            async with connect.execute(query_text, (record_id, )) as cursor:
                return await cursor.fetchone()

    async def create_record(self, table_name, pk_name, data):
        async with aiosqlite.connect(self.DATABASE_URL) as connect:
            field_list = ', '.join(data.keys())
            data_list = ', '.join('?' for _ in range(len(data)))
            query_text = self.INSERT.format(
                table_name=table_name, pk_name=pk_name, field_list=field_list, data_list=data_list)
            cursor = await connect.execute(query_text, tuple(data.values()))
            await connect.commit()
            return cursor.lastrowid

    async def update_record(self, table_name, pk_name, record_id, data):
        async with aiosqlite.connect(self.DATABASE_URL) as connect:
            set_query = ', '.join(f'{key} = ?' for key in data.keys())
            query_text = self.UPDATE.format(table_name=table_name, pk_name=pk_name, set_query=set_query)
            await connect.execute(query_text, (*data.values(), record_id))
            await connect.commit()

    async def delete_record(self, table_name, pk_name, record_id):
        async with aiosqlite.connect(self.DATABASE_URL) as connect:
            query_text = self.DELETE.format(table_name=table_name, pk_name=pk_name)
            await connect.execute(query_text, (record_id, ))
            await connect.commit()

    async def list(self, table_name, search_field, pk_name, search_string, limit, offset):
        async with aiosqlite.connect(self.DATABASE_URL) as connect:
            query_text, params = self.get_select_query(table_name, search_field, pk_name, search_string, limit, offset)
            connect.row_factory = self.dict_factory
            async with connect.execute(query_text, params) as cursor:
                return [row async for row in cursor]

    async def count(self, table_name, search_field, pk_name, search_string):
        async with aiosqlite.connect(self.DATABASE_URL) as connect:
            subquery_text, params = self.get_select_query(
                table_name, search_field, pk_name, search_string, limit=None, offset=None)
            query_text = self.SELECT_COUNT.format(subquery=subquery_text)
            async with connect.execute(query_text, params) as cursor:
                result = await cursor.fetchone()
                return result[0]
