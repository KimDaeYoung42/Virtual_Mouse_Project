# Virtual_Mouse_Project

![image](https://github.com/KimDaeYoung42/Virtual_Mouse_Project/assets/130177839/d558befc-19d4-4c75-8dec-b71e37e1b7e7)
![서버 파일전송](https://github.com/KimDaeYoung42/Virtual_Mouse_Project/assets/130177839/f8127749-ccea-4e62-8627-07ec41ec210d)


## 공지 
This project code is old code.       
Check out the project code on the link below.      
이 프로젝트 코드는 구 코드입니다. 아래 링크의 프로젝트 코드를 확인하십시오.    
https://github.com/KimDaeYoung42/Virtual_Mouse_Project-Network-Plus    


------------------------------------
## [Project development schedule]    
● Development Phase 1 : 2023.6.1 ~ 7.14    

## 코드 설명 (Code Description)

### 1. main.py     
The starting point of the program     
프로그램 시작점      

### 2. App.py (UI_App_Main.ui, UI_App_Main.py, icon_toolbar.py interlocking)     
Main Program (Junction)    
메인 프로그램 (분기점)      

### 3. App_Active.py (UI_App_WebCam.ui, UI_App_WebCam.py interlocking)     
Virtual Mouse, Keyboard Gesture Code   
가상 마우스, 키보드 제스처 코드       

#### 3.1 MouseModule.py     
Detailed code for each mouse function (modified)    
각 마우스 기능 (모듈화) 세부 코드       

### 4. HandTrackingModule.py     
Hand tracking module code    
핸드 트래킹 모듈 코드         

### 5. Network_Con.py     
Network-related code    
네트워크 관련 코드 

### 99. App_Help.py    
Contact, development team information   
연락처, 개발팀 정보

 -------------------------------------------
## Gesture function    
### Common features / two-handed gestures    
0. Deactivation event    
1.1 / 2.1 Mouse Move Event    

### 1. Left hand gesture standards    
1.2 Left-click related to mouse (No. 1 Left-click / Left-Press (Continue Press)    
1.3 Left mouse double click event (left click 2)    
1.4 Mouse Drag and Drop Events    
1.5 mouse scrolling magnification and reduction events    
1.5.1 Screen Scroll - Perform a Zoom Operation    
1.5.2 Scrolling Screen - Performing a Shrinking Operation    

### 2. Based on right hand gestures    
2.2 Right-click event (1 right-click / right press)    
2.3 Window zoom event    
2.4 Keyboard functionality Image keyboard on (puppy fingers only)    

 -------------------------------------------
## 제스처 기능      
### 공통 기능 / 양손 제스처           
0. 행동 해제 이벤트     
1.1 / 2.1 마우스 이동 이벤트     

### 1. 왼손 제스처 기준      
1.2 마우스 좌클릭 관련 (1번 좌클릭 / 좌 프레스(계속 누르는) )     
1.3 마우스 좌 더블클릭 이벤트 (2번 좌클릭)     
1.4 마우스 드래그 and 드롭 이벤트     
1.5 마우스 스크롤 확대 및 축소 이벤트     
1.5.1 화면 스크롤 - 확대 동작 수행     
1.5.2 화면 스크롤 - 축소 동작 수행     

### 2. 오른손 제스처 기준 
2.2 마우스 우클릭 이벤트 (1번 우클릭 / 우 프레스 (계속 누르는) )     
2.3 윈도우 창 확대 축소 이벤트     
2.4 키보드 기능 화상키보드 켜기 (새끼손가락만) 
