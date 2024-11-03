import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images = [
    ('ajo.jpeg', '2109012'),
    ('alexis.jpeg', '2009020'),
    ('angel.jpeg', '2109021'),
    ('carlo.jpeg', '2109058'),
    ('christopher.jpeg', '2109048'),
    ('hector.jpeg', '2109077'),
    ('juanito.jpeg', '2109061'),
    ('juliana.jpeg', '2109128'),
    ('karla.jpeg', '2109050'),
    ('luis.jpeg', '2109099'),
    ('miguel.jpeg', '2009009'),
    ('pris.jpeg', '2109148'),
    ('julio.jpeg', '2009048'),
    ('sam.jpeg', '2109028'),
    ('sansores.jpeg', '2109139'),
    ('sonia.jpeg', '2109104'),
    ('yahir.jpeg', '2109145'),
    ('antonio.jpeg', '2009121')
]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(f'images/{image[0]}', 'rb')
    object = s3.Object('upypersons-images', 'index/' + image[0])
    ret = object.put(Body=file, Metadata={'FullName': image[1]})






    
