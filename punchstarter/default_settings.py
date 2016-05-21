import os
import cloudinary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = os.environ.get('DEBUG', True)
SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI',"sqlite:///"+ BASE_DIR + "/app.db")
SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS',True)
CLOUDINARY_CLOUD_NAME=os.environ.get('CLOUDINARY_CLOUD_NAME',"papajo")
CLOUDINARY_API_KEY=os.environ.get('CLOUDINARY_API_KEY',"222585141824773")
CLOUDINARY_API_SECRET=os.environ.get('CLOUDINARY_API_SECRET',"Ery2sWQZNsUvo5wqwnESC7yohJY")

SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_EMAIL_SENDER = 'Punchstarter'

cloudinary.config(
  cloud_name = CLOUDINARY_CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRET
)
