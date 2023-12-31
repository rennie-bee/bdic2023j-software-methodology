# **bdic-2023j-software-methodology-study-abroad-platform**
## **1.  Introduction**
This project is a special Q&A Platform for students.



## **2. Deployment**

### 2. 1 Run with Docker

**You can download the docker image we have prepared from Docker Hub, or you can generate a new docker image based on the Dockerfile inside the code.**

> The premise of using docker is that your computer has docker

#### 2.1.1 Download Docker Image

* Download

```shell
docker docker pull ouxiaoou/platform:latest
```

* Run 

```shell
docker run -d -p 5000:5000 ouxiaoou/platform:latest
```

#### 2.1.2 Generate a new Docker Image

* Generate

```shell
docker build -t [your_image_name] .
```

* Run 

```shell
docker run -d -p 5000:5000 [your_image_name]
```

#### 2.1.3 Open

* Open Web APP

```shell
# If your computer is mac you can use this.
open -a "Google Chrome"  http://127.0.0.1:5000/ 
# If your computer is windows you can use this.
You can visit directly in the browser: 127.0.0.1:5000 to view.
```

* Kill Run

```shell
docker ps   #View the CONTAINER ID of the running container
```

```shell
docker kill <CONTAINER ID>  #Stop run
```



### 2.2 Run with Virtualenv Environment

**Please use PyCharm as much as possible for the entire project, which can simplify the process of environment configuration.**

#### **2.2.1 Clone project to local** 

```shell
git clone https://csgitlab.ucd.ie/18206155/debugger.git
```

#### 2.2.2 Configure Python interpreter

You'll need to find Project Interpreter in Preferences of PyCharm to create a new Virtualenv Environment. 

> This is a brand new virtual environment and will not be affected by other environments in your computer.

#### 2.2.3 Install all the packages

```shell
pip install -r requirements.txt
```
#### 2.2.4 Run codes

* For Linux and macOS,

```shell script
export FLASK_APP=flasky.py
flask run
```

* For Windows

```shell script
set FLASK_APP=flasky.py
flask run
```

#### 2.2.5 Problem that may arise

**In the process of using pip to download the package, we have various problems. You can refer to these following information.**

1. If the terminal prompts "Requirement already satisfied: ..." but it cannot find the package we originally installed when running.
* Solution: We need to clear the cache data of PyCharm and reinstall all the packages we need through the "requirements.txt" file.
* And How to Clear the Cache Data: <https://jingyan.baidu.com/article/656db918b1e142a281249cc8.html>


2. Internet speed is too slow resulting in download failure.
* Solution：Download via douban source.  <http://pypi.douban.com/simple>
* Reference: <https://blog.csdn.net/ITYTI/article/details/83313463>

3. After excluding the above problems, still cannot install any packet.
* Error info: Cannot connect to proxy solution：
* Solution: It may be caused by a proxy server set on the computer. Just shut off the proxy the sever.
* Reference: <https://www.cnblogs.com/arvinls/p/6149417.html>



## 3. Test

### 3.1 Student Account 

#### 3.1.1 Registration to verify identity

This is a forum platform for students at Beijing University of Technology, so you need to complete verification to successfully enroll student users.

> Only the Student ID, ID and Student ID in the database match the Student ID, ID can complete the student user registration. 

Here's the data for you to test registration to verify identity.

| StudentID | ID                 |
| --------- | ------------------ |
| 18372301  | 111111111111111111 |
| 18372302  | 222222222222222222 |
| 18372303  | 333333333333333333 |
| 18372304  | 444444444444444444 |
| 18372305  | 555555555555555555 |
| 18372306  | 666666666666666666 |
| 18372307  | 777777777777777777 |
| 18372308  | 888888888888888888 |

#### 3.1.2 A Student Account For Test

Here is an student account for you to test.

| StudentID | Password |
| --------- | -------- |
| 84291189  | password |

