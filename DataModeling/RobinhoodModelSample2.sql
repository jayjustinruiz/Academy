Table dim_users as user{
  user_id int
  user_first_name varchar
  user_last_name varchar
  age int
  gender varchar
  email_address varchar
  monthly_income int
  occupation int
  city varchar
  state varchar
  home_owner varchar
  marital_status varchar
  user_since date
  linked_bank_account boolean
  balance_amount decimal
  Indexes {
    (user_id) [pk]
  }
}

Table dim_products as prod{
  product_id int
  seller_id int
  product_name varchar
  sub_category varchar
  category varchar
  price int
  Indexes {
    (product_id) [pk]
  }
}

Table dim_sellers as sell{
  seller_id int
  seller_name varchar
  seller_description varchar
  business_category varchar
  business_age int
  membership_type varchar
  Indexes {
    (seller_id) [pk]
  }
}

Table fact_transactions as trans{
  order_id int
  transaction_id int
  transaction_date date
  product_id int
  seller_id int
  user_id int
  quantity_purchased int
  order_value int
  payment_method varchar
  Indexes {
    (order_id) [pk]
  }
}

Table fact_product_history as prices{
  product_id int
  seller_id int
  product_name varchar
  price int
  price_open int
  price_change int
  price_1month_historical int
  price_5month_historical int
  price_12month_historical int
  price_change_1month int
  price_change_5month int
  price_change_12month int
  Indexes {
    (product_id) [pk]
  }
}

Ref: trans.user_id > user.user_id
Ref: trans.seller_id > sell.seller_id
Ref: trans.product_id > prod.product_id
Ref: trans.product_id > prices.product_id
Ref: prices.seller_id > sell.seller_id
Ref: prices.product_id > prod.product_id
Ref: prod.seller_id > sell.seller_id
