--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: visitas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visitas (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    data_cadastro date NOT NULL,
    endereco character varying(255) NOT NULL,
    problema text,
    hora time without time zone,
    valor numeric,
    forma_pagamento character varying(50)
);


ALTER TABLE public.visitas OWNER TO postgres;

--
-- Name: visitas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visitas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visitas_id_seq OWNER TO postgres;

--
-- Name: visitas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visitas_id_seq OWNED BY public.visitas.id;


--
-- Name: visitas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visitas ALTER COLUMN id SET DEFAULT nextval('public.visitas_id_seq'::regclass);


--
-- Data for Name: visitas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.visitas (id, nome, data_cadastro, endereco, problema, hora, valor, forma_pagamento) FROM stdin;
\.


--
-- Name: visitas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.visitas_id_seq', 7, true);


--
-- Name: visitas visitas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visitas
    ADD CONSTRAINT visitas_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

