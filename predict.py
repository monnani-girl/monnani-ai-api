import argparse
import cv2
import numpy as np
import os
import torch

from src import models, preprocess


def get_image_tensor(image_path: str, device, transforms) -> torch.Tensor:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError('Missing or corrupt image: {}'.format(image_path))

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(transforms(image))
    
    image = image.transpose(2, 0, 1).astype(np.float32)[np.newaxis, ...]
    return torch.from_numpy(image).to(device)


def predict(image_path1, image_path2, model, transforms, device, threshold):
    images1 = get_image_tensor(image_path1, device, transforms)
    images2 = get_image_tensor(image_path2, device, transforms)

    pred = 0
    with torch.no_grad():
        feats1, feats2 = model(images1, images2)
        dist = torch.nn.functional.pairwise_distance(feats1, feats2)
        dist = dist.data.cpu().numpy()[0]
        if dist < threshold:
            pred = 1
    return dist, pred


def get_model(device, weight_path):
    model = models.SiameseNet(160).to(device)
    model.train(False)
    model.eval()

    if not os.path.exists(weight_path):
        raise FileNotFoundError('The weights must be present at: {}'.format(weight_path))
    state_dict = torch.load(weight_path)
    model.load_state_dict(state_dict)
    return model



def get_sim(image_path1, image_path2):  
    gpu = -1
    weight_path = "weights/face-siamese-crop.pt"
    threshold = 1.8
    
    # Get the device
    device = 'cpu'
    if gpu >= 0:
        device = 'cuda:{}'.format(gpu)

    # Initialize model and pre-processor
    model = get_model(device, weight_path)
    transforms = preprocess.get_transforms_inference()

    # Predict!
    prob, pred = predict(
        image_path1=image_path1,
        image_path2=image_path2,
        model=model,
        transforms=transforms,
        device=device,
        threshold=threshold,
    )

    print('Dis-similarity score: {:.2f}'.format(prob))
    if pred == 1:
        print('Same person!')
        # return 'same'
    else:
        print('Not the same person!')
        # return 'not same'
    return prob

def main():
    # res = get_sim("./data/potato.jpg", "./data/potato.jpg")
    print("============")
    # print(res)
    
if __name__ == '__main__':
    main()
