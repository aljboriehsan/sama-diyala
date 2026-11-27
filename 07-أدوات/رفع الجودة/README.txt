رفع جودة الصور ×2 بنموذج EDSR (OpenCV dnn_superres)، أفضل من التكبير العادي ويزيل تشويش JPEG.
يحتاج opencv-contrib-python-headless في بيئة منفصلة (لا يتعارض مع cv2 الموجود) والنموذج EDSR_x2.pb (38MB):
  python3 -m venv venv && ./venv/bin/pip install opencv-contrib-python-headless numpy
  curl -L -o EDSR_x2.pb https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x2.pb
  ./venv/bin/python edsr_x2.py <الصورة> <الناتج.png>    (قرابة 6 دقائق لصورة 1080×1080 على المعالج)
