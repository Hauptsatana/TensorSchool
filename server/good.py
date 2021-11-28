from db import Database


class Good:
    __slots__ = ('id', 'name', 'description', 'photo', 'price', 'search_name')

    TABLE_NAME = 'good'
    PK_FIELD = 'id'
    SEARCH_FIELD = 'search_name'

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __setattr__(self, key, value):
        """ Костыль, т.к. мой SQLite так и не запустился в режиме поиска без учета регистра. """
        if key == 'name' and value:
            self.search_name = value.lower()
        super().__setattr__(key, value)

    @classmethod
    async def by_id(cls, good_id):
        data = await Database().read_record(cls.TABLE_NAME, cls.PK_FIELD, good_id)
        if not data:
            raise IndexError
        return cls(**data)

    @classmethod
    async def get_list(cls, search_string, limit, offset):
        data = await Database().list(cls.TABLE_NAME, cls.SEARCH_FIELD, cls.PK_FIELD, search_string, limit, offset)
        return [cls(**row).to_json() for row in data]

    @classmethod
    async def get_count(cls, search_string):
        return await Database().count(cls.TABLE_NAME, cls.SEARCH_FIELD, cls.PK_FIELD, search_string)

    async def save(self):
        if self.id:
            await Database().update_record(self.TABLE_NAME, self.PK_FIELD, self.id, self.to_json(save_db=True))
        else:
            self.id = await Database().create_record(self.TABLE_NAME, self.PK_FIELD, self.to_json(save_db=True))
        return self.id

    async def delete(self):
        if not self.id:
            return
        await Database().delete_record(self.TABLE_NAME, self.PK_FIELD, self.id)

    def to_json(self, save_db=False):
        data = {key: getattr(self, key) for key in self.__slots__}
        if save_db:
            del data['id']
        else:
            del data['search_name']
        return data

    def update(self, new_data):
        for key, value in new_data.items():
            if key == 'id' or key not in self.__slots__:
                continue
            setattr(self, key, value)
