drop table if exists entries;
create table entries (
    author text not null,
    body text not null
);

insert into entries values ('a','b');
