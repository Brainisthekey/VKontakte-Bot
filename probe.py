import json
from io import BytesIO

import requests
from PIL import Image

response = requests.get(url='https://api.thecatapi.com/v1/images/search')
avatar = json.loads(response.content)[0]['url']
print(avatar)
avatar_file_like = BytesIO(requests.get(avatar).content)
print(avatar_file_like)
avatar_file = Image.open(avatar_file_like)
avatar_file.show()
size= (120, 120)
avatar_file.thumbnail(size)
avatar_file.show()




#base.past(avatar_file, AVATAR_OFFSET)
# base.show()
# avatar_file.show()
