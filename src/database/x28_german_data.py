from src.database.data_source import DataSource


class X28GermanData(DataSource):

    def create_where_clause(self, args):
        id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        return lambda row: (id < 0 or row.id == id) and row.language in [None, 'de']
