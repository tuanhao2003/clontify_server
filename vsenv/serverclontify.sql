--
-- PostgreSQL database cluster dump
--

-- Started on 2025-05-17 17:23:57 UTC

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
ALTER ROLE admin WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:toxUUm5xwEExwIyN1FUH6Q==$TFAylDvUUaOzjaV1K2iXFI7hfZfgIJo4XVGMBElR6f4=:3thJ/CLSzfay/26bqw9TS4Z7L8dfA6SbqpmQSxnnfR4=';

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

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:57 UTC

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
-- TOC entry 3341 (class 1262 OID 16523)
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


-- Completed on 2025-05-17 17:23:57 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "admin" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:57 UTC

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
-- TOC entry 3341 (class 1262 OID 16524)
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

-- Completed on 2025-05-17 17:23:57 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "authservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:57 UTC

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
-- TOC entry 3373 (class 1262 OID 16525)
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
-- TOC entry 214 (class 1259 OID 16526)
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
-- TOC entry 215 (class 1259 OID 16531)
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
-- TOC entry 216 (class 1259 OID 16536)
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
-- TOC entry 217 (class 1259 OID 16541)
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
-- TOC entry 3364 (class 0 OID 16526)
-- Dependencies: 214
-- Data for Name: app_accounts; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_accounts ("createdAt", "updatedAt", "deletedAt", "isActive", id, "roleId", username, email, password) FROM stdin;
2025-05-17 09:48:25.92799+00	2025-05-17 09:48:25.928419+00	\N	t	b69608cd-0643-4777-9076-7832c63b8ee8	7a96a6e4-71a1-4f1c-8b73-a328ca0a3ebd	huynhhoaithu123456@gmail.com	huynhhoaithu123456@gmail.com	pbkdf2_sha256$1000000$sV4raDj7t0fZHr6iZ7evzD$2iogCo4Tqi1fpn04zB4EMwLVZi5W5Np7E//2xC3OC0M=
2025-05-17 13:49:37.601939+00	2025-05-17 13:49:37.602239+00	\N	t	cd1f9d14-685a-4108-a899-c95089073675	7a96a6e4-71a1-4f1c-8b73-a328ca0a3ebd	loc01633224199@gmail.com	loc01633224199@gmail.com	pbkdf2_sha256$1000000$xlmUj1aRt6tMipXZOQ1cd7$MccTgo7XDACPGs/+Ug3q3SRg7bf9dHJg5tK4dfhe++U=
2025-05-16 03:12:46.789007+00	2025-05-17 13:52:26.927238+00	\N	t	e8716e1b-8f73-45ee-9fad-177aea71e0dc	7a96a6e4-71a1-4f1c-8b73-a328ca0a3ebd	huynhthanhloc913@gmail.com	huynhthanhloc913@gmail.com	pbkdf2_sha256$1000000$DM3LfpK93O4L988Ywl1QHY$UigCAR0KTRGwf8+ShRGLPCk5REPxdYW1Q9v9jOrR2TE=
2025-05-17 17:11:18.738531+00	2025-05-17 17:11:18.738974+00	\N	t	00c0d49f-29d4-4fa3-bc41-e5879c955bb5	7a96a6e4-71a1-4f1c-8b73-a328ca0a3ebd	mmsb@gmail.com	mmsb@gmail.com	pbkdf2_sha256$1000000$RxyCLZyMgE2LA1hCJgGPoc$rg8fQ3v51lL3es1CGMZy9FyyvgWSDRA5KddR91yufc4=
\.


--
-- TOC entry 3365 (class 0 OID 16531)
-- Dependencies: 215
-- Data for Name: app_roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_roles ("createdAt", "updatedAt", "deletedAt", "isActive", id, name, description) FROM stdin;
2025-05-16 03:11:32.699945+00	2025-05-16 03:11:32.699945+00	\N	t	8fd0337b-7f29-4bd2-aad4-e46b92a08bb8	ADMIN	Administrator role with full access
2025-05-16 03:11:32.699945+00	2025-05-16 03:11:32.699945+00	\N	t	7a96a6e4-71a1-4f1c-8b73-a328ca0a3ebd	NORMAL	Normal user role with limited access
2025-05-16 03:11:32.699945+00	2025-05-16 03:11:32.699945+00	\N	t	78a1effd-495c-4ab1-a6f9-f1e0678dd712	MODERATOR	Moderator role with content management access
2025-05-16 03:11:32.699945+00	2025-05-16 03:11:32.699945+00	\N	t	c83fd36f-c138-44b6-9233-5b9240443f63	ARTIST	Artist role for music creators
\.


--
-- TOC entry 3366 (class 0 OID 16536)
-- Dependencies: 216
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-16 03:09:30.684802+00
\.


--
-- TOC entry 3374 (class 0 OID 0)
-- Dependencies: 217
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3209 (class 2606 OID 16543)
-- Name: app_accounts app_accounts_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_accounts
    ADD CONSTRAINT app_accounts_email_key UNIQUE (email);


--
-- TOC entry 3211 (class 2606 OID 16545)
-- Name: app_accounts app_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_accounts
    ADD CONSTRAINT app_accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 3214 (class 2606 OID 16547)
-- Name: app_accounts app_accounts_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_accounts
    ADD CONSTRAINT app_accounts_username_key UNIQUE (username);


--
-- TOC entry 3217 (class 2606 OID 16549)
-- Name: app_roles app_roles_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_roles
    ADD CONSTRAINT app_roles_name_key UNIQUE (name);


--
-- TOC entry 3219 (class 2606 OID 16551)
-- Name: app_roles app_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_roles
    ADD CONSTRAINT app_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3221 (class 2606 OID 16553)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3207 (class 1259 OID 16554)
-- Name: app_accounts_email_c93a1a72_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_accounts_email_c93a1a72_like ON public.app_accounts USING btree (email varchar_pattern_ops);


--
-- TOC entry 3212 (class 1259 OID 16555)
-- Name: app_accounts_username_77785171_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_accounts_username_77785171_like ON public.app_accounts USING btree (username varchar_pattern_ops);


--
-- TOC entry 3215 (class 1259 OID 16556)
-- Name: app_roles_name_49386e5b_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_roles_name_49386e5b_like ON public.app_roles USING btree (name varchar_pattern_ops);


-- Completed on 2025-05-17 17:23:58 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "musicservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:58 UTC

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
-- TOC entry 3411 (class 1262 OID 16557)
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
-- TOC entry 214 (class 1259 OID 16558)
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
-- TOC entry 215 (class 1259 OID 16563)
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
-- TOC entry 216 (class 1259 OID 16567)
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
-- TOC entry 217 (class 1259 OID 16568)
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
-- TOC entry 218 (class 1259 OID 16573)
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
-- TOC entry 219 (class 1259 OID 16576)
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
-- TOC entry 220 (class 1259 OID 16577)
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
-- TOC entry 221 (class 1259 OID 16583)
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
-- TOC entry 222 (class 1259 OID 16586)
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
-- TOC entry 223 (class 1259 OID 16587)
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
-- TOC entry 224 (class 1259 OID 16592)
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
-- TOC entry 3395 (class 0 OID 16558)
-- Dependencies: 214
-- Data for Name: app_albums; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_albums ("createdAt", "updatedAt", "deletedAt", "isActive", id, name, description, "storageImageId", "artistId") FROM stdin;
2025-05-17 06:24:15.204489+00	2025-05-17 06:24:15.21661+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	album con vịt	con vịt làm nhạc	fa5241cd-1fc2-414c-8ee8-885b0fafe80c	2f13a966-2624-406a-9e7e-1dcbe1359ded
\.


--
-- TOC entry 3396 (class 0 OID 16563)
-- Dependencies: 215
-- Data for Name: app_albumsong; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_albumsong (id, "createdAt", "updatedAt", "deletedAt", "isActive", "albumId", "songId", "order") FROM stdin;
1	2025-05-16 08:25:15.281082+00	2025-05-16 08:25:15.28135+00	\N	t	ee342311-db01-4a62-bf2d-d469f7f28c46	9d8c3af2-f9c3-4fde-a6e5-b5098f28223c	\N
\.


--
-- TOC entry 3398 (class 0 OID 16568)
-- Dependencies: 217
-- Data for Name: app_genres; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_genres ("createdAt", "updatedAt", "deletedAt", "isActive", id, name, description) FROM stdin;
\.


--
-- TOC entry 3399 (class 0 OID 16573)
-- Dependencies: 218
-- Data for Name: app_genresong; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_genresong (id, "createdAt", "updatedAt", "deletedAt", "isActive", "songID", "genreID") FROM stdin;
\.


--
-- TOC entry 3401 (class 0 OID 16577)
-- Dependencies: 220
-- Data for Name: app_songs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_songs ("createdAt", "updatedAt", "deletedAt", "isActive", id, title, description, "artistId", "storageId", "storageImageId", duration, "songType") FROM stdin;
2025-05-17 07:46:09.551779+00	2025-05-17 07:46:09.562471+00	\N	t	9d8c3af2-f9c3-4fde-a6e5-b5098f28223c	cứu lấy âm nhạc	Con vịt làm nhạc đầu tay	9d8c3af2-f9c3-4fde-a6e5-b5098f28222b	2bf58607-ec90-42b6-b237-e12889be84d3	fa5241cd-1fc2-414c-8ee8-885b0fafe80f	25	SONG
\.


--
-- TOC entry 3402 (class 0 OID 16583)
-- Dependencies: 221
-- Data for Name: app_songsubartist; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_songsubartist (id, "createdAt", "updatedAt", "deletedAt", "isActive", "songID", "subArtistID") FROM stdin;
\.


--
-- TOC entry 3404 (class 0 OID 16587)
-- Dependencies: 223
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-16 03:09:30.249255+00
\.


--
-- TOC entry 3412 (class 0 OID 0)
-- Dependencies: 216
-- Name: app_albumsong_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_albumsong_id_seq', 2, true);


--
-- TOC entry 3413 (class 0 OID 0)
-- Dependencies: 219
-- Name: app_genresong_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_genresong_id_seq', 1, false);


--
-- TOC entry 3414 (class 0 OID 0)
-- Dependencies: 222
-- Name: app_songsubartist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_songsubartist_id_seq', 1, false);


--
-- TOC entry 3415 (class 0 OID 0)
-- Dependencies: 224
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3229 (class 2606 OID 16594)
-- Name: app_albums app_albums_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_albums
    ADD CONSTRAINT app_albums_pkey PRIMARY KEY (id);


--
-- TOC entry 3231 (class 2606 OID 16596)
-- Name: app_albumsong app_albumsong_albumId_songId_7f9306e5_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_albumsong
    ADD CONSTRAINT "app_albumsong_albumId_songId_7f9306e5_uniq" UNIQUE ("albumId", "songId");


--
-- TOC entry 3233 (class 2606 OID 16598)
-- Name: app_albumsong app_albumsong_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_albumsong
    ADD CONSTRAINT app_albumsong_pkey PRIMARY KEY (id);


--
-- TOC entry 3236 (class 2606 OID 16600)
-- Name: app_genres app_genres_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genres
    ADD CONSTRAINT app_genres_name_key UNIQUE (name);


--
-- TOC entry 3238 (class 2606 OID 16602)
-- Name: app_genres app_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genres
    ADD CONSTRAINT app_genres_pkey PRIMARY KEY (id);


--
-- TOC entry 3240 (class 2606 OID 16604)
-- Name: app_genresong app_genresong_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genresong
    ADD CONSTRAINT app_genresong_pkey PRIMARY KEY (id);


--
-- TOC entry 3242 (class 2606 OID 16606)
-- Name: app_genresong app_genresong_songID_genreID_0f2b3e43_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_genresong
    ADD CONSTRAINT "app_genresong_songID_genreID_0f2b3e43_uniq" UNIQUE ("songID", "genreID");


--
-- TOC entry 3244 (class 2606 OID 16608)
-- Name: app_songs app_songs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songs
    ADD CONSTRAINT app_songs_pkey PRIMARY KEY (id);


--
-- TOC entry 3246 (class 2606 OID 16610)
-- Name: app_songs app_songs_storageId_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songs
    ADD CONSTRAINT "app_songs_storageId_key" UNIQUE ("storageId");


--
-- TOC entry 3248 (class 2606 OID 16612)
-- Name: app_songsubartist app_songsubartist_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songsubartist
    ADD CONSTRAINT app_songsubartist_pkey PRIMARY KEY (id);


--
-- TOC entry 3250 (class 2606 OID 16614)
-- Name: app_songsubartist app_songsubartist_songID_subArtistID_07c369d1_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_songsubartist
    ADD CONSTRAINT "app_songsubartist_songID_subArtistID_07c369d1_uniq" UNIQUE ("songID", "subArtistID");


--
-- TOC entry 3252 (class 2606 OID 16616)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3234 (class 1259 OID 16617)
-- Name: app_genres_name_d0524fa1_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_genres_name_d0524fa1_like ON public.app_genres USING btree (name varchar_pattern_ops);


-- Completed on 2025-05-17 17:23:58 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:58 UTC

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
-- TOC entry 3341 (class 1262 OID 16618)
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


-- Completed on 2025-05-17 17:23:58 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "storageservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:58 UTC

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
-- TOC entry 3360 (class 1262 OID 16619)
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
-- TOC entry 214 (class 1259 OID 16620)
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
-- TOC entry 215 (class 1259 OID 16625)
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
-- TOC entry 216 (class 1259 OID 16630)
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
-- TOC entry 3352 (class 0 OID 16620)
-- Dependencies: 214
-- Data for Name: app_storagedata; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_storagedata ("createdAt", "updatedAt", "deletedAt", "isActive", id, "userId", "fileName", "fileType", "fileSize", "fileUrl", description) FROM stdin;
2025-05-17 06:29:11.646591+00	2025-05-17 06:29:11.659205+00	\N	t	2bf58607-ec90-42b6-b237-e12889be84d3	2f13a966-2624-406a-9e7e-1dcbe1359ded	358236eb-92f1-43e8-8f86-f787f0fea3a4.mp3	audio/mpeg	409964	audios/358236eb-92f1-43e8-8f86-f787f0fea3a4.mp3	nhạc của con vịt
2025-05-17 06:22:59.183593+00	2025-05-17 06:22:59.195057+00	\N	t	fa5241cd-1fc2-414c-8ee8-885b0fafe80f	2f13a966-2624-406a-9e7e-1dcbe1359ded	55a12c88-7a34-4002-af53-696d95e7cdf0.jpg	image/jpeg	32730	images/55a12c88-7a34-4002-af53-696d95e7cdf0.jpg	Con vịt
2025-05-17 06:22:59.183593+00	2025-05-17 06:22:59.195057+00	\N	t	fa5241cd-1fc2-414c-8ee8-885b0fafe80c	2f13a966-2624-406a-9e7e-1dcbe1359ded	55a12c88-7a34-4002-af53-696d95e7cd0.jpg	image/jpeg	32730	https://i.ytimg.com/vi/zh_PH_XmS4A/maxresdefault.jpg	album con vịt
\.


--
-- TOC entry 3353 (class 0 OID 16625)
-- Dependencies: 215
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-16 03:09:30.889014+00
\.


--
-- TOC entry 3361 (class 0 OID 0)
-- Dependencies: 216
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3205 (class 2606 OID 16632)
-- Name: app_storagedata app_storagedata_fileName_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_storagedata
    ADD CONSTRAINT "app_storagedata_fileName_key" UNIQUE ("fileName");


--
-- TOC entry 3207 (class 2606 OID 16634)
-- Name: app_storagedata app_storagedata_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_storagedata
    ADD CONSTRAINT app_storagedata_pkey PRIMARY KEY (id);


--
-- TOC entry 3209 (class 2606 OID 16636)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3203 (class 1259 OID 16637)
-- Name: app_storagedata_fileName_ee290168_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "app_storagedata_fileName_ee290168_like" ON public.app_storagedata USING btree ("fileName" varchar_pattern_ops);


-- Completed on 2025-05-17 17:23:58 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "usersservice" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-17 17:23:58 UTC

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
-- TOC entry 3370 (class 1262 OID 16638)
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
-- TOC entry 214 (class 1259 OID 16639)
-- Name: app_favorites; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_favorites (
    id bigint NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "deletedAt" timestamp with time zone,
    "isActive" boolean NOT NULL,
    "profileID" uuid NOT NULL,
    "songID" uuid NOT NULL
);


ALTER TABLE public.app_favorites OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16642)
-- Name: app_favorites_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.app_favorites ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.app_favorites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 216 (class 1259 OID 16643)
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
-- TOC entry 217 (class 1259 OID 16648)
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
-- TOC entry 218 (class 1259 OID 16653)
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
-- TOC entry 3360 (class 0 OID 16639)
-- Dependencies: 214
-- Data for Name: app_favorites; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_favorites (id, "createdAt", "updatedAt", "deletedAt", "isActive", "profileID", "songID") FROM stdin;
1	2025-05-17 17:21:42.788083+00	2025-05-17 17:21:42.788083+00	\N	t	d801ba03-323b-438c-8887-47bf33c8cc07	9d8c3af2-f9c3-4fde-a6e5-b5098f28223c
\.


--
-- TOC entry 3362 (class 0 OID 16643)
-- Dependencies: 216
-- Data for Name: app_profiles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.app_profiles ("createdAt", "updatedAt", "deletedAt", "isActive", id, "accountID", "fullName", "avatarUrl", bio, "dateOfBirth", "phoneNumber") FROM stdin;
2025-05-16 03:12:46.838979+00	2025-05-16 15:04:00.414412+00	\N	t	efd7d6cf-85a8-4e46-aacd-22608f941752	e8716e1b-8f73-45ee-9fad-177aea71e0dc	Huỳnh Thanh Lộc	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8WOsLxlKgTXh7gry1qONjjpnozv1IwdHf165tgttVd5FiaWx4G8yOo4LCWt9uPt6y0EWxE89oyHdEPbgre41s8Q	chac chan la nhu vay roi\nWumen bu yijang\n	2003-11-04	
2025-05-17 09:48:25.984941+00	2025-05-17 09:52:07.251893+00	\N	t	9d8c3af2-f9c3-4fde-a6e5-b5098f28222b	b69608cd-0643-4777-9076-7832c63b8ee8	Nguyễn Huỳnh Tuấn Hào	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoRASepRti6x5t2Se54-1R_mJHvziliPOR-A&s		2003-11-04	
2025-05-17 13:49:37.630368+00	2025-05-17 13:49:37.630745+00	\N	t	ae1a5353-c3ac-447b-86af-89aca1b80fc7	cd1f9d14-685a-4108-a899-c95089073675	Gia Bảo	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8WOsLxlKgTXh7gry1qONjjpnozv1IwdHf165tgttVd5FiaWx4G8yOo4LCWt9uPt6y0EWxE89oyHdEPbgre41s8Q		2003-11-05	
2025-05-17 17:11:18.804395+00	2025-05-17 17:11:18.805118+00	\N	t	d801ba03-323b-438c-8887-47bf33c8cc07	00c0d49f-29d4-4fa3-bc41-e5879c955bb5	SIeu Beo	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8WOsLxlKgTXh7gry1qONjjpnozv1IwdHf165tgttVd5FiaWx4G8yOo4LCWt9uPt6y0EWxE89oyHdEPbgre41s8Q		2003-12-26	
\.


--
-- TOC entry 3363 (class 0 OID 16648)
-- Dependencies: 217
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2025-05-16 03:09:30.665153+00
\.


--
-- TOC entry 3371 (class 0 OID 0)
-- Dependencies: 215
-- Name: app_favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.app_favorites_id_seq', 1, true);


--
-- TOC entry 3372 (class 0 OID 0)
-- Dependencies: 218
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, true);


--
-- TOC entry 3209 (class 2606 OID 16655)
-- Name: app_favorites app_favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_favorites
    ADD CONSTRAINT app_favorites_pkey PRIMARY KEY (id);


--
-- TOC entry 3211 (class 2606 OID 16657)
-- Name: app_favorites app_favorites_profileID_songID_7178901b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_favorites
    ADD CONSTRAINT "app_favorites_profileID_songID_7178901b_uniq" UNIQUE ("profileID", "songID");


--
-- TOC entry 3213 (class 2606 OID 16659)
-- Name: app_profiles app_profiles_accountID_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_profiles
    ADD CONSTRAINT "app_profiles_accountID_key" UNIQUE ("accountID");


--
-- TOC entry 3215 (class 2606 OID 16661)
-- Name: app_profiles app_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_profiles
    ADD CONSTRAINT app_profiles_pkey PRIMARY KEY (id);


--
-- TOC entry 3217 (class 2606 OID 16663)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


-- Completed on 2025-05-17 17:23:58 UTC

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-05-17 17:23:58 UTC

--
-- PostgreSQL database cluster dump complete
--

