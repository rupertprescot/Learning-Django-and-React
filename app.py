from pprint import pprint

from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

bucket = config.bucket

session = boto3.Session(profile_name=config.aws_profile)

s3 = session.client('s3')

objects = s3.list_objects(Bucket=bucket)
image_urls = {}
for key in objects['Contents']:
  name = key['Key'].rsplit('.', 1)[0]
  image_urls[name] = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key['Key']}, ExpiresIn=3600)

client = session.client('rekognition')


def find_in_collection(source_file):
  collection_id = config.collection
  response = client.search_faces_by_image(
    CollectionId=collection_id,
    Image={
      'Bytes': source_file.read()
    }
  )
  pprint(response)
  results = []

  if response['FaceMatches']:
    for faceMatch in response['FaceMatches']:
      name = faceMatch['Face']['ExternalImageId']
      similarity = str(faceMatch['Similarity'])
      results.append({
        'message': "The face matches {0} with {1}% confidence".format(name, similarity),
        'name': name
      })
  else:
    results.append({
      'message': "The face doesn't match any of our images: {0}".format(response)
    })

  return results


@app.route("/collection_images", methods=['GET'])
def get_images_from_s3():
  return jsonify(image_urls)


@app.route("/find_image", methods=['POST'])
def image():
  source_file = request.files['image']
  results = find_in_collection(source_file)
  return jsonify(results)


if __name__ == '__main__':
  app.run(debug=True)
