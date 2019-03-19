import boto3
import config

names = ['Name1', 'Name2']

session = boto3.Session(profile_name=config.aws_profile)
client = session.client('rekognition')


def create_collection():
  collection_response = client.create_collection(
    CollectionId=config.collection
  )
  print(collection_response)


def index():
  for name in names:
    indexing_response = client.index_faces(
      CollectionId=config.collection,
      Image={
        'S3Object': {
          'Bucket': config.bucket,
          'Name': '{0}.jpg'.format(name)
        }
      },
      ExternalImageId=name
    )
    print(indexing_response)


def deleteCollection(id):
  response = client.delete_collection(id)
  print(response['StatusCode'])


if __name__ == '__main__':
  # create_collection()
  index()
  # deleteCollection('HackDayFaces')
