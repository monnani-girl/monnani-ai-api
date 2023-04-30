from fastapi import FastAPI,File, UploadFile, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import os
import operator
import base64
import json
from ai_module import face_detect, face_recognition
from models import crop

crop_router = APIRouter()

@crop_router.get("/")
async def hello():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]



@crop_router.post("/products")
async def upload_photo(req : crop.CropReqBody):
  farm_count_dict = {"pumpkin":0,"broccoli":0,"potato":0,"tangerine":0,"carrot":0,"cabbage":0}
  photo_weight = 5
  
  base64_data = req.photo
  image_data = base64.b64decode(base64_data)
  UPLOAD_DIR = "./img_data/out_img"
  filename = "src_face.jpg"
  with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
      f.write(image_data)
  # face detection    
  image, faces = face_detect.detect_faces(f'{UPLOAD_DIR}/src_face.jpg')
  if len(faces) == 0:
    return {"message" : "얼굴이 감지되지 않았습니다. 정면 사진을 사용해주세요."}
  if len(faces) != 1:
    return {"message" : '너무 많은 얼굴이 탐지되었습니다. 한명의 얼굴만 촬영해주세요.'}
  face = faces[0]
  image = image[face['startY'] : face['endY'], face['startX'] : face['endX']]
  face_detect.save(image)

  items = ["pumpkin", "broccoli","potato","tangerine","carrot","cabbage"]
  image_path2 = f'{UPLOAD_DIR}/detect_src_face.jpg'
  cand_dict = {}
  # 결과값이 작아야 같은 사람
  for item in items:  
    image_path1 = f'./img_data/crop_target/{item}.jpg'
    res = face_recognition.get_sim(image_path1, image_path2)
    cand_dict[item] = res
  tup = min(cand_dict.items(), key=operator.itemgetter(1))
  farm_count_dict[tup[0]] += photo_weight
    
  with open ("./db/crops_score.json","r") as f :
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
  
  translate_dict = {"carrot":"당근","pumpkin":"미니 밤호박","cabbage":"양배추","tangerine":"귤","broccoli":"브로콜리","potato":"감자"}
  
  #auote
  with open("./db/quote.json","r",encoding="utf-8") as f:
    data = json.load(f)
    for content in data:
      if translate_dict[result_farm] == content["product"]:
        result["nickname"] = content["nickname"]
        result["quote"] = content["quote"]
        
  products = []
  with open("./db/product.json","r", encoding="utf-8") as f :
    data =json.load(f)
    for content in data:
      if content["product"] == translate_dict[result_farm]:
        products.append(content)
  result["products"] = products
  
  
  return {"result" : result}