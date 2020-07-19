if __name__ == "__main__":
    import pandas
    pd = pandas.read_csv('/Users/feng/downloads/postcodes.csv')

    first_postcodes = list(set(map(lambda x: x[:3], list(pd['Postcode']))))
    result_df = pandas.DataFrame(first_postcodes, columns=['first_postcode'])
    result_df.to_csv('first_postcodes.csv')
