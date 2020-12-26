## 注册用户

#### URL：
POST http://$address$/auth/register

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N

#### Response

Status Code:


码 | 描述
--- | ---
200 | 注册成功
5XX | 注册失败，用户名重复

Body:
```
{
    "message":"$error message$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 注销用户

#### URL：
POST http://$address$/auth/unregister

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N

#### Response

Status Code:


码 | 描述
--- | ---
200 | 注销成功
401 | 注销失败，用户名不存在或密码不正确


Body:
```
{
    "message":"$error message$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 用户登录

#### URL：
POST http://$address$/auth/login

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$",
    "terminal":"$terminal code$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N
terminal | string | 终端代码 | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 登录成功
401 | 登录失败，用户名或密码错误

Body:
```
{
    "message":"$error message$",
    "token":"$access token$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N
token | string | 访问token，用户登录后每个需要授权的请求应在headers中传入这个token | 成功时不为空

#### 说明 

1.terminal标识是哪个设备登录的，不同的设备拥有不同的ID，测试时可以随机生成。 

2.token是登录后，在客户端中缓存的令牌，在用户登录时由服务端生成，用户在接下来的访问请求时不需要密码。token会定期地失效，对于不同的设备，token是不同的。token只对特定的时期特定的设备是有效的。

## 用户更改密码

#### URL：
POST http://$address$/auth/password

#### Request

Body:
```
{
    "user_id":"$user name$",
    "oldPassword":"$old password$",
    "newPassword":"$new password$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
oldPassword | string | 旧的登陆密码 | N
newPassword | string | 新的登陆密码 | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 更改密码成功
401 | 更改密码失败

Body:
```
{
    "message":"$error message$",
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 用户登出

#### URL：
POST http://$address$/auth/logout

#### Request

Headers:

key | 类型 | 描述
---|---|---
token | string | 访问token

Body:
```
{
    "user_id":"$user name$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 登出成功
401 | 登出失败，用户名或token错误

Body:
```
{
    "message":"$error message$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 查询：作者名

#### URL：

POST http://$address$/auth/search_author

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "author":"$search name$"
    "page":"$page num$"
}
```

| 变量名  | 类型   | 描述   | 是否可为空 |
| ------- | ------ | ------ | ---------- |
| user_id | string | 作者名 | N          |
| page    | int    | 页码   | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 查询：内容

#### URL：

POST http://$address$/auth/search_book_intro

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "book_intro":"$search name$"
    "page":"$page num$"
}
```

| 变量名     | 类型   | 描述     | 是否可为空 |
| ---------- | ------ | -------- | ---------- |
| book_intro | string | 书的内容 | N          |
| page       | int    | 页码     | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 查询：标签

#### URL：

POST http://$address$/auth/search_tags

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "tags":"$search name$"
    "page":"$page num$"
}
```

| 变量名 | 类型   | 描述 | 是否可为空 |
| ------ | ------ | ---- | ---------- |
| tags   | string | 标签 | N          |
| page   | int    | 页码 | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 查询：题目

#### URL：

POST http://$address$/auth/title

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "title":"$search name$"
    "page":"$page num$"
}
```

| 变量名 | 类型   | 描述 | 是否可为空 |
| ------ | ------ | ---- | ---------- |
| title  | string | 标题 | N          |
| page   | int    | 页码 | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 商铺查询：作者名

#### URL：

POST http://$address$/auth/search_author_in_store

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "author":"$search name$"
    "store_id":"$store name$"
    "page":"$page num$"
}
```

| 变量名   | 类型   | 描述   | 是否可为空 |
| -------- | ------ | ------ | ---------- |
| author   | string | 作者名 | N          |
| store_id | string | 商店   | N          |
| page     | int    | 页码   | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 商铺查询：内容

#### URL：

POST http://$address$/auth/search_book_intro_in_store

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "book_intro":"$search name$"
    "store_id":"$store name$"
    "page":"$page num$"
}
```

| 变量名     | 类型   | 描述     | 是否可为空 |
| ---------- | ------ | -------- | ---------- |
| book_intro | string | 书的内容 | N          |
| store_id   | string | 商店     | N          |
| page       | int    | 页码     | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 商铺查询：标签

#### URL：

POST http://$address$/auth/search_tags_in_store

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "tags":"$search name$"
    "store_id":"$store name$"
    "page":"$page num$"
}
```

| 变量名   | 类型   | 描述 | 是否可为空 |
| -------- | ------ | ---- | ---------- |
| tags     | string | 标签 | N          |
| store_id | string | 商店 | N          |
| page     | int    | 页码 | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |

## 商铺查询：题目

#### URL：

POST http://$address$/auth/search_title_in_store

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:

```
{
    "title":"$search name$"
    "store_id":"$store name$"
    "page":"$page num$"
}
```

| 变量名   | 类型   | 描述 | 是否可为空 |
| -------- | ------ | ---- | ---------- |
| title    | string | 题目 | N          |
| store_id | string | 商店 | N          |
| page     | int    | 页码 | N          |

#### Response

Status Code:

| 码   | 描述                        |
| ---- | --------------------------- |
| 200  | 查询成功                    |
| 401  | 查询失败，用户名或token错误 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------: |
| message | string | 返回错误消息，成功时为"ok" |          N |