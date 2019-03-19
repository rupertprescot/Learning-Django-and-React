import configparser
from pprint import pprint

from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('settings.cfg')
CORS(app, resources={r"/*": {"origins": "*"}})

session = boto3.Session(profile_name=config['aws']['AWS_PROFILE'])
client = session.client('rekognition')


def find_in_collection(source_file):
  collection_id = 'HackDayFaces'
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


@app.route("/find_image", methods=['POST'])
def image():
  source_file = request.files['image']
  results = find_in_collection(source_file)
  return jsonify(results)


if __name__ == '__main__':
  app.run(debug=True)
