Table dim_users as user{
  user_id int
  user_name varchar
  email_address varchar
  date_of_birth date
  contact_number int
  employment varchar
  city varchar
  country varchar
  citizenship varchar
  social_security_number varchar
  investment_experience varchar
  Indexes {
    (user_id) [pk]
  }
}


Table fact_user_trades as trade{
  trade_id int
  trade_date date
  trade_timestamp timestamp
  user_id int
  stock_name varchar
  traded_units int
  traded_value int
  Indexes {
    (trade_id) [pk]
  }
}


Table fact_browsing_sessions as browse{
  browse_id int
  session_id int
  stock_name varchar
  browse_duration int
  Indexes {
    (browse_id) [pk]
  }
}



Table fact_account_updates as update{
  update_id int
  update_date date
  update_time timestamp
  stock_add_watchlist varchar
  funds_added int
  stock_order_name varchar
  stock_order_type varchar
  stock_order_value int
  Indexes {
    (update_id) [pk]
  }
}


Table fact_user_session as session{
  session_id int
  user_id int
  session_date date
  session_start_time timestamp
  session_end_time timestamp
  update_id int
  trade_id int 
  Indexes {
    (session_id) [pk]
  }
}


Ref:session.user_id > user.user_id
Ref:session.update_id > update.update_id
Ref:session.trade_id > trade.trade_id
Ref:browse.session_id > session.session_id
Ref:trade.user_id > user.user_id