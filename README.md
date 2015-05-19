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
* 書籍相關 
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
    
    