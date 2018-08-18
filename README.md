# GameTable
  * Excel로 게임에 필요한 데이터 파일을 관리하고자 만듦
  * Key Value Pair가 기본
  * Key 기반으로 계층구조 만들 수 있음
  * 혼자 쓸려고 만든거라 사용법과 설명이 불친절함

## Requirements
  * Python 3.5

## Usage
  * Excel로 Json 만들기
    * generator.py 스크립트 내 EXCEL_PATH변수를 Excel 시트들이 있는 상대 경로(generator.py 기준)으로 지정후 저장
    * generator.py 실행
    * generator.py 실행시 첫번째 인자로 Json결과물이 나올 상대경로 입력
  * Unity에서 사용법
    * TablePostProcess.cs를 참고하면 generator.py를 C#코드 상에서 실행하는 코드가 있음
    * 엑셀 파일의 변경이 검출되었을 대 자동으로 Json을 만드는 기능을 하는 코드
    * TableLocator.cs, ~Description.cs ~Table.cs등의 코드를 참고하면 사용방법 쉽게 이해 가능
    * 엑셀 작성 규칙은 샘플로 있는 엑셀 보고 참고
    
## TODO
  * deploy unitypackage
  * improve documents
  * add c++ sample 
  * add override feature
