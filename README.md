# 첫번째 프로젝트 - fruitStore

## Problem Statement

- 한개의 주문에 여러 개의 상품이 있을 경우 어떻게 해야 하는지
- 상품정보고시 내용을 DB에 저장 해야 하는지
- 무통장입금 계좌를 저장해야 하는지

## Requirements



- 유저 관련 기능
    - 회원가입
    - 로그인
- 관리자 기능
    - 상품
        - 조회, 등록, 수정, 삭제
            - S3에 이미지 업로드
    - 주문
        - 등록, 수정, 삭제
- 일반 유저 기능
    - 상품
        - 조회
        - 리뷰 생성, 수정, 삭제
    - 장바구니
        - 제품 담기, 빼기
    - 주문
        - 생성 및 취소요청
    - 결제
        - 생성, 조회

### 개발 조건



- REST API에서 벗어난 Param 또는 요청 오류에 대한 응답처리
- 정보 입력, 수정 시 데이터, 형식의 유효성 검사
- 데이터 조회 결과는 JSON으로 응답

### Cutsomize



- 결제 API에 대한 응답은 임의로  Success, Fallure 으로 지정 각 케이스에 대해서 다룰것.
- 이미지 저장은 S3 ****업로드****
- DB는 RDS상에서

## Non-Requirements

- QnA
    - 등록, 수정, 삭제,
    - 답변하기 (수정, 삭제)
- 리뷰 생성, 삭제, 수정
- 쿠폰
- 네이버 소셜 로그인
- 네이버페이
- 뱃지 기능 MD
- 카드 결제 기능
- 무통장 입금 확인 기능

## 개발



- 프로젝트 셋업(Git repository & Server 초기세팅)
- 모델링 및 ERD
    ![fruitstore_(1)](https://user-images.githubusercontent.com/101803254/197968824-39355715-da18-40fd-bc62-c4860c65cd44.png)
    
    
    유저관리 : /users/
    
    주문관리 : /orders/
    
    상품관리 : /products/
    
    결제관리: /payments/
    
    카트관리:/carts/
    
    ## 주문, 배송 상태 흐름도
    ![image](https://user-images.githubusercontent.com/101803254/198198485-d37749f8-4090-4c6e-8519-d2f22c7a2326.png)

  
