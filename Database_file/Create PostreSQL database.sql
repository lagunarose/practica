create table Users
(
ID_IP varchar(50) not null constraint PK_IP primary key,
Login varchar(50) not null constraint UQ_Login UNIQUE,
Pasword varchar(15) not null constraint CH_Pasword_UPPER CHECK 
(Pasword similar to '%[A-Z]%')
constraint CH_Pasword_LOWER CHECK 
(Pasword similar to '%[a-z]%')
constraint CH_Pasword_SYMBOL CHECK 
(Pasword similar to '%[!@#$%^&*]%')
);

drop table Users

create or replace procedure User_insert (p_IP varchar(50), p_Login varchar(50), p_Pasword varchar(15))
language plpgsql
as $$
	declare p_exsit_IP int := count(*) from Users
		where id_IP = p_IP;
	declare p_exsit_Login int := count(*) from Users
		where Login = p_Login;
	declare p_exsit_Pasword int := count(*) from Users
		where Pasword = p_Pasword;

	declare p_admin_ip_exsist varchar(15) := count(*) from Users
		where ID_IP similar to '.*[0-9]*'
		and length(ID_IP) = 15;
	declare p_IP_len int := 15;
begin 
	if p_exsit_IP > 0 then
	 raise notice 'Данный IP уже есть в системе';
	else 
		if p_Login = '' or p_Login = ' ' then
		 raise notice 'Поле логина не может быть пустым и состоять из пробелов';
		else 
			if p_exsit_Login > 0 then
				raise notice 'Данный логин уже есть в системе';	
			else
				if p_Pasword = '' or p_Pasword = ' ' then
					raise notice 'Поле пароля не может быть пустым и состоять из пробелов';
				elsif length(p_Pasword) < 8  and length(p_Pasword) > 1 then
					raise notice 'Пароль не должен быть меньше 8 символов';
				elsif not p_Pasword similar to '%[A-Z]%' or not p_Pasword similar to '%[a-z]%' 
				or not p_Pasword similar to '%[!@#$%^&*]%' then		
					raise notice 'В пароле должны содержаться:
	    1. Хотя бы одна заглавная и прописная буква
	    2. Хотя бы один спец.символ';
				else
					if p_IP = '' or p_IP = ' ' then
						if p_admin_ip_exsist = '0' then
							p_admin_ip_exsist := '.';
						end if;
						p_IP_len := p_IP_len - length(p_admin_ip_exsist);
						for i in 1..p_IP_len loop
							p_IP = p_IP||'.';
						end loop;
						p_IP := p_IP||p_admin_ip_exsist;
					end if;
					insert into Users(id_IP,Login,Pasword)
					values (p_IP,p_Login,p_Pasword);
					raise notice 'Все прошло успешно';
				end if;
			end if;
		end if;
	end if;
end;
$$;

call User_insert('11212121','ISS','qQQQ#####111')
call User_insert('', 'Admin1', 'A!a12341234');
select * from Users;

delete from Users
		where ID_IP similar to '.*[0-9]*'
		or length(ID_IP) = 15;

create or replace procedure User_drop (p_IP varchar)
language plpgsql
as $$
	declare p_exsit_IP int := count(*) from Users
	where id_IP = p_IP;
begin 
	if p_exsit_IP = 0 then
	 raise notice 'Данного IP нет в системе';
	else 
				delete from Users 
					where id_IP = p_IP;
				raise notice 'Все прошло успешно';
	end if;
end;
$$;
call User_drop('11212121')




create or replace procedure User_update (p_IP varchar(50), p_Login varchar(50), p_Pasword varchar(15))
language plpgsql
as $$
	declare p_exsit_IP int := count(*) from Users
	where id_IP = p_IP;
	declare p_exsit_Login int := count(*) from Users
	where Login = p_Login;
	declare p_exsit_Pasword int := count(*) from Users
	where Pasword = p_Pasword;
begin 
	if p_exsit_IP = 0 then
	 raise notice 'Данного IP нет в системе';
	else 
		if p_Login = '' or p_Login = ' ' then
		 raise notice 'Поле логина не может быть пустым и состоять из пробелов';
		else 
			if p_exsit_Login > 0 then
				raise notice 'Данный логин уже есть в системе';	
			else
				if p_Pasword = '' or p_Pasword = ' ' then
					raise notice 'Поле пароля не может быть пустым и состоять из пробелов';
				elsif length(p_Pasword) < 8  and length(p_Pasword) > 1 then
					raise notice 'Пароль не должен быть меньше 8 символов';
				elsif not p_Pasword similar to '%[A-Z]%' or not p_Pasword similar to '%[a-z]%' 
				or not p_Pasword similar to '%[!@#$%^&*]%' then		
					raise notice 'В пароле должны содержаться:
	    1. Хотя бы одна заглавная и прописная буква
	    2. Хотя бы один спец.символ';
				else
					update Users set 
					 Login = p_Login,
					 Pasword = p_Pasword
					where id_IP = p_IP;
					raise notice 'Все прошло успешно';
				end if;
			end if;
		end if;
	end if;
end;
$$;
call User_update('11212121','ISS','qQQQ#####111')

create or replace function Users_is_registreted (p_Login varchar, p_Pasword varchar)
returns table (ID_IP varchar)
language plpgsql
as $$
	begin 	 
		return query select
		Users.id_ip as "IP" from Users
		where Login = p_Login and Pasword = p_Pasword
		group by Users.ID_IP;
		raise notice 'Все прошло успешно';
	end;
$$;
select * from Users_is_registreted ('IS','qQQQ#####111')


create or replace function Users_check_registreted (p_Login varchar, p_Pasword varchar)
returns varchar
language plpgsql
as $$
	declare p_User_excist int := count(*) from Users
		where Login = p_Login and Pasword = p_Pasword;
	begin 	
		if p_User_excist = 1 then
			return '1';
		raise notice 'Все прошло успешно';
		else
			return 'Данного клиента нет в системе';
		end if;
	end;
$$;

select * from Users_check_registreted('ISS','qQQQ#####111')

/* ################################################################ */

CREATE TABLE Logs
(
	ID_Logs serial not null constraint PK_Logs primary key,
	Log_IP varchar(15) not null,
	Log_Date date not null default(current_date),
	Log_Log varchar not null
);

drop table Logs;

create or replace procedure Logs_insert (p_IP varchar(15), p_Date varchar, p_Log varchar)
language plpgsql
as $$
DECLARE
	p_excist_row int := count(*) from Logs
		where Log_Log = p_Log;
	p_date_date date;
begin
	if p_excist_row = 0 then
		p_date_date := to_date(p_Date::varchar, 'DD/MM/YYYY');
		insert into Logs(Log_IP, Log_Date, Log_Log)
			values(p_IP, p_date_date, p_Log);
		raise notice 'Все прошло успешно';
	else
		raise notice 'Данный лог уже есть в системе';
	end if;
end;
$$;

create or replace function Logs_sort_IP(p_IP varchar)
returns table ("Лог" varchar)
language plpgsql
as $$
	begin
	if (p_IP similar to '.*[0-9]*') and (length(p_IP) = 15) then
		return query select Log_Log from Logs;
		raise notice 'Все прошло успешно';
	else
		return query select Log_Log from Logs
			where Log_IP = p_IP
			order by Log_Date ASC;
		raise notice 'Все прошло успешно';
	end if;
	end;
$$;

create or replace function Logs_sort_date(p_IP varchar, p_Date varchar)
returns table ("Лог" varchar)
language plpgsql
as $$
	declare
	p_date_date date;
	begin
	p_date_date := to_date(p_Date, 'DD/MM/YYYY');
	if (p_IP similar to '.*[0-9]*') and (length(p_IP) = 15) then
		return query select Log_Log from Logs
			where p_date_date = Log_Date;
		raise notice 'Все прошло успешно';
	else
		return query select Log_Log from Logs
			where Log_IP = p_IP
			and p_date_date = Log_Date;
		raise notice 'Все прошло успешно';
	end if;
	end;
$$;

create or replace function Logs_sort_dates(p_IP varchar, p_Date_1 varchar, p_Date_2 varchar)
returns table ("Лог" varchar)
language plpgsql
as $$
	declare
	p_date_date_1 date;
	p_date_date_2 date;
	begin
	p_date_date_1 := to_date(p_Date_1, 'DD/MM/YYYY');
	p_date_date_2 := to_date(p_Date_2, 'DD/MM/YYYY');
	if (p_IP similar to '.*[0-9]*') and (length(p_IP) = 15) then
		return query select Log_Log from Logs
			where Log_Date between p_date_date_1 and p_date_date_2;
		raise notice 'Все прошло успешно';
	else
		return query select Log_Log from Logs
			where Log_IP = p_IP
			and Log_Date between p_date_date_1 and p_date_date_2;
			raise notice 'Все прошло успешно';
	end if;
	end;
$$;

select '...........100' similar to '.*[0-9]*';
select to_date('22/06/2023', 'DD/MM/yy');

select * from Logs;
select * from Users;
truncate table Logs;
truncate table Users;

call logs_insert('::1', '22/06/2023', '::1 - - [22/Jun/2023:21:59:19 +0300] "GET / HTTP/1.1" 200 46');
call logs_insert('::2', '22/06/2023', '::2 - - [22/Jun/2023:21:59:19 +0300] "GET / HTTP/1.1" 200 46');
call logs_insert('::3', '22/07/2023', '::3 - - [22/Jun/2023:21:59:19 +0300] "GET / HTTP/1.1" 200 46');
call logs_insert('::3', '22/09/2023', '::3 - - [22/09/2023:21:59:19 +0300] "GET / HTTP/1.1" 200 46');

select * from logs_sort_ip('::1');
select * from logs_sort_ip('::2');
select * from logs_sort_ip('::3');
select * from logs_sort_ip('.....0123456789');

select * from logs_sort_date('::3', '22/07/2023');
select * from logs_sort_date('::3', '22/09/2023');

select * from logs_sort_dates('::3', '22/07/2023', '22/09/2023');
select * from logs_sort_dates('.....0123456789', '22/06/2023', '22/09/2023');

/*			РОЛИ			*/
create role Users with password 'user_practica';
alter role Users LOGIN;
grant connect on database "Practice" to Users;

grant execute on procedure logs_insert to Users;
grant execute on procedure user_drop to Users;
grant execute on procedure user_insert to Users;
grant execute on procedure user_update to Users;

grant execute on function logs_sort_date to Users;
grant execute on function logs_sort_dates to Users;
grant execute on function logs_sort_ip to Users;
grant execute on function users_check_registreted to Users;
grant execute on function users_is_registreted to Users;

grant select, insert, update, delete on Users to Users;
grant select, insert, update, delete on Logs to Users;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO Users;