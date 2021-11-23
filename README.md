# DjangoMySite

## 설정

### 로컬 개발환경

python 설치

가상환경 디렉토리 생성
```
~> mkdir venvs
```

venv 생성
```python
~\vevns> python -m venv mysite
```

가상환경 진입
```python
~\venvs\mysite\scripts> activate
```

pip 업그레이드(필요시)
```python
~\venvs\mysite\scripts> python -m pip install --upgrade pip
```

필요 패키지 설치
```python
~\venvs\mysite\scripts> pip install -r {프로젝트 경로}\requirements.txt
```

venv 디렉토리에 mysite.cmd 복사하고 환경변수 값 설정


### 운영환경
venv 디렉토리에 mysite.env, mysite.sh 복사하고 환경변수 값 설정

### 사용 패키지
[MyPythonPakages](https://github.com/boritjjaroo/MyPythonPackages)의 naver 모듈 사용
