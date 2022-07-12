/*Cette fonction a pour but d'extraire le NOMBRE de besoins qui ne sont pas encore offerts*/
create or replace function nombre_de_besoins_non_offerts()
returns int
language plpgsql
as $$
declare nombre_besoins_non_offerts int;
begin
	select count(besoin_nom)
	into nombre_besoins_non_offerts
	from besoin
	where besoin_offert = false;
	return nombre_besoins_non_offerts;
end;
$$;

/*Cette fonction a pour but d'extraire le nombre de besoins qui ne sont pas encore programmés*/
create or replace function nombre_de_besoins_non_programmes()
returns int
language plpgsql
as $$
declare nombre_besoins_non_programmes int;
begin
	select count(besoin_nom)
	into nombre_besoins_non_programmes
	from besoin
	where besoin_programme = false;
	return nombre_besoins_non_programmes;
end;
$$;

/*Cette fonction a pour but d'extraire et trier par ordre, le nombre de besoins les plus demandés*/
create or replace function besoins_les_plus_demandes()
returns void
language plpgsql
as $$
begin 
	select count(besoin_id) 
	from elu
	group by besoin_id
	order by besoin_id desc;
end;
$$;

