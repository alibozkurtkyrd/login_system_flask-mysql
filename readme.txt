+ This python flask application. 

	flask can be installed by using "pip install Flask" command.
	
	run my_app.py python file 
	
	The output prints as the address : http://127.0.0.1:5000/
	
	
	
+ logintest database has two tables as accounts and  other_information 

	accounts table contains username, password and email information, use 
	
	other_informaiton talbe contains username, firstname,surname,phone_no, authentication
	and address column. Username is foreign key that connects with accounts table 

	other_information talbe has "authentication" column in which there is two option admin and user.
	only admin can see all users' infomation by pressing "Admin rights" button in home.html page.
	
+ mysql survive against same SQL injection attacks

	For instance " or ""=" write in username-name and password it is not permit to show data. because 
	I did not passes username from client directly I use specified type like:
		"cursor.execute("SELECT * FROM accounts WHERE username = %s'", (username, ));"
		
		on the other side "cursor.execute("SELECT * FROM accounts WHERE username = '{}'".format(username));"
		type in NOT safe.
		
+ System should be able to reduce the errors that come from manually filling out forms.

	username and password is required otherwise system has warn user to filled out input.
	
+ In home.html page upgrade function is not WORKING
		

