FROM python:3.7.7
WORKDIR /debugger
COPY . /debugger
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
ENTRYPOINT ["python"]
CMD ["flasky.py"]