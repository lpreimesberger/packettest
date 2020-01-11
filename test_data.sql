
create table customer (
  id int primary key,
  name text not null
);

create table location (
  id serial primary key,
  name text not null,
  city text not null,
  state text
);

create table connection (
  id int primary key,
  descripton text not null,
  customer_id int not null references customer (id),
  location_id int not null references location (id)
);

create table connection_attribute (
  id int primary key,
  connection_id int not null references connection (id),
  name text not null,
  value text
);


insert into customer values
(1, 'Vandelay Industries'),
(2, 'Dunder Mifflin'),
(3, 'Reynholm Industries');

insert into location values
(1, 'LAS', 'Las Vegas', 'NV'),
(2, 'PDX', 'Portland', 'OR'),
(3, 'NYC', 'New York', 'NY'),
(4, 'CHI', 'Chicago', 'IL');

insert into connection values
(1, 'Dunder LAS', 1, 1),
(2, 'Dunder PDX', 1, 2),
(3, 'Dunder NYC', 1, 3),

(4, 'Vandelay NYC', 2, 3),
(5, 'Vandelay CHI', 2, 4),

(6, 'Reynholm LAS', 3, 1),
(7, 'Reynholm PDX', 3, 2)
;

insert into connection_attribute values
(1, 1, 'speed', '10G'),
(2, 1, 'status', 'active'),

(3, 2, 'speed', '10G'),
(4, 2, 'status', 'inactive'),

(5, 3, 'speed', '1G'),
(6, 3, 'status', 'active'),

(7, 4, 'speed', '100G'),
(8, 4, 'status', 'active'),
(9, 4, 'maintenance', 'scheduled'),

(10, 6, 'speed', '100G'),
(11, 6, 'status', 'active'),

(12, 7, 'speed', '1G'),
(13, 7, 'status', 'inactive')
;
