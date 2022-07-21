def get_parser(type, **kwargs):
    from federatedscope.db.parser.parser import SQLParser
    return SQLParser(**kwargs)
