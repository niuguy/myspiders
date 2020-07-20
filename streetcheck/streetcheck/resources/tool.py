if __name__ == "__main__":
    # from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    # storage_client = storage.Client()

    # # Make an authenticated API request
    # buckets = list(storage_client.list_buckets())
    # print(buckets)
    import boto3

    s3 = boto3.resource('s3', aws_access_key_id='AKIAZYWRGTF4CF24HLWY',
                         aws_secret_access_key='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')
    bucketname = 'scraper-tfw'
    filename = 'reading_postcodes.csv'
    obj = s3.Object(bucketname, filename)
    body = obj.get()['Body'].read()
    # s3_file = s3.Bucket(bucketname).download_file(filename, 's3-file.csv')
    print(body)
    # # Output the bucket names
    # with open('reading_postcodes.csv', 'wb') as f:
    #     s3.download_fileobj('scraper-tfw', 'reading_postcodes.csv', f)                
