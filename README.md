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


## 登入後可進行的各項操作
* 書籍相關 /api/book
    * 取得 GET /api/book
    
    ```
[
    {
        "publisher": "222端出版",
        "ISBN": "123456fffff7890",
        "tags": [
            "LightNovel",
            "Novel"
        ],
        "deleted": false,
        "price": "20330",
        "author": "東方",
        "publish_date": "20150101",
        "book_id": 11,
        "user_id": 3,
        "_id": {
            "$oid": "55554aa3c024da4e6ba73f19"
        },
        "bookname": "雨港ss030基隆 - 桐花雨"
    },
    {
        "publisher": "222端出版",
        "ISBN": "123456fffff7890",
        "tags": [
            "LightNooooovel",
            "OuO",
            "HentaiBooks"
        ],
        "deleted": false,
        "price": "20330",
        "author": "東方",
        "publish_date": "20150101",
        "book_id": 12,
        "user_id": 3,
        "_id": {
            "$oid": "55554b78c024da4e8f9c41ea"
        },
        "bookname": "雨港ss030基隆 - 桐花雨"
    },
]
    
    ```
    取得特定編號 GET /api/book/<book_id>  
    ex: GET /api/book/11
    
    ```
[
    {
        "publisher": "222端出版",
        "ISBN": "123456fffff7890",
        "tags": [
            "LightNovel",
            "Novel"
        ],
        "deleted": false,
        "price": "20330",
        "author": "東方",
        "publish_date": "20150101",
        "book_id": 11,
        "user_id": 3,
        "_id": {
            "$oid": "55554aa3c024da4e6ba73f19"
        },
        "bookname": "雨港ss030基隆 - 桐花雨"
    }
]
    ```
    
     
    * 新增 POST /api/book  
    至少要提供書名
    
    ```   
{
    "bookname": "雨港ss030基隆 - 桐花雨",
    "author": "東方",
    "publisher": "222端出版",
    "publish_date": "20150101",
    "price": "20330",
    "ISBN": "123456fffff7890",
    "tags":[
      "LightNovel",
      "OuO"
    ]
}
    ```

    * 修改 PUT /api/book/<book_id>  
    和新增時的資料結構相同，但只需傳送想要修改的資料就好  
    要修改TAG時，需要連原有的TAG一起傳送（一次傳送所有TAG）
    
    ```
{
    "bookname": "雨港ss030基隆 - 桐花雨",
    "author": "東方",
    "publisher": "尖端出版",
    "publish_date": "20150101",
    "price": "20330",
    "ISBN": "123456fffff7890",
    "tags":[
        "LightNovel",
        "Novel",
        "My favorite"
    ]
}
    ```
    
    * 刪除 DELETE /api/book/<book_id>
    
* 使用者相關 /api/user
    * 取得自己的使用者資料 GET /api/user/<user_id>

    ```
{
    "username": "哈哈哈XDD",
    "_id": {
        "$oid": "5576f59883dc492a0a165c86"
    },
    "user_id": 54,
    "deactivated": false,
    "head_image_url": "http://163.13.128.116:5001/54/head_images/10d11b58-f138-40fd-81c3-f2fd553542a5.png",
    "password": "111",
    "email": "哈哈哈"
}
```
    * 新增使用者 POST /api/user (要提供token，註冊完畢token會自動對應新註冊的使用者)
    
    ```
{
    "username": "ikaros",
    "email": "ikaros@gmail.com",
    "password": "ikaros"
}
```
    * 修改使用者 PUT /api/user/<user_id> (todo: 修改成用token對應user_id)
    
    	資料結構同新增使用者
    	
    * 刪除使用者 DELETE /api/user/<user_id> (todo: 修改成用token對應user_id)
    