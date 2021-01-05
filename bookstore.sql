drop database if exists bookstore;

create database bookstore;

create table if not exists bookstore.user (
	user_id varchar(200) primary key, 
	password text not null, 
	balance integer not null, 
	token text, 
	terminal text 
);

create table if not exists bookstore.user_store(
	user_id varchar(200), 
	store_id varchar(200) unique, 
	primary key(user_id, store_id)
	-- foreign key(user_id) references bookstore.user(user_id) on delete cascade on update cascade
);

create table if not exists bookstore.store( 
	store_id varchar(200), 
	book_id varchar(200), 
	book_info longtext, 
	stock_level integer,
	primary key(store_id, book_id)
	-- foreign key(store_id) references bookstore.user_store(store_id) on delete cascade on update cascade
);

create table if not exists bookstore.new_order( 
	order_id varchar(200) primary key, 
	user_id varchar(200), 
	store_id varchar(200), 
	order_time timestamp not null default NOW(), 
	state enum('unpaid', 'undelivered', 'delivering', 'done', 'cancelled', 'timeout') default 'unpaid'
	-- foreign key(user_id) references bookstore.user(user_id) on delete cascade on update cascade, 
	-- foreign key(store_id) references bookstore.user_store(store_id) on delete cascade on update cascade
);

create table if not exists bookstore.new_order_detail( 
	order_id varchar(200), 
	book_id varchar(200), 
	count integer, 
	price integer, 
	primary key(order_id, book_id)
	-- foreign key(order_id) references bookstore.new_order(order_id) on delete cascade on update cascade, 
);

create table if not exists bookstore.unpay_order(
	order_id varchar(200), 
	order_time timestamp
);

create table if not exists bookstore.book_comment(
	user_id varchar(200), 
	store_id varchar(200), 
	book_id varchar(200), 
	comment text, 
	rate int, 
	primary key(user_id, store_id, book_id)
	-- foreign key(user_id) references bookstore.user(user_id) on delete cascade on update cascade, 
	-- foreign key(store_id) references bookstore.store(store_id) on delete cascade on update cascade
);

create table if not exists bookstore.user_cart(
	user_id varchar(200),
	store_id varchar(200),
	book_id varchar(200),
	count int,
	primary key(user_id, store_id, book_id)
	-- foreign key(user_id) references bookstore.user(user_id) on delete cascade on update cascade,
	-- foreign key(store_id) references bookstore.store(store_id) on delete cascade on update cascade
);

drop table if exists bookstore.search_author;

create table bookstore.search_author (
  author varchar(10) not null,
  search_id int not null,
  book_id varchar(10) default null,
  primary key (author,search_id)
);

drop table if exists bookstore.search_book_intro;

create table bookstore.search_book_intro (
  book_intro varchar(10) not null,
  search_id int not null,
  book_id varchar(10) default null,
  primary key (book_intro,search_id)
);

drop table if exists bookstore.search_tags;

create table bookstore.search_tags (
  tags varchar(10) not null,
  search_id int not null,
  book_id varchar(10) default null,
  primary key (tags,search_id)
);

drop table if exists bookstore.search_title;

create table bookstore.search_title (
  title varchar(10) not null,
  search_id int not null,
  book_id varchar(10) default null,
  primary key (title,search_id)
);

drop procedure if exists bookstore.new_order;
delimiter //
create procedure bookstore.new_order(in user_id_ varchar(200), in store_id_ varchar(200), in order_id_ varchar(200), in book_ids varchar(1400), in counts varchar(1400), in book_num int, out flag int, out msg varchar(200))
label:begin
	declare user_num varchar(200) default '';
	declare store_num varchar(200) default '';
	declare book_id_ varchar(100);
	declare book_count_ varchar(100);
	declare i int default 1;
	declare is_exist_ varchar(200) default '';
	declare stock_level_ int default 0;
	declare book_info_ longtext;
	declare price_ int default 0;
	declare is_enough_ int default 1;
	declare time_ timestamp;
	
	declare exit handler for sqlexception
	begin
	rollback;
	set flag = 5;
	set msg = 'store procedure "new_order" error';
	end;
	
	select user_id into user_num from user where user_id=user_id_;
	select store_id into store_num from user_store where store_id=store_id_;
	
	set flag = 0;
	set msg = '';
	
	if length(user_num) = 0 then
		set flag = 1;
		set msg = user_id_;
		leave label;
	elseif length(store_num) = 0 then
		set flag = 2;
		set msg = store_id_;
		leave label;
	else
		start transaction;		
		insert into new_order(order_id, store_id, user_id)
		values(order_id_, store_id_, user_id_);
		
		select order_time from new_order 
		where order_id=order_id_
		into time_;
		
		insert into unpay_order(order_id, order_time)
		values(order_id_, time_);
		
		while i <= book_num do
			set is_exist_ = '';
			set book_id_ = substring_index(substring_index(book_ids,'&',i),'&',-1);
			set book_count_ = substring_index(substring_index(counts,'&',i),'&',-1);
			
			select store_id, stock_level, book_info
			from store 
			where store_id=store_id_ and book_id=book_id_
			into is_exist_, stock_level_, book_info_;
			
			if length(is_exist_) = 0 then
				set flag = 3;
				set msg = book_id_;
				rollback;
			else
				select stock_level_ >= book_count_ into is_enough_;
				if is_enough_ = 0 then
					set flag = 4;
					set msg = book_id_;
					rollback;
				else
					select json_extract(book_info_,'$.price') into price_;
					
					update store set stock_level=stock_level-book_count_
					where store_id=store_id_ and book_id=book_id_;
					
					insert into new_order_detail(order_id, book_id, count, price)
					values(order_id_, book_id_, book_count_, price_);
				end if;
			end if;
			set i = i + 1;
		end while;
		commit;
	end if;
end //
delimiter ;
drop procedure if exists bookstore.payment;
delimiter //
create procedure bookstore.payment(in user_id_ varchar(200), in password_ varchar(200), in order_id_ text, out flag int, out msg varchar(200))
label:begin
	declare buyer_id_ varchar(200) default '';
	declare store_id_ varchar(200) default '';
	declare balance_ int default 0;
	declare rpassword_ varchar(200) default '';
	declare seller_id_ varchar(200) default '';
	declare seller_id_i_ varchar(200) default '';
	declare book_id_ varchar(200) default '';
	declare count_ int default 0;
	declare price_ int default 0;
	declare total_price_ int default 0;
	declare has_pay_ varchar(200) default '';
	
	declare done int default 0;
	declare book_list cursor for
	select book_id, count, price from new_order_detail
	where order_id=order_id_;
	declare continue handler for not found set done = 1;
	
	declare exit handler for sqlexception
	begin
	rollback;
	set flag = 8;
	set msg = 'store procedure "payment" error';
	end;
	
	set flag = 0;
	set msg = '';
	
	select order_id from unpay_order
	where order_id=order_id_
	into has_pay_;
	
	if length(has_pay_) = 0 then
		set flag = 9; -- has pay; error.error_invalid_order_id(order_id)
		set msg = order_id_;
		leave label;
	end if;
	
	select user_id, store_id 
	from new_order
	where order_id=order_id_
	into buyer_id_, store_id_;
	
	set msg = '';
	if length(store_id_) = 0 then
		set flag = 1; -- error.error_invalid_order_id(order_id)
		set msg = order_id_;
		leave label;
	end if;
	
	set msg = '';
	if buyer_id_ <> user_id_ then
		set flag = 2; -- error.error_authorization_fail()
		set msg = 'buyer_id is not user_id';
		leave label;
	end if;
	
	select balance, password
	from user
	where user_id=buyer_id_
	into balance_, rpassword_;
	
	set msg = '';
	if length(rpassword_) = 0 then
		set flag = 3; -- error.error_non_exist_user_id(buyer_id)
		set msg = buyer_id_;
		leave label;
	end if;
	
	set msg = '';
	if rpassword_ <> password_ then
		set flag = 4; -- error.error_authorization_fail()
		set msg = 'password error';
		leave label;
	end if;
	
	select user_id from user_store
	where store_id=store_id_
	into seller_id_;
	
	set msg = '';
	if length(seller_id_) = 0 then
		set flag = 5; -- error.error_non_exist_store_id(store_id)
		set msg = store_id_;
		leave label;
	end if;
	
	set msg = seller_id_;
	
	select user_id from user 
	where user_id=seller_id_
	into seller_id_i_;
	
	if length(seller_id_i_) = 0 then
		set flag = 6; -- error.error_non_exist_user_id(seller_id)
		leave label;
	end if;
	
	open book_list;
read_loop:loop
	fetch book_list into book_id_, count_, price_;
	
	if done then
		leave read_loop;
	end if;
	
	set total_price_ = total_price_ + price_ * count_;
	end loop;
	close book_list;
	
	-- set msg = '';
	if balance_ < total_price_ then
		set flag = 7; -- error.error_not_sufficient_funds(order_id)
		set msg = order_id_;
		leave label;
	end if;
	set msg = '';
	
	start transaction;
	update user set balance=balance-total_price_ where user_id=buyer_id_ and balance>=total_price_;
	update user set balance=balance+total_price_ where user_id=seller_id_;
	update new_order set state='undelivered' where order_id=order_id_;
	delete from unpay_order where order_id=order_id_;
	commit;
end //
delimiter ;
drop procedure if exists bookstore.auto_cancel;
delimiter //
create procedure bookstore.auto_cancel()
label:begin
	declare now_ timestamp default now();
	declare order_id_ varchar(200) default '';
	
	declare done int default 0;
	declare unpay_order_ cursor for
	select order_id from unpay_order where timestampdiff(minute,order_time,now_)>30;
	declare continue handler for not found set done = 1;
	
	declare exit handler for sqlexception
	begin
	rollback;
	end;
	
	start transaction;
	open unpay_order_;
update_loop:loop
	fetch unpay_order_ into order_id_;
	
	if done then
		leave update_loop;
	end if;
	
	update new_order set state='timeout' where order_id=order_id_; -- change state for new_order
	end loop;
	close unpay_order_;
	
	delete from unpay_order where timestampdiff(minute,order_time,now_)>30; -- delete timeout order from unpay_order
	commit;
end //
delimiter ;
drop procedure if exists bookstore.man_cancel;
delimiter //
create procedure bookstore.man_cancel(in user_id_ varchar(200), in password_ varchar(200), in order_id_ text, out flag int, out msg varchar(200))
label:begin
	declare store_id_ varchar(200) default '';
	declare seller_id_ varchar(200) default '';
	declare rpassword_ varchar(200) default '';
	declare order_state_ varchar(20) default '';
	declare book_id_ varchar(200) default '';
	declare count_ int default 0;
	declare price_ int default 0;
	declare total_price_ int default 0;
	
	declare done int default 0;
	declare book_list cursor for
	select book_id, count, price from new_order_detail
	where order_id=order_id_;
	declare continue handler for not found set done = 1;
	
	declare exit handler for sqlexception
	begin
	rollback;
	set flag = 7;
	end;
	
	set flag = 0;
	set msg = '';
	
	-- confirm user_id and password
	select password from user
	where user_id=user_id_
	into rpassword_;
	
	if length(rpassword_) = 0 then
		set flag = 1; -- error.error_non_exist_user_id(user_id)
		set msg = user_id_;
		leave label;
	end if;
	set msg = '';
	
	if rpassword_<>password_ then
		set flag = 2; -- error.error_authorization_fail()
		set msg = 'password error';
		leave label;
	end if;
	set msg = '';
	
	-- confirm order exists
	select store_id, state from new_order
	where order_id=order_id_
	into store_id_, order_state_;
	
	if length(store_id_) = 0 then
		set flag = 3; -- error.error_invalid_order_id(order_id)
		set msg = order_id_;
		leave label;
	end if;
	set msg = '';
	
	-- confirm order has not cancelled
	if order_state_ = 'cancelled' then
		set flag = 4; -- error.error_order_has_cancelled(order_id)
		set msg = order_id_;
		leave label;
	end if;
	set msg = '';
	
	-- confirm store exists
	select user_id from user_store
	where store_id=store_id_
	into seller_id_;
	
	if length(seller_id_) = 0 then
		set flag = 5; -- error.error_non_exist_store_id(store_id)
		set msg = store_id_;
		leave label;
	end if;
	set msg = '';
	
	-- confirm seller exists
	set msg = seller_id_;
	set seller_id_ = '';
	select user_id from user
	where user_id=msg
	into seller_id_;
	
	if length(seller_id_) = 0 then
		set flag = 6; -- error non_exist_seller
		leave label;
	end if;
	set msg = '';
	
	-- make changes
	start transaction;
	update new_order set state='cancelled' where order_id=order_id_;
	if order_state_ = 'unpaid' then
		delete from unpay_order where order_id=order_id_;
	else
		open book_list;
		read_loop:loop
			fetch book_list into book_id_, count_, price_;
			
			if done then
				leave read_loop;
			end if;
			
			set total_price_ = total_price_ + price_ * count_;
		end loop;
		close book_list;
		
		update user set balance=balance-total_price_ where user_id=seller_id_;
		update user set balance=balance+total_price_ where user_id=user_id_;
	end if;
	commit;
	-- select store_id_,seller_id_,rpassword_,order_state_,total_price_;	
end //
delimiter ;
create event bookstore.e_auto_cancel on schedule every 1 minute do call auto_cancel();
