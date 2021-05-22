CREATE DATABASE IF NOT EXISTS `logintest` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `logintest`;

create table if not exists accounts(
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
     PRIMARY KEY (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table if not exists other_information(

    other_id int(11) NOT NULL AUTO_INCREMENT,
    username varchar(50),
    first_name varchar(50) not null,
    surname varchar(50) not null,
    phone_no varchar(50),
    authentication varchar(12),
    address varchar(250),
     
	PRIMARY KEY (other_id),
	FOREIGN KEY (username) REFERENCES accounts(username) 
      
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

select * from accounts;
select * from other_information;

select * from accounts as a join other_information as o on a.username = o.username;

select * from accounts as a left join other_information as o on a.username = o.username;

select * from accounts where username in (select username from other_information);

select authentication from other_information where username= 'test4user';
# DELETE FROM acounts WHERE username= 'test2user';