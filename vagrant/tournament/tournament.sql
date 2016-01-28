-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create table players (

	id serial primary key,
	name text not null

);

create table matches(

	id_match serial primary key,
	id_player1 integer references players(id),
	id_player2 integer references players(id),
	winner integer references players(id)

);


create table standings (

	id_player integer references players(id),
	n_wins integer,
	n_loss integer
);