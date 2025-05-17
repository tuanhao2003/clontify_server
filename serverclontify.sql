--
-- PostgreSQL database cluster dump
--

-- Started on 2025-05-17 07:38:31 UTC

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--

DROP DATABASE IF EXISTS admin;
DROP DATABASE IF EXISTS authservice;
DROP DATABASE IF EXISTS musicservice;
DROP DATABASE IF EXISTS storageservice;
DROP DATABASE IF EXISTS usersservice;




--
-- Drop roles
--

DROP ROLE IF EXISTS admin;


--
-- Roles
--

CREATE ROLE admin;
ALTER ROLE admin WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:LzAu705kYRQqugdE0cEDDA==$vOULEB0hBfje4pgiisTFalKlXmO8BgCNI9G2izVYopM=:7VJpUcbDdLyn5ESDwFvRhOoeF2T73Gh9VPdxJ5dmPDI=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:31 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- TOC entry 3341 (class 1262 OID 1)
-- Name: template1; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO admin;

\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3342 (class 0 OID 0)
-- Dependencies: 3341
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- TOC entry 3344 (class 0 OID 0)
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: admin
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3343 (class 0 OID 0)
-- Dependencies: 3341
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: admin
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


-- Completed on 2025-05-17 07:38:31 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "admin" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:31 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3341 (class 1262 OID 16384)
-- Name: admin; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE admin WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE admin OWNER TO admin;

\connect admin

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-05-17 07:38:31 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "authservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:31 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3373 (class 1262 OID 16385)
-- Name: authservice; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE authservice WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE authservice OWNER TO admin;

\connect authservice

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 16464)
-- Name: app_accounts; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_accounts (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    "roleId" uuid NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(254) NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.app_accounts OWNER TO admin;

--
-- TOC entry 217 (class 1259 OID 16479)
-- Name: app_roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_roles (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    name character varying(50) NOT NULL,
    description text
);


ALTER TABLE public.app_roles OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16450)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 16449)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3366 (class 0 OID 16464)
-- Dependencies: 216
-- Data for Name: app_accounts; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_accounts ("createdAt", "updatedAt", "deletedAt", "isActive", id, "roleId", username, email, password) FROM stdin;
2025-05-15 06:36:19.101057+00	2025-05-15 06:36:33.125263+00	\N	t	2f13a966-2624-406a-9e7e-1dcbe1359ded	27a3ff12-5e8a-4ca9-bb27-072e2497052e	admin@test.com	admin@test.com	pbkdf2_sha256$1000000$pghGPStHrmfZ1jGy9c1Nc6$i7TRLVHWlJLKjmBLKqN53SU6nB1dbz4JghZPLVrSWms=
\.


--
-- TOC entry 3367 (class 0 OID 16479)
-- Dependencies: 217
-- Data for Name: app_roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_roles ("createdAt", "updatedAt", "deletedAt", "isActive", id, name, description) FROM stdin;
2025-05-15 06:34:49.846085+00	2025-05-15 06:34:49.846085+00	\N	t	1e4578f1-b23f-402e-a197-589ea7f79578	ADMIN	Administrator role with full access
2025-05-15 06:34:49.846085+00	2025-05-15 06:34:49.846085+00	\N	t	27a3ff12-5e8a-4ca9-bb27-072e2497052e	NORMAL	Normal user role with limited access
2025-05-15 06:34:49.846085+00	2025-05-15 06:34:49.846085+00	\N	t	9b6f3b6c-629e-447d-9004-3632cfa971ac	MODERATOR	Moderator role with content management access
2025-05-15 06:34:49.846085+00	2025-05-15 06:34:49.846085+00	\N	t	5bb9c237-b42b-4628-aa3d-0bed008a8fdb	ARTIST	Artist role for music creators
\.


--
-- TOC entry 3365 (class 0 OID 16450)
-- Dependencies: 215
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-14 17:46:46.354571+00
\.


--
-- TOC entry 3374 (class 0 OID 0)
-- Dependencies: 214
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3211 (class 2606 OID 16478)
-- Name: app_accounts app_accounts_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_accounts
    ADD CONSTRAINT app_accounts_email_key UNIQUE (email);


--
-- TOC entry 3213 (class 2606 OID 16472)
-- Name: app_accounts app_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_accounts
    ADD CONSTRAINT app_accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 3216 (class 2606 OID 16476)
-- Name: app_accounts app_accounts_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_accounts
    ADD CONSTRAINT app_accounts_username_key UNIQUE (username);


--
-- TOC entry 3219 (class 2606 OID 16487)
-- Name: app_roles app_roles_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_roles
    ADD CONSTRAINT app_roles_name_key UNIQUE (name);


--
-- TOC entry 3221 (class 2606 OID 16485)
-- Name: app_roles app_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_roles
    ADD CONSTRAINT app_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3208 (class 2606 OID 16458)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3209 (class 1259 OID 16489)
-- Name: app_accounts_email_c93a1a72_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_accounts_email_c93a1a72_like ON public.app_accounts USING btree (email varchar_pattern_ops);


--
-- TOC entry 3214 (class 1259 OID 16488)
-- Name: app_accounts_username_77785171_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_accounts_username_77785171_like ON public.app_accounts USING btree (username varchar_pattern_ops);


--
-- TOC entry 3217 (class 1259 OID 16490)
-- Name: app_roles_name_49386e5b_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_roles_name_49386e5b_like ON public.app_roles USING btree (name varchar_pattern_ops);


-- Completed on 2025-05-17 07:38:31 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "musicservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:31 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3405 (class 1262 OID 16387)
-- Name: musicservice; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE musicservice WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE musicservice OWNER TO admin;

\connect musicservice

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 16397)
-- Name: app_albums; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_albums (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    "storageImageId" uuid,
    "artistId" uuid NOT NULL
);


ALTER TABLE public.app_albums OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16405)
-- Name: app_albumsong; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_albumsong (
    id bigint NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    "albumId" uuid NOT NULL,
    "songId" uuid NOT NULL,
    "order" integer,
    CONSTRAINT app_albumsong_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.app_albumsong OWNER TO admin;

--
-- TOC entry 217 (class 1259 OID 16404)
-- Name: app_albumsong_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.app_albumsong ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_albumsong_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16411)
-- Name: app_genres; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_genres (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    description text
);


ALTER TABLE public.app_genres OWNER TO admin;

--
-- TOC entry 221 (class 1259 OID 16421)
-- Name: app_genresong; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_genresong (
    id bigint NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    "songID" uuid NOT NULL,
    "genreID" uuid NOT NULL
);


ALTER TABLE public.app_genresong OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 16420)
-- Name: app_genresong_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.app_genresong ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_genresong_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 222 (class 1259 OID 16426)
-- Name: app_songs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_songs (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    description character varying,
    "artistId" uuid NOT NULL,
    "storageId" uuid NOT NULL,
    "storageImageId" uuid,
    duration integer,
    "songType" character varying(255) NOT NULL,
    CONSTRAINT app_songs_duration_check CHECK ((duration >= 0))
);


ALTER TABLE public.app_songs OWNER TO admin;

--
-- TOC entry 224 (class 1259 OID 16437)
-- Name: app_songsubartist; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_songsubartist (
    id bigint NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    "songID" uuid NOT NULL,
    "subArtistID" uuid NOT NULL
);


ALTER TABLE public.app_songsubartist OWNER TO admin;

--
-- TOC entry 223 (class 1259 OID 16436)
-- Name: app_songsubartist_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.app_songsubartist ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_songsubartist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 215 (class 1259 OID 16390)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 16389)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3391 (class 0 OID 16397)
-- Dependencies: 216
-- Data for Name: app_albums; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_albums ("createdAt", "updatedAt", "deletedAt", "isActive", id, name, description, "storageImageId", "artistId") FROM stdin;
2025-05-17 06:24:15.204489+00	2025-05-17 06:24:15.21661+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	album con vịt	con vịt làm nhạc	fa5241cd-1fc2-414c-8ee8-885b0fafe80f	2f13a966-2624-406a-9e7e-1dcbe1359ded
\.


--
-- TOC entry 3393 (class 0 OID 16405)
-- Dependencies: 218
-- Data for Name: app_albumsong; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_albumsong (id, "createdAt", "updatedAt", "deletedAt", "isActive", "albumId", "songId", "order") FROM stdin;
1	2025-05-17 06:32:18.556508+00	2025-05-17 06:32:18.556934+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	1d2e42d2-1d75-48d5-a1d7-b3316093fa98	\N
2	2025-05-17 06:38:23.580059+00	2025-05-17 06:38:23.580534+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	2ba7d538-c5ad-4389-b2f1-39fe05742d92	\N
3	2025-05-17 06:44:00.496476+00	2025-05-17 06:44:00.496831+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	5e52c7dd-8eb3-46fd-adbe-137d90e20ecd	\N
4	2025-05-17 06:47:45.998519+00	2025-05-17 06:47:45.998978+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	eb458f7b-256e-4a09-8ae6-fab5816d4ee7	\N
5	2025-05-17 06:49:06.846119+00	2025-05-17 06:49:06.846987+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	722077d4-91e8-48a9-9e63-16c4cea8a6c1	\N
6	2025-05-17 06:51:58.276254+00	2025-05-17 06:51:58.276794+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	f60fafda-893d-4c72-ae36-17f1c2a1275d	\N
7	2025-05-17 06:55:06.779207+00	2025-05-17 06:55:06.780044+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	605affec-defb-4e9e-8952-2b46185f1406	\N
8	2025-05-17 07:02:53.542255+00	2025-05-17 07:02:53.542901+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	3e5d4095-345e-440e-ae43-56a16de61cab	\N
9	2025-05-17 07:14:05.240798+00	2025-05-17 07:14:05.241204+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	1998043a-c548-482d-a44b-daa281388afa	\N
10	2025-05-17 07:16:20.853114+00	2025-05-17 07:16:20.853564+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	63231225-f90f-4f0e-959c-eb45cf75ca8d	\N
11	2025-05-17 07:27:04.105715+00	2025-05-17 07:27:04.106248+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	3e7a77a9-d04c-4e2b-acf7-7a8a3a7fc1a6	\N
12	2025-05-17 07:32:16.35375+00	2025-05-17 07:32:16.354245+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	f1bc13a5-47af-40cb-8a97-08ffe823f957	\N
13	2025-05-17 07:34:05.169221+00	2025-05-17 07:34:05.169673+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	5f31ccc2-8839-444d-8021-a1c5b7f1b334	\N
\.


--
-- TOC entry 3394 (class 0 OID 16411)
-- Dependencies: 219
-- Data for Name: app_genres; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_genres ("createdAt", "updatedAt", "deletedAt", "isActive", id, name, description) FROM stdin;
\.


--
-- TOC entry 3396 (class 0 OID 16421)
-- Dependencies: 221
-- Data for Name: app_genresong; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_genresong (id, "createdAt", "updatedAt", "deletedAt", "isActive", "songID", "genreID") FROM stdin;
\.


--
-- TOC entry 3397 (class 0 OID 16426)
-- Dependencies: 222
-- Data for Name: app_songs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_songs ("createdAt", "updatedAt", "deletedAt", "isActive", id, title, description, "artistId", "storageId", "storageImageId", duration, "songType") FROM stdin;
2025-05-17 07:34:05.139537+00	2025-05-17 07:34:05.152928+00	\N	t	5f31ccc2-8839-444d-8021-a1c5b7f1b334	Cứu lấy con vịt 188k	Con vịt làm nhạc đầu tay	2f13a966-2624-406a-9e7e-1dcbe1359ded	2bf58607-ec90-42b6-b237-e12889be84d3	fa5241cd-1fc2-414c-8ee8-885b0fafe80f	25	SONG
\.


--
-- TOC entry 3399 (class 0 OID 16437)
-- Dependencies: 224
-- Data for Name: app_songsubartist; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_songsubartist (id, "createdAt", "updatedAt", "deletedAt", "isActive", "songID", "subArtistID") FROM stdin;
\.


--
-- TOC entry 3390 (class 0 OID 16390)
-- Dependencies: 215
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-14 17:46:46.045652+00
\.


--
-- TOC entry 3406 (class 0 OID 0)
-- Dependencies: 217
-- Name: app_albumsong_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_albumsong_id_seq', 13, true);


--
-- TOC entry 3407 (class 0 OID 0)
-- Dependencies: 220
-- Name: app_genresong_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_genresong_id_seq', 1, false);


--
-- TOC entry 3408 (class 0 OID 0)
-- Dependencies: 223
-- Name: app_songsubartist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_songsubartist_id_seq', 1, false);


--
-- TOC entry 3409 (class 0 OID 0)
-- Dependencies: 214
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3231 (class 2606 OID 16403)
-- Name: app_albums app_albums_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_albums
    ADD CONSTRAINT app_albums_pkey PRIMARY KEY (id);


--
-- TOC entry 3233 (class 2606 OID 16410)
-- Name: app_albumsong app_albumsong_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_albumsong
    ADD CONSTRAINT app_albumsong_pkey PRIMARY KEY (id);


--
-- TOC entry 3236 (class 2606 OID 16419)
-- Name: app_genres app_genres_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genres
    ADD CONSTRAINT app_genres_name_key UNIQUE (name);


--
-- TOC entry 3238 (class 2606 OID 16417)
-- Name: app_genres app_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genres
    ADD CONSTRAINT app_genres_pkey PRIMARY KEY (id);


--
-- TOC entry 3240 (class 2606 OID 16425)
-- Name: app_genresong app_genresong_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genresong
    ADD CONSTRAINT app_genresong_pkey PRIMARY KEY (id);


--
-- TOC entry 3242 (class 2606 OID 16433)
-- Name: app_songs app_songs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songs
    ADD CONSTRAINT app_songs_pkey PRIMARY KEY (id);


--
-- TOC entry 3244 (class 2606 OID 16435)
-- Name: app_songs app_songs_storageId_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songs
    ADD CONSTRAINT "app_songs_storageId_key" UNIQUE ("storageId");


--
-- TOC entry 3246 (class 2606 OID 16441)
-- Name: app_songsubartist app_songsubartist_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songsubartist
    ADD CONSTRAINT app_songsubartist_pkey PRIMARY KEY (id);


--
-- TOC entry 3229 (class 2606 OID 16396)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3234 (class 1259 OID 16442)
-- Name: app_genres_name_d0524fa1_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_genres_name_d0524fa1_like ON public.app_genres USING btree (name varchar_pattern_ops);


-- Completed on 2025-05-17 07:38:32 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:32 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE postgres;
--
-- TOC entry 3341 (class 1262 OID 5)
-- Name: postgres; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO admin;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3342 (class 0 OID 0)
-- Dependencies: 3341
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


-- Completed on 2025-05-17 07:38:32 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "storageservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:32 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3360 (class 1262 OID 16388)
-- Name: storageservice; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE storageservice WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE storageservice OWNER TO admin;

\connect storageservice

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 24589)
-- Name: app_storagedata; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_storagedata (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    "userId" uuid NOT NULL,
    "fileName" character varying(255) NOT NULL,
    "fileType" character varying(255) NOT NULL,
    "fileSize" integer NOT NULL,
    "fileUrl" character varying(200),
    description text
);


ALTER TABLE public.app_storagedata OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 24582)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 24581)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3354 (class 0 OID 24589)
-- Dependencies: 216
-- Data for Name: app_storagedata; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_storagedata ("createdAt", "updatedAt", "deletedAt", "isActive", id, "userId", "fileName", "fileType", "fileSize", "fileUrl", description) FROM stdin;
2025-05-17 06:29:11.646591+00	2025-05-17 06:29:11.659205+00	\N	t	2bf58607-ec90-42b6-b237-e12889be84d3	2f13a966-2624-406a-9e7e-1dcbe1359ded	358236eb-92f1-43e8-8f86-f787f0fea3a4.mp3	audio/mpeg	409964	audios/358236eb-92f1-43e8-8f86-f787f0fea3a4.mp3	nhạc của con vịt
2025-05-17 06:22:59.183593+00	2025-05-17 06:22:59.195057+00	\N	t	fa5241cd-1fc2-414c-8ee8-885b0fafe80f	2f13a966-2624-406a-9e7e-1dcbe1359ded	55a12c88-7a34-4002-af53-696d95e7cdf0.jpg	image/jpeg	32730	images/55a12c88-7a34-4002-af53-696d95e7cdf0.jpg	Con vịt
\.


--
-- TOC entry 3353 (class 0 OID 24582)
-- Dependencies: 215
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-15 06:32:24.748304+00
\.


--
-- TOC entry 3361 (class 0 OID 0)
-- Dependencies: 214
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3207 (class 2606 OID 24597)
-- Name: app_storagedata app_storagedata_fileName_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_storagedata
    ADD CONSTRAINT "app_storagedata_fileName_key" UNIQUE ("fileName");


--
-- TOC entry 3209 (class 2606 OID 24595)
-- Name: app_storagedata app_storagedata_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_storagedata
    ADD CONSTRAINT app_storagedata_pkey PRIMARY KEY (id);


--
-- TOC entry 3204 (class 2606 OID 24588)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3205 (class 1259 OID 24598)
-- Name: app_storagedata_fileName_ee290168_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "app_storagedata_fileName_ee290168_like" ON public.app_storagedata USING btree ("fileName" varchar_pattern_ops);


-- Completed on 2025-05-17 07:38:32 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "usersservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.10

-- Started on 2025-05-17 07:38:32 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3359 (class 1262 OID 16386)
-- Name: usersservice; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE usersservice WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE usersservice OWNER TO admin;

\connect usersservice

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 16459)
-- Name: app_profiles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_profiles (
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    id uuid NOT NULL,
    "accountID" uuid NOT NULL,
    "fullName" text NOT NULL,
    "avatarUrl" character varying(200),
    bio text,
    "dateOfBirth" date,
    "phoneNumber" character varying(20)
);


ALTER TABLE public.app_profiles OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16444)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 16443)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3353 (class 0 OID 16459)
-- Dependencies: 216
-- Data for Name: app_profiles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_profiles ("createdAt", "updatedAt", "deletedAt", "isActive", id, "accountID", "fullName", "avatarUrl", bio, "dateOfBirth", "phoneNumber") FROM stdin;
2025-05-15 06:36:19.179188+00	2025-05-15 06:36:19.179643+00	\N	t	efd7d6cf-85a8-4e46-aacd-22608f941752	2f13a966-2624-406a-9e7e-1dcbe1359ded	Dimsum	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8WOsLxlKgTXh7gry1qONjjpnozv1IwdHf165tgttVd5FiaWx4G8yOo4LCWt9uPt6y0EWxE89oyHdEPbgre41s8Q		2003-01-01	
\.


--
-- TOC entry 3352 (class 0 OID 16444)
-- Dependencies: 215
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-14 17:46:46.291627+00
\.


--
-- TOC entry 3360 (class 0 OID 0)
-- Dependencies: 214
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3206 (class 2606 OID 16474)
-- Name: app_profiles app_profiles_accountID_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_profiles
    ADD CONSTRAINT "app_profiles_accountID_key" UNIQUE ("accountID");


--
-- TOC entry 3208 (class 2606 OID 16470)
-- Name: app_profiles app_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_profiles
    ADD CONSTRAINT app_profiles_pkey PRIMARY KEY (id);


--
-- TOC entry 3204 (class 2606 OID 16456)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


-- Completed on 2025-05-17 07:38:32 UTC

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-05-17 07:38:32 UTC

--
-- PostgreSQL database cluster dump complete
--

