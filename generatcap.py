#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import image
from keras.models import load_model, Model
import matplotlib.pyplot as plt
import pickle
import numpy as np

import warnings
warnings.filterwarnings("ignore")



model = load_model("model_9.h5")
model.make_predict_function()

model_temp = ResNet50(weights="imagenet", input_shape=(224,224,3))

# Create a new model, by removing the last layer (output layer of 1000 classes) from the resnet50
model_resnet = Model(model_temp.input, model_temp.layers[-2].output)
model_resnet.make_predict_function()


    
# Load the word_to_idx and idx_to_word from disk

with open("word_to_idx.pkl", "rb") as w2i:
    word_to_idx = pickle.load(w2i)

with open("idx_to_word.pkl", "rb") as i2w:
    idx_to_word = pickle.load(i2w)
    

max_len = 35


def preprocess_image(img):
    img = image.load_img(img, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def encode_image(img):
    img = preprocess_image(img)
    feature_vector = model_resnet.predict(img)
    feature_vector = feature_vector.reshape(1, feature_vector.shape[1])
    return feature_vector



def predict_caption(photo):
    in_text = "startseq"

    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence], maxlen=max_len, padding='post')

        ypred =  model.predict([photo,sequence])
        ypred = ypred.argmax()
        word = idx_to_word[ypred]
        in_text+= ' ' +word

        if word =='endseq':
            break


    final_caption =  in_text.split()
    final_caption = final_caption[1:-1]
    final_caption = ' '.join(final_caption)

    return final_caption




def caption_this_image(input_img): 

    photo = encode_image(input_img)
    

    caption = predict_caption(photo)
    return caption

def extract(file_path):
    pdf_file = fitz.open(file_path)
    # STEP 3
# iterate over PDF pages
    for page_index in range(len(pdf_file)):
        text = pdf_file[page_index].get_text_words()
        words = ""
        for i in range(len(text)):
              words += text[i][4]+" "


        page = pdf_file[page_index]
        image_list = page.get_images()

        
        for image_index, img in enumerate(page.get_images(), start=1):

            # get the XREF of the image
            xref = img[0]

            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # get the image extension
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
            img_path =f"image{page_index+1}_{image_index}.{image_ext}"
            caption = caption_this_image(img_path)
            words+="the caption is "+caption+". "
    return words

            
            
