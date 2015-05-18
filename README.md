# 輕小說管理器後端Server #
## 基本流程: ##
###1.取得Token  
GET /api/token 回傳  

```  
{  
	"expire_time": 1432024168, // interger, token過期的時間      
	"token": "aaanff1hqnyhc650aa5xgww23q53ag2i", // 32字元的Token    
	"_id": {    
          "$oid": "5559a2e8f72e496e37f1496d" // Mongodb物件的Unique ID    
    },    
    "user_id": 0 // 使用此Token登入的user 預設為0(匿名)    
  }
```

###2.登入
將Token放在Header並POST到 /api/user/login

Header：

```
Content-Type: application/json
Token: (Token)
```
POST資料：

```
{
	"username": "user",
	"password": "pass"
}
```
回傳

```
{
    "message": "Login successful"
}

```

###3.進行操作
將登入過的Token放在Header，即可進行各項操作
