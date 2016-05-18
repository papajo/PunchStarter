import os
import cloudinary

DEBUG=True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/app.db'

cloudinary.config(
  cloud_name = "papajo",
  api_key = "222585141824773",
  api_secret = "Ery2sWQZNsUvo5wqwnESC7yohJY"
)
