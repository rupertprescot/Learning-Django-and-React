import configparser

import boto3

database = [{
  'image': 'Beatrice.jpg',
  'id': '123',
  'name': 'Beatrice'
}, {
  'image': 'Sonia.jpg',
  'id': '568',
  'name': 'Sonia'
}]

config = configparser.ConfigParser()
config.read('settings.cfg')
session = boto3.Session(profile_name=config['aws']['AWS_PROFILE'])
client = session.client('rekognition')


def create_collection():
  collection_response = client.create_collection(
    CollectionId='HackDayFaces'
  )
  print(collection_response)


def index():
  for faceData in database:
    # image = open(faceData['image'], 'rb')
    indexing_response = client.index_faces(
      CollectionId='HackDayFaces',
      Image={
        # 'Bytes': image.read()
        'S3Object': {
          'Bucket': 'com-elsevier-hackdays-march-2019-faces-emma-rupert',
          'Name': faceData['image']
        }
      },
      ExternalImageId=faceData['name']
    )
    print(indexing_response)
    # image.close()


def deleteCollection(id):
  response = client.delete_collection(id)
  print(response['StatusCode'])


if __name__ == '__main__':
  # create_collection()
  index()
  # deleteCollection('HackDayFaces')
  # aws:rekognition:eu-west-1:324315958165:collection/HackDayFaces
  # {'FaceRecords': [{'Face': {'FaceId': '253ec7f3-d829-4f06-9f7a-35fb1fe87a84', 'BoundingBox': {'Width': 0.3334830403327942, 'Height': 0.452055960893631, 'Left': 0.35590916872024536, 'Top': 0.1682734191417694}, 'ImageId': '666122bd-6fe4-34fa-a521-c75f6eca59dc', 'ExternalImageId': 'Sonia', 'Confidence': 100.0}, 'FaceDetail': {'BoundingBox': {'Width': 0.3334830403327942, 'Height': 0.452055960893631, 'Left': 0.35590916872024536, 'Top': 0.1682734191417694}, 'Landmarks': [{'Type': 'eyeLeft', 'X': 0.4154892563819885, 'Y': 0.36682990193367004}, {'Type': 'eyeRight', 'X': 0.555491030216217, 'Y': 0.33295175433158875}, {'Type': 'mouthLeft', 'X': 0.4649885892868042, 'Y': 0.506281316280365}, {'Type': 'mouthRight', 'X': 0.5812823176383972, 'Y': 0.4785038232803345}, {'Type': 'nose', 'X': 0.49358057975769043, 'Y': 0.4298785924911499}], 'Pose': {'Roll': -18.490812301635742, 'Yaw': -17.797761917114258, 'Pitch': 2.1784143447875977}, 'Quality': {'Brightness': 69.29369354248047, 'Sharpness': 46.02980041503906}, 'Confidence': 100.0}}], 'FaceModelVersion': '4.0', 'UnindexedFaces': [], 'ResponseMetadata': {'RequestId': '2c3c532f-4990-11e9-ab15-f1f17285a3a2', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Mon, 18 Mar 2019 15:11:57 GMT', 'x-amzn-requestid': '2c3c532f-4990-11e9-ab15-f1f17285a3a2', 'content-length': '998', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
  # {'FaceRecords': [{'Face': {'FaceId': '248c34f2-b104-41f3-a900-dd3850a8f341', 'BoundingBox': {'Width': 0.7153925895690918, 'Height': 0.7541715502738953, 'Left': 0.14574430882930756, 'Top': 0.16000407934188843}, 'ImageId': 'fdf17423-4ef3-33fd-9fde-dcb88d217ba4', 'ExternalImageId': 'Beatrice', 'Confidence': 99.9996337890625}, 'FaceDetail': {'BoundingBox': {'Width': 0.7153925895690918, 'Height': 0.7541715502738953, 'Left': 0.14574430882930756, 'Top': 0.16000407934188843}, 'Landmarks': [{'Type': 'eyeLeft', 'X': 0.30690643191337585, 'Y': 0.46734559535980225}, {'Type': 'eyeRight', 'X': 0.643059492111206, 'Y': 0.4535500109195709}, {'Type': 'mouthLeft', 'X': 0.35417690873146057, 'Y': 0.7363496422767639}, {'Type': 'mouthRight', 'X': 0.6315929293632507, 'Y': 0.7249525189399719}, {'Type': 'nose', 'X': 0.4743560254573822, 'Y': 0.5971735119819641}], 'Pose': {'Roll': -3.5206496715545654, 'Yaw': -0.4118121862411499, 'Pitch': 5.058844566345215}, 'Quality': {'Brightness': 89.91715240478516, 'Sharpness': 89.85481262207031}, 'Confidence': 99.9996337890625}}], 'FaceModelVersion': '4.0', 'UnindexedFaces': [], 'ResponseMetadata': {'RequestId': '2c79d1b3-4990-11e9-b68a-c7de48ffb71b', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Mon, 18 Mar 2019 15:11:58 GMT', 'x-amzn-requestid': '2c79d1b3-4990-11e9-b68a-c7de48ffb71b', 'content-length': '1027', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
