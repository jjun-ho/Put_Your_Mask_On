# Put_Your_Mask_On

dlib 얼굴 인식 라이브러리르 이용해 얼굴의 랜드마크를 저장하고,
마스크를 쓰지않은 사람을 인식하고 인식된 사람에게 가상으로 마스크를 착용시키며 경고 문구를 화면에 출력하며 마스크 착용을 유도.
마스크를 착용하지 않은 사람이 인식 되었을 때만 경고음을 출력하고 화면이 녹화됨.

key '0' : Mode0, 기본 카메라 모드. 

key '1' : Mode1, 얼굴 인식 모드.

key '2' : Mode2, 마스크 착용 모드.

key 'b' : 경고음 ON/OFF.

key 'c' : 녹화 ON/OFF.

key 'esc' : esc 종료.

실행전 opencv / dlib(+face_landmarks.dat) 다운.
