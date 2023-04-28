SET FOREIGN_KEY_CHECKS=0; -- to disable them
delete from purchases;
delete from ticket;
delete from airline_staff;
delete from booking_agent;
delete from customer;
delete from flight;
delete from airport;
delete from airplane;
delete from airline;

insert into airline values ('China Eastern');
insert into airline values ('Sichuan Airline');

insert into airport values ('JFK', 'NYC');
insert into airport values ('PVG', 'Shanghai');

insert into customer values ('111@nyu.edu', 'jeff', '123456', '666', '123', 'Shanghai', 'China', '12345678', 'AB123456', '2025-5-11', 'China', '2003-03-08');
insert into customer values ('121@nyu.edu', 'copy', '1234567', '6666', '1234', 'Shanghai', 'China', '87654321', 'CD123456', '2026-5-11', 'China', '2003-03-08');

insert into booking_agent values ('222@nyu.edu', '34556', '33456');

insert into airplane values ('China Eastern', '111', '250');
insert into airplane values ('Sichuan Airline', '1111', '290');

insert into airline_staff values ('Feiwu', '12345', 'Peter', 'Yao', '1111-11-11','China Eastern');

insert into flight values ('China Eastern', '123', 'JFK', '2022-04-22 10:34:23.55', 'PVG','2022-04-22 12:34:23.55', '500', 'delayed', '111');
insert into flight values ('Sichuan Airline', '14234', 'PVG','2022-04-22 11:34:23.55', 'JFK', '2022-04-22 13:34:23.55', '500', 'in-progress', '1111');
insert into flight values ('Sichuan Airline', '13234', 'JFK', '2022-05-22 10:34:23.55', 'PVG', '2022-05-22 13:34:23.55','500', 'upcoming', '1111');

insert into ticket values ('1', 'China Eastern', '123');
insert into ticket values ('2', 'Sichuan Airline', '14234');

insert into purchases values ('1', '121@nyu.edu', null, '2022-04-20');
insert into purchases values ('2', '111@nyu.edu', 33456, '2022-04-19')
