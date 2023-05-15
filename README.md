# my first flask api

## Install App
```
git clone git@github.com:loinguyen3108/Home-Test-Thuoc-Si.git
```

Sau khi môi trường bên project Dev-Stack-Flask chạy thành công thì có thể test được các API.

- Create new customer

Requests:
```
URL: localhost:8000/user/sign_up
Method: POST
Request Data: {
    "first_name": "Anh",
    "last_name": "Nguyen",
    "email": "hometest@gmail.com",
    "gender": "MALE",
    "address": "USA",
    "password": "hometest123"
}
Header: {}
```
Response:
![alt text](https://github.com/loinguyen3108/Home-Test-Thuoc-Si/blob/main/images/Sign_Up_PM.png?raw=true)

- Login

Requests:
```
URL: localhost:8000/user/login
Method: POST
Request Data: {
    "email": "hometest@gmail.com",
    "password": "hometest123"
}
Header: {}
```
Response:
![alt text](https://github.com/loinguyen3108/Home-Test-Thuoc-Si/blob/main/images/Login_PM.png?raw=true)

- Read customer's information

Requests:
```
URL: localhost:8000/user/3
Method: GET
Request Data: {}
Header: {"Authorization": "<token được lấy từ login>"}
```
Response:
![alt text](https://github.com/loinguyen3108/Home-Test-Thuoc-Si/blob/main/images/Get_User_PM.png?raw=true)

- Update customer

Requests:
```
URL: localhost:8000/user/3
Method: POST
Request Data: {
    "first_name": "Ba",
    "last_name": "Tran",
    "gender": "MALE",
    "address": "VN"
}
Header: {"Authorization": "<token được lấy từ login>"}
```
Reponse:
![alt text](https://github.com/loinguyen3108/Home-Test-Thuoc-Si/blob/main/images/Update_User.png?raw=true)

- Delete customer

Requests:
```
URL: localhost:8000/user/3
Method: DELETE
Request Data: {}
Header: {"Authorization": "<token được lấy từ login>"}
```
Reponse:
![alt text](https://github.com/loinguyen3108/Home-Test-Thuoc-Si/blob/main/images/Delete_User.png?raw=true)

- Get All User

Requests:
```
URL: localhost:8000/user/get_all_user
Method: GET
Request Data: {}
Header: {"Authorization": "<token được lấy từ login>"}
```
Reponse:
![alt text](https://github.com/loinguyen3108/Home-Test-Thuoc-Si/blob/main/images/Get_All_User.png?raw=true)
