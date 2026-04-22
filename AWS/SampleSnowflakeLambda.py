import snowflake.connector

#login to Snowflake
ctx = snowflake.connector.connect(
	user ='demo_user'
	password = 'Password'
	acount = 'account'
	warehouse = "computer_wh"
	database = "DEMO_DB"
	schema ="PUBLIC"
	)
cs = ctx.cursor()
print ('Sucessfully Login to Snowflake')
try:
	for CustomerID, Customer Name in ctx.cursor().execute("SELECT CUSTOMER_ID.CUSTOMER_NAME FROM customer;"):
		print ('{0},{1}'.format(CUSTOMER_ID,CUSTOMER_NAME))
finally:
	cs.close()
ctx.close()


