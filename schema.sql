create database if not exists codetest;

use codetest;

drop table if exists person;
drop table if exists place;


create table `place` (
  `id` int not null auto_increment,
  `city` varchar(80) default null,
  `county` varchar(30) default null,
  `country` varchar(60) default null,
  primary key (`id`)
);

create table `person` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `place_of_birth_id` int,
  primary key (`id`),
  constraint fk_person_place_of_birth foreign key (place_of_birth_id) references place(id)
);
