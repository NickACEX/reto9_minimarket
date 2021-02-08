


Script_SQL

CREATE DATABASE minimarket
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Peru.1252'
    LC_CTYPE = 'Spanish_Peru.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

------------------------

CREATE TABLE public.productos
(
    producto_id integer NOT NULL DEFAULT nextval('producto_id_seq'::regclass),
    nombre character varying(150) COLLATE pg_catalog."default",
    stock integer,
	precio integer,
    CONSTRAINT producto_id_pk PRIMARY KEY (producto_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.productos
    OWNER to postgres;

--------------
-- Table: public.facturas

-- DROP TABLE public.facturas;

CREATE TABLE public.facturas
(
    factura_id integer NOT NULL,
    producto_id integer NOT NULL,
    fecha_registro character varying(150) COLLATE pg_catalog."default",
	cantidad integer,
    costo integer,
    CONSTRAINT fac_prod_id_pk PRIMARY KEY (factura_id, producto_id),
    CONSTRAINT producto_id_fk FOREIGN KEY (producto_id)
        REFERENCES public.productos (producto_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.facturas
    OWNER to postgres;



CREATE TABLE public.perfiles
(
    perfil_id integer NOT NULL,
	perfil character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT perfil_id_pk PRIMARY KEY (perfil_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.perfiles
    OWNER to postgres;

INSERT INTO perfiles VALUES ('1', 'Administrador');
INSERT INTO perfiles VALUES ('2', 'Cajero');
INSERT INTO perfiles VALUES ('3', 'Almacenero');



	
CREATE TABLE public.usuarios
(
    usuario_id integer NOT NULL DEFAULT  nextval('usuario_id_seq'::regclass),
	usuario character varying(20) COLLATE pg_catalog."default",
  	contraseña character varying(20) COLLATE pg_catalog."default",
    perfil_id integer,
    CONSTRAINT usuario_id_pk PRIMARY KEY (usuario_id),
	CONSTRAINT perfil_id_fk FOREIGN KEY (perfil_id)
        REFERENCES public.perfiles (perfil_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.usuarios
    OWNER to postgres;

INSERT INTO usuarios VALUES ('1', 'admin','admin','1');
