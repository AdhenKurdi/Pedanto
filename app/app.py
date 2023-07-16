# =[Modules dan Packages]========================

from flask import Flask,render_template,request,jsonify
from werkzeug.utils import secure_filename
import numpy as np
import os
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from fungsi import get_model


# =[Variabel Global]=============================

app = Flask(__name__, static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS']  = ['.jpg','.JPG']
app.config['UPLOAD_PATH']        = './static/images/uploads/'

model = None

##NUM_CLASSES = 10
##leaf_classes = ["Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Healthy", "Tomato___Late_blight", "Tomato___Leaf_Mold", 
##		  		   "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites", "Tomato___Target_Spot", "Tomato___Mosaic_virus", "Tomato___Yellow_Leaf_Curl_Virus"]

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]
@app.route("/")
def beranda():
	return render_template('index.html')

@app.route("/index.html")
def HalamanUtama():
	return render_template('index.html')

@app.route("/Prediksi.html")
def prediksi():
	return render_template('Prediksi.html')

@app.route("/Informasi.html")
def Informasi():
	return render_template('Informasi.html')

@app.route("/Obat.html")
def Obat():
	return render_template('Obat.html')

@app.route("/Bacterial-spot.html")
def Bacterialspot():
	return render_template('Bacterial-spot.html')

@app.route("/early-bright.html")
def earlybright():
	return render_template('early-bright.html')

@app.route("/Late-Blight.html")
def LateBlight():
	return render_template('Late-Blight.html')

@app.route("/Spider-Mite.html")
def SpiderMite():
	return render_template('Spider-Mite.html')

@app.route("/LeafMold.html")
def LeafMold():
	return render_template('LeafMold.html')

@app.route("/SLS.html")
def SLS():
	return render_template('SLS.html')

@app.route("/TYLC.html")
def TYLC():
	return render_template('TYLC.html')

@app.route("/Mosaic-Virus.html")
def MosaicVirus():
	return render_template('Mosaic-Virus.html')

@app.route("/Target-Spot.html")
def TargetSpot():
	return render_template('Target-Spot.html')

@app.route("/Halaman-Obat2.html")
def HalamanObat2():
	return render_template('Halaman-Obat2.html')

@app.route("/Halaman-Bacterial-Spot.html")
def HalamanBacterialSpot():
	return render_template('Halaman-Bacterial-Spot.html')

@app.route("/Halaman-Early-blight.html")
def HalamanEarlyblight():
	return render_template('Halaman-Early-blight.html')

@app.route("/Halaman-Late-blight.html")
def HalamanLateblight():
	return render_template('Halaman-Late-blight.html')
	
@app.route("/Halaman-Leaf-Mold.html")
def HalamanLeafMold():
	return render_template('Halaman-Leaf-Mold.html')
	
@app.route("/Halaman-Septoria-leaf-spot.html")
def HalamanSeptorialeafspot():
	return render_template('Halaman-Septoria-leaf-spot.html')

@app.route("/Halaman-Spider-mites.html")
def HalamanSpidermites():
	return render_template('Halaman-Spider-mites.html')

@app.route("/Halaman-Target-Spot.html")
def HalamanTargetSpot():
	return render_template('Halaman-Target-Spot.html')
	
@app.route("/Halaman-Mosaic-Virus.html")
def HalamanMosaicVirus():
	return render_template('Halaman-Mosaic-Virus.html')

@app.route("/Halaman-Yellow-Leaf-Curl-Virus.html")
def HalamanYellowLeafCurlVirus():
	return render_template('Halaman-Yellow-Leaf-Curl-Virus.html')


# [Routing untuk API]	
@app.route("/api/deteksi",methods=['POST'])
def apiDeteksi():
	# Set nilai default untuk hasil prediksi dan gambar yang diprediksi
	hasil_prediksi  = '(none)'
	gambar_prediksi = '(none)'

	# Get File Gambar yg telah diupload pengguna
	uploaded_file = request.files['file']
	filename      = secure_filename(uploaded_file.filename)
	
	# Periksa apakah ada file yg dipilih untuk diupload
	if filename != '':
	
		# Set/mendapatkan extension dan path dari file yg diupload
		file_ext        = os.path.splitext(filename)[1]
		gambar_prediksi = '/static/images/uploads/' + filename
		
		# Periksa apakah extension file yg diupload sesuai (jpg)
		if file_ext in app.config['UPLOAD_EXTENSIONS']:
			
			# Simpan Gambar
			uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
			
			# Memuat Gambar
			img = Image.open('.' + gambar_prediksi)
			
			# Mengubah Ukuran Gambar
			##img = img.resize((256, 256, 3))
			
			# Konversi Gambar ke Array
			##img_array   = np.array(img)
			#x = image.img_to_array(img)
			#x = np.expand_dims(x, axis=0)
			image = np.asarray(img)
			
		# Prediksi Gambar
		##pred	= model.predict(x)
		pred	= np.argmax(model.predict(image.reshape(-1,256,256,3)/255))
		print ("pred:",pred)
		if pred==0:
			hasil_prediksi =("Bacterial Spot")
		elif pred==1:
			hasil_prediksi =("Early Blight")
		elif pred==2:
			hasil_prediksi =("Healthy")
		elif pred==3:
			hasil_prediksi =("Late Blight")
		elif pred==4:
			hasil_prediksi =("Leaf Mold")
		elif pred==5:
			hasil_prediksi =("Mosaic Virus")
		elif pred==6:
			hasil_prediksi =("Septoria Leaf Spot")
		elif pred==7:
			hasil_prediksi =("Spider Mites")
		elif pred==8:
			hasil_prediksi =("Target Spot")
		else:
			hasil_prediksi =("Yellow Leaf Curl Virus")

			
			
		# Return hasil prediksi dengan format JSON
		return jsonify({
			"prediksi": hasil_prediksi,
			"gambar_prediksi" : gambar_prediksi
			})
	else:
		# Return hasil prediksi dengan format JSON
		gambar_prediksi = '(none)'
		return jsonify({
			"prediksi": hasil_prediksi,
			"gambar_prediksi" : gambar_prediksi
			})

# =[Main]========================================		

if __name__ == '__main__':
	
	# Load model yang telah ditraining
	model = get_model()
	model.load_weights("model_resnet152V2.h5")

	# Run Flask di localhost 
	app.run(host="localhost", port=5001, debug=True)