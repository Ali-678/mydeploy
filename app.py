#!/usr/bin/env python
# coding: utf-8

# In[8]:


from generatcap import *
import fitz # PyMuPDF
import io
from PIL import Image
def extract_text_caption_image(file_path):
    words = ""
    pdf_file = fitz.open(file_path)

    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        text = pdf_file[page_index].get_text_words()
        for i in range(len(text)):
            words += text[i][4]+" "
      # get the page itself
        image_list = page.get_images()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image = np.array(image)
            words+="the caption(( "+caption_this_image_for_pdf(image)+")) "
    return words


# In[ ]:


from flask import Flask, render_template, url_for, request, redirect,flash,session
import warnings
warnings.filterwarnings("ignore")
# from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = 'AJDJRJS24$($(#$$33--' #<--- SECRET_KEY must be set in 
@app.route('/')
def hello():
    session['secrrt']='sec'
    return render_template('index.html')



@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pdf-file' in request.files:
            pdf_file = request.files['pdf-file']
            if pdf_file.filename == '':
                flash('No pdf file selected')
                return redirect(request.url)
            if pdf_file and allowed_file(pdf_file.filename):
        #         file = secure_filename(pdf_file.filename)
                pdf_file.save("static/"+pdf_file.filename)
                caption = extract_text_caption_image("static/"+pdf_file.filename)
                result_dic = {

                    'description' : caption
                }
            return render_template('index.html', results = result_dic)
        else:
            img_file = request.files['img-file']
            if img_file.filename == '':
                flash('No image file selected')
                return redirect(request.url)
            if img_file and allowed_file(img_file.filename):
                img_file.save("static/"+img_file.filename)
                caption = caption_this_image("static/"+img_file.filename)
            
                result_dic = {

                    'description' : caption
                }
            return render_template('index.html', results = result_dic)
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug = True,use_debugger=False, use_reloader=False)


# In[ ]:




