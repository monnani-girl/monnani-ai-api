from typing import Optional

from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import predict
import os
import operator
from pydantic import BaseModel

import base64
import json

import face_detect

app = FastAPI()

origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Req(BaseModel):
    season: str
    weather: str
    feel: str
    travel: str
    photo : str

@app.get("/")
def hello():
  return {"message":"monnani v0.9", "docker_img_tag":3}


@app.post("/result/product")
async def upload_photo(req : Req):
  farm_count_dict = {"pumpkin":0,"broccoli":0,"potato":0,"tangerine":0,"carrot":0,"cabbage":0}
  photo_weight = 5
  
  base64_data = req.photo
  image_data = base64.b64decode(base64_data)
  UPLOAD_DIR = "./outImg"
  filename = "result.jpg"
  with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
      f.write(image_data)
  # face detection    
  image, faces = face_detect.detect_faces('./outImg/result.jpg')
  if len(faces) == 0:
    return {"message" : "아무 얼굴도 탐지되지 않았습니다. 정면 사진을 넣어주세요."}
  if len(faces) != 1:
    return {"message" : '너무 많은 얼굴이 탐지되었습니다. 정확히 한 명만 나온 사진을 넣어주세요.'}
  face = faces[0]
  image = image[face['startY'] : face['endY'], face['startX'] : face['endX']]
  face_detect.save(image)

  items = ["pumpkin", "broccoli","potato","tangerine","carrot","cabbage"]
  image_path2 = "./outImg/detect_result.jpg"
  cand_dict = {}
  # 결과값이 작아야 같은 사람
  for item in items:  
    image_path1 = f"./data/{item}.jpg"
    res = predict.get_sim(image_path1, image_path2)
    cand_dict[item] = res
  tup = min(cand_dict.items(), key=operator.itemgetter(1))
  farm_count_dict[tup[0]] += photo_weight
    
  with open ("./dummy.json","r") as f :
    data = json.load(f)
    
    for k,v in data.items():
      category_dict = v["category"]
      if k =="season":
        arr = category_dict[req.season]
        for item in arr:
          farm_count_dict[item] += v["weight"]
      elif k =="weather":
        arr = category_dict[req.weather]
        for item in arr:
          farm_count_dict[item] += v["weight"]
      elif k =="feel":
        arr = category_dict[req.feel]
        for item in arr:
          farm_count_dict[item] += v["weight"]
      else:
        arr = category_dict[req.travel]
        for item in arr:
          farm_count_dict[item] += v["weight"]

  result_tup = max(farm_count_dict.items(), key=operator.itemgetter(1))
  result_farm = tup[0]
  result = {}
  result["type"]=result_farm
  sales = []
  translate_dict = {"carrot":"당근","pumpkin":"미니 밤호박","cabbage":"양배추","tangerine":"귤","broccoli":"브로콜리","potato":"감자"}
  with open("./sales.json","r", encoding="utf-8") as f :
    data =json.load(f)
    for content in data:
      if content["product"] == translate_dict[result_farm]:
        sales.append(content)
  result["sales"] = sales
    
  return result