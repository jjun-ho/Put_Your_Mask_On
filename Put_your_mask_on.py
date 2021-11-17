import cv2
import dlib
import numpy as np
from playsound import playsound
from PIL import ImageFont, ImageDraw, Image
import datetime

mode_a = 0
mode_b = False
mode_c = False
color = (190, 190, 190)

is_record = False    # 녹화상태는 처음엔 거짓으로 설정
on_record =False
cnt_record = 0      # 영상 녹화 시간 관련 변수
max_cnt_record = 5  # 최소 촬영시간

fourcc = cv2.VideoWriter_fourcc(*'XVID')    # 영상을 기록할 코덱 설정
font = ImageFont.truetype('fonts/SCDream6.otf', 20) # 글꼴파일을 불러옴

#웹캠으로부터 영상을 가져옴.
# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#얼굴 검출을 위해 디폴트 얼굴 검출기 사용.
detector = dlib.get_frontal_face_detector()
#검출된 얼굴에서 눈,코,입 같은 랜드마크를 찾기위해 사용할 학습모델 로드.
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#부위별로 분리하여 출력할 수 있도록 각 부위별로 리스트 정의.
ALL = list(range(0, 68))
RIGHT_EYEBROW = list(range(17, 22))
LEFT_EYEBROW = list(range(22, 27))
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
NOSE = list(range(27, 36))
MOUTH_OUTLINE = list(range(48, 61))
MOUTH_INNER = list(range(61, 68))
JAWLINE = list(range(0, 17))
#초기값 = 전체 랜드마크 보여줌.
index = ALL

#얼굴 인식 랜드마크 출력 함수.
def landmark():
    for i, pt in enumerate(list_points[index]):
        pt_pos = (pt[0], pt[1])
        cv2.circle(img_frame, pt_pos, 2, (255, 255, 0), -1)
    cv2.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),(255, 255, 255), 3)

#웹캠으로부터 입력을 받기 위해 무한반복.
while True:
    # 현재시각을 불러와 문자열로저장
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')  # 파일이름으로는 :를 못쓰기 때문에 따로 만들어줌

    ret,img_frame = cap.read()                             #웹캠으로부터 이미지 불러옴.
    img_frame =  cv2.flip(img_frame, 1)                    #이미지 반전.
    img_gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY) #그레이스케일로 변환.

    faces = detector(img_gray, 1) #얼굴 검출, 두번쨰 인자-업샘플링(이미지확대) 횟수.
    #검출된 얼굴 갯수만큼 반복.
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        # Mode0
        if mode_a == 0:
            cv2.imshow("Put Your Mask On",img_frame)
        # Mode1
        elif mode_a == 1:
            shape = predictor(img_gray, face)  # 얼굴에서 68개 점 찾기. #여기
            # 검출된 랜드마크 리스트에 저장.
            list_points = []
            for p in shape.parts():
                list_points.append([p.x, p.y])
            # 리스트를 넘파이 배열로 변환.
            list_points = np.array(list_points)
            landmark()
        #Mode2
        elif mode_a == 2:
            landmarks = predictor(img_gray, face)
            points = []
            for n in range(1, 16):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                point = (x, y)
                points.append(point)
                cv2.circle(img_frame, (x, y), 2, (255, 255, 0), -1)

            mask_c = [((landmarks.part(29).x), (landmarks.part(29).y))]
            fmask_c = points + mask_c
            fmask_c = np.array(fmask_c, dtype=np.int32)
            cv2.polylines(img_frame, [fmask_c], True, color, thickness=2, lineType=cv2.LINE_8)
            cv2.fillPoly(img_frame, [fmask_c], color, lineType=cv2.LINE_AA)
            if mode_b == True:
                playsound("beep.MP3")
            # 글자가 잘보이도록 배경 추가.
            cv2.rectangle(img=img_frame, pt1=(10, 15), pt2=(410, 35), color=(0, 0, 0), thickness=-1)
            img_frame = Image.fromarray(img_frame)
            draw = ImageDraw.Draw(img_frame)
            draw.text(xy=(10, 15), text=nowDatetime + "  마스크 착용해 주세요 ", font=font, fill=(255, 255, 255))
            img_frame = np.array(img_frame)

            if mode_c == True:
                if len(faces):  #마스크를 착용하지 않은 사람 인식 될 때.
                    is_record = True  # 녹화 준비
                    if on_record == False:
                        video = cv2.VideoWriter("Put Your Mask On " + nowDatetime_path + ".avi", fourcc, 1,
                                                (img_frame.shape[1], img_frame.shape[0]))
                    cnt_record = max_cnt_record

                if is_record == True:  # 녹화중이면.
                    print('녹화 중')
                    video.write(img_frame)  # 현재 프레임 저장.
                    cnt_record -= 1  # 녹화시간 1 감소.
                    on_record = True  # 녹화중 여부를 참으로.
                if cnt_record == 0:  # 녹화시간이 다 되면.
                    is_record = False  # 녹화관련 변수들을 거짓으로.
                    on_record = False

    cv2.imshow("Put Your Mask On", img_frame)

    key = cv2.waitKey(1)
    if key == 27:         #esc 종료
        break
    elif key == ord('0'):  #Mode0, 기본 카메라 모드.
        mode_a = 0
    elif key == ord('1'):  #Mode1, 얼굴 인식 모드.
        index = ALL
        mode_a = 1
    elif key == ord('2'):  #Mode2, 마스크 착용 모드.
        mode_a = 2
    elif key == ord('b'):
        mode_b = not mode_b  #경고음 ON/OFF.
    elif key == ord('c'):
        mode_c = not mode_c  #녹화 ON/OFF.

cap.release()
cv2.destroyAllWindows()
