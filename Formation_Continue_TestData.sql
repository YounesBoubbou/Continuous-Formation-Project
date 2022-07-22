/* Population de la table des besoins avec quelques valeurs
hypothéthiques nécessaire au test de quelques fonctions d'agrégat*/
insert into besoin(besoin_nom, besoin_offert, besoin_programme)
	values ('finances', true, true),
		   ('urbanisme', true, false),
		   ('police administrative', true, true),
		   ('Etat civil', false, false),
		   ('Environnement', false, true),
		   ('Transport public', true, false),
		   ('Mecanismes de planification stratégique', false, false),
		   ('Democratie participative', true, true), 
		   ('Mécanismes délaboration et du suivi des projets', false, false),
		   ('Partenatiats et coopération décentralisés', false, true);

insert into commune(commune_nom, commune_adresse)
			values('Rabat', 'Avenue Mohammed Belhassan El Ouazzani'),
				  ('Temara', 'W3GR+X87, N1, Temara 12000'),
				  ('Sale', 'Av, Hassan II Rte de Meknés , Salé');

insert into domaine_de_formation(domaine_theme, domaine_lieu, domaine_date, domaine_formateur, domaine_effectif_max_elus)
			values('Urbanisme', 'Rabat', '2022-09-21', 'Younes Boubbou', 50)	