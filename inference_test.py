import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image

# 이미지 전처리 함수
def preprocess_input(image, input_shape):
    image = image.resize(input_shape[:2], Image.ANTIALIAS)
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
    image_array = tf.expand_dims(image_array, axis=0)
    return image_array

# TensorFlow Lite 모델 로드
interpreter = tflite.Interpreter(model_path='converted_model_edgetpu.tflite')

# 입력 텐서의 정보 가져오기
input_details = interpreter.get_input_details()
input_shape = input_details[0]['shape']

# 모델에 따라 다른 크기의 입력을 사용하고 싶을 때
target_size = (input_shape[1], input_shape[2])

# 이미지 전처리
image_path = 'input_image.jpg'
image = Image.open(image_path)
input_data = preprocess_input(image, target_size)

# Edge TPU Delegate 추가
interpreter.allocate_tensors()

# Edge TPU Delegate를 사용하기 위해 설정
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.set_delegate(tflite.load_delegate('libedgetpu.so.1'))  # Edge TPU Delegate 로드

# 추론 실행
interpreter.invoke()

# 결과 얻기
output_details = interpreter.get_output_details()
output_data = interpreter.get_tensor(output_details[0]['index'])

# 결과 출력
print("Inference result:", output_data)
