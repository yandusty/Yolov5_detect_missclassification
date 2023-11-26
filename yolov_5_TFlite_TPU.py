import picamera
import picamera.array
import cv2
import numpy as np
import tensorflow as tf

# TFLite 모델 로드
interpreter = tf.lite.Interpreter(model_path="path/to/your/tflite_model.tflite")
interpreter.allocate_tensors()

# 입력 및 출력 텐서 인덱스 가져오기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# TPU를 사용하여 추론 수행하는 함수 정의
def infer_with_tpu(frame):
    # 입력 이미지 전처리
    input_shape = input_details[0]['shape']
    input_data = cv2.resize(frame, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(input_data, axis=0)
    input_data = input_data.astype(np.float32)

    # 입력 텐서에 데이터 로드
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # 추론 수행
    interpreter.invoke()

    # 출력 텐서에서 결과 가져오기
    output_data = interpreter.get_tensor(output_details[0]['index'])

    return output_data

# 경고 영역 및 클래스 설정
plastic_area = [(100, 100), (300, 300)]
plastic_class_index = 0  # 예시로 플라스틱 클래스 인덱스를 0으로 가정

# 카메라 초기화
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        # 카메라 설정
        camera.resolution = (640, 480)
        camera.framerate = 30

        # 동영상 프레임에 대한 루프
        for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
            # TPU를 사용하여 객체 감지 및 경고 트리거
            result = infer_with_tpu(frame.array)

            # 플라스틱 영역 화면에 표시
            cv2.rectangle(frame.array, plastic_area[0], plastic_area[1], (0, 0, 255), 2)

            # 결과 후처리
            output_class_index = np.argmax(result)
            if output_class_index == plastic_class_index:
                x, y, w, h = result[0]['box']

                # 플라스틱 영역과 객체 간의 교차 여부 확인
                if x >= plastic_area[0][0] and y >= plastic_area[0][1] and x + w <= plastic_area[1][0] and y + h <= plastic_area[1][1]:
                    cv2.rectangle(frame.array, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    # 경고: 플라스틱을 잘못된 위치에 놓았을 때
                    cv2.rectangle(frame.array, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    print("경고: 플라스틱을 올바른 위치에 놓아주세요!")

            # 결과 프레임 출력
            cv2.imshow('Result Frame', frame.array)

            # 스트림 초기화
            stream.truncate(0)

            # 'q' 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
