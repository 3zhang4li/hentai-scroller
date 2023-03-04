from ImageFetcher import ImageFetcher
from flask import Flask, render_template
from cryptography.fernet import Fernet
from dotenv import dotenv_values
from flask import Response
import urllib.request
import shutil 
import os 
import re 
import boto3
import glob

app = Flask(__name__)
config = dotenv_values(f".env")
raw = config.get("FERNET_KEY")
key = raw.encode("utf-8")
fernet = Fernet(key)

firstSec = config.get("APP_SECRET_1").encode("utf-8")
firstDec = fernet.decrypt(firstSec).decode()

IMAGES_FOLDER = os.path.join('static', firstDec)
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER

def saveImages(imageURLs, sauce):
  for i in range(len(imageURLs)):
    if (os.path.isfile(f"static/{firstDec}/{sauce}/{i}.png")):
      continue
    else:
      urllib.request.urlretrieve(imageURLs[i], f"static/{firstDec}/{sauce}/{i}.png")
  
@app.route('/')
def hello_world():
  path = f"static/{firstDec}"
  linkList = os.listdir(path)
  if os.path.isfile(f"static/{firstDec}/.DS_Store"):
    linkList.remove(".DS_Store")

  finalList = []
  for i in range(len(linkList)):
    finalList.append([linkList[i], f"{firstDec}/{linkList[i]}/0.png"])
  return render_template("home.html", finalList=finalList)

@app.route('/<sauce_id>')
def main(sauce_id):
  def imgCompare(img):
    try:
      match = re.search(rf"({firstDec}/)(" + sauce_id + r"/)(\d{1,3})(.png)", img)
      idx = int(match.groups()[2])
      return idx
    except re.error:
      print("Comparison error, defaulting to equal")
      return 0

  if not(os.path.exists(f"static/{firstDec}/{sauce_id}")):
    if sauce_id != "favicon.ico":
      os.makedirs(f"static/{firstDec}/{sauce_id}")
      fetcher = ImageFetcher()
      fetcher.setupDriver()
      fetcher.setSauce(sauce_id)
      images = fetcher.getImages()
      saveImages(images, sauce_id)

  try:
    imageList = os.listdir(f"static/{firstDec}/{sauce_id}")
  except FileNotFoundError:
    imageList = []

  imagelist = [f"{firstDec}/{sauce_id}/" + image for image in imageList]
  if os.path.isfile(f"{firstDec}/{sauce_id}/.DS_Store"):
    imagelist.remove(f"{firstDec}/{sauce_id}/.DS_Store")

  imagelist = sorted(imagelist, key=imgCompare)

  return render_template("index.html", imagelist=imagelist)


@app.route('/<sauce_id>/delete')
def delete(sauce_id):
  # Delete all files
  shutil.rmtree(f"static/{firstDec}/{sauce_id}")
  return Response(status=201)

app.run(port=1224)
