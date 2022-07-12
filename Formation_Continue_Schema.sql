drop table if exists Elu;
drop table if exists Domaine_De_Formation;
drop table if exists Besoin;
drop table if exists Commune;

create table Domaine_De_Formation(
	Domaine_Id serial not null primary key,
	Domaine_Theme varchar(50) unique not null,
	Domaine_Lieu varchar (50) not null,
	Domaine_Date date not null,
	Domaine_Formateur varchar(50) not null,
	Domaine_effectif_max_elus int not null
);

create table Besoin(
	Besoin_Id serial not null primary key,
	Besoin_Nom varchar(50) unique not null,
	Besoin_Offert boolean not null,
	Besoin_Programme boolean not null
);

create table Commune(
	Commune_Id serial not null primary key,
	Commune_Nom varchar(50) unique not null,
	Commune_Adresse varchar(50) unique not null
);

create table Elu(
	Elu_Id serial not null primary key,
	Elu_Nom varchar(50) not null, 
	Elu_Prenom varchar(50) not null, 
	Elu_Telephone char(10) unique not null, 
	Elu_email varchar(50) unique not null, 
	Elu_Niveau_Etudes varchar(50) not null, check(Elu_Niveau_Etudes = 'Néant' or Elu_Niveau_Etudes = 'Primaire'
										or Elu_Niveau_Etudes = 'Collège'
										or Elu_Niveau_Etudes = 'Lycée' or Elu_Niveau_Etudes = 'Institut Technique' 
										or Elu_Niveau_Etudes = 'Universitaire' or Elu_Niveau_Etudes = 'Supérieur'),
	Elu_Fonction varchar(50) not null,
	Elu_Commune varchar(50) not null, 
	Elu_Souhait varchar(50) not null,
	Domaine_Id int not null,
	Besoin_Id int not null,
	Commune_Id int not null,
	constraint inscrit foreign key(Domaine_Id) references Domaine_De_Formation(Domaine_Id)
	on update cascade on delete set null,
	constraint exprime foreign key(Besoin_Id) references Besoin(Besoin_Id)
	on update cascade on delete set null,
	constraint Appartient foreign key(Commune_Id) references Commune(Commune_Id)
	on update cascade on delete set null
	);
