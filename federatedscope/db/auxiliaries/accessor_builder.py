def get_accessor(type, **kwargs):
    if type == 'csv':
        from federatedscope.db.accessor.csv_accessor import CsvAccessor
        return CsvAccessor(**kwargs)
    else:
        raise NotImplementedError(
            f'Does not support data in {type} currently.')
