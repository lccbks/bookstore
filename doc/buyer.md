## 买家下单

#### URL：
POST http://[address]/buyer/new_order

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "store_id": "store_id",
  "books": [
    {
      "id": "1000067",
      "count": 1
    },
    {
      "id": "1000134",
      "count": 4
    }
  ]
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
store_id | string | 商铺ID | N
books | class | 书籍购买列表 | N

books数组：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
id | string | 书籍的ID | N
count | string | 购买数量 | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 下单成功
5XX | 买家用户ID不存在
5XX | 商铺ID不存在
5XX | 购买的图书不存在
5XX | 商品库存不足

##### Body:
```json
{
  "order_id": "uuid"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | string | 订单号，只有返回200时才有效 | N


## 买家付款

#### URL：
POST http://[address]/buyer/payment

#### Request

##### Body:
```json
{
  "user_id": "buyer_id",
  "order_id": "order_id",
  "password": "password"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
order_id | string | 订单ID | N
password | string | 买家用户密码 | N 


#### Response

Status Code:

码 | 描述
--- | ---
200 | 付款成功
5XX | 账户余额不足
5XX | 无效参数
401 | 授权失败 


## 买家充值

#### URL：
POST http://[address]/buyer/add_funds

#### Request

##### Body:
```json
{
  "user_id": "user_id",
  "password": "password",
  "add_value": 10
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N
add_value | int | 充值金额，以分为单位 | N


Status Code:

码 | 描述
--- | ---
200 | 充值成功
401 | 授权失败
5XX | 无效参数

## 买家确认收货

#### URL:

POST http://[address]/buyer/comfirm_receipt

#### Requset

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "$user id$",
  "order_id": "$order id$"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 卖家用户ID | N          |
| order_id | string | 订单ID     | N          |

#### Response

Status Code:

| 码   | 描述         |
| ---- | :----------- |
| 200  | 收货成功     |
| 511  | 用户ID不存在 |
| 529  | 订单ID不存在 |

## 买家查询订单状态

#### URL:

POST http://[address]/buyer/query_order_state

#### Requset

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "$user id$",
  "order_id": "$order id$"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | string | 订单ID     | N          |

#### Response

##### Status Code:

| 码   | 描述         |
| ---- | :----------- |
| 200  | 查询成功     |
| 511  | 用户ID不存在 |
| 529  | 订单ID不存在 |

##### Body:

```json
{
  "state": "$state$"
}
```

##### 属性说明：

| 变量名 | 类型   | 描述                          | 是否可为空 |
| ------ | ------ | ----------------------------- | ---------- |
| state  | string | 订单状态，只有返回200时才有效 | N          |

## 买家取消订单

#### URL:

POST http://[address]/buyer/cancel_order

#### Requset

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "$user id$",
  "password": "$password$",
  "order_id": "$order id$"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| password | string | 用户密码   | N          |
| order_id | string | 订单ID     | N          |

#### Response

##### Status Code:

| 码   | 描述                               |
| ---- | :--------------------------------- |
| 200  | 取消成功                           |
| 401  | 取消失败，用户名不存在或密码不正确 |
| 511  | 用户ID不存在                       |
| 529  | 订单ID不存在                       |

## 买家对买过的图书评论

#### URL:

POST http://[address]/buyer/add_comment

#### Requset

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
    "user_id":"$user id$",
    "store_id":"$$store id",
    "book_id":"$book id$",
    "comment":"$comment$",
    "rate":"$rate$"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| store_id | string | 商铺ID     | N          |
| book_id  | string | 图书ID     | N          |
| comment  | string | 买家评论   | N          |
| rate     | int    | 买家打分   | N          |

#### Response

##### Status Code:

| 码   | 描述                     |
| ---- | :----------------------- |
| 200  | 评论成功                 |
| 511  | 用户ID不存在             |
| 513  | 商铺ID不存在             |
| 531  | 订单状态错误，订单未完成 |
| 532  | 该商铺中不存在该图书     |
| 533  | 用户已评论过             |

## 买家查看评论

#### URL:

POST http://[address]/buyer/view_comments

#### Requset

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
    "user_id":"$user id$",
    "store_id":"$$store id",
    "book_id":"$book id$"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| store_id | string | 商铺ID     | N          |
| book_id  | string | 图书ID     | N          |

#### Response

##### Status Code:

| 码   | 描述                 |
| ---- | :------------------- |
| 200  | 评论成功             |
| 511  | 用户ID不存在         |
| 513  | 商铺ID不存在         |
| 532  | 该商铺中不存在该图书 |