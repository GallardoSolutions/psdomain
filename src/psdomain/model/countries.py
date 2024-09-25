def normalize_country(values, field='fobCountry'):
    try:
        if values[field]:
            values[field] = values[field].upper()
            if values[field] == 'CHINA':
                values[field] = 'CN'
            elif values[field] == 'USA':
                values[field] = 'US'
    except ValueError:
        raise ValueError(f"Invalid country value: {values[field]}")
    return values
