--
-- PostgreSQL database dump
--

\restrict 9cDKBdtw6ofwdqK4YMFl5yMM2iMIy66AtnzDFRuAHHgcul7g7qesrihM6LwUnsk

-- Dumped from database version 16.11 (Debian 16.11-1.pgdg13+1)
-- Dumped by pg_dump version 16.11 (Debian 16.11-1.pgdg13+1)

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
-- Name: alternativas_productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alternativas_productos (
    id integer NOT NULL,
    producto_id integer NOT NULL,
    marca text NOT NULL,
    presentacion text NOT NULL,
    laboratorio text,
    costo_unitario real,
    margen_porcentaje real,
    precio_ofertado real,
    observaciones text
);


ALTER TABLE public.alternativas_productos OWNER TO postgres;

--
-- Name: alternativas_productos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alternativas_productos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.alternativas_productos_id_seq OWNER TO postgres;

--
-- Name: alternativas_productos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alternativas_productos_id_seq OWNED BY public.alternativas_productos.id;


--
-- Name: celty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.celty (
    id integer NOT NULL,
    numero_registro text NOT NULL,
    monodroga text,
    marca text,
    presentacion text,
    laboratorio text,
    precio_caja real,
    precio_unitario real,
    costo_unitario real,
    fecha text
);


ALTER TABLE public.celty OWNER TO postgres;

--
-- Name: celty_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.celty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.celty_id_seq OWNER TO postgres;

--
-- Name: celty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.celty_id_seq OWNED BY public.celty.id;


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    id integer NOT NULL,
    nombre text NOT NULL,
    razon_social text,
    cuit text,
    direccion text,
    telefono text,
    email text,
    organismo_jurisdiccion text,
    activo boolean DEFAULT true
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: clientes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clientes_id_seq OWNER TO postgres;

--
-- Name: clientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clientes_id_seq OWNED BY public.clientes.id;


--
-- Name: formas_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formas_pago (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.formas_pago OWNER TO postgres;

--
-- Name: formas_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formas_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.formas_pago_id_seq OWNER TO postgres;

--
-- Name: formas_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formas_pago_id_seq OWNED BY public.formas_pago.id;


--
-- Name: licitaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.licitaciones (
    id integer NOT NULL,
    numero_licitacion text NOT NULL,
    cliente_id integer,
    tipo_licitacion_id integer,
    fecha text NOT NULL,
    oferente_ganador text,
    marca_ganadora text,
    precio_ganador real,
    portal_origen text,
    modalidad_entrega text,
    forma_pago text,
    requiere_poliza boolean DEFAULT false,
    monto_poliza real,
    observaciones text,
    mantenimiento_oferta text,
    numero_presupuesto integer,
    tipo_adjudicacion text DEFAULT 'Parcial'::text,
    CONSTRAINT licitaciones_numero_licitacion_check CHECK ((length(numero_licitacion) > 0))
);


ALTER TABLE public.licitaciones OWNER TO postgres;

--
-- Name: licitaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.licitaciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.licitaciones_id_seq OWNER TO postgres;

--
-- Name: licitaciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.licitaciones_id_seq OWNED BY public.licitaciones.id;


--
-- Name: mantenimientos_oferta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mantenimientos_oferta (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.mantenimientos_oferta OWNER TO postgres;

--
-- Name: mantenimientos_oferta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mantenimientos_oferta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mantenimientos_oferta_id_seq OWNER TO postgres;

--
-- Name: mantenimientos_oferta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mantenimientos_oferta_id_seq OWNED BY public.mantenimientos_oferta.id;


--
-- Name: marcas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marcas (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.marcas OWNER TO postgres;

--
-- Name: marcas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marcas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.marcas_id_seq OWNER TO postgres;

--
-- Name: marcas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marcas_id_seq OWNED BY public.marcas.id;


--
-- Name: modalidades_entrega; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modalidades_entrega (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.modalidades_entrega OWNER TO postgres;

--
-- Name: modalidades_entrega_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.modalidades_entrega_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.modalidades_entrega_id_seq OWNER TO postgres;

--
-- Name: modalidades_entrega_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.modalidades_entrega_id_seq OWNED BY public.modalidades_entrega.id;


--
-- Name: motivos_perdida; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.motivos_perdida (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.motivos_perdida OWNER TO postgres;

--
-- Name: motivos_perdida_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.motivos_perdida_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.motivos_perdida_id_seq OWNER TO postgres;

--
-- Name: motivos_perdida_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.motivos_perdida_id_seq OWNED BY public.motivos_perdida.id;


--
-- Name: oferentes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oferentes (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.oferentes OWNER TO postgres;

--
-- Name: oferentes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.oferentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.oferentes_id_seq OWNER TO postgres;

--
-- Name: oferentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.oferentes_id_seq OWNED BY public.oferentes.id;


--
-- Name: ofertas_productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ofertas_productos (
    id integer NOT NULL,
    producto_id integer NOT NULL,
    oferente text NOT NULL,
    laboratorio text NOT NULL,
    precio real NOT NULL
);


ALTER TABLE public.ofertas_productos OWNER TO postgres;

--
-- Name: ofertas_productos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ofertas_productos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ofertas_productos_id_seq OWNER TO postgres;

--
-- Name: ofertas_productos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ofertas_productos_id_seq OWNED BY public.ofertas_productos.id;


--
-- Name: organismos_jurisdiccion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organismos_jurisdiccion (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.organismos_jurisdiccion OWNER TO postgres;

--
-- Name: organismos_jurisdiccion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organismos_jurisdiccion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organismos_jurisdiccion_id_seq OWNER TO postgres;

--
-- Name: organismos_jurisdiccion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organismos_jurisdiccion_id_seq OWNED BY public.organismos_jurisdiccion.id;


--
-- Name: portales_origen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.portales_origen (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.portales_origen OWNER TO postgres;

--
-- Name: portales_origen_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.portales_origen_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.portales_origen_id_seq OWNER TO postgres;

--
-- Name: portales_origen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.portales_origen_id_seq OWNED BY public.portales_origen.id;


--
-- Name: presupuestos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.presupuestos (
    id integer NOT NULL,
    numero integer NOT NULL,
    licitacion_id integer NOT NULL,
    fecha_generacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.presupuestos OWNER TO postgres;

--
-- Name: presupuestos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.presupuestos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.presupuestos_id_seq OWNER TO postgres;

--
-- Name: presupuestos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.presupuestos_id_seq OWNED BY public.presupuestos.id;


--
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    id integer NOT NULL,
    licitacion_id integer NOT NULL,
    monodroga text NOT NULL,
    marca text NOT NULL,
    presentacion text NOT NULL,
    cantidad integer NOT NULL,
    precio_ofertado real NOT NULL,
    resultado text NOT NULL,
    precio_ganador real,
    oferente_ganador text,
    marca_ofrecida text,
    marca_ganadora text,
    motivo_perdida text,
    numero_renglon text,
    costo_unitario real,
    margen_porcentaje real,
    observaciones text,
    producto_cotizar text DEFAULT 'principal'::text,
    CONSTRAINT productos_cantidad_check CHECK ((cantidad > 0)),
    CONSTRAINT productos_precio_ganador_check CHECK ((precio_ganador >= (0)::double precision)),
    CONSTRAINT productos_precio_ofertado_check CHECK ((precio_ofertado >= (0)::double precision)),
    CONSTRAINT productos_resultado_check CHECK ((resultado = ANY (ARRAY['Adjudicado'::text, 'Parcial'::text, 'No Adjudicado'::text])))
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- Name: productos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.productos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.productos_id_seq OWNER TO postgres;

--
-- Name: productos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.productos_id_seq OWNED BY public.productos.id;


--
-- Name: tipos_licitacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_licitacion (
    id integer NOT NULL,
    nombre text NOT NULL,
    activo boolean DEFAULT true
);


ALTER TABLE public.tipos_licitacion OWNER TO postgres;

--
-- Name: tipos_licitacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipos_licitacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_licitacion_id_seq OWNER TO postgres;

--
-- Name: tipos_licitacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_licitacion_id_seq OWNED BY public.tipos_licitacion.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    username text NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    activo boolean DEFAULT true,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: alternativas_productos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alternativas_productos ALTER COLUMN id SET DEFAULT nextval('public.alternativas_productos_id_seq'::regclass);


--
-- Name: celty id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celty ALTER COLUMN id SET DEFAULT nextval('public.celty_id_seq'::regclass);


--
-- Name: clientes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id SET DEFAULT nextval('public.clientes_id_seq'::regclass);


--
-- Name: formas_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formas_pago ALTER COLUMN id SET DEFAULT nextval('public.formas_pago_id_seq'::regclass);


--
-- Name: licitaciones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licitaciones ALTER COLUMN id SET DEFAULT nextval('public.licitaciones_id_seq'::regclass);


--
-- Name: mantenimientos_oferta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimientos_oferta ALTER COLUMN id SET DEFAULT nextval('public.mantenimientos_oferta_id_seq'::regclass);


--
-- Name: marcas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas ALTER COLUMN id SET DEFAULT nextval('public.marcas_id_seq'::regclass);


--
-- Name: modalidades_entrega id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modalidades_entrega ALTER COLUMN id SET DEFAULT nextval('public.modalidades_entrega_id_seq'::regclass);


--
-- Name: motivos_perdida id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivos_perdida ALTER COLUMN id SET DEFAULT nextval('public.motivos_perdida_id_seq'::regclass);


--
-- Name: oferentes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferentes ALTER COLUMN id SET DEFAULT nextval('public.oferentes_id_seq'::regclass);


--
-- Name: ofertas_productos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_productos ALTER COLUMN id SET DEFAULT nextval('public.ofertas_productos_id_seq'::regclass);


--
-- Name: organismos_jurisdiccion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismos_jurisdiccion ALTER COLUMN id SET DEFAULT nextval('public.organismos_jurisdiccion_id_seq'::regclass);


--
-- Name: portales_origen id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portales_origen ALTER COLUMN id SET DEFAULT nextval('public.portales_origen_id_seq'::regclass);


--
-- Name: presupuestos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presupuestos ALTER COLUMN id SET DEFAULT nextval('public.presupuestos_id_seq'::regclass);


--
-- Name: productos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos ALTER COLUMN id SET DEFAULT nextval('public.productos_id_seq'::regclass);


--
-- Name: tipos_licitacion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_licitacion ALTER COLUMN id SET DEFAULT nextval('public.tipos_licitacion_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: alternativas_productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alternativas_productos (id, producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones) FROM stdin;
15	2	IMIPENEM CELTYC	500 mg IV f.a.x 50	Celtyc	200	10	220	Corto Vencimiento
16	3	FENTANILO CELTYC	0.25 mg a.x 50 x 5ml	Celtyc	500	10	550	Vencimiento corto
\.


--
-- Data for Name: celty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.celty (id, numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, costo_unitario, fecha) FROM stdin;
71	17556	RANITIDINA	XYLOCAINA	spray x 50 g	ASTRAZENECA	727.67	36.3835	\N	11/06/2007
72	40243	ONDANSETRON	DICLOLAM	75 mg comp.x 15	AUSTRAL	8605	2151.25	\N	26/06/2014
73	28566	RANITIDINA	AGUA INYECTABLE BP	a.pl st.x 5 ml	B.BRAUN	2807.3	28.073	\N	12/08/2021
74	28569	RANITIDINA	CLORURO DE SODIO 0.9% BP	a.pl st.x 5 ml	B.BRAUN	2807.3	28.073	\N	14/12/2020
75	28567	SODIO CLORURO	AGUA INYECTABLE BP	a.pl st.x 10 ml	B.BRAUN	3714.2	61.90333	\N	16/12/2025
76	28570	SODIO CLORURO	CLORURO DE SODIO 0.9% BP	a.pl st.x 10 ml	B.BRAUN	3714.2	123.80666	\N	16/12/2025
77	56214	SOLUCION PARENTERAL	MIDAZOLAM B.BRAUN	5 mg/ml a.x 20 x 10 ml	B.BRAUN	105861.52	17643.586	\N	01/04/2003
78	55437	SOLUCION PARENTERAL	SOLUC.FISIOLOGICA 0.9% SIST.CERRADO EP	env.x 100 ml	B.BRAUN	9787.2	9787.2	\N	26/04/2002
79	55443	SOLUCION PARENTERAL	AGUA DESTILADA INYECTABLE SIST.CERRADO EP	env.x 500 ml	B.BRAUN	12807.7	12807.7	\N	26/04/2002
80	55436	SOLUCION PARENTERAL	SOLUC.RINGER CON LACTATO SIST.CERRADO EP	env.x 500 ml	B.BRAUN	14229.5	14229.5	\N	26/04/2002
81	55442	SOLUCION PARENTERAL	SOLUC.DEXTROSA AL 5% SIST.CERRADO EP	env.x 500 ml	B.BRAUN	19023.7	19023.7	\N	18/05/2017
82	58512	SOLUCION PARENTERAL	MIDAZOLAM B.BRAUN	1 mg/ml EP x 10 x 50 ml	B.BRAUN	215304.38	215304.38	\N	21/10/2021
83	29732	SODIO CLORURO	OXA GEL PLUS	gel x 50 g	BETA	18295.95	18295.95	\N	02/06/2014
84	41380	RANITIDINA	METOCLOPRAMIDA BIOL	10 mg a.x 100 x 2 ml	BIOL	279149	9304.967	\N	10/05/2024
85	51456	SODIO CLORURO	METOCLOPRAMIDA BIOL	10 mg/2 ml a.x 3 x 2 ml	BIOL	9928	9928	\N	12/04/2010
86	41378	SOLUCION PARENTERAL	FUROSEMIDA BIOL	20 mg a.x 100 x 2 ml	BIOL	618369.4	6183.694	\N	01/06/2002
87	55638	SOLUCION PARENTERAL	NORADRENALINA BIOL	1 mg/ml a.x 100 x 4 ml	BIOL	876261.9	8762.619	\N	29/12/2009
88	19974	POTASIO CLORURO	FURTENK	40 mg comp.rec.x 50	BIOTENK	20940.46	209.4046	\N	21/04/2008
89	26480	SOLUCION PARENTERAL	MIDATENK	0.2% gts.ped. x 20 ml	BIOTENK	7374.41	7374.41	\N	03/12/2002
90	21234	FENTANILO	BLOKIUM	50 mg comp.x 15	CASASCO	7183.29	71.8329	\N	01/12/2025
91	21235	FUROSEMIDA	BLOKIUM	50 mg comp.x 30	CASASCO	11109.86	222.1972	\N	01/12/2025
92	21236	ONDANSETRON	BLOKIUM	75 mg comp.x 15	CASASCO	16513.06	16513.06	\N	07/02/2002
93	37848	RANITIDINA	TELEDOL	20 mg comp.x 20	CASASCO	17627.11	881.3555	\N	20/01/2003
94	46670	SOLUCION PARENTERAL	HYPERSOL	3% spray nasal x 45 ml	CASSARA	9550	9550	\N	01/11/1992
95	48170	SOLUCION PARENTERAL	HYPERSOL GOTAS	sol.hipert nica x 7.5ml	CASSARA	9720	9720	\N	08/09/2011
17	61306	SODIO CLORURO	KETOROLAC CELTYC 30	30 mg iny.a.x 100 x 1 ml	CELTYC	335600	13983.333	\N	07/03/2017
32	61629	SODIO CLORURO	SOLUC. FISIOLOGICA CELTYC	a.x 100 x 5 ml	CELTYC	352500	29375	\N	11/06/2021
1298	2211	KETOROLAC	RELIVERAN	a.x 3	Novartis	31.78	1.589	\N	17/12/2025
15	60793	SODIO CLORURO	HIOSCINA AMP CELTYC	20 mg a.x 100	CELTYC	400200	400200	\N	02/12/2024
12	60189	SOLUCION PARENTERAL	FUROSEMIDA CELTYC	20 mg a.x 100 x 2 ml	CELTYC	492900	41075	\N	15/04/2002
25	62415	SOLUCION PARENTERAL	MIDAZOLAM CELTYC	15 mg/3 ml iny.a.x 100	CELTYC	565100	11302	\N	10/07/2003
29	60190	SOLUCION PARENTERAL	CLORURO DE POTASIO CELTYC	1.115 g a.x 100 x 5 ml	CELTYC	675300	13506	\N	10/03/1997
4	60195	SOLUCION PARENTERAL	DICLOFENAC CELTYC	75 mg a.x 100 x 3 ml	CELTYC	1.0331e+06	1.0331e+06	\N	01/11/1992
30	60194	SOLUCION PARENTERAL	RANITIDINA CELTYC	50 mg a.x 100 x 5 ml	CELTYC	1.0699e+06	1.0699e+06	\N	04/01/1999
31	61628	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA CELTYC	a.x 100 x 10 ml	CELTYC	1.2541e+06	1.2541e+06	\N	26/04/2002
20	60790	SOLUCION PARENTERAL	SULFATO DE MAGNESIO 25% CELTYC	25% a.x 100 x 5 ml	CELTYC	1.3188e+06	1.3188e+06	\N	03/12/2002
19	60193	SOLUCION PARENTERAL	LIDOCAINA EPINEFRINA CELTYC	2% f.a.x 25 x 20 ml	CELTYC	357600	3576	\N	06/04/2022
10	60196	SOLUCION PARENTERAL	FENTANILO CELTYC	0.25 mg a.x 50 x 5ml	CELTYC	911550	911550	\N	18/01/2003
26	62352	SOLUCION PARENTERAL	NITROGLICERINA CELTYC	25 mg a.x 100	CELTYC	2.1783e+06	2.1783e+06	\N	21/10/2021
27	60792	SOLUCION PARENTERAL	NORADRENALINA AMP CELTYC	4 mg a.x 100	CELTYC	2.23199e+06	2.23199e+06	\N	15/05/2019
13	61437	SOLUCION PARENTERAL	HIDROCORTISONA CELTYC 100	100 mg f.a.x 50	CELTYC	1.4251e+06	1.4251e+06	\N	15/11/2024
7	61819	SOLUCION PARENTERAL	ENOXAPARINA CELTYC	40 mg jga.prell.x 10	CELTYC	365100	365100	\N	15/11/2024
1	60192	SOLUCION PARENTERAL	CEFEPIME CELTYC	1 g f.a.x 50	CELTYC	1.9244e+06	1.9244e+06	\N	20/11/2024
28	60791	SOLUCION PARENTERAL	ONDANSETRON AMP CELTYC	8 mg iny.a.x 100 x 4 ml	CELTYC	4.0122e+06	4.0122e+06	\N	02/09/2024
35	61304	SOLUCION PARENTERAL	VANCOMICINA CELTYC 500	500 mg f.a.x 50	CELTYC	2.11139e+06	2.11139e+06	\N	15/11/2024
14	61438	SOLUCION PARENTERAL	HIDROCORTISONA CELTYC 500	500 mg f.a.x 50	CELTYC	2.1956e+06	2.1956e+06	\N	10/04/2025
3	62351	SOLUCION PARENTERAL	COLISTINA CELTYC	100 mg f.a.x 50	CELTYC	2.61744e+06	2.61744e+06	\N	28/05/2025
8	61927	SOLUCION PARENTERAL	ENOXAPARINA CELTYC	60 mg jga.prell.x 10	CELTYC	540300	540300	\N	02/09/2024
9	61928	SOLUCION PARENTERAL	ENOXAPARINA CELTYC	80 mg jga.prell.x 10	CELTYC	710300	710300	\N	12/11/2025
2	60191	SOLUCION PARENTERAL	CEFEPIME CELTYC	2 g f.a.x 25	CELTYC	2.0251e+06	2.0251e+06	\N	02/09/2024
34	61305	SOLUCION PARENTERAL	VANCOMICINA CELTYC 1000	1000 mg f.a.x 50	CELTYC	4.2342e+06	4.2342e+06	\N	10/04/2025
5	61929	SOLUCION PARENTERAL	ENOXAPARINA CELTYC	100 mg jga.prell.x 10	CELTYC	880350	880350	\N	02/09/2024
16	59342	VANCOMICINA	IMIPENEM CELTYC	500 mg IV f.a.x 50	CELTYC	5.7642e+06	5.7642e+06	\N	18/01/2003
22	61820	VANCOMICINA	MEROPENEM CELTYC	1000 mg f.a.x 50	CELTYC	9.1293e+06	9.1293e+06	\N	02/09/2024
124	22063	CEFEPIME	FUROSEMIDA DF	40 mg comp.x 50	DENVER FARMA	6.6	6.6	\N	22/11/2010
125	22340	HIOSCINA N-BUTILBR	LIDOCAINA DENVER FARMA	2% s/epi.a.x 1 x 5 ml	DENVER FARMA	6.19	0.619	\N	30/12/2025
126	54211	POTASIO CLORURO	FUROSEMIDA DENVER FARMA	40 mg comp.x 50	DENVER FARMA	21627.61	432.5522	\N	01/06/2002
127	30217	POTASIO CLORURO	DICLOFENAC DENVER FARMA	75 mg/3 ml a.x 6	DENVER FARMA	14431.92	14431.92	\N	04/06/2012
128	19510	SOLUCION PARENTERAL	LIDOCAINA DENVER FARMA	2% s/epi.a.x 100 x 5 ml	DENVER FARMA	583010	5830.1	\N	10/03/1997
129	20857	SOLUCION PARENTERAL	FUROSEMIDA DENVER FARMA	20 mg a.x 100 x 2 ml	DENVER FARMA	779216	779216	\N	01/11/1998
130	19505	SOLUCION PARENTERAL	DICLOFENAC DENVER FARMA	75 mg/3 ml a.x 100	DENVER FARMA	1.02701e+06	1.02701e+06	\N	03/12/2002
131	13204	SOLUCION PARENTERAL	LIDOCAINA DENVER FARMA	2% jalea x 25 ml	DENVER FARMA	10599.34	10599.34	\N	28/01/2003
132	19512	SOLUCION PARENTERAL	RANITIDINA DENVER FARMA	50 mg/5 ml a.x 100	DENVER FARMA	1.147712e+06	1.147712e+06	\N	26/04/2002
133	57673	SOLUCION PARENTERAL	FENTANILO DENVER FARMA	0.25 mg iny.a.x100 x 5ml	DENVER FARMA	1.79701e+06	1.79701e+06	\N	06/05/2014
134	56049	SOLUCION PARENTERAL	MIDAZOLAM DENVER FARMA	15 mg/3 ml a.x 100 x 3ml	DENVER FARMA	3.072012e+06	3.072012e+06	\N	08/07/2022
135	56466	SOLUCION PARENTERAL	HEPARINOX	60 mg jga.prell.x 10	DENVER FARMA	685000	685000	\N	02/09/2024
136	30539	SOLUCION PARENTERAL	NITRODOM	pomo x 15 g	DOMINGUEZ	91007.95	91007.95	\N	02/09/2024
137	21048	SODIO CLORURO	AGUA DESTILADA DRAWER	a.x 100 x 5 ml	DRAWER	461677.22	19236.55	\N	02/09/2025
138	41926	SOLUCION PARENTERAL	HIOSCINA DRAWER	20 mg iny.a.x 100 x 1 ml	DRAWER	621934.2	103655.695	\N	01/04/2003
139	41923	SOLUCION PARENTERAL	DICLOFENAC DRAWER	75 mg a.x 100 x 3 ml	DRAWER	982705.3	982705.3	\N	01/04/2003
140	21067	SOLUCION PARENTERAL	CLORURO DE POTASIO DRAWER	15 mEq iny.a.x 100 x 5ml	DRAWER	674655.06	13493.102	\N	10/03/1997
141	29999	SOLUCION PARENTERAL	SOLUC.FISIOLOGICA DRAWER	a.x 100 x 5 ml	DRAWER	720434.5	720434.5	\N	06/04/2004
142	41919	SOLUCION PARENTERAL	AGUA DESTILADA DRAWER	a.x 100 x 10 ml	DRAWER	721692.6	7216.9263	\N	23/04/2002
143	32590	SOLUCION PARENTERAL	FUROSEMIDA DRAWER	20 mg a.x 100 x 2 ml	DRAWER	745871.6	7458.716	\N	01/04/1998
144	32610	SOLUCION PARENTERAL	METOCLOPRAMIDA DRAWER	10 mg a.x 100 x 2 ml	DRAWER	757659.2	757659.2	\N	28/01/2003
145	59199	SOLUCION PARENTERAL	CLORHIDRATO DE LIDOCAINA	2% s/epi.f.a.x 50x 25 ml	DRAWER	511754.88	511754.88	\N	03/12/2002
146	32620	SOLUCION PARENTERAL	RANITIDINA DRAWER	50 mg iny.x 100 x 5 ml	DRAWER	1.1e+06	1.1e+06	\N	03/12/2002
147	30000	SOLUCION PARENTERAL	SULFATO DE MAGNESIO DRAWER	25% a.x 100 x 5 ml	DRAWER	2.167189e+06	2.167189e+06	\N	21/10/2021
148	32601	SOLUCION PARENTERAL	HIDROCORTISONA DRAWER	100 mg iny.f.a.x 100	DRAWER	2.6954205e+06	2.6954205e+06	\N	28/01/2022
149	58004	SOLUCION PARENTERAL	MIDAZOLAM DRAWER	iny.a.x 100 x 3 ml	DRAWER	3.0343855e+06	3.0343855e+06	\N	08/07/2022
150	58000	SOLUCION PARENTERAL	HIDROCORTISONA DRAWER	500 mg iny.f.a.x 100	DRAWER	4.221011e+06	4.221011e+06	\N	19/04/2024
151	41931	SOLUCION PARENTERAL	VANCOMICINA DRAWER	500 mg f.a.x 100	DRAWER	4.9782105e+06	4.9782105e+06	\N	02/12/2024
152	58007	VANCOMICINA	VANCOMICINA DRAWER	1000 mg f.a.x 50	DRAWER	5.8374325e+06	5.8374325e+06	\N	03/04/2002
153	58001	VANCOMICINA	IMIPENEM DRAWER	500 mg f.a.x 50	DRAWER	8.0870345e+06	8.0870345e+06	\N	11/02/2003
154	58002	VANCOMICINA	MEROPENEM DRAWER	500 mg f.a.x 50	DRAWER	1.0696466e+07	1.0696466e+07	\N	02/09/2024
155	58003	VANCOMICINA	MEROPENEM DRAWER	1000 mg f.a.x 50	DRAWER	2.0233754e+07	674458.44	\N	23/10/2025
156	30246	CEFEPIME	BUTILESCOPOLAMINA DUNCAN / RUPE N	10 mg comp.x 1020	DUNCAN	190	190	\N	21/10/2021
157	19474	DICLOFENAC SODICO	FUROSEMIDA DUNCAN /KOLKIN	20 mg a.x 100 x 2 ml	DUNCAN	100	20	\N	15/01/2005
158	11355	MIDAZOLAM	KOLKIN	40 mg comp.x 50	DUNCAN	6141.86	3070.93	\N	25/02/2002
159	41644	MIDAZOLAM	KOLKIN	20 mg a.x 100 x 2 ml	DUNCAN	12600.3	1260.03	\N	25/02/2002
160	19477	MIDAZOLAM	MAGNESIO SULFATO	25% a.x 100 x 5 ml	DUNCAN	14381.95	14381.95	\N	11/03/2008
161	19486	NITROGLICERINA	RUPE N	20 mg a.x 100 x 1 ml	DUNCAN	21964.58	2196.458	\N	21/06/2017
162	51487	RANITIDINA	RUPEMET	10 mg a.x 3 x 2 ml	DUNCAN	3092.26	154.613	\N	04/05/2015
163	61839	DICLOFENAC SODICO	ACLOXIGENAC	50 mg comp.rec.x 500	ECZANE	77509.21	3875.4604	\N	01/01/2001
164	61841	METOCLOPRAMIDA	ACLOXIGENAC	75 mg comp.rec.x 500	ECZANE	111358.94	111358.94	\N	28/01/2003
165	6475	RANITIDINA	HOLOMAGNESIO	comp.rec.x 100	ELEA	127703.97	2554.0793	\N	26/04/2002
166	47541	RANITIDINA	CONTROL K	c ps.x 60	ELEA	99726.74	997.2674	\N	04/12/2020
167	41207	SOLUCION PARENTERAL	OMATEX	40 mg jga.prell.x 10	ELEA	406378.78	406378.78	\N	01/08/2025
168	41209	SOLUCION PARENTERAL	OMATEX	60 mg jga.prell.x 10	ELEA	601580.5	601580.5	\N	01/08/2025
169	41210	SOLUCION PARENTERAL	OMATEX	80 mg jga.prell.x 10	ELEA	781579.7	781579.7	\N	17/06/2025
170	18739	MIDAZOLAM	VANCOCIN	1 g f.a.x 1	ELI LILLY	177.71	1.7771	\N	06/10/2025
171	7977	RANITIDINA	HIDROTISONA	10 mg comp.x 30	EUROFARMA	19721.23	657.3743	\N	01/07/2007
172	27365	DICLOFENAC SODICO	PRIMAVERA-N	comp.x 20	FABRA	11.18	0.559	\N	24/04/2015
173	13780	KETOROLAC	KETOROLAC FABRA	30 mg iny.x 1 x 1 ml	FABRA	7.58	0.758	\N	21/04/2008
174	15834	MAGNESIO	TRINITROGLICERINA FABRA	a.x 1	FABRA	30.98	1.0326667	\N	26/10/2005
175	20203	RANITIDINA	KETOROLAC FABRA	20 mg comp.x 20	FABRA	17408	870.4	\N	26/07/2010
176	51495	SODIO CLORURO	PRIMAVERA-N	10 mg a.x 3	FABRA	9001	9001	\N	16/02/2006
177	59162	SOLUCION PARENTERAL	FIORITINA	4 mg a.x 25 x 4 ml	FABRA	345216.2	345216.2	\N	01/11/1992
178	24104	SOLUCION PARENTERAL	ONDANSETRON FABRA	8 mg a.x 1	FABRA	33951	33951	\N	01/01/2024
179	15836	SOLUCION PARENTERAL	VANCOMICINA FABRA	1000 mg iny.f.a.x 1	FABRA	37344	37344	\N	01/01/2024
180	42994	SOLUCION PARENTERAL	MEROPENEM FABRA	500 mg f.a.x 1	FABRA	82272	82272	\N	12/11/2025
181	38546	SOLUCION PARENTERAL	IMIPENEM FABRA	500 mg IV pvo.p/iny.x 1	FABRA	105372	105372	\N	02/09/2024
182	42995	VANCOMICINA	MEROPENEM FABRA	1000 mg f.a.x 1	FABRA	158502	158502	\N	21/04/2008
183	27276	MIDAZOLAM	HIOSCINA FADA	20 mg a.x 100 x 1 ml	FADA PHARMA	13129.55	13129.55	\N	18/01/2003
184	21617	MIDAZOLAM	ORAKIT 15	a.x 100 x 5 ml	FADA PHARMA	18163.41	363.2682	\N	29/10/2025
185	17898	RANITIDINA	SOLUC.CLORURADA HIPERTONICA FADA	20% a.x 100 x 10 ml	FADA PHARMA	58122.25	968.70416	\N	01/12/2000
186	3460	RANITIDINA	SULFATO DE MAGNESIO	25% a.x 100 x 5 ml	FADA PHARMA	79882.93	1331.3822	\N	15/04/2011
187	48540	RANITIDINA	FADAFLUMAZ	0.5 mg iny.a.x 50 x 5 ml	FADA PHARMA	79018.8	2633.96	\N	21/12/2020
188	55702	RANITIDINA	FADA CEFEPIME	1 g f.a.x 25	FADA PHARMA	60818.84	60818.84	\N	01/03/2014
189	58373	SODIO CLORURO	DISGRADON	10 mg iny.a.x 25 x 2 ml	FADA PHARMA	89146.18	89146.18	\N	14/11/2019
190	31837	SOLUCION PARENTERAL	FADA MIDAZOLAM	15 mg/3 ml iny.a.x 25	FADA PHARMA	316878.8	316878.8	\N	03/12/2002
191	22959	SOLUCION PARENTERAL	FRIDALIT 100	100 mg f.a.x 100 x 5 ml	FADA PHARMA	1.5347451e+06	1.5347451e+06	\N	26/04/2002
192	22583	SOLUCION PARENTERAL	FADAFLUMAZ	0.5 mg iny.a.x 25 x 5 ml	FADA PHARMA	487061.72	487061.72	\N	18/05/2017
193	24556	SOLUCION PARENTERAL	ENETEGE	a.x 100 x 5 ml	FADA PHARMA	2.0003614e+06	2.0003614e+06	\N	18/05/2017
194	45832	SOLUCION PARENTERAL	NOLISIM	100 mg/2ml IM/IV f.a.x1	FADA PHARMA	47345.76	47345.76	\N	28/05/2025
195	21630	SOLUCION PARENTERAL	VAREDET	1000 mg iny.f.a.x25x20ml	FADA PHARMA	1.5917876e+06	1.5917876e+06	\N	02/09/2024
196	51999	SOLUCION PARENTERAL	FADA IMIPENEM	500 mg IV f.a.x 25	FADA PHARMA	2.6564665e+06	2.6564665e+06	\N	02/09/2024
197	57559	VANCOMICINA	FADA MEROPENEM	1 g f.a.x 25	FADA PHARMA	4.417675e+06	4.417675e+06	\N	16/08/2016
198	15869	SOLUCION PARENTERAL	MEDROCIL	1% pomo x 30 g	FORTBENTON	11274.88	11274.88	\N	18/05/2006
199	2216	POTASIO CLORURO	RELIVERAN	comp.x 20	GADOR	7987.96	7987.96	\N	09/02/2002
200	22950	SOLUCION PARENTERAL	FLUMAGE	0.5 mg a.x 50 x 5 ml	GEMEPE	980170.25	980170.25	\N	18/05/2017
201	37183	RANITIDINA	RODINAC 75	comp.x 15	GÉMINIS FARMACÉUTICA	13954.74	697.737	\N	02/12/2016
202	61554	SOLUCION PARENTERAL	AGUA ESTERIL PARA INYECTABLES	a.pl st.x 10 ml	GENÉRICO	9890.25	9890.25	\N	21/04/2009
203	59070	SOLUCION PARENTERAL	SOLUC.FISIOL. DE CLORURO DE SODIO	sachet x 100 ml	GENÉRICO	13770	13770	\N	26/04/2002
204	58916	SOLUCION PARENTERAL	SOLUC.PARENT. MAXFUSOR PLUS	520AP isot.cl.sod.x500ml	GENÉRICO	15169.38	15169.38	\N	26/04/2002
205	59072	SOLUCION PARENTERAL	SOLUC.FISIOL. DE CLORURO DE SODIO	sachet x 500 ml	GENÉRICO	17625.6	17625.6	\N	15/04/2012
206	59073	SOLUCION PARENTERAL	SOLUC.FISIOL. DE CLORURO DE SODIO	sachet x 1000 ml	GENÉRICO	24786	24786	\N	16/10/2019
207	59076	SOLUCION PARENTERAL	SOLUC. MOLAR CLORURO DE POTASIO	sachet x 100 ml	GENÉRICO	26438.4	26438.4	\N	15/05/2019
208	61574	SOLUCION PARENTERAL	SOLUC. MOLAR CLORURO DE POTASIO	env. flex. x 100 ml	GENÉRICO	33059.12	330.5912	\N	04/08/2025
209	55529	SODIO CLORURO	GOBBICAINA	2% s/epi.a.x 50 x 5 ml	GOBBI	211743.84	2117.4385	\N	22/10/2025
210	54133	SOLUCION PARENTERAL	RANITIDINA GOBBI	50 mg a.x 50 x 5 ml	GOBBI	253552.94	42258.82	\N	31/05/2002
211	55643	SOLUCION PARENTERAL	DICLONOVAG	75 mg a.x 50 x 3 ml	GOBBI	643639.56	643639.56	\N	03/12/2002
212	25582	SOLUCION PARENTERAL	GOBBIZOLAM	15 mg iny.a.x 50 x 3 ml	GOBBI	554235.06	554235.06	\N	02/12/2003
213	55076	SOLUCION PARENTERAL	GOBBICAINA	2% s/epi.f.a.x 25 x 20ml	GOBBI	336759.84	336759.84	\N	26/04/2002
214	56631	SOLUCION PARENTERAL	GOBBICAINA	2% c/epi.a.x 25 x 20ml	GOBBI	404111.8	404111.8	\N	13/03/2009
215	52801	SOLUCION PARENTERAL	FENTANOVAG	iny.a.x 50 x 5 ml	GOBBI	846578	846578	\N	18/05/2017
216	55073	SOLUCION PARENTERAL	ONDANSETRON GOBBI	8 mg iny.a. x 50 x 4 ml	GOBBI	1.1146399e+06	1.1146399e+06	\N	29/07/2008
217	53944	SOLUCION PARENTERAL	FLUMANOVAG	0.5 mg/5 ml a.x 50	GOBBI	1.1598905e+06	1.1598905e+06	\N	15/05/2019
218	14302	SOLUCION PARENTERAL	LIGNOCAINA GRAY	2% f.a.x 20 ml	GRAY	16831.34	16831.34	\N	18/05/2017
219	31665	SOLUCION PARENTERAL	LIGNOCAINA SPRAY	10% spray x 50 g	GRAY	20011.68	20011.68	\N	18/05/2017
220	60583	SOLUCION PARENTERAL	NITROGRAY	25 mg a.x 100 x 5 ml	GRAY	2.0019806e+06	2.0019806e+06	\N	20/05/2008
221	60394	RANITIDINA	METOCLOPRAMIDA UNC	a. x 100 x 2 ml	HEMODERIVADOS	144550	48183.332	\N	31/07/2004
222	56135	FENTANILO	FLEXANA	50 mg comp.x 15	HLB PHARMA	5196.89	207.8756	\N	27/06/2025
223	58718	FUROSEMIDA	FLEXANA	50 mg comp.x 30	HLB PHARMA	7926.11	158.5222	\N	18/06/2024
224	59081	ONDANSETRON	AGUA DESTILADA HLB	a.x 100 x 5 ml	HLB PHARMA	25700	257	\N	19/10/2000
225	59080	ONDANSETRON	AGUA DESTILADA HLB	a.x 100 x 10 ml	HLB PHARMA	26600	2660	\N	26/06/2014
226	56136	ONDANSETRON	FLEXANA	75 mg comp.x 15	HLB PHARMA	12817.59	2563.518	\N	05/01/2009
227	59087	POTASIO CLORURO	DICLOFENAC HLB	a. x 100 x 3 ml	HLB PHARMA	297432	297432	\N	02/07/2024
228	59288	RANITIDINA	DAFUROSE	20 mg a.x 100 x 2 ml	HLB PHARMA	297432	5948.64	\N	29/10/2025
229	59099	RANITIDINA	SOLUC. DE CLORURO DE POTASIO 22%	a. x 100 x 5 ml	HLB PHARMA	297432	2974.32	\N	04/08/2025
230	59098	RANITIDINA	RANITIDINA HLB	a. x 100 x 5 ml	HLB PHARMA	297432	2974.32	\N	01/01/2025
231	59096	SODIO CLORURO	SOLUC. DE LIDOCAINA	2% a.x 100 x 5 ml	HLB PHARMA	306244.8	306244.8	\N	01/10/2003
232	59097	SODIO CLORURO	TRIMPOL	10 mg a. x 100 x 2 ml	HLB PHARMA	308448	308448	\N	01/09/2007
233	58834	SODIO CLORURO	NORADRENALINA	1 mg/ml a.x 100 x 4 ml	HLB PHARMA	423014.4	4230.144	\N	22/10/2025
234	59085	SODIO CLORURO	SOLUC.CLORURO DE SODIO HIPERT. HLB	a. x 100 x 10 ml	HLB PHARMA	438436.8	438436.8	\N	15/12/2025
235	59101	SODIO CLORURO	SUERO FISIOLOGICO	a. x 100 x 10 ml	HLB PHARMA	440640	440640	\N	15/11/2024
236	58669	SOLUCION PARENTERAL	FENTANILO HLB	0.25 mg a.x 100 x 5 ml	HLB PHARMA	867000	867000	\N	26/04/2002
237	58671	SOLUCION PARENTERAL	MIDAZOLAM HLB PHARMA	15 mg iny.a.x 100 x 3 ml	HLB PHARMA	561816	561816	\N	30/09/2005
238	59071	SOLUCION PARENTERAL	SOLUC.FISIOL. DE CLORURO DE SODIO	sachet x 250 ml	HLB PHARMA	15973.2	15973.2	\N	03/10/2002
239	38082	SOLUCION PARENTERAL	DUROGESIC D-TRANS	25 mcg/h parch.matriz.x5	JANSSEN-CILAG	161708.1	3234.1619	\N	06/10/2025
240	38083	SOLUCION PARENTERAL	DUROGESIC D-TRANS	50 mcg/h parch.matriz.x5	JANSSEN-CILAG	291061.78	291061.78	\N	28/05/2025
241	53175	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA JAYOR BOLSA SIMPLE	sachet x 500 ml	JAYOR	23620.51	23620.51	\N	16/10/2019
242	53173	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA JAYOR BOLSA SIMPLE	sachet x 100 ml	JAYOR	35692.9	35692.9	\N	19/04/2024
243	53174	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA JAYOR BOLSA SIMPLE	sachet x 250 ml	JAYOR	36666.18	36666.18	\N	19/04/2024
244	53178	SOLUCION PARENTERAL	SOLUC. DEXTROSA 5% JAYOR BOLSA SIMPLE	sachet x 250 ml	JAYOR	39269.74	39269.74	\N	01/01/2024
245	53177	SOLUCION PARENTERAL	SOLUC. DEXTROSA 5% JAYOR BOLSA SIMPLE	sachet x 100 ml	JAYOR	43999.52	43999.52	\N	02/09/2024
246	53179	SOLUCION PARENTERAL	SOLUC. DEXTROSA 5% JAYOR BOLSA SIMPLE	sachet x 500 ml	JAYOR	45537.12	45537.12	\N	02/09/2024
247	55618	SOLUCION PARENTERAL	AGUA DESTILADA BOLSA SIMPLE	sachet x 500 ml	JAYOR	49379.52	49379.52	\N	01/08/2025
248	53176	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA JAYOR BOLSA SIMPLE	sachet x 1000 ml	JAYOR	53941.96	53941.96	\N	02/09/2024
249	56208	SOLUCION PARENTERAL	SOLUC. DEXTROSA 10% JAYOR BOLSA SIMPLE	sachet x 500 ml	JAYOR	54033.04	54033.04	\N	02/09/2024
250	53180	SOLUCION PARENTERAL	SOLUC. DEXTROSA 5% JAYOR BOLSA SIMPLE	sachet x 1000 ml	JAYOR	58180.4	58180.4	\N	12/11/2025
251	55619	SOLUCION PARENTERAL	SOLUC. RINGER LACTATO BOLSA SIMPLE	sachet x 500 ml	JAYOR	70379.3	70379.3	\N	12/11/2025
252	41284	SOLUCION PARENTERAL	FENTANILO KILAB	0.25mg a.x 50 x 5ml (EH)	KILAB	587375	587375	\N	03/12/2002
253	60178	VANCOMICINA	IMIPENEM CILASTATINA KILAB	500 mg f.a.x 50	KILAB	5.7175e+06	5.7175e+06	\N	18/01/2003
254	59718	VANCOMICINA	MEROPENEM KILAB	500 mg f.a.x 50	KILAB	9.125e+06	365000	\N	17/06/2020
255	60802	VANCOMICINA	MEROPENEM KILAB	1000 mg f.a.x 50	KILAB	1.0925e+07	910416.7	\N	29/08/2024
256	7780	DICLOFENAC SODICO	NOVOMIT	10 mg comp.x 10	KLONAL	6.37	0.42466667	\N	24/12/1999
257	13451	DICLOFENAC SODICO	LUAR G	10 mg comp.x 20	KLONAL	24.66	2.466	\N	27/03/2021
258	28052	LIDOCAINA	LIDOCAINA	2% f.a.x 20 ml	KLONAL	14.61	14.61	\N	04/07/2011
259	2554	LIDOCAINA	FUROSEMIDA KLONAL	40 mg comp.x 50	KLONAL	984.05	984.05	\N	26/04/2019
260	53603	NORADRENALINA	GASTROZAC	a.x 100 x 5 ml	KLONAL	23506.56	235.0656	\N	16/06/2005
261	56334	ONDANSETRON	KLONAFENAC	75 mg comp.x 15	KLONAL	7268.55	7268.55	\N	07/02/2002
262	54655	POTASIO CLORURO	KLONAFENAC	75 mg iny.a.x 100 x 3 ml	KLONAL	288890	2888.9	\N	01/08/2021
263	21812	POTASIO CLORURO	HIDROCORTISONA	10 mg comp.x 30	KLONAL	14435.86	144.3586	\N	06/08/2024
264	53622	RANITIDINA	NOVOMIT	10 mg a.x 100 x 2 ml	KLONAL	210230.77	7007.692	\N	02/12/2019
265	53623	SODIO CLORURO	SOLUC.FISIOLOGICA KLONAL	a.x 100 x 5 ml	KLONAL	424440.75	424440.75	\N	05/12/2025
266	53602	SODIO CLORURO	FUROSEMIDA KLONAL	20 mg a.x 100 x 2 ml	KLONAL	437221.16	4372.212	\N	13/08/2025
267	53584	SODIO CLORURO	AGUA DESTILADA	a.x 100 x 5 ml	KLONAL	438703.7	438703.7	\N	02/07/2024
268	53615	SOLUCION PARENTERAL	LIDOCAINA KLONAL	2% f.a.x 100 x 5 ml	KLONAL	530251.8	88375.3	\N	01/04/2003
269	57419	SOLUCION PARENTERAL	KLENAC	iny.a.x 100 x 1 ml	KLONAL	542393.56	5423.9355	\N	13/06/2000
270	53618	SOLUCION PARENTERAL	LUAR G	20 mg a.x 100 x 1 ml	KLONAL	640932.75	6409.3276	\N	03/01/2008
271	5749	SOLUCION PARENTERAL	NOVOMIT	0.2% n .gts.x 20 ml	KLONAL	6883.95	6883.95	\N	22/01/2007
272	5748	SOLUCION PARENTERAL	NOVOMIT	0.5% ad.gts.x 20 ml	KLONAL	7845.86	7845.86	\N	01/10/1992
273	26845	SOLUCION PARENTERAL	HIDROCORTISONA	1% cr.x 15 g	KLONAL	9246.19	9246.19	\N	03/12/2002
274	59764	SOLUCION PARENTERAL	KLONAZOLAM	15 mg/3 ml iny.a.x 100	KLONAL	1.1313459e+06	1.1313459e+06	\N	03/12/2002
275	57413	SOLUCION PARENTERAL	HIDROCORTISONA KLONAL	100 mg f.a.x 100	KLONAL	1.5840788e+06	1.5840788e+06	\N	15/10/2002
276	60269	SOLUCION PARENTERAL	LIDOCAINA KLONAL	2% f.a.x 20 x 20 ml	KLONAL	435037.3	4350.373	\N	01/02/2022
277	53599	SOLUCION PARENTERAL	HIDROCORTISONA	500 mg f.a.x 100	KLONAL	2.7207528e+06	2.7207528e+06	\N	28/06/2021
278	53582	SOLUCION PARENTERAL	CEFIMEN-K	1 g iny.f.a.x 45	KLONAL	1.4445952e+06	14445.952	\N	11/08/2025
279	57416	SOLUCION PARENTERAL	VANCOMAX	500 mg f.a.x 100	KLONAL	4.900813e+06	4.900813e+06	\N	14/05/2024
280	57417	SOLUCION PARENTERAL	KLONISTINA	f.a.x 100 x 100 mg	KLONAL	5.520737e+06	5.520737e+06	\N	02/09/2024
281	53626	SOLUCION PARENTERAL	VANCOMAX	1000 mg f.a.x 30	KLONAL	1.9043906e+06	1.9043906e+06	\N	17/06/2025
282	53608	SOLUCION PARENTERAL	KLOPENEM	500 mg f.a.x 25	KLONAL	2.4754548e+06	2.4754548e+06	\N	02/09/2024
283	53606	VANCOMICINA	KLONAM	500 mg f.a.x 42	KLONAL	5.004667e+06	5.004667e+06	\N	11/11/2015
284	53610	VANCOMICINA	KLOPENEM	1 g f.a.x 42	KLONAL	8.387591e+06	8.387591e+06	\N	20/12/2025
285	61557	POTASIO CLORURO	SOLUC. CLORURO DE SODIO 0.9%	a.pl st.x 10 ml	LABORATORIOS TECSOLPAR	10118.64	10118.64	\N	13/05/2024
286	46951	MEROPENEM	MIDALAN	15 mg iny.x 2 x 3 ml	LAFEDAR	94.34	94.34	\N	11/11/2015
287	52659	SOLUCION PARENTERAL	LAFECAINA	jalea pomo x 25 ml	LAFEDAR	8695.41	434.7705	\N	19/07/2002
288	51331	SOLUCION PARENTERAL	DASENTRON	8 mg comp.x 10	LAFEDAR	87829.52	87829.52	\N	03/12/2002
289	4822	SOLUCION PARENTERAL	PRIMPERIL	gts.x 20 ml	LAFEDAR	9709.34	97.0934	\N	06/04/2022
290	22157	SOLUCION PARENTERAL	LAFECAINA 2%	viscosa fco.x 50 ml	LAFEDAR	10766.83	10766.83	\N	11/01/2011
291	35568	SOLUCION PARENTERAL	FULLCAINA	spray x 50 ml	LAFEDAR	24026.36	24026.36	\N	15/05/2019
292	51330	SOLUCION PARENTERAL	DASENTRON	8 mg a.x 1	LAFEDAR	39879.68	39879.68	\N	14/05/2024
293	54136	SOLUCION PARENTERAL	COLISTYN	100 mg f.a.iny.x 1	LAFEDAR	41203.78	41203.78	\N	02/09/2024
294	32596	SOLUCION PARENTERAL	DILUTOL	40mg jga.prell.x10x0.4ml	LAZAR	380373.66	380373.66	\N	19/04/2024
295	32598	SOLUCION PARENTERAL	DILUTOL	60mg jga.prell.x10x0.6ml	LAZAR	555880.3	555880.3	\N	12/11/2025
296	32599	SOLUCION PARENTERAL	DILUTOL	80mg jga.prell.x10x0.8ml	LAZAR	751248.5	751248.5	\N	12/11/2025
297	18256	SOLUCION PARENTERAL	ONDANSETRON LKM 8	8 mg comp.x 10	LKM ONCO/ESPECI	274238	274238	\N	15/05/2019
298	29766	SOLUCION PARENTERAL	LACTID HC	1% cr.x 15 g	MEDISOL	6700	67	\N	01/06/2002
299	44857	SOLUCION PARENTERAL	GASTROCALM	gts.x 20 ml	MEDISOL	6700	2233.3333	\N	01/12/1996
300	21113	FUROSEMIDA	DIASTONE	50 mg comp.x 30	MICROSULES ARG.	9504	190.08	\N	29/12/2025
301	1897	RANITIDINA	KEMANAT	10 mg comp.x 20	MICROSULES ARG.	11783.93	235.6786	\N	20/02/2002
302	9616	RANITIDINA	KEMANAT	10 mg comp.x 10	MICROSULES ARG.	7547.38	377.369	\N	02/11/2007
303	1899	RANITIDINA	KEMANAT	20 mg comp.x 20	MICROSULES ARG.	18070.85	602.3617	\N	28/12/2007
304	9617	RANITIDINA	KEMANAT	20 mg comp.x 10	MICROSULES ARG.	11427.2	1632.4572	\N	26/04/2002
305	25631	SOLUCION PARENTERAL	FINABER	8 mg iny.a.x 5 x 4 ml	MICROSULES ARG.	126582.7	126582.7	\N	28/01/2022
306	15206	SOLUCION PARENTERAL	FINABER	8 mg iny.a.x 1 x 4 ml	MICROSULES ARG.	32824.71	32824.71	\N	02/12/2024
307	25821	KETOROLAC	CLORURO DE POTASIO MOLAR	PVC/Norflex x 50 x 100ml	NORGREEN	379.47	18.9735	\N	08/08/2008
308	40305	RANITIDINA	FUROSEMIDA NORGREEN	20 mg a.x 1 x 2 ml	NORGREEN	2151.06	107.553	\N	03/02/2021
309	40288	RANITIDINA	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	0.9% a.x 1 x 5 ml	NORGREEN	2880.13	28.8013	\N	02/07/2024
310	40346	SODIO CLORURO	MIDAZOLAM NORGREEN	15 mg a.x 1 x 3 ml	NORGREEN	3723.9	37.239	\N	13/08/2025
311	40286	SODIO CLORURO	AGUA DESTILADA INYECTABLE NORGREEN	a.x 100 x 10 ml	NORGREEN	386890.7	6448.178	\N	23/12/2025
312	40289	SODIO CLORURO	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	0.9% a.x 1 x 10 ml	NORGREEN	4242.04	169.6816	\N	16/10/2025
313	40343	SOLUCION PARENTERAL	LIDOCAINA NORGREEN	2% a.x 1 x 5 ml	NORGREEN	5834.82	58.3482	\N	10/03/1997
314	40300	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	25% a.x 1 x 10 ml	NORGREEN	8925.59	8925.59	\N	03/12/2002
315	40311	SOLUCION PARENTERAL	SULFATO DE MAGNESIO 25% NORGREEN	25% a.x 1 x 5 ml	NORGREEN	12095.96	12095.96	\N	03/12/2002
316	40341	SOLUCION PARENTERAL	LIDOCAINA NORGREEN	2% f.a.x 1 x 20 ml	NORGREEN	23993.46	23993.46	\N	21/10/2021
317	40356	SOLUCION PARENTERAL	LIDOCAINA NORGREEN	1% f.a.x 1 x 20 ml	NORGREEN	24477.27	244.7727	\N	22/10/2021
318	40313	SOLUCION PARENTERAL	MEROPENEM NORGREEN	500 mg f.a.x 1 x 20 ml	NORGREEN	99491.62	99491.62	\N	02/09/2024
319	36535	MEROPENEM	AGUA DESTILADA NORTHIA	a.x 100 x 5 ml	NORTHIA	5653.88	113.0776	\N	13/08/2025
320	36557	MIDAZOLAM	CIFESPASMO	20 mg a.x 100 x 1 ml	NORTHIA	13996.75	6998.375	\N	28/11/2013
321	36516	MIDAZOLAM	CLORURO DE POTASIO NORTHIA	15 mEq x 100 x 5 ml	NORTHIA	18163.34	9081.67	\N	08/12/2025
322	36529	RANITIDINA	DRIM-NORTH	15 mg/3 ml iny.a.x 100	NORTHIA	84900.13	2830.0044	\N	01/07/2004
323	45997	RANITIDINA	NOREPINEFRINA NORTHIA	4 mg a.x 100 x 4 ml	NORTHIA	110161.62	3672.054	\N	30/03/2012
324	51815	RANITIDINA	ONDANSETRON NORTHIA	8 mg iny.a.x 100	NORTHIA	162318.02	2705.3	\N	20/11/2020
325	58606	SODIO CLORURO	DIPGIX	30 mg iny.a.x 25 x 2 ml	NORTHIA	104827.72	1048.2772	\N	22/10/2025
326	58823	SODIO CLORURO	CLORURO DE POTASIO NORTHIA	15 mEq x 25 x 5 ml	NORTHIA	116107.85	116107.85	\N	02/07/2024
327	59444	SODIO CLORURO	CIFESPASMO	20 mg a.x 25 x 1 ml	NORTHIA	117575.53	117575.53	\N	19/12/2025
328	36563	SOLUCION PARENTERAL	FENDIBINA	50 mg a.x 100 x 5 ml	NORTHIA	485095.06	4850.9507	\N	13/06/2000
329	58824	SOLUCION PARENTERAL	DICLOCALM	75 mg a.x 25 x 3 ml	NORTHIA	145047.34	1450.4734	\N	03/01/2008
330	59439	SOLUCION PARENTERAL	FENTANILO NORTHIA	0.25 mg iny.a.x 25 x 5ml	NORTHIA	312731.62	312731.62	\N	03/12/2002
331	58685	SOLUCION PARENTERAL	DRIM-NORTH	15 mg/3 ml iny.a.x 25	NORTHIA	316878.8	316878.8	\N	26/04/2002
332	36549	SOLUCION PARENTERAL	HIDROCORTISONA NORTHIA	100 mg f.a.x 50	NORTHIA	767372.56	767372.56	\N	01/10/1992
333	45498	SOLUCION PARENTERAL	ENOXANORTH	20 mg jga.prell.x 10	NORTHIA	189093.98	189093.98	\N	18/05/2017
334	45989	SOLUCION PARENTERAL	DAUXONA	a.x 100 x 5 ml	NORTHIA	2.0003614e+06	2.0003614e+06	\N	06/07/2015
335	36550	SOLUCION PARENTERAL	HIDROCORTISONA NORTHIA	500 mg f.a.x 50	NORTHIA	1.4016065e+06	1.4016065e+06	\N	15/01/2024
336	59445	SOLUCION PARENTERAL	ONDANSETRON NORTHIA	8 mg iny.a.x 25	NORTHIA	722953.94	7229.539	\N	11/08/2025
337	52055	SOLUCION PARENTERAL	ENOXANORTH	40 mg jga.prell.x 50	NORTHIA	1.7969422e+06	35938.844	\N	02/09/2024
338	36513	SOLUCION PARENTERAL	VANCOMICINA NORTHIA	500 mg iny.f.a.x 50	NORTHIA	1.8828431e+06	1.8828431e+06	\N	01/01/2024
339	55700	SOLUCION PARENTERAL	CEFEPIME	1 g f.a.x 25	NORTHIA	954196.2	954196.2	\N	19/04/2024
340	52056	SOLUCION PARENTERAL	ENOXANORTH	60 mg jga.prell.x 50	NORTHIA	2.6754055e+06	2.6754055e+06	\N	02/09/2024
341	55701	SOLUCION PARENTERAL	CEFEPIME	2 g f.a.x 25	NORTHIA	1.5605084e+06	1.5605084e+06	\N	02/09/2024
342	36514	SOLUCION PARENTERAL	VANCOMICINA NORTHIA	1000 mg iny.f.a.x 50	NORTHIA	3.1835748e+06	3.1835748e+06	\N	02/09/2024
343	45501	SOLUCION PARENTERAL	ENOXANORTH	80 mg jga.prell.x 10	NORTHIA	715848.3	715848.3	\N	27/02/2025
344	57560	SOLUCION PARENTERAL	MEROEFECTIL	500 mg iny.f.a.x 25	NORTHIA	2.275537e+06	2.275537e+06	\N	02/09/2024
345	57557	SOLUCION PARENTERAL	IMIPECIL	500 mg IV f.a.x 25	NORTHIA	2.6564665e+06	2.6564665e+06	\N	02/09/2024
346	57558	VANCOMICINA	MEROEFECTIL NORTHIA	1000 mg IV iny.f.a.x 25	NORTHIA	4.417675e+06	88353.5	\N	20/12/2017
347	1649	POTASIO CLORURO	BUSCAPINA	grag.x 20	OPELLA HEALTHCA	10455.19	104.5519	\N	13/08/2025
348	50305	RANITIDINA	BUSCAPINA PERLAS	c ps.blandas x 20	OPELLA HEALTHCA	11405.36	11.40536	\N	22/01/2014
349	56121	SODIO CLORURO	LIDOXA	jalea x 20 x 25 ml	OXAPHARMA	87900	87900	\N	04/11/2025
350	43807	SOLUCION PARENTERAL	PROAVENAL H	cr.x 50 g	PANALAB	34131.88	34131.88	\N	02/12/2024
351	9605	RANITIDINA	DOLTEN	10 mg comp.x 10	PFIZER	11227.26	467.8025	\N	27/02/2008
352	9938	RANITIDINA	DOLTEN	20 mg comp.x 20	PFIZER	27597.61	5519.522	\N	03/04/2002
353	9606	RANITIDINA	DOLTEN	30 mg iny.a.x 5 x 2 ml	PFIZER	7979.7	265.99	\N	28/08/2020
354	21652	RANITIDINA	DOLTEN SL	10 mg comp.subl.x 10	PFIZER	16063.64	535.45465	\N	13/03/2021
355	16488	SODIO CLORURO	MEROZEN	500 mg IV vial x 1	PFIZER	4260.42	4260.42	\N	15/12/2025
356	39250	RANITIDINA	ALFACOLIN	pvo.iny. f.a.x 1 x100 mg	PINT PHARMA	1558.18	1558.18	\N	04/05/2015
357	46814	SODIO CLORURO	NACLIN	a.x 30 x 5 ml	QUÍMICA LUAR	116744.02	116744.02	\N	03/04/2024
358	22435	LIDOCAINA	MIDAZOLAM RICHET	15 mg/3 ml a.x 1	RICHET	13.37	0.1337	\N	15/08/2002
359	35289	SOLUCION PARENTERAL	ONDANSETRON RICHET	8 mg comp.x 10	RICHET	74313.55	743.1355	\N	23/04/2002
360	21806	SOLUCION PARENTERAL	FLUMAZENIL RICHET	0.5 mg iny.a.x 5	RICHET	153132.38	153132.38	\N	08/07/2022
361	7742	SOLUCION PARENTERAL	HIDROCORTISONA RICHET	500 mg liof.f.a.x 1	RICHET	51566.02	51566.02	\N	17/06/2025
362	39374	SOLUCION PARENTERAL	COLISTINA RICHET	iny.f.a.x 2 ml + solv.	RICHET	54389.77	54389.77	\N	12/11/2025
363	30471	SOLUCION PARENTERAL	CEFEPIME RICHET	1 g f.a.x 1	RICHET	77895.99	77895.99	\N	12/11/2025
364	30472	VANCOMICINA	CEFEPIME RICHET	2 g f.a.x 1	RICHET	127548.7	127548.7	\N	05/09/2005
365	38109	VANCOMICINA	IMIPENEM CILASTATIN RICHET	500 mg IV f.a.x 1	RICHET	129882.43	129882.43	\N	05/03/2014
366	36342	LIDOCAINA	DALAM 15	15 mg comp.rec.x 30	RICHMOND	788.16	788.16	\N	19/01/2024
367	56866	RANITIDINA	SOLUCION FISIOLOGICA ISOTONICA RIGECIN	48 sach. x 100ml	RIGECIN	33607.42	240.053	\N	12/04/2007
368	56868	RANITIDINA	SOLUCION FISIOLOGICA ISOTONICA RIGECIN	15 sach. x 500ml	RIGECIN	15219.16	507.30533	\N	18/11/2002
369	56865	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	a.x 100 x 10ml	RIGECIN	661866	661866	\N	06/09/2006
370	56867	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	24 sachet x 250ml	RIGECIN	528920.4	528920.4	\N	15/05/2019
371	56869	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	8 sachet x 1000ml	RIGECIN	248521.6	2485.216	\N	04/08/2025
372	56870	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	4 sachet x 2000ml	RIGECIN	167437.12	167437.12	\N	01/08/2025
373	17108	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	620AD isot.cl.sod.x500ml	RIVERO	13850.04	13850.04	\N	03/12/2002
374	14465	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	611AD dext.5% aguax500ml	RIVERO	15958.52	15958.52	\N	03/12/2002
375	14467	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	620HD isot.cl.sod.x100ml	RIVERO	17653.02	17653.02	\N	15/09/2012
376	14468	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	620QD isot.cl.sod.x250ml	RIVERO	18171.88	18171.88	\N	18/05/2017
377	38285	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	542H bicar.sod.molx100ml	RIVERO	18847.04	18847.04	\N	18/05/2017
378	59768	SOLUCION PARENTERAL	SOLUC.PARENT. MAXFUSOR PLUS	511AP dext.5%agua x500ml	RIVERO	20720.38	20720.38	\N	23/02/2021
379	7454	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	1054 isot.cl.sod.x2000ml	RIVERO	21037.7	21037.7	\N	21/10/2021
380	15452	SOLUCION PARENTERAL	NIGLINAR	25 mg iny.a. x 1 x 5 ml	RIVERO	22100.56	22100.56	\N	29/07/2008
381	7390	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	656A agua p/iny.x 500 ml	RIVERO	25765.47	25765.47	\N	28/01/2022
382	1656	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G63 fosf.sod.x 10ml	RIVERO	26977.84	26977.84	\N	15/05/2019
383	7404	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G65 fosf.pot.x 10 ml	RIVERO	26977.84	26977.84	\N	28/01/2022
384	12567	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	624ADB Ring.lact.x 500ml	RIVERO	32516.55	325.1655	\N	22/10/2025
385	7458	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	1062 glicina1.5% x2000ml	RIVERO	38886.24	38886.24	\N	01/01/2024
386	22418	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G57 sulf.cinc x 10 ml	RIVERO	39559.3	39559.3	\N	01/01/2024
387	11810	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	645A manitol 15% x 500ml	RIVERO	39906.89	39906.89	\N	02/12/2024
388	7456	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	1058 p/dia.c/dx.2%2000ml	RIVERO	40480.83	40480.83	\N	01/01/2024
389	11809	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	616A dext.50% aguax500ml	RIVERO	58140.69	58140.69	\N	02/09/2024
390	26815	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-62sol.normot rm.x100ml	RIVERO	356525.88	3565.2588	\N	04/08/2025
391	47045	RANITIDINA	DORIXINA FORTE NF	30 mg a.x 3	ROEMMERS	4841	161.36667	\N	12/02/2021
392	6848	MEROPENEM	SOLUC.PARENT.100 ML	bicarb.sod.sol.molar	ROUX OCEFA	54.92	54.92	\N	17/12/2025
393	56561	FUROSEMIDA	DOLOFENAC 50	50 mg comp.x 30	SANITAS	497.18	497.18	\N	12/11/2018
394	4314	MIDAZOLAM	LASIX	a.x 10 x 2 ml	SANOFI-AVENTIS	1496.17	14.9617	\N	10/11/2015
395	50137	RANITIDINA	LASIX	40 mg comp.x 60	SANOFI-AVENTIS	68572.98	1371.4596	\N	01/11/2015
396	13528	SOLUCION PARENTERAL	CLEXANE	20 mg jga.prell.x 10	SANOFI-AVENTIS	263644.34	263644.34	\N	28/01/2022
397	13530	SOLUCION PARENTERAL	CLEXANE	40 mg jga.prell.x 10	SANOFI-AVENTIS	511930.8	511930.8	\N	01/12/2025
398	18693	SOLUCION PARENTERAL	CLEXANE	60 mg jga.prell.x 10	SANOFI-AVENTIS	744859.25	744859.25	\N	02/09/2024
399	18694	SOLUCION PARENTERAL	CLEXANE	80 mg jga.prell.x 10	SANOFI-AVENTIS	982907.06	982907.06	\N	02/09/2024
400	18695	VANCOMICINA	CLEXANE	100 mg jga.prell.x 10	SANOFI-AVENTIS	1.2158355e+06	1.2158355e+06	\N	01/02/2003
401	39301	ONDANSETRON	DICLOFENAC SANT GALL	75 mg comp.x 30	SANT GALL	95.67	19.134	\N	12/08/2011
402	53249	KETOROLAC	FLEXIPLEN CAPSULA BLANDA	75 mg c ps.bl.x 10	SAVANT GENERIC	6894.79	344.7395	\N	15/12/2014
403	48452	MEROPENEM	DUPRAC SL	10 mg comp.subl.x 10	SAVANT GENERIC	485.91	485.91	\N	18/11/2002
404	48453	METOCLOPRAMIDA	DUPRAC	20 mg comp.x 10	SAVANT GENERIC	591.56	29.578	\N	14/06/2002
405	18165	RANITIDINA	LIDOCAINA	2% s/epi.a.x 5 ml	SCOTT-CASSARA	1474	24.566668	\N	15/08/2019
406	18169	SOLUCION PARENTERAL	LIDOCAINA VISCOSA	fco.got.x 50 ml	SCOTT-CASSARA	7810	78.1	\N	01/06/2002
407	18168	SOLUCION PARENTERAL	LIDOCAINA JALEA	2% jalea c/aplic.x 25 ml	SCOTT-CASSARA	8890	8890	\N	01/11/1992
408	51141	SOLUCION PARENTERAL	LIDOCAINA SPRAY	10%spr.x50g c/valv.aplic	SCOTT-CASSARA	32380	1295.2	\N	06/10/2025
409	30268	ONDANSETRON	VESALION	75 mg comp.x 15	SIEGFRIED	18585.18	18585.18	\N	24/02/2003
410	55162	SOLUCION PARENTERAL	MAR-V	3% spray nasal x 30 ml	SIEGFRIED	6846.2	6846.2	\N	06/09/2006
411	2048	SOLUCION PARENTERAL	MICROSONA	1% cr.x 15 g	SIEGFRIED	10775.05	215.501	\N	26/04/2002
412	25621	SOLUCION PARENTERAL	ALFICETIN	iny.a.x 1	SIEGFRIED	13215.22	13215.22	\N	03/12/2002
413	52501	RANITIDINA	REM CHOBET	15 mg comp.x 50	SOUBEIRAN CHOBET	29941.43	748.53577	\N	26/04/2002
414	52500	RANITIDINA	REM CHOBET	15 mg comp.x 30	SOUBEIRAN CHOBET	18746.36	37.49272	\N	26/04/2002
415	32660	SOLUCION PARENTERAL	REM CHOBET	15 mg/3 ml a.x 2	SOUBEIRAN CHOBET	19869.67	198.6967	\N	03/07/1996
416	30321	SOLUCION PARENTERAL	REM CHOBET	50 mg/10 ml a.x 25	SOUBEIRAN CHOBET	765037.2	765037.2	\N	15/11/2024
417	54521	SOLUCION PARENTERAL	ESPIROTECH INYECTABLE	f.a.x 1+disolv.x1	TECHSPHERE	30674.49	306.7449	\N	13/05/2024
418	46799	RANITIDINA	TOTAL MAGNESIANO	comp.rec.x 60	TEMIS-LOSTALO	89566.75	895.6675	\N	01/10/2020
419	45692	RANITIDINA	TOTAL MAGNESIANO EFERVESCENTE	pvo.sob.x 30	TEMIS-LOSTALO	44845.55	1494.8517	\N	27/12/2017
420	46798	RANITIDINA	TOTAL MAGNESIANO	comp.rec.x 30	TEMIS-LOSTALO	46437.77	464.3777	\N	01/10/2020
421	33027	DICLOFENAC SODICO	DICLOGESIC	50 mg comp.rec.x 15	TRB-PHARMA	6500	216.66667	\N	08/04/2025
422	13798	LIDOCAINA + ADRENALINA	DICLOGESIC	75 mg comp.rec.x 15	TRB-PHARMA	14500	14500	\N	04/07/2007
423	56033	SOLUCION PARENTERAL	METOC	0.5% gts.x 20 ml	VALMAX	7900	7900	\N	03/12/2002
424	34070	ONDANSETRON	METOCLOPRAMIDA VANNIER	comp.x 20	VANNIER	7250.11	7250.11	\N	01/01/2026
425	18554	POTASIO CLORURO	FUROSEMIDA VANNIER	comp.x 50	VANNIER	21505.55	21505.55	\N	20/07/2007
426	19496	FUROSEMIDA	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 100 x 10 ml	VEINFAR	380	12.666667	\N	03/09/2025
427	26529	HIOSCINA N-BUTILBR	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 100 x 10 ml	VEINFAR	626.94	6.2694	\N	13/08/2025
428	19555	RANITIDINA	METOCLOPRAMIDA LARJAN	10 mg a.x 100 x 2 ml	VEINFAR	285220	2852.2	\N	06/08/2024
429	15622	SODIO CLORURO	FURSEMIDA LARJAN	20 mg a.x 100 x 2 ml	VEINFAR	331990	331990	\N	17/04/2009
430	24593	SODIO CLORURO	RANITIDINA LARJAN	50 mg a.x 100 x 5 ml	VEINFAR	428190	428190	\N	15/11/2024
431	34162	SODIO CLORURO	KETOROLAC LARJAN	30 mg iny.a.x 100 x 2 ml	VEINFAR	430770	430770	\N	03/12/2025
432	19534	SODIO CLORURO	CLORURO DE POTASIO	15 mEq x 100 x 5 ml	VEINFAR	465480	465480	\N	17/06/2025
433	19561	SODIO CLORURO	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 100 x 10 ml	VEINFAR	466200	466200	\N	02/01/2026
434	15635	SOLUCION PARENTERAL	MAGNESIO	a.x 100 x 5 ml	VEINFAR	1.09454e+06	1.09454e+06	\N	03/12/2002
435	39322	SOLUCION PARENTERAL	MEROPENEM LARJAN	500 mg IV iny.f.a.x 1	VEINFAR	73460	73460	\N	02/09/2024
436	59694	SOLUCION PARENTERAL	IMIPENEM CILASTATINA LARJAN	a.x 1	VEINFAR	84110	84110	\N	02/09/2024
437	39323	VANCOMICINA	MEROPENEM LARJAN	1000 mg IV iny.f.a.x 1	VEINFAR	148650	148650	\N	03/04/2002
438	44975	CEFEPIME	RANITIDINA 150 VENT-3	150 mg blist.comp.x 10	Vent 3	5.12	5.12	\N	01/02/2003
439	44976	CEFEPIME	RANITIDINA 300 VENT-3	300 mg blist.comp.x 10	Vent 3	8.48	8.48	\N	05/03/2014
440	12707	CEFEPIME	MAGNESIO	625 mg comp.x 100	H. M dica Argen	10.9	10.9	\N	03/04/2012
441	27668	CEFEPIME	MAGNESIUM	500 mg tab.x 100	Feel Young	14.85	14.85	\N	21/10/2021
442	30247	CEFEPIME	FUROSEMIDA DUNCAN /KOLKIN	40 mg comp.x 1000	Duncan	150	150	\N	28/06/2021
443	21080	CEFEPIME	PASMODINA	10 mg comp.x 20	Drawer	3.33	3.33	\N	28/06/2021
444	22082	CEFEPIME	CELIT	10 mg comp.x 20	Fada Pharma	3.7	0.148	\N	19/04/2022
445	22657	CEFEPIME	CELIT	10 mg comp.x 500	Fada Pharma	92.5	92.5	\N	28/06/2021
446	29351	CEFEPIME	FADA METOCLOPRAMIDA	10 mg comp.x 500	Fada Pharma	92.5	92.5	\N	28/06/2021
447	24756	CEFEPIME	FUROSEM	40 mg comp.x 50	Investi	9.95	0.398	\N	19/04/2022
448	26594	CEFEPIME	MAGNESIO WP	comp.x 100	Wunder Pharm	19.9	0.4422222	\N	23/10/2025
449	695	CEFEPIME	LIZARONA	comp.x 10	Northia	2.03	0.0812	\N	06/10/2025
450	5923	CEFEPIME	METOCLOPRAMIDA RICHET	10 mg comp.x 20	Richet	4.19	0.0838	\N	13/08/2025
451	34853	CEFEPIME	MAGNESIO GOLD-FISH	caps.x 30	Drog. Argentina	6.55	0.0655	\N	12/12/2025
452	19525	CEFEPIME	FUROSEMIDA DUNCAN /KOLKIN	40 mg comp.x 500	Duncan	110.88	1.1088	\N	06/10/2025
453	29350	CEFEPIME	FADA METOCLOPRAMIDA	10 mg comp.x 20	Fada Pharma	4.9	0.196	\N	20/12/2025
454	28547	CEFEPIME	FRECUENTAL	40 mg comp.x 60	Lacefa	15.2	0.608	\N	06/10/2025
455	26990	CEFEPIME	ULCOTENK	150 mg comp.x 30	Biotenk	8	0.16	\N	06/10/2025
456	17844	CEFEPIME	TOP LIFE MAGNESIO	softgels x 60	Lasifarma	16.4	16.4	\N	20/12/2025
457	34603	CEFEPIME	FURTENK	40 mg comp.rec.x 40	Biotenk	11.2	0.448	\N	13/08/2025
458	28546	CEFEPIME	FRECUENTAL	40 mg comp.x 30	Lacefa	8.6	0.172	\N	12/12/2025
459	34134	CEFEPIME	FUROSEMIDA RIGO	40 mg comp.x 60	Rig	17.39	0.6956	\N	20/12/2025
460	34133	CEFEPIME	FUROSEMIDA RIGO	40 mg comp.x 30	Rig	8.7	8.7	\N	20/12/2025
461	18768	COLISTINA METANSULFONATO	TOP LIFE MAGNESIO	blist.caps.x 10	Lasifarma	2.9	0.725	\N	18/01/2003
462	29907	COLISTINA METANSULFONATO	SOLUC.FISIOLOGICA	blist.monods.x 12 x 3 ml	Valmax	3.5	3.5	\N	13/06/2011
463	40624	COLISTINA METANSULFONATO	EXCELENTIA ANTIESPASMODICO	comp.rec.x 20	Excelentia	5.9	5.9	\N	04/09/2017
464	30648	COLISTINA METANSULFONATO	MAGNESIO ISA	400 mg comp.x 20	ISA	5.95	5.95	\N	01/11/2021
465	2451	COLISTINA METANSULFONATO	FENDIBINA	comp.x 50	Northia	14.9	0.596	\N	16/03/2023
466	26313	COLISTINA METANSULFONATO	AGUA DESTILADA EXPERIENTIA	a.x 100 x 3 ml	Experientia	30	30	\N	21/10/2021
467	6049	COLISTINA METANSULFONATO	ELIUR	comp.x 20	Northia	6.06	6.06	\N	12/12/2025
468	13663	COLISTINA METANSULFONATO	HIDROCORTISONA FABRA	10 mg comp.x 20	Fabra	6.08	6.08	\N	01/01/2026
469	2988	COLISTINA METANSULFONATO	FURSEMIDA SINTESINA	40 mg comp.x 20	Sintesina	6.12	0.1224	\N	01/01/2026
470	29908	COLISTINA METANSULFONATO	SOLUC.FISIOLOGICA	blist.monods.x 12 x 5 ml	Valmax	3.75	3.75	\N	16/12/2025
471	27141	COLISTINA METANSULFONATO	SOLUC.FISIOLOGICA	fco.monods.x 6 x 3 ml	Valmax	1.9	0.076	\N	27/06/2025
472	30751	COLISTINA METANSULFONATO	MAGNESIUM	500 mg tab.x 30	Feel Young	9.64	9.64	\N	06/10/2025
473	27582	COLISTINA METANSULFONATO	RANITIC	150 mg comp.x 60	Investi	19.9	0.398	\N	13/08/2025
474	19586	COLISTINA METANSULFONATO	MAGNESIO LAFARMEN	400 mg caps.x 60	Lafarmen	20	20	\N	17/09/2025
475	18555	COLISTINA METANSULFONATO	METOCLOPRAMIDA VANNIER	comp.x 50	Vannier	16.73	0.1673	\N	23/10/2025
476	36935	COLISTINA METANSULFONATO	ALIVIAN	150 mg comp.x 120	Vitarum	41.2	1.3733333	\N	16/12/2025
477	11788	COLISTINA METANSULFONATO	ELIUR	comp.x 50	Northia	17.2	0.5733333	\N	01/01/2026
478	43879	DICLOFENAC SODICO	DHARAM SINGH	Nat.sob.x 100 x 1 g c/u	Dharam Singh	35	35	\N	01/03/2017
479	27142	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	fco.monods.x 6 x 5 ml	Valmax	2.1	2.1	\N	16/12/2025
480	20752	DICLOFENAC SODICO	MAGNESOIDE	comp.x 50	Argenfarma	18	18	\N	16/12/2025
481	26339	DICLOFENAC SODICO	SOLUC.FISIOLOGICA EXPERIENTIA	a.x 100 x 3 ml	Experientia	36	36	\N	01/12/2025
482	23635	DICLOFENAC SODICO	RANITIDINA DRAWER	150 mg comp.rec.x 50	Drawer	18.17	1.2113333	\N	03/09/2022
483	24038	DICLOFENAC SODICO	FURIX	40 mg comp.x 20	Investi	7.51	0.25033334	\N	31/07/2016
484	29947	DICLOFENAC SODICO	SG33	comp.ran.x 50	Sigma	19	0.037698414	\N	12/12/2025
485	30694	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	monods.x 6 x 3 ml	Valmax	2.35	0.15666667	\N	18/06/2024
486	35163	DICLOFENAC SODICO	FADA FUROSEMIDA	40 mg comp.x 50	Fada Pharma	19.9	0.66333336	\N	18/06/2024
487	23969	DICLOFENAC SODICO	ALUDROX AC	comp.x 20	Bag	8	0.53333336	\N	02/05/2024
488	22549	DICLOFENAC SODICO	RANITIDINA LAZAR	100 mg comp.x 30	Lazar	12	0.8	\N	20/12/2025
489	26314	DICLOFENAC SODICO	AGUA DESTILADA EXPERIENTIA	a.x 100 x 5 ml	Experientia	41	2.7333333	\N	16/12/2025
490	25475	DICLOFENAC SODICO	KLONAFENAC	1 mg/ml colirio x 5 ml	Klonal	127.22	4.240667	\N	05/08/2021
491	27435	DICLOFENAC SODICO	RANITIDINA SHABBA	150 mg comp.rec.x 20	Shabba	8.55	0.855	\N	03/05/2002
492	30695	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	monods.x 6 x 5 ml	Valmax	2.6	0.17333333	\N	18/01/2003
493	28985	DICLOFENAC SODICO	FURIX	Rtd.30 mg caps.x 50	Investi	21.97	1.4646667	\N	16/03/2017
494	21089	DICLOFENAC SODICO	RANITIDINA DRAWER	150 mg comp.rec.x 20	Drawer	8.9	0.445	\N	03/05/2002
495	340	DICLOFENAC SODICO	AGUA DESTILADA APOLO	a.x 1 x 3 ml	Apolo	0.45	0.015	\N	18/01/2003
496	30956	DICLOFENAC SODICO	FURSEMIDA PHARMA	40 mg comp.x 50	Pharma del Plat	22.51	1.5006666	\N	06/09/2012
497	28984	DICLOFENAC SODICO	FURIX	Rtd.30 mg caps.x 20	Investi	9.14	0.60933334	\N	16/12/2025
498	34130	DICLOFENAC SODICO	RANITIDINA RIGO	150 mg comp.x 20	Rig	9.24	0.308	\N	06/09/2012
499	21252	DICLOFENAC SODICO	FURAGRAND	40 mg comp.x 40	Fada Pharma	18.71	1.2473333	\N	27/08/2024
500	46957	DICLOFENAC SODICO	DIFENAC	1% sol.oft.x 10 ml	Lafedar	10083.26	112.036224	\N	24/10/2025
501	26340	DICLOFENAC SODICO	SOLUC.FISIOLOGICA EXPERIENTIA	a.x 100 x 5 ml	Experientia	48	9.6	\N	31/05/2017
502	17118	DICLOFENAC SODICO	MAGNESIO ISA	400 mg comp.x 30	ISA	14.5	0.019333333	\N	05/05/2025
503	11138	DICLOFENAC SODICO	RANITIDINA ILAB	150 mg comp.x 40	Inmunolab	19.46	1.946	\N	01/12/2025
504	29363	DICLOFENAC SODICO	FADA RANITIDINA	150 mg comp.x 30	Fada Pharma	14.9	0.745	\N	01/12/2025
505	32084	DICLOFENAC SODICO	SG33	comp.ran.x 30	Sigma	15	0.5	\N	01/02/2021
506	26315	DICLOFENAC SODICO	AGUA DESTILADA EXPERIENTIA	a.x 100 x 10 ml	Experientia	50	0.1	\N	01/12/2025
507	31707	DICLOFENAC SODICO	REFLUX	150 mg comp.x 10	Adium	5.08	0.508	\N	01/12/2025
508	31708	DICLOFENAC SODICO	REFLUX	150 mg comp.x 30	Adium	15.24	1.016	\N	18/12/2025
509	41353	DICLOFENAC SODICO	ADESIAL	150 mg comp.x 140.	Vitarum	71.19	4.746	\N	17/12/2025
510	46956	DICLOFENAC SODICO	DIFENAC	1% sol.oft.x 5 ml	Lafedar	13717.79	1371.779	\N	01/01/2001
511	36934	DICLOFENAC SODICO	ALIVIAN	150 mg comp.x 20	Vitarum	10.2	0.51	\N	01/01/2001
512	29364	DICLOFENAC SODICO	FADA RANITIDINA	150 mg comp.x 50	Fada Pharma	25.52	12.76	\N	27/07/2012
513	29365	DICLOFENAC SODICO	FADA RANITIDINA	150 mg comp.x 500	Fada Pharma	255.2	63.8	\N	04/11/2015
514	11171	DICLOFENAC SODICO	INSUFLEN	comp.x 50	Fada Pharma	25.52	2.552	\N	12/12/2025
515	21612	DICLOFENAC SODICO	INSUFLEN	comp.x 500	Fada Pharma	255.2	12.76	\N	12/12/2025
516	4156	DICLOFENAC SODICO	ORALSONE	comp.x 30	Gram n	15.58	3.116	\N	12/12/2025
517	40726	DICLOFENAC SODICO	KINALGIN	1.5% sol.t pica x 60 ml	Teva Argentina	19432.75	194.3275	\N	27/08/2008
518	32561	DICLOFENAC SODICO	APRICAL RANITIDINA	150 mg comp.rec.x 100	Adium	52.7	5.27	\N	08/04/2004
519	35543	DICLOFENAC SODICO	DOLVAN	100 mg AP comp.x 15	Gador	1840.45	92.0225	\N	08/04/2004
520	26001	DICLOFENAC SODICO	RANITIDINA FABOP 150	150 mg comp.x 30	Fabop	15.95	1.595	\N	01/03/2005
521	40180	DICLOFENAC SODICO	ADESIAL	150 mg comp.x 120	Vitarum	64.54	3.227	\N	01/03/2005
522	11886	DICLOFENAC SODICO	ILIADIN 40	40 mg comp.x 50	Tuteur	26.9	5.38	\N	01/03/2005
523	32560	DICLOFENAC SODICO	APRICAL RANITIDINA	150 mg comp.rec.x 30	Adium	16.46	1.646	\N	23/01/2024
524	36564	DICLOFENAC SODICO	FENDIBINA	150 mg comp.x 500	Northia	275	27.5	\N	03/12/2025
525	32559	DICLOFENAC SODICO	APRICAL RANITIDINA	150 mg comp.rec.x 10	Adium	5.5	0.55	\N	18/01/2003
526	40224	DICLOFENAC SODICO	RANITIDINA 150 VENT-3	150 mg comp.x 30	Vent 3	16.7	1.67	\N	24/04/2015
527	40225	DICLOFENAC SODICO	RANITIDINA 150 VENT-3	150 mg comp.x 60	Vent 3	33.5	1.675	\N	18/01/2003
528	26341	DICLOFENAC SODICO	SOLUC.FISIOLOGICA EXPERIENTIA	a.x 100 x 10 ml	Experientia	56	5.6	\N	28/11/2007
529	33419	DICLOFENAC SODICO	CISCOMAX REPEL	150 mg comp.rec.x 60	Eczane	33.8	3.38	\N	28/11/2013
530	114	DICLOFENAC SODICO	TEOGRAND	comp.rec.x 50	Fada Pharma	28.25	2.825	\N	18/06/2024
531	32303	DICLOFENAC SODICO	FABOACID R	150 mg comp.rec.x 60	Fabop	33.9	3.39	\N	20/11/2025
532	37825	DICLOFENAC SODICO	RANITIDINA GEN MED	150 mg comp.rec.x 60	Gen Med	34.03	0.3403	\N	28/11/2013
533	32562	DICLOFENAC SODICO	APRICAL RANITIDINA	150 mg comp.rec.x 500	Adium	285	14.25	\N	28/11/2007
534	32864	DICLOFENAC SODICO	REFLUX	75 mg comp.x 30	Monte Verde	17.1	0.855	\N	28/11/2013
535	33418	DICLOFENAC SODICO	CISCOMAX REPEL	150 mg comp.rec.x 20	Eczane	11.44	0.047666665	\N	01/07/2000
536	27798	DICLOFENAC SODICO	PAXYL	10 mg comp.x 20	Elvetium	11.5	0.575	\N	20/11/2025
537	23002	DICLOFENAC SODICO	MAGNEFORTE	10 mmol comp.efer.x 20	Investi	11.5	11.5	\N	01/03/2014
538	17377	DICLOFENAC SODICO	RANITRAL 150	150 mg comp.x 60	Austral	34.8	3.48	\N	03/01/2024
539	27143	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	fco.monods.x 6 x 10 ml	Valmax	3.5	0.23333333	\N	27/12/2025
540	36937	DICLOFENAC SODICO	ALIVIAN	300 mg comp.x 140	Vitarum	82	2.7333333	\N	27/12/2025
541	37902	DICLOFENAC SODICO	PREDNOCRIS	150 mg comp.rec.x 30	LKM	17.72	1.1813333	\N	14/09/2018
542	12041	DICLOFENAC SODICO	METOCLOPRAMIDA MARTIAN	1% a.x 1	LKM	0.6	0.02	\N	14/09/2018
543	40223	DICLOFENAC SODICO	RANITIDINA 150 VENT-3	150 mg comp.x 20	Vent 3	12	1.2	\N	15/01/2005
544	30700	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	Twist-Off monods.x12x5ml	Valmax	7.2	0.36	\N	15/01/2005
545	30697	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	Twist-Off monods.x6 x4ml	Valmax	3.6	0.18	\N	01/03/2002
546	29478	DICLOFENAC SODICO	RANITIDINA PHARMA	150 mg comp.x 20	Pharma del Plat	12.04	1.204	\N	15/06/2016
547	37824	DICLOFENAC SODICO	RANITIDINA GEN MED	150 mg comp.rec.x 20	Gen Med	12.08	0.1208	\N	03/11/2015
548	40179	DICLOFENAC SODICO	ADESIAL	150 mg comp.x 20	Vitarum	12.1	1.21	\N	31/10/2003
549	9580	DICLOFENAC SODICO	TEOGRAND	comp.rec.x 20	Fada Pharma	12.24	1.224	\N	24/12/1999
550	5594	DICLOFENAC SODICO	RANITIDINA MILLET	150 mg comp.rec.x 20	Millet-Franklin	12.32	1.232	\N	18/01/2003
551	30699	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	Twist-Off monods.x6 x5ml	Valmax	3.7	0.37	\N	15/07/2008
552	5752	DICLOFENAC SODICO	GASTROZAC	150 mg comp.x 20	Klonal	12.39	1.239	\N	26/06/2014
553	29416	DICLOFENAC SODICO	HIOSCINA VANNIER	10 mg comp.x 20	Vannier	12.54	1.254	\N	08/04/2013
554	32302	DICLOFENAC SODICO	FABOACID R	150 mg comp.rec.x 20	Fabop	12.6	1.26	\N	29/08/2016
555	35544	DICLOFENAC SODICO	DOLVAN	100 mg AP comp.x 30	Gador	171.73	17.173	\N	01/12/2025
556	32729	DICLOFENAC SODICO	RANITIDINA LARJAN	150 mg comp.x 20	Veinfar	12.65	1.265	\N	19/12/2025
557	41493	DICLOFENAC SODICO	FABOACID	150 mg comp.x 60	Fabop	37.97	0.3797	\N	10/08/2011
558	17376	DICLOFENAC SODICO	RANITRAL 150	150 mg comp.x 20	Austral	12.7	0.127	\N	26/06/2014
559	32654	DICLOFENAC SODICO	DUALID	150 mg comp.x 20	Duncan	12.7	0.127	\N	12/05/2014
560	20253	DICLOFENAC SODICO	TOMAG	75 mg comp.x 20	Temis-Lostal	12.7	0.8466667	\N	15/04/2011
561	41494	DICLOFENAC SODICO	FABOACID	150 mg comp.x 90	Fabop	57.15	3.81	\N	01/12/2010
562	15813	DICLOFENAC SODICO	COLOBOLINA	comp.x 20	Fabra	12.78	0.852	\N	14/08/2012
563	37054	DICLOFENAC SODICO	LORBITIDINA	150 mg comp.rec.x 60	Filaxis Farmac	38.64	2.576	\N	06/07/2015
564	19951	DICLOFENAC SODICO	RANITIDI G.N.O.	150 mg comp.rec.x 20	Arion	13	0.8666667	\N	06/09/2012
565	24134	DICLOFENAC SODICO	MIDAZOLAM LAFEDAR	7.5 mg comp.x 20	Lafedar	13.03	0.86866665	\N	27/11/2015
566	5757	DICLOFENAC SODICO	GASTROZAC	300 mg comp.x 60	Klonal	39.51	2.634	\N	02/05/2024
567	58360	DICLOFENAC SODICO	DICLOFENAC AP KILAB	100 mg c ps. x 504 (EH)	Kilab	440052.47	29336.832	\N	16/12/2025
568	28986	DICLOFENAC SODICO	FURIX	Rtd.60 mg caps.x 20	Investi	13.42	0.8946667	\N	06/10/2025
569	32567	DICLOFENAC SODICO	AGUA DESTILADA DRAWER	a.x 50 x 5 ml	Drawer	34.35	2.29	\N	01/12/2025
570	32621	DICLOFENAC SODICO	SOLUC.FISIOLOGICA DRAWER	a.x 50 x 5 ml	Drawer	34.35	1.7175	\N	31/10/2003
571	11378	DICLOFENAC SODICO	DUALID	150 mg comp.x 40	Duncan	27.5	1.375	\N	24/12/1999
572	56137	DICLOFENAC SODICO	DICLOFENAC AP HLB	100 mg c ps.acc.prol.x15	HLB Pharma	12671.38	633.569	\N	26/06/2014
573	56355	DICLOFENAC SODICO	DICLOFENAC AP HLB	100 mg c ps.acc.prol.x30	HLB Pharma	23880.68	1194.034	\N	08/04/2013
574	55693	DICLOFENAC SODICO	ACLOXIGENAC LP	100 mg c ps.LP.x 15	Eczane	9405.99	470.2995	\N	29/11/2013
575	16853	DICLOFENAC SODICO	RANITIDINA VANNIER	150 mg comp.x 20	Vannier	13.95	0.6975	\N	01/12/2025
576	47482	DICLOFENAC SODICO	FUROSEMIDA PUNTANOS	40 mg comp.x 20	Laboratorios Pu	14	0.46666667	\N	15/04/2011
577	30696	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	monods.x 6 x 10 ml	Valmax	4.2	0.14	\N	24/12/1999
578	19443	DICLOFENAC SODICO	SOLUC.FISIOLOGICA BIOL	a.x 100 x 5 ml	Biol	70.06	2.3353333	\N	01/12/2010
579	20387	DICLOFENAC SODICO	RANITUL	150 mg comp.x 20	Oriental	14.2	0.47333333	\N	14/08/2012
580	11137	DICLOFENAC SODICO	RANITIDINA ILAB	150 mg comp.x 20	Inmunolab	14.33	0.47766668	\N	06/07/2015
581	25197	DICLOFENAC SODICO	URGIS	150 mg comp.x 20	Cetus	14.4	0.48	\N	06/09/2012
582	1292	DICLOFENAC SODICO	RATICINA	comp.x 50	Laboratorios Be	36.16	1.2053334	\N	14/04/2018
583	37053	DICLOFENAC SODICO	LORBITIDINA	150 mg comp.rec.x 20	Filaxis Farmac	14.49	0.483	\N	25/08/2016
584	26002	DICLOFENAC SODICO	RANITIDINA FABOP 300	300 mg comp.x 20	Fabop	14.5	0.48333332	\N	06/10/2025
585	57631	DICLOFENAC SODICO	BEFOL AP RETARD	100 mg c ps.x 15	Biotenk	13009.61	26.01922	\N	01/12/2025
586	29705	DICLOFENAC SODICO	FURSEMIDA FABRA 40	comp.x 60	Fabra	43.75	4.375	\N	03/10/2003
587	52007	DICLOFENAC SODICO	LAFENAC	100 mg c ps.x 15	Lafedar	25029.26	2502.926	\N	01/11/2005
588	34131	DICLOFENAC SODICO	RANITIDINA RIGO	300 mg comp.x 20	Rig	15	1.5	\N	05/09/2002
589	34132	DICLOFENAC SODICO	RANITIDINA RIGO	300 mg comp.x 30	Rig	22.5	2.25	\N	01/02/2007
590	55750	DICLOFENAC SODICO	FLEXIPLEN RETARD	100 mg c ps.x 30	Savant Generic	2078.68	207.868	\N	01/10/2005
591	19419	DICLOFENAC SODICO	AGUA BIDESTILADA BIOL	a.x 100 x 5 ml	Biol	75.44	7.544	\N	02/02/2007
592	32609	DICLOFENAC SODICO	METOCLOPRAMIDA DRAWER	10 mg a.x 50	Drawer	37.9	3.79	\N	01/09/2005
593	17868	DICLOFENAC SODICO	IMANOL AP	100 mg caps.x 10	Biosintex	24.3	2.43	\N	18/11/2002
594	24039	DICLOFENAC SODICO	FURIX	40 mg comp.x 50	Investi	38.12	3.812	\N	15/11/2012
595	22236	DICLOFENAC SODICO	DAMIXA RETARD	100 mg caps.x 15	Merck Serono	42.9	4.29	\N	07/07/2020
596	41435	DICLOFENAC SODICO	DICLONEX 100 AP	100 mg caps.x 15	Nexo Pharmaceut	88	8.8	\N	17/02/2020
597	18892	DICLOFENAC SODICO	AGUA BIDESTILADA APIRETOGENA	a.x 100 x 3 ml	Welt	77.39	0.7739	\N	03/09/2018
598	18895	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 100 x 3 ml	Welt	77.39	0.7739	\N	26/10/2017
599	456	DICLOFENAC SODICO	GASTRIAL	150 mg comp.x 10	Sanofi-Aventis	7.8	0.52	\N	26/06/2014
600	32576	DICLOFENAC SODICO	CLORURO DE POTASIO DRAWER	15 mEq iny.a.x 50 x 5ml	Drawer	39.35	2.6233332	\N	24/08/2004
601	13447	DICLOFENAC SODICO	LUAR G	20 mg a.x 6	Klonal	4.73	0.31533334	\N	06/07/2015
602	26332	DICLOFENAC SODICO	FUROSEMIDA EXPERIENTIA	20 mg a.x 100 x 2 ml	Experientia	79	5.266667	\N	14/10/2010
603	32298	DICLOFENAC SODICO	FABOFUROX	40 mg comp.x 50	Savant Consumer	39.6	2.64	\N	16/09/2013
604	27436	DICLOFENAC SODICO	RANITIDINA SHABBA	300 mg comp.rec.x 30	Shabba	23.76	1.584	\N	30/12/2016
605	32109	DICLOFENAC SODICO	TAURAL	150 mg comp.x 100	Roemmers	79.35	5.29	\N	15/12/2015
606	17867	DICLOFENAC SODICO	IMANOL AP	100 mg caps.x 20	Biosintex	36.8	2.4533334	\N	06/07/2015
607	32589	DICLOFENAC SODICO	FUROSEMIDA DRAWER	20 mg a.x 50 x 2 ml	Drawer	40.05	2.67	\N	31/12/2013
608	22237	DICLOFENAC SODICO	DAMIXA RETARD	100 mg caps.x 30	Merck Serono	65.7	4.38	\N	16/03/2017
609	5761	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 6 x 5 ml	Klonal	4.95	0.33	\N	11/08/2020
610	33042	DICLOFENAC SODICO	DICLOFENAC HEXA 100 RETARD	100 mg comp.rec.x 15	Fada Pharma	47.26	3.1506667	\N	03/09/2022
611	32619	DICLOFENAC SODICO	RANITIDINA DRAWER	50 mg iny.x 50	Drawer	41.5	2.7666667	\N	18/06/2024
612	38198	DICLOFENAC SODICO	PRIMPERIL	comp.x 10	Lafedar	8.3	0.55333334	\N	25/09/2024
613	36279	DICLOFENAC SODICO	DIFENAC RETARD	100 mg comp.rec.x 15	Lafedar	20864.7	1390.98	\N	29/12/2025
614	42336	DICLOFENAC SODICO	FENDIBINA	150 mg comp.rec.x 100	Northia	83.43	5.562	\N	18/12/2025
615	12231	DICLOFENAC SODICO	K-DUR	750 mg(10 mEq)comp.x 20	MSD Argentina S	16.69	0.111266665	\N	12/04/2007
616	18893	DICLOFENAC SODICO	AGUA BIDESTILADA APIRETOGENA	a.x 100 x 5 ml	Welt	84.06	4.203	\N	26/06/2014
617	33043	DICLOFENAC SODICO	DICLOFENAC HEXA 100 RETARD	100 mg comp.rec.x 30	Fada Pharma	92.79	4.6395	\N	21/12/2005
618	8538	DICLOFENAC SODICO	SUSTAC	comp.x 60	Pfizer	50.9	2.545	\N	05/11/2015
619	20400	DICLOFENAC SODICO	FURSEMIDA FABRA 40	comp.x 20	Fabra	16.98	0.849	\N	01/03/2014
620	21117	DICLOFENAC SODICO	DIASTONE RETARD	100 mg comp.x 15	Microsules Arg.	13736.36	686.818	\N	10/06/2016
621	63586	DICLOFENAC SODICO	FABOGESIC FLEXI RETARD	100 mg comp.x 90	Savant Consumer	27521.08	1376.054	\N	17/02/2020
622	30981	DICLOFENAC SODICO	VIZERUL	comp.x 20	Montpellier	17.28	0.576	\N	22/11/2004
623	2249	DICLOFENAC SODICO	VOLTAREN	100 mg sup.x 5	Novartis	71.59	2.3863332	\N	01/02/2007
624	9048	DICLOFENAC SODICO	ORALSONE	comp.x 8	Gram n	6.93	0.231	\N	24/08/2004
625	24136	DICLOFENAC SODICO	MIDAZOLAM LAFEDAR	15 mg comp.x 30	Lafedar	25.99	0.8663333	\N	01/10/2004
626	58988	DICLOFENAC SODICO	NORVIKEN 100 VENT-3	100mg bl st.x 50 x15c ps	Vent 3	139906.64	4663.5547	\N	03/03/2006
627	11140	DICLOFENAC SODICO	RANITIDINA ILAB	300 mg comp.x 40	Inmunolab	35.05	1.1683333	\N	06/07/2015
628	28965	DICLOFENAC SODICO	PASMOVIT	comp.rec.x 20	Finadiet	17.55	0.585	\N	16/09/2013
629	61842	DICLOFENAC SODICO	ACLOXIGENAC LP	100mg c ps.lib.prol.x 10	Eczane	9261.04	308.70132	\N	23/02/2006
630	61843	DICLOFENAC SODICO	ACLOXIGENAC LP	100mg c ps.lib.prol.x 20	Eczane	16508.07	550.269	\N	15/12/2015
631	22934	DICLOFENAC SODICO	RANITIDINA DENVER FARMA	300 mg comp.x 20	Denver Farma	17.82	0.594	\N	06/07/2015
632	24135	DICLOFENAC SODICO	MIDAZOLAM LAFEDAR	15 mg comp.x 10	Lafedar	8.93	0.29766667	\N	21/07/2017
633	28953	DICLOFENAC SODICO	SOLUC.FISIOLOGICA ESTERILIZADA	monodosis x 20 ml	Walker	0.9	0.03	\N	31/12/2013
634	33896	DICLOFENAC SODICO	MAGNESIO 102 PLUS	sob.x 20	ISA	18.1	0.60333335	\N	11/08/2020
635	27581	DICLOFENAC SODICO	RANITIC	150 mg comp.x 20	Investi	18.21	0.607	\N	27/08/2021
636	36775	DICLOFENAC SODICO	RANITIDINA LAN	300 mg comp.rec.x 20	Lanpharm	18.21	0.607	\N	18/06/2024
637	19372	DICLOFENAC SODICO	OPOLAM	40 mg comp.x 20	Microsules Arg.	18.33	0.611	\N	29/12/2025
638	21988	DICLOFENAC SODICO	CLORURO DE POTASIO BIOL	20 mEq a.x 100 x 5 ml	Biol	91.71	3.057	\N	18/12/2025
639	36936	DICLOFENAC SODICO	ALIVIAN	300 mg comp.x 10	Vitarum	9.2	0.23	\N	10/06/2016
640	54885	DICLOFENAC SODICO	NORVIKEN 100 VENT-3	100mg c ps.lib.prol.x 30	Vent 3	654.27	1.3217576	\N	19/05/2006
641	61844	DICLOFENAC SODICO	ACLOXIGENAC LP	100mg c ps.lib.prol.x500	Eczane	145133.62	290.26727	\N	03/10/2003
642	30655	DICLOFENAC SODICO	DUALID	300 mg comp.x 20	Duncan	18.51	0.03702	\N	03/10/2003
643	40182	DICLOFENAC SODICO	ADESIAL	300 mg comp.x 140	Vitarum	130.5	0.261	\N	16/09/2005
644	41605	DICLOFENAC SODICO	DICLOGESIC 100 AP	100mg comp.acc.prol.x 10	Trb-Pharma	10000	20	\N	27/11/2002
645	36611	DICLOFENAC SODICO	HIDROCORTISONA FABRA	10 mg comp.x 30	Fabra	28.26	0.35325	\N	30/11/2007
646	2689	DICLOFENAC SODICO	CIFESPASMO	20 mg a.x 6	Northia	5.68	0.284	\N	19/08/2025
647	21238	DICLOFENAC SODICO	BLOKIUM	100mg comp.acc.prol.x 15	Casasco	17647.88	1764.788	\N	22/03/2001
648	27799	DICLOFENAC SODICO	PAXYL	20 mg comp.x 20	Elvetium	19	0.079166666	\N	01/07/2000
649	47484	DICLOFENAC SODICO	RANITIDINA PUNTANOS	150 mg comp.x 20	Laboratorios Pu	19	0.95	\N	01/05/2002
650	2710	DICLOFENAC SODICO	FUROSEMIDA DRAWER	20 mg a.x 6	Drawer	5.7	0.38	\N	17/12/2025
651	5753	DICLOFENAC SODICO	GASTROZAC	150 mg comp.x 60	Klonal	57.06	1.902	\N	17/12/2025
652	1968	DICLOFENAC SODICO	LUVIER	150 mg comp.x 20	Casasco	19.05	0.1905	\N	26/06/2014
653	28053	DICLOFENAC SODICO	LIDOCAINA	1% a.x 100 x 5 ml	Klonal	95.48	15.913333	\N	13/01/2005
654	225	DICLOFENAC SODICO	RANITIDINA MILLET 300	300 mg comp.rec.x 30	Millet-Franklin	28.88	0.2888	\N	01/06/2002
655	42184	DICLOFENAC SODICO	XEDENOL	100mgcomp.rec.lib.prox15	Baliarda	17933.44	2988.9067	\N	01/02/2003
656	28741	DICLOFENAC SODICO	NOLARAC	10 mg comp.x 20	Fada Pharma	19.95	3.325	\N	01/11/2005
657	29344	DICLOFENAC SODICO	FADA KETOROLAC/NOLARAC	10 mg comp.x 500	Fada Pharma	498.75	83.125	\N	26/06/2014
658	24560	DICLOFENAC SODICO	NOLARAC	10 mg comp.x 500	Fada Pharma	498.75	498.75	\N	01/02/2002
659	28002	DICLOFENAC SODICO	ULTRAGESIC	140 mg caps.x 10	Adium	12.5	0.125	\N	14/06/2002
660	40228	DICLOFENAC SODICO	RANITIDINA 300 VENT-3	300 mg comp.x 60	Vent 3	60	10	\N	28/03/2002
661	34611	DICLOFENAC SODICO	ULCOTENK	300 mg comp.rec.x 20	Biotenk	20	3.3333333	\N	26/06/2014
662	28003	DICLOFENAC SODICO	ULTRAGESIC	140 mg caps.x 20	Adium	24	4.8	\N	17/03/2010
663	40008	DICLOFENAC SODICO	VOLTAREN 24 HS	15 mg parches x 2	Novartis Consum	24.43	0.2443	\N	04/11/2008
664	28487	DICLOFENAC SODICO	DICLAC	150 mg comp.rapirtd.x 10	Siegfried	12494.82	4164.94	\N	05/03/2014
665	1291	DICLOFENAC SODICO	RATICINA	comp.x 20	Laboratorios Be	20.58	6.86	\N	28/11/2013
666	26719	DICLOFENAC SODICO	FURSEMIDA BIOCROM	20 mg a.x 100	Biocrom	103	17.166666	\N	09/03/2017
667	40227	DICLOFENAC SODICO	RANITIDINA 300 VENT-3	300 mg comp.x 30	Vent 3	31	5.1666665	\N	30/11/2016
668	24041	DICLOFENAC SODICO	FURIX	250 mg comp.x 20	Investi	20.67	0.4134	\N	10/06/2016
669	8537	DICLOFENAC SODICO	SUSTAC	comp.x 20	Pfizer	20.94	4.188	\N	17/02/2020
670	28740	DICLOFENAC SODICO	NOLARAC	10 mg comp.x 10	Fada Pharma	10.5	2.625	\N	10/09/2020
671	26986	DICLOFENAC SODICO	MAGNESIO TECNONAT	comp.x 10	Tecnonat	10.5	0.105	\N	12/08/2021
672	21987	DICLOFENAC SODICO	CLORURO DE POTASIO BIOL	15 mEq a.x 100 x 5 ml	Biol	105.27	10.527	\N	03/12/2025
673	28825	DICLOFENAC SODICO	DICLAC	150 mg comp.rapirtd.x 20	Siegfried	24490.19	2449.019	\N	01/01/2026
674	23360	DICLOFENAC SODICO	ORMIR	comp.x 30	Neuropharma	32	3.2	\N	31/10/2009
675	32564	DICLOFENAC SODICO	APRICAL RANITIDINA	300 mg comp.rec.x 30	Adium	32.12	1.606	\N	31/10/2009
676	32565	DICLOFENAC SODICO	APRICAL RANITIDINA	300 mg comp.rec.x 100	Adium	107.1	7.14	\N	17/12/2025
677	34226	DICLOFENAC SODICO	DICLAC	150 mg comp.rapirtd.x 5	Siegfried	2888	96.26667	\N	20/12/2022
678	37830	DICLOFENAC SODICO	DICLAC	150 mg comp.rapirtd.x100	Investi	319.91	10.663667	\N	01/06/2024
679	816	DICLOFENAC SODICO	TRINITRON RETARD	comp.x 30	Eurofarma	32.62	1.0873333	\N	17/12/2025
680	33922	DICLOFENAC SODICO	DICLOFENAC MONTE VERDE	150mg comp.lib.prol.x 10	Monte Verde	37.95	5.4214287	\N	26/06/2014
681	25818	DICLOFENAC SODICO	CLORURO DE POTASIO	15 mEq a.x 100 x 5 ml	Norgreen	109.01	7.2673335	\N	06/05/2021
682	33923	DICLOFENAC SODICO	DICLOFENAC MONTE VERDE	150mg comp.lib.prol.x 20	Monte Verde	75.14	7.514	\N	12/12/2025
683	31709	DICLOFENAC SODICO	REFLUX	300 mg comp.x 30	Adium	32.97	1.6485	\N	12/12/2025
684	22638	DICLOFENAC SODICO	AKTIOSAN 150 UNO	150mg comp.Rapiretardx10	Investi	25.3	2.53	\N	26/06/2014
685	21092	DICLOFENAC SODICO	SOLVENTE INDOLORO DRAWER	iny.a.x 100 x 5 ml	Drawer	110	11	\N	06/08/2012
686	40226	DICLOFENAC SODICO	RANITIDINA 300 VENT-3	300 mg comp.x 20	Vent 3	22	2.2	\N	31/03/2017
687	29480	DICLOFENAC SODICO	RANITIDINA PHARMA	300 mg comp.x 20	Pharma del Plat	22	2.2	\N	01/10/2017
688	22639	DICLOFENAC SODICO	AKTIOSAN 150 UNO	150mg comp.Rapiretardx20	Investi	50.09	5.009	\N	01/12/2025
689	35860	DICLOFENAC SODICO	AKTIOSAN 150 UNO	150mg comp.Rapiretardx5	Investi	14.9	1.49	\N	01/12/2025
690	32603	DICLOFENAC SODICO	PASMODINA	20 mg iny.a.x 100	Drawer	111.05	11.105	\N	19/12/2025
691	7926	DICLOFENAC SODICO	TAURAL	150 mg comp.x 20	Roemmers	22.4	0.224	\N	16/09/2013
692	40181	DICLOFENAC SODICO	ADESIAL	300 mg comp.x 10	Vitarum	11.2	0.112	\N	08/06/2021
693	54397	DICLOFENAC SODICO	FLEXIPLEN CAPSULA BLANDA	25 mg c ps.bl.x 10	Savant Generic	1399.61	1.3721666	\N	12/08/2021
694	29343	DICLOFENAC SODICO	FADA KETOROLAC/NOLARAC	10 mg comp.x 20	Fada Pharma	22.5	1.5	\N	11/12/2007
695	32304	DICLOFENAC SODICO	FABOACID R	300 mg comp.rec.x 30	Fabop	33.98	2.2653334	\N	01/09/2005
696	30698	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PARA NEBULIZAR	Twist-Off monods.x12x4ml	Valmax	6.8	0.45333335	\N	11/05/2006
697	15630	DICLOFENAC SODICO	SOLUC.FISIOLOGICA VEINFAR	iny.x 100 x 3 ml	Veinfar	114	7.6	\N	14/11/2008
698	41496	DICLOFENAC SODICO	FABOACID	300 mg comp.x 90	Fabop	102.76	6.8506665	\N	06/07/2015
699	18612	DICLOFENAC SODICO	KERARER	10 mg comp.x 20	LKM	22.9	1.5266666	\N	27/11/2015
700	62209	DICLOFENAC SODICO	FABOGESIC FLEXI 25	25 mg c ps.x 10	Savant Consumer	4370	291.33334	\N	02/05/2024
701	28971	DICLOFENAC SODICO	AKTIOSAN	25 mg comp.rec.x 10	Investi	7.4	0.49333334	\N	02/08/2025
702	8642	DICLOFENAC SODICO	ACIDEX	comp.rec.x 50	Teva Argentina	57.79	3.8526666	\N	06/10/2025
703	41775	DICLOFENAC SODICO	DOXTRAN MAX	25 mg comp.rec.x 10	Phoenix	12.4	0.82666665	\N	29/12/2025
704	17378	DICLOFENAC SODICO	RANITRAL 300	300 mg comp.x 30	Austral	34.8	2.32	\N	01/01/2026
705	20137	DICLOFENAC SODICO	AKTIOSAN	25 mg comp.rec.x 20	Investi	12.63	0.842	\N	16/12/2025
706	18504	DICLOFENAC SODICO	AGUA BIDESTILADA RIGO	a.x 3 x 5 ml	Rig	3.5	0.23333333	\N	01/12/2025
707	18514	DICLOFENAC SODICO	SOLUC.FISIOLOGICA RIGO	a.x 3 x 5 ml	Rig	3.5	0.23333333	\N	25/08/2025
708	32500	DICLOFENAC SODICO	LIDOCAINA	2% a.x 100 x 5 ml	Klonal	116.67	5.8335	\N	01/03/2014
709	28054	DICLOFENAC SODICO	LIDOCAINA	2% c/epi.a.x 100 x 5 ml	Klonal	116.67	5.8335	\N	01/02/2016
710	30639	DICLOFENAC SODICO	ESPAVEN	comp.x 21	E. J. Gezzi	24.66	1.233	\N	01/12/2025
711	5735	DICLOFENAC SODICO	NOVOMIT	10 mg a.x 6	Klonal	7.08	0.354	\N	19/12/2025
712	41776	DICLOFENAC SODICO	DOXTRAN MAX	25 mg comp.rec.x 20	Phoenix	23.6	0.8428571	\N	15/04/2011
713	37905	DICLOFENAC SODICO	PREDNOCRIS	300 mg comp.rec.x 30	LKM	35.45	1.2660714	\N	16/04/2012
714	36361	DICLOFENAC SODICO	FLEXIN	25 mg comp.x 10	Sidus	5.2	0.17333333	\N	11/12/2007
715	46007	DICLOFENAC SODICO	REUMOSAN RAPIDA ACCION	25 mg comp.x 10	E. J. Gezzi	17.36	0.5786667	\N	02/08/2012
716	59282	DICLOFENAC SODICO	FLEXANA	25 mg comp.x 10	HLB Pharma	552.34	18.411333	\N	14/11/2008
717	62791	DICLOFENAC SODICO	BLOKIUM	25 mg comp.x 10 (VL)	Casasco	3484.56	116.152	\N	06/07/2015
718	46009	DICLOFENAC SODICO	REUMOSAN RAPIDA ACCION	25 mg comp.x 100	E. J. Gezzi	135.74	4.524667	\N	01/10/2020
719	21081	DICLOFENAC SODICO	PASMODINA	20 mg iny.a.x 6	Drawer	7.2	0.24	\N	29/12/2025
720	18506	DICLOFENAC SODICO	CLORURO DE POTASIO RIGO	15 mEq x 3 x 5 ml	Rig	3.6	0.12	\N	06/10/2025
721	36362	DICLOFENAC SODICO	FLEXIN	25 mg comp.x 20	Sidus	10.6	0.35333332	\N	01/12/2025
722	46008	DICLOFENAC SODICO	REUMOSAN RAPIDA ACCION	25 mg comp.x 20	E. J. Gezzi	33.94	1.1313334	\N	30/12/2025
723	23727	DICLOFENAC SODICO	ATLAMAC	10 mg comp.x 20	Casasco	24.14	0.6035	\N	28/08/2024
724	26380	DICLOFENAC SODICO	AKTIOSAN	25 mg tab.rec.x 10 x 24	Investi	114.96	0.22992	\N	01/12/2025
725	15615	DICLOFENAC SODICO	AGUA DESTILADA	a.x 100 x 3 ml	Veinfar	122	0.13555555	\N	27/07/2021
726	32602	DICLOFENAC SODICO	PASMODINA	20 mg iny.a.x 50	Drawer	61.1	6.11	\N	01/12/2001
727	19444	DICLOFENAC SODICO	SOLUC.FISIOLOGICA BIOL	a.x 100 x 10 ml	Biol	122.62	12.262	\N	03/11/2015
728	32566	DICLOFENAC SODICO	APRICAL RANITIDINA	300 mg comp.rec.x 500	Adium	615	61.5	\N	17/02/2020
729	15829	DICLOFENAC SODICO	VINGIONAL	300 mg comp.x 20	Fabra	24.74	2.474	\N	15/12/2025
730	62792	DICLOFENAC SODICO	BLOKIUM	25mg comp.x 20 (VL)	Casasco	6783.9	67.839	\N	06/05/2016
731	36176	DICLOFENAC SODICO	BLOKIUM GEL 5	5 g pomo x 30 g	Casasco	42.2	0.422	\N	03/11/2015
732	29342	DICLOFENAC SODICO	FADA KETOROLAC/NOLARAC	10 mg comp.x 10	Fada Pharma	12.5	0.125	\N	06/05/2021
733	19874	DICLOFENAC SODICO	KELAC	10 mg comp.x 20	Richmond	25.02	1.668	\N	26/08/2015
734	53248	DICLOFENAC SODICO	FLEXIPLEN CAPSULA BLANDA	50 mg c ps.bl.x 10	Savant Generic	1825.58	121.70533	\N	15/12/2015
735	19873	DICLOFENAC SODICO	KELAC	10 mg comp.x 10	Richmond	12.6	0.84	\N	30/12/2016
736	33053	DICLOFENAC SODICO	MAGNESIO	comp.x 10	Nativa	12.6	0.84	\N	21/12/2015
737	31982	DICLOFENAC SODICO	DIOXAFLEX 50	50 mg c ps.blandas x 15	Bag	7112.16	474.144	\N	06/07/2015
738	2738	DICLOFENAC SODICO	METOCLOPRAMIDA DRAWER	10 mg a.x 6	Drawer	7.59	0.506	\N	14/11/2016
739	13000	DICLOFENAC SODICO	ZANTAC EFERVESCENTE	150 mg comp.x 30	GlaxoSmithKline	38	2.5333333	\N	16/03/2017
740	37056	DICLOFENAC SODICO	LORBITIDINA	300 mg comp.rec.x 30	Filaxis Farmac	38.51	2.5673332	\N	31/12/2016
741	42401	DICLOFENAC SODICO	DIOXAFLEX 50	50 mg c ps.blandas x 30	Bag	13203.51	880.234	\N	02/04/2020
742	32563	DICLOFENAC SODICO	APRICAL RANITIDINA	300 mg comp.rec.x 10	Adium	12.92	0.8613333	\N	01/03/2021
743	25846	DICLOFENAC SODICO	RANITIDI G.N.O.	300 mg comp.rec.x 10	Arion	13	0.8666667	\N	03/09/2022
744	25847	DICLOFENAC SODICO	RANITIDI G.N.O.	300 mg comp.rec.x 30	Arion	39	2.6	\N	30/10/2025
745	26617	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	fco.x 20 ml	Roux Ocefa	1.3	0.086666666	\N	23/09/2025
746	18505	DICLOFENAC SODICO	AGUA BIDESTILADA RIGO	a.x 3 x 10 ml	Rig	3.9	0.26	\N	29/12/2025
747	18513	DICLOFENAC SODICO	SOLUC.FISIOLOGICA RIGO	a.x 3 x 10 ml	Rig	3.9	0.26	\N	18/06/2024
748	32210	DICLOFENAC SODICO	AGUA OXIGENADA FLORIDA	10 vol.env.x 100 ml	Drog.Florida	1.3	0.086666666	\N	27/12/2025
749	47245	DICLOFENAC SODICO	XEDENOL CB	50 mg caps.bl.x 15	Baliarda	148.75	9.916667	\N	21/08/2025
750	25370	DICLOFENAC SODICO	SINALGICO SL	10 mg comp.subl.x 30	Laboratorios Be	39.72	2.648	\N	12/12/2025
751	47246	DICLOFENAC SODICO	XEDENOL CB	50 mg caps.bl.x 30	Baliarda	306.44	1.459238	\N	11/06/2007
752	3643	DICLOFENAC SODICO	VIZERUL	comp.x 60	Montpellier	79.79	2.6596668	\N	22/11/2004
753	8641	DICLOFENAC SODICO	ACIDEX	comp.rec.x 20	Teva Argentina	26.6	0.88666666	\N	26/08/2015
754	31067	DICLOFENAC SODICO	DICLAC	50 mg comp.cub.ent r.x10	Investi	11.6	0.38666666	\N	15/12/2015
755	19420	DICLOFENAC SODICO	AGUA BIDESTILADA BIOL	a.x 100 x 10 ml	Biol	133.08	4.436	\N	21/12/2015
756	25198	DICLOFENAC SODICO	URGIS	300 mg comp.x 30	Cetus	40	1.3333334	\N	06/07/2015
757	18507	DICLOFENAC SODICO	CLORURO DE SODIO RIGO	20% a.x 3 x 10 ml	Rig	4	0.13333334	\N	14/11/2016
758	22763	DICLOFENAC SODICO	MAGNESIO	tab.x 100	Natural Life	134.91	4.497	\N	21/07/2017
759	37654	DICLOFENAC SODICO	AGUA OXIGENADA	20 vol.x 100 ml	Zasu	1.35	0.045	\N	14/11/2016
760	25798	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 100 x 10 ml	Norgreen	135.44	4.5146666	\N	01/12/2020
761	30003	DICLOFENAC SODICO	DICLAC	50 mg comp.cub.ent r.x20	Investi	21.5	0.71666664	\N	27/06/2020
762	29185	DICLOFENAC SODICO	DICLAC	50 mg comp.dispers.x 20	Investi	15.95	0.5316667	\N	29/12/2025
763	18510	DICLOFENAC SODICO	SOLUC.GLUCOSADA HIPERTONICA RIGO	25% a.x 3 x 10 ml	Rig	4.1	0.13666667	\N	18/06/2024
764	10807	DICLOFENAC SODICO	TELUS	300 mg comp.x 30	Teva Argentina	41.02	1.3673333	\N	27/12/2025
765	4135	DICLOFENAC SODICO	GASTRIAL	150 mg comp.x 60	Sanofi-Aventis	82.3	2.7433333	\N	12/12/2025
766	42402	DICLOFENAC SODICO	DIOXAFLEX	50 mg comp.mast.x 10	Bag	65.19	2.173	\N	22/10/2025
767	16925	DICLOFENAC SODICO	RANITIDINA DENVER FARMA	150 mg comp.x 20	Denver Farma	27.56	0.05567677	\N	19/05/2006
768	42403	DICLOFENAC SODICO	DIOXAFLEX	50 mg comp.mast.x 100	Bag	258.14	0.51628	\N	16/09/2005
769	17865	DICLOFENAC SODICO	IMANOL	50 mg comp.rec.x 10	Biosintex	10.9	0.12111111	\N	24/10/2025
770	20252	DICLOFENAC SODICO	TOMAG	75 mg comp.x 10	Temis-Lostal	13.93	2.786	\N	08/04/2011
771	4134	DICLOFENAC SODICO	GASTRIAL	150 mg comp.x 30	Sanofi-Aventis	41.8	6.9666667	\N	18/01/2003
772	8645	DICLOFENAC SODICO	ACIDEX AP	comp.rec.x 50	Teva Argentina	69.79	17.4475	\N	18/08/2021
773	23359	DICLOFENAC SODICO	ORMIR	comp.x 10	Neuropharma	14	0.14	\N	01/08/2021
774	31626	DICLOFENAC SODICO	FURSEMIDA NORTHIA	40 mg comp.x 50	Northia	70.32	14.064	\N	24/11/2022
775	25305	DICLOFENAC SODICO	DISIPAN NF	50 mg comp.rec.x 10	Laboratorios Be	11.89	3.9633334	\N	24/11/2022
776	18894	DICLOFENAC SODICO	AGUA BIDESTILADA APIRETOGENA	a.x 50 x 10 ml	Welt	70.7	0.707	\N	19/04/2022
777	18897	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 50 x 10 ml	Welt	70.7	11.783334	\N	14/11/2025
778	41940	DICLOFENAC SODICO	LABSIDEX	150 mg comp.x 20	Labsa	28.38	4.73	\N	01/12/2025
779	28972	DICLOFENAC SODICO	AKTIOSAN	50 mg comp.rec.x 10	Investi	12.63	0.1263	\N	18/12/2023
780	31099	DICLOFENAC SODICO	NALGIFLEX	50 mg comp.rec.x 10	Ronnet	13.16	2.632	\N	19/08/2025
781	37655	DICLOFENAC SODICO	AGUA OXIGENADA	30 vol.x 100 ml	Zasu	1.45	0.29	\N	18/12/2025
782	11139	DICLOFENAC SODICO	RANITIDINA ILAB	300 mg comp.x 20	Inmunolab	29.23	9.743333	\N	18/12/2025
783	35788	DICLOFENAC SODICO	FLOGOLISIN	50 mg comp.rec.x 10	Lazar	16.42	3.284	\N	17/12/2025
784	35251	DICLOFENAC SODICO	DOXTRAN	50 mg comp.rec.x 10	Phoenix	34.08	0.1704	\N	22/10/2025
785	2555	DICLOFENAC SODICO	FUROSEMIDA KLONAL	20 mg a.x 6	Klonal	8.89	0.0889	\N	11/08/2025
786	24993	DICLOFENAC SODICO	KETOROLAC AHIMSA	comp.x 10	Fada Pharma	14.85	0.99	\N	28/02/2025
787	12999	DICLOFENAC SODICO	ZANTAC EFERVESCENTE	150 mg comp.x 10	GlaxoSmithKline	14.9	0.149	\N	02/07/2024
788	26779	DICLOFENAC SODICO	AGUA OXIGENADA PHARMA	10 vol.x 100 ml	Pharma del Plat	1.49	0.09933333	\N	08/12/2023
789	38094	DICLOFENAC SODICO	IGLODINE 50	50 mg comp.rec.x 10	Fecofar	77.12	5.141333	\N	27/12/2025
790	55690	DICLOFENAC SODICO	ACLOXIGENAC	50 mg comp.rec.x 10	Eczane	3138.09	209.206	\N	19/12/2025
791	26760	DICLOFENAC SODICO	SAL INGLESA PHARMA	pote x 40 g	Pharma del Plat	1.5	0.09375	\N	20/03/2024
792	26335	DICLOFENAC SODICO	METOCLOPRAMIDA EXPERIENTIA	0.5% gts.x 100 x 20 ml	Experientia	150	5	\N	08/12/2023
793	30524	DICLOFENAC SODICO	ULCOTENK	300 mg comp.rec.x 10	Biotenk	15	0.5	\N	27/12/2025
794	34934	DICLOFENAC SODICO	SALFIS	soluc.salina x 100 ml	Argenfarma	1.5	0.05	\N	13/03/2025
795	34315	DICLOFENAC SODICO	SOLUC.FISIOLOGICA ESTERIL	env.x 100 ml	Tetrafarm	1.5	0.1875	\N	20/03/2024
796	25593	DICLOFENAC SODICO	AGUA OXIGENADA	10 vol.env.x 100 ml	Fecofar	1.5	0.1	\N	14/11/2025
797	18508	DICLOFENAC SODICO	CLORURO DE SODIO RIGO	20% a.x 3 x 20 ml	Rig	4.5	0.3	\N	03/09/2025
798	18511	DICLOFENAC SODICO	SOLUC.GLUCOSADA HIPERTONICA RIGO	25% a.x 3 x 20 ml	Rig	4.5	0.45	\N	24/11/2010
799	30978	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	sachet x 100 ml	Pharma del Plat	1.5	0.15	\N	03/11/2015
800	33909	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PHARMA	fco.x 60 ml	Pharma del Plat	1.5	0.15	\N	01/11/2021
801	42337	DICLOFENAC SODICO	FENDIBINA	300 comp.rec.x 100	Northia	150.15	1.5015	\N	01/06/2003
802	32770	DICLOFENAC SODICO	METAFLEX 50	50 mg comp.rec.x 10	Montpellier	4137.3	206.865	\N	24/11/2010
803	36839	DICLOFENAC SODICO	DOXTRAN	50 mg comp.rec.x 100	Phoenix	87.94	4.397	\N	03/11/2015
804	45050	DICLOFENAC SODICO	GOBBICAINA	1% s/epi.a.x 1 x 5 ml	Gobbi	37.75	1.8875	\N	01/11/2021
805	46525	DICLOFENAC SODICO	FLOGOLISIN	50 mg comp.rec.x 100	Lazar	143.83	35.9575	\N	26/07/2012
806	43054	DICLOFENAC SODICO	DICLOFENAC NORTHIA	50 mg comp.rec.x 100	Northia	147.25	147.25	\N	11/04/2018
807	33861	DICLOFENAC SODICO	GASTRIAL	150 mg comp.x 20	Sanofi-Aventis	30.61	30.61	\N	11/05/2010
808	37163	DICLOFENAC SODICO	DICLOFENAC GP PHARM	50 mg comp.rec.x 15	Filaxis Farmac	17.23	1.723	\N	01/03/2005
809	26710	DICLOFENAC SODICO	AGUA DESTILADA BIOCROM	a.x 100 x 5 ml	Biocrom	155	7.75	\N	01/03/2005
810	36865	DICLOFENAC SODICO	DICLOFENAC GEN MED	50 mg comp.rec.x 15	Gen Med	17.3	1.73	\N	24/04/2015
811	25306	DICLOFENAC SODICO	DISIPAN NF	50 mg comp.rec.x 15	Laboratorios Be	17.75	0.8875	\N	27/07/2009
812	47483	DICLOFENAC SODICO	RANITIDINA PUNTANOS	300 mg comp.x 30	Laboratorios Pu	47	2.35	\N	12/12/2011
813	365	DICLOFENAC SODICO	SOLUC.FISIOLOGICA APOLO	a.x 1 x 5 ml	Apolo	1.57	0.0785	\N	24/04/2015
814	31838	DICLOFENAC SODICO	FADA MIDAZOLAM	15 mg comp.rec.x 30	Fada Pharma	47.16	4.716	\N	28/11/2013
815	30570	DICLOFENAC SODICO	FURSEMIDA BIOCROM	20 mg a.x 10	Biocrom	15.8	1.58	\N	08/04/2025
816	40686	DICLOFENAC SODICO	ESPAVEN FORTE	comp.rec.x 21	E. J. Gezzi	33.19	3.319	\N	08/04/2025
817	28977	DICLOFENAC SODICO	AINEDIF	50 mg comp.rec.x 15	Penn Pharmaceut	19.96	0.1996	\N	17/12/2019
818	18611	DICLOFENAC SODICO	KERARER	10 mg comp.x 10	LKM	15.83	1.0553334	\N	03/02/2014
819	8644	DICLOFENAC SODICO	ACIDEX AP	comp.rec.x 20	Teva Argentina	31.79	2.1193333	\N	08/04/2021
820	46118	DICLOFENAC SODICO	DICLOFENAC TECHSPHERE	50 mg comp.rec.x 15	Techsphere	23.87	1.5913334	\N	17/12/2019
821	27875	DICLOFENAC SODICO	DICLOFENAC HEXA	50 mg comp.rec.x 15	Fada Pharma	24.72	1.648	\N	16/09/2020
822	48140	DICLOFENAC SODICO	IBUXIM DICLO	50 mg comp.rec.x 15	Savant Consumer	49.69	3.3126667	\N	03/09/2025
823	19464	DICLOFENAC SODICO	AGUA DESTILADA APIROGENA	a.x 100 x 5 ml	Duncan	160	10.666667	\N	15/12/2025
824	55689	DICLOFENAC SODICO	ACLOXIGENAC	50 mg comp.rec.x 15	Eczane	3790.22	252.68134	\N	03/09/2025
825	32823	DICLOFENAC SODICO	RANIMED	150 mg comp.x 20	Lepetit	32.21	1.6105	\N	28/11/2013
826	36277	DICLOFENAC SODICO	DIFENAC	50 mg comp.rec.x 15	Lafedar	4122.32	137.41066	\N	16/09/2020
827	35858	DICLOFENAC SODICO	NALGIFLEX	50 mg comp.rec.x 15	Ronnet	4792	159.73334	\N	08/02/2022
828	341	DICLOFENAC SODICO	AGUA DESTILADA APOLO	a.x 1 x 5 ml	Apolo	1.62	0.054	\N	05/12/2022
829	17866	DICLOFENAC SODICO	IMANOL	50 mg comp.rec.x 20	Biosintex	19.63	0.65433335	\N	15/12/2025
830	45051	DICLOFENAC SODICO	GOBBICAINA	2% s/epi.a.x 1 x 5 ml	Gobbi	41.53	4.153	\N	15/09/2005
831	25307	DICLOFENAC SODICO	DISIPAN NF	50 mg comp.rec.x 20	Laboratorios Be	23.67	2.367	\N	10/06/2016
832	25819	DICLOFENAC SODICO	CLORURO DE POTASIO	20 mEq a.x 100 x 5 ml	Norgreen	166.8	16.68	\N	08/04/2025
833	35789	DICLOFENAC SODICO	FLOGOLISIN	50 mg comp.rec.x 20	Lazar	31.64	3.164	\N	19/12/2025
834	20399	DICLOFENAC SODICO	FURSEMIDA FABRA	iny.a.x 5	Fabra	8.42	0.0842	\N	06/05/2021
835	37055	DICLOFENAC SODICO	LORBITIDINA	300 mg comp.rec.x 10	Filaxis Farmac	16.9	1.1266667	\N	18/01/2003
836	35146	DICLOFENAC SODICO	DOXTRAN	50 mg comp.rec.x 20	Phoenix	41.79	2.786	\N	11/09/2013
837	37542	DICLOFENAC SODICO	HIERBAS DEL OASIS SUPLEMENTO DIETARIO	Magnesio blist.x15x10c/u	Hierbas del Oas	17	1.1333333	\N	05/12/2012
838	35194	DICLOFENAC SODICO	SILFOX	50 mg comp.rec.x 20	Teva Argentina	46.23	3.082	\N	19/12/2025
839	20694	DICLOFENAC SODICO	PRIMPERIL-METOCLOPRAMIDA	a.x 6	Lacefa	10.32	0.516	\N	05/02/2016
840	18614	DICLOFENAC SODICO	KERARER	20 mg comp.x 20	LKM	34.68	1.734	\N	06/05/2021
841	61838	DICLOFENAC SODICO	ACLOXIGENAC	50 mg comp.rec.x 20	Eczane	6119.2	305.96	\N	27/12/2025
842	3746	DICLOFENAC SODICO	SUSTAC	300 mg comp.x 30	Pfizer	52.35	2.6175	\N	19/12/2025
843	37164	DICLOFENAC SODICO	DICLOFENAC GP PHARM	50 mg comp.rec.x 30	Filaxis Farmac	27.6	0.92	\N	18/01/2003
844	2322	DICLOFENAC SODICO	ELIUR	iny.a.x 10 x 2 ml	Northia	17.49	0.583	\N	15/09/2005
845	342	DICLOFENAC SODICO	AGUA DESTILADA APOLO	a.x 1 x 10 ml	Apolo	1.77	0.059	\N	03/12/2014
846	26711	DICLOFENAC SODICO	AGUA DESTILADA BIOCROM	a.x 100 x 10 ml	Biocrom	178	5.9333334	\N	19/12/2025
847	8193	DICLOFENAC SODICO	GASTRIAL 300	300 mg comp.x 30	Sanofi-Aventis	53.43	1.33575	\N	06/09/2021
848	19876	DICLOFENAC SODICO	KELAC	20 mg comp.x 20	Richmond	35.79	35.79	\N	27/06/2014
849	37845	DICLOFENAC SODICO	TELEDOL	10 mg comp.x 10	Casasco	17.9	17.9	\N	18/12/2018
850	26336	DICLOFENAC SODICO	METOCLOPRAMIDA EXPERIENTIA	10 mg a.x 100 x 2 ml	Experientia	179	179	\N	27/12/2021
851	21265	DICLOFENAC SODICO	AGUA DESTILADA APIROGENA	a.x 100 x 10 ml	Duncan	180	180	\N	18/06/2024
852	19495	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 100 x 5 ml	Duncan	180	180	\N	15/12/2025
853	25308	DICLOFENAC SODICO	DISIPAN NF	50 mg comp.rec.x 30	Laboratorios Be	31.73	31.73	\N	31/10/2025
854	23728	DICLOFENAC SODICO	ATLAMAC	20 mg comp.x 20	Casasco	36.51	36.51	\N	15/12/2025
855	36866	DICLOFENAC SODICO	DICLOFENAC GEN MED	50 mg comp.rec.x 30	Gen Med	32.75	32.75	\N	02/10/2025
856	27583	DICLOFENAC SODICO	RANITIC	300 mg comp.x 30	Investi	55.07	55.07	\N	19/08/2025
857	28978	DICLOFENAC SODICO	AINEDIF	50 mg comp.rec.x 30	Penn Pharmaceut	33.64	1.682	\N	06/02/2002
858	19497	DICLOFENAC SODICO	SOLVENTE INDOLORO	1% a.x 100 x 5 ml	Duncan	190	190	\N	01/10/2025
859	7179	DICLOFENAC SODICO	AGUA DESTILADA	a.x 1 x 5 ml	Richmond	1.9	1.9	\N	13/05/2024
860	7284	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 1 x 5 ml	Richmond	1.9	0.076	\N	06/10/2025
861	46119	DICLOFENAC SODICO	DICLOFENAC TECHSPHERE	50 mg comp.rec.x 30	Techsphere	45.18	1.8072	\N	06/10/2025
862	27876	DICLOFENAC SODICO	DICLOFENAC HEXA	50 mg comp.rec.x 30	Fada Pharma	46.64	0.4664	\N	04/08/2025
863	24044	DICLOFENAC SODICO	FURIX	500 mg comp.x 20	Investi	38.86	0.3886	\N	01/12/2024
864	32771	DICLOFENAC SODICO	METAFLEX 50	50 mg comp.rec.x 30	Montpellier	146.8	1.468	\N	13/08/2025
865	40269	DICLOFENAC SODICO	MAGNESIUM PUSH	caja x 6 tubos	Laboratorio ENA	117	2.34	\N	29/10/2025
866	40270	DICLOFENAC SODICO	MAGNESIUM PUSH	tubo x 10 tab.	Laboratorio ENA	19.5	19.5	\N	18/01/2003
867	32211	DICLOFENAC SODICO	AGUA OXIGENADA FLORIDA	10 vol.env.x 250 ml	Drog.Florida	1.95	0.975	\N	19/08/2025
868	38095	DICLOFENAC SODICO	IGLODINE 50	50 mg comp.rec.x 30	Fecofar	179.64	35.928	\N	19/08/2025
869	26796	DICLOFENAC SODICO	SOLUC.FISIOLOGICA PHARMA	env.monods.x 100 ml	Pharma del Plat	1.97	1.97	\N	31/07/2013
870	43350	DICLOFENAC SODICO	LABSIDEX 300	300 mg comp.rec.x 20	Labsa	39.5	2.6333334	\N	23/09/2025
871	10726	DICLOFENAC SODICO	AGUA BIDESTILADA	iny.a.x 5 ml	Northia	1.98	1.98	\N	29/12/2025
872	44436	DICLOFENAC SODICO	NALGIFLEX	50 mg comp.rec.x 30	Ronnet	7785	7785	\N	16/08/2024
873	5740	DICLOFENAC SODICO	NOVOMIT	10 mg a.x 2	Klonal	3.97	3.97	\N	08/04/2025
874	19875	DICLOFENAC SODICO	KELAC	20 mg comp.x 10	Richmond	19.9	0.66333336	\N	03/07/2008
875	26060	DICLOFENAC SODICO	INDOFENO	50 mg comp.x 10	Fada Pharma	6.95	0.695	\N	01/12/2000
876	54696	DICLOFENAC SODICO	PEPSIPANCREOL	10 mg comp.x 20	Mar	40	2	\N	01/12/2000
877	41941	DICLOFENAC SODICO	LABSIDEX 300	300 mg comp.x 30	Labsa	60	60	\N	01/12/2005
878	31717	DICLOFENAC SODICO	HIOSCINA	a.x 100 x 2 ml	Veinfar	201	201	\N	28/11/2005
879	24988	DICLOFENAC SODICO	DICLOGRAND	50 mg comp.x 10	Fada Pharma	7.28	0.728	\N	01/02/2007
880	31610	ENOXAPARINA SODICA	KETOROLAC NORTHIA	10 mg comp.x 20	Northia	40.98	20.49	\N	11/11/2010
881	29494	ENOXAPARINA SODICA	DICLOFENAC PHARMA	50 mg comp.x 10	Pharma del Plat	8.58	0.858	\N	27/07/2010
882	37206	ENOXAPARINA SODICA	FLEXIPLEN	50 mg comp.x 10	Vitarum	8.65	4.325	\N	27/07/2010
883	501	ENOXAPARINA SODICA	GASTRIAL 300	300 mg comp.x 10	Sanofi-Aventis	20.79	20.79	\N	03/08/2010
884	10733	ENOXAPARINA SODICA	SOLUC.FISIOLOGICA	env.x 5 ml	Northia	2.08	1.04	\N	03/08/2010
885	30534	ENOXAPARINA SODICA	ZANTAC EFERVESCENTE	150 mg comp.x 24	GlaxoSmithKline	50.09	5.009	\N	03/08/2010
886	32292	ENOXAPARINA SODICA	FABOFLEM	50 mg comp.x 10	Fabop	9.25	0.925	\N	27/07/2010
887	2366	ENOXAPARINA SODICA	LIZARONA	Ni os gts.x 20 ml	Northia	2.1	1.05	\N	02/08/2012
888	2367	ENOXAPARINA SODICA	LIZARONA	Ni os gts.x 40 ml	Northia	2.1	1.05	\N	27/07/2010
889	12917	ENOXAPARINA SODICA	TOTAL MAGNESIANO	grag.x 60	Temis-Lostal	127.75	63.875	\N	03/08/2010
890	4029	ENOXAPARINA SODICA	ZANTAC	150 mg comp.x 60	GlaxoSmithKline	128.3	12.83	\N	03/08/2010
891	5755	ENOXAPARINA SODICA	GASTROZAC	300 mg comp.x 20	Klonal	42.87	4.287	\N	27/07/2010
892	26780	ENOXAPARINA SODICA	AGUA OXIGENADA PHARMA	10 vol.x 250 ml	Pharma del Plat	2.15	2.15	\N	03/08/2010
893	26127	ENOXAPARINA SODICA	KLONAFENAC	50 mg comp.x 10	Klonal	12.92	1.292	\N	03/08/2010
894	27468	ENOXAPARINA SODICA	GAVAC	75 mg comp.x 7	Gador	15.33	1.533	\N	27/07/2010
895	37826	ENOXAPARINA SODICA	RANITIDINA TECHSPHERE	300 mg comp.rec.x 30	Techsphere	66.2	66.2	\N	03/08/2010
896	18613	ENOXAPARINA SODICA	KERARER	20 mg comp.x 10	LKM	22.18	11.09	\N	03/08/2010
897	11885	ENOXAPARINA SODICA	ILIADIN	20 mg/2 ml a.x 100	Tuteur	222.43	22.243	\N	03/08/2010
898	12210	ENOXAPARINA SODICA	BUSCAPINA	a.x 5	Boehringer Inge	11.21	1.121	\N	10/12/2012
899	2404	ENOXAPARINA SODICA	FENDIBINA	150 mg comp.rec.x 20	Northia	45.09	4.509	\N	13/01/2015
900	31464	ENOXAPARINA SODICA	XYLOCAINA	1% a.x 5 x 5 ml	AstraZeneca	11.28	5.64	\N	02/03/2020
901	15814	ENOXAPARINA SODICA	COLOBOLINA	iny.a.x 5	Fabra	11.31	1.131	\N	13/03/2021
902	25826	ENOXAPARINA SODICA	SOLUC.DEXTROSA	25% a.x 100 x 10 ml	Norgreen	227.93	113.965	\N	13/03/2021
903	12916	ENOXAPARINA SODICA	TOTAL MAGNESIANO	grag.x 30	Temis-Lostal	68.64	6.864	\N	27/12/2017
904	16523	ENOXAPARINA SODICA	SOLUC.PARENT.1000 ML	agua bidest.	Rigecin	2.29	0.229	\N	12/12/2019
905	29323	ENOXAPARINA SODICA	FADA DICLOFENAC	50 mg comp.x 10	Fada Pharma	13.55	1.355	\N	12/12/2019
906	13891	ENOXAPARINA SODICA	CLORURO DE POTASIO	15 mEq iny.x 1	Fabra	2.3	0.23	\N	12/12/2019
907	343	ENOXAPARINA SODICA	AGUA DESTILADA APOLO	a.x 1 x 20 ml	Apolo	2.31	0.231	\N	12/12/2019
908	13650	ENOXAPARINA SODICA	XINA	50 mg comp.x 10	Finadiet	14.98	7.49	\N	30/09/2022
909	4968	ENOXAPARINA SODICA	RANITIDINA LAZAR	150 mg comp.x 50	Lazar	116.45	11.645	\N	13/08/2025
910	25594	ENOXAPARINA SODICA	AGUA OXIGENADA	10 vol.env.x 220 ml	Fecofar	2.33	0.233	\N	06/10/2025
911	47369	ENOXAPARINA SODICA	DICLOFENAC PUNTANOS	50 mg comp.x 10	Laboratorios Pu	15.5	1.55	\N	17/12/2025
912	27800	ENOXAPARINA SODICA	PAXYL	30 mg a.x 3 x 1 ml	Elvetium	7	0.7	\N	09/12/2025
913	4028	ENOXAPARINA SODICA	ZANTAC	150 mg comp.x 20	GlaxoSmithKline	46.8	4.68	\N	01/12/2025
914	26731	ENOXAPARINA SODICA	CLORURO DE POTASIO BIOCROM	15 mEq a.x 100	Biocrom	234.36	4.6872	\N	06/10/2025
915	9844	ENOXAPARINA SODICA	CONTROL K	caps.x 50	Elea (inactivo)	118.63	11.863	\N	13/08/2025
916	4967	ENOXAPARINA SODICA	RANITIDINA LAZAR	150 mg comp.x 20	Lazar	47.5	4.75	\N	06/10/2025
917	6575	ENOXAPARINA SODICA	ZANTAC	25mg/ml iny.IV a.x5 x2ml	GlaxoSmithKline	11.92	1.192	\N	30/12/2025
918	21091	ENOXAPARINA SODICA	RANITIDINA DRAWER	50 mg iny.x 6	Drawer	14.37	7.185	\N	06/10/2025
919	16524	ENOXAPARINA SODICA	SOLUC.PARENT.1000 ML	fisiol.isot.	Rigecin	2.4	1.2	\N	30/12/2025
920	3003	ENOXAPARINA SODICA	FURSEMIDA SINTESINA	20 mg iny.a.x 5 x 2 ml	Sintesina	12.02	1.202	\N	17/12/2025
921	13892	ENOXAPARINA SODICA	CLORURO DE POTASIO	20 mEq iny.x 1	Fabra	2.41	1.205	\N	17/12/2025
922	25800	ENOXAPARINA SODICA	SOLUC.HIPERTONICA CLORURO DE SODIO	20% a.x 100 x 10 ml	Norgreen	241.14	24.114	\N	01/10/2025
923	27481	ENOXAPARINA SODICA	ONDANSETRON CEVALLOS	8 mg iny.a.x 100 x 4 ml	Cevallos	242	24.2	\N	09/12/2025
924	30322	ENOXAPARINA SODICA	ULCOTENK	150 mg comp.rec.x 20	Biotenk	48.57	4.857	\N	01/12/2025
925	39048	ENOXAPARINA SODICA	DOLOFENAC 50	50 mg comp.x 10	Sanitas	93	46.5	\N	01/12/2025
926	31609	ENOXAPARINA SODICA	KETOROLAC NORTHIA	10 mg comp.x 10	Northia	24.57	0.4914	\N	06/10/2025
927	15255	ENOXAPARINA SODICA	SOLUC.PARENT.100 ML	fisiol.clor.sodio	Apolo	2.46	0.246	\N	13/08/2025
928	36365	ENOXAPARINA SODICA	ALGIOXIB	50 mg comp.x 10	Ferring	98.14	9.814	\N	06/10/2025
929	50709	ENOXAPARINA SODICA	GASTROSEDOL	150 mg comp.x 10	Nova Argentia	24.9	2.49	\N	30/12/2025
930	34935	ENOXAPARINA SODICA	SALFIS	soluc.salina x 250 ml	Argenfarma	2.5	0.25	\N	17/12/2025
931	38416	ENOXAPARINA SODICA	VESALION	50 mg comp.x 100	Nova Argentia	100.75	10.075	\N	01/10/2025
932	15633	ENOXAPARINA SODICA	SOLUC.FISIOLOGICA VEINFAR	iny.x 100 x 20 ml	Veinfar	253	25.3	\N	13/08/2025
933	33476	ENOXAPARINA SODICA	BLOKIUM	50 mg comp.x 100	Casasco	455.8	45.58	\N	06/10/2025
934	1969	ENOXAPARINA SODICA	LUVIER	150 mg comp.x 60	Casasco	152.27	15.227	\N	09/12/2025
935	5750	ENOXAPARINA SODICA	GASTROZAC	50 mg a.x 6	Klonal	15.24	1.524	\N	01/12/2025
936	366	ENOXAPARINA SODICA	SOLUC.FISIOLOGICA APOLO	a.x 1 x 10 ml	Apolo	2.55	0.255	\N	30/12/2025
937	31335	ENOXAPARINA SODICA	XINA	50 mg comp.x 15	Finadiet	14.11	1.411	\N	17/12/2025
938	31891	ENOXAPARINA SODICA	FLOGENAC	50 mg comp.x 15	Adium	15.25	1.525	\N	13/08/2025
939	31465	ENOXAPARINA SODICA	XYLOCAINA	2% a.x 5 x 5 ml	AstraZeneca	12.88	1.288	\N	01/10/2025
940	15604	ENOXAPARINA SODICA	DICLOFENAC SODICO RICHET	50 mg comp.x 15	Richet	20.8	2.08	\N	09/12/2025
941	30572	ENOXAPARINA SODICA	CLORURO DE POTASIO BIOCROM	15 mEq a.x 1	Biocrom	2.6	0.26	\N	01/12/2025
942	1121	FENTANILO	BIOMAG	gran.sob.x 15	Baliarda	39.09	39.09	\N	04/07/2011
943	25799	FENTANILO	SOLUC.FISIOLOGICA	a.x 100 x 20 ml	Norgreen	260.96	260.96	\N	30/09/2013
944	15256	FENTANILO	SOLUC.PARENT.100 ML	isot.dext.5% en agua	Apolo	2.61	2.61	\N	10/11/2015
945	37652	FENTANILO	AGUA OXIGENADA	10 vol.x 100 ml	Zasu	2.62	0.0262	\N	10/11/2015
946	5310	FENTANILO	CONTROL K	caps.x 20	Elea (inactivo)	52.41	52.41	\N	04/05/2015
947	40687	FENTANILO	ESPAVEN EXTRA FORTE	comp.rec.x 21	E. J. Gezzi	55.39	55.39	\N	19/08/2016
948	18417	FENTANILO	BANOCLUS	50 mg comp.x 15	Lepetit	21.3	4.26	\N	02/04/2007
949	15666	FENTANILO	LIDOCAINA	2% f.a.x 5 ml s/epi.	Apolo	2.65	2.65	\N	16/06/2017
950	23815	FENTANILO	SOLVENTE INDOLORO APOLO	a.x 1 x 5 ml	Apolo	2.65	0.53	\N	01/09/2007
951	45063	FENTANILO	KETOROLAC NORTHIA	10 mg comp.subl.x 10	Northia	26.75	0.535	\N	11/11/2019
952	2456	FENTANILO	LIZARONA	iny.a.x 3 x 2 ml	Northia	8.06	1.612	\N	04/07/2011
953	2476	FENTANILO	LIZARONA	iny.a.x 6 x 2 ml	Northia	16.12	3.224	\N	18/01/2003
954	8643	FENTANILO	ACIDEX	iny.a.x 6	Teva Argentina	16.16	3.232	\N	04/07/2011
955	38137	FENTANILO	DICLOFENAC NORTHIA	50 mg comp.x 15	Northia	23.94	7.98	\N	04/12/2020
956	31867	FENTANILO	VIROBRON NF	50 mg comp.x 15	Temis-Lostal	28.74	1.0264286	\N	27/06/2020
957	5691	FENTANILO	CLORURO DE POTASIO	15 mEq a.x 6 x 5 ml	Klonal	16.79	0.5996429	\N	22/05/2021
958	25683	FENTANILO	KETOROLAC ASOFARMA	10 mg comp.subl.x 10	Asofarma	28	0.28	\N	05/11/2021
959	39298	FENTANILO	DICLOFENAC SANT GALL	50 mg comp.x 15	Sant Gall	41.54	0.8308	\N	05/11/2021
960	22920	FENTANILO	CLORURO DE POTASIO DENVER FARMA	15 mEq a.x 5 ml	Denver Farma	2.82	0.564	\N	28/03/2019
961	22930	FENTANILO	GLUCOSA HIPERTONICA DF	25% a.x 1 x 10 ml	Denver Farma	2.82	0.564	\N	28/03/2019
962	35221	FENTANILO	VIARTRIL NF	50 mg comp.x 15	Spedrog Caillon	44.06	8.812	\N	17/06/2025
963	2250	FENTANILO	VOLTAREN	50 mg comp.x 15	Novartis	49.7	9.94	\N	28/03/2019
964	30975	FENTANILO	MAGNESIO CLORURO	pote x 33 g	Pharma del Plat	2.86	0.102142856	\N	01/12/2025
965	29180	FENTANILO	GASTROLETS 300	300 mg comp.rec.x 20	Fada Pharma	57.4	0.574	\N	30/04/2024
966	10285	FENTANILO	TOTAL MAGNESIANO EFERVESCENTE	pvo.sob.x 48	Temis-Lostal	138.89	1.3889	\N	11/08/2025
967	12356	FENTANILO	CELIT	a.x 100 x 2 ml	Fada Pharma	290	29	\N	02/01/2024
968	32911	FENTANILO	IRIX SOLUCION SALINA	env.x 35 ml	Gram n	2.9	0.029	\N	11/08/2025
969	13267	FENTANILO	SOLUC.PARENT.100 ML	dext.5% en agua	Fidex	2.9	0.58	\N	17/06/2025
970	35386	FENTANILO	DICLONEX 50	50 mg comp.x 15	Nexo Pharmaceut	57	0.57	\N	02/07/2024
971	12379	FENTANILO	VIAFUROX	a.x 100 x 2 ml	Fada Pharma	293.55	10.483929	\N	01/12/2025
972	30266	FENTANILO	VESALION	50 mg comp.x 15	Nova Argentia	225.97	8.070357	\N	01/12/2025
973	35539	FENTANILO	DOLVAN	50 mg comp.x 15	Gador	798.09	39.9045	\N	01/11/2024
974	28568	FENTANILO	AGUA INYECTABLE BP	a.pl st.x 20 x 20 ml	B. Braun	58.9	11.78	\N	05/02/2025
975	28571	FENTANILO	CLORURO DE SODIO 0.9% BP	a.pl st.x 20 x 20 ml	B. Braun	58.9	1.178	\N	12/12/2025
976	15618	FENTANILO	AGUA DESTILADA	a.x 100 x 20 ml	Veinfar	295	11.8	\N	06/10/2025
977	46486	FENTANILO	DICLOLAM 50	50 mg comp.x 15	Austral	5210	208.4	\N	06/10/2025
978	21112	FENTANILO	DIASTONE	50 mg comp.x 15	Microsules Arg.	5836	5836	\N	25/07/2025
979	6979	FENTANILO	FONDERYL	comp.x 20	Megalabs Argent	59.37	1.1874	\N	29/10/2025
980	7242	FENTANILO	FURSEMIDA	20 mg a.x 1 x 2 ml	Richmond	2.99	0.0598	\N	13/08/2025
981	363	FENTANILO	SOLUC.CLORURO POTASIO	a.x 5 ml	Apolo	2.99	0.598	\N	09/12/2025
982	37208	FENTANILO	FLEXIPLEN	50 mg comp.x 150	Vitarum	63	12.6	\N	11/12/2025
983	36538	FENTANILO	SOLVENTE INDOLORO NORTHIA	50 mg iny.a.x 100 x 5 ml	Northia	300	60	\N	09/12/2025
984	12334	FENTANILO	SOLVENTE INDOLORO NORTHIA	a.x 5 ml	Northia	3	0.6	\N	11/12/2025
985	7285	FLUMAZENIL	SOLUC.FISIOLOGICA	a.x 1 x 10 ml	Richmond	3.03	3.03	\N	19/05/2017
986	3055	FLUMAZENIL	SOLUC.PARENT.500 ML	fisiol.isot.0.85%	Rigecin	3.08	0.616	\N	11/02/2002
987	10284	FLUMAZENIL	TOTAL MAGNESIANO EFERVESCENTE	pvo.sob.x 24	Temis-Lostal	74.18	2.9672	\N	26/04/2002
988	13651	FLUMAZENIL	XINA	50 mg comp.x 20	Finadiet	16.49	0.1649	\N	05/03/2003
989	10729	FLUMAZENIL	CLORURO DE POTASIO	15 mEq a.x 5 ml	Northia	3.1	3.1	\N	18/01/2003
990	25595	FLUMAZENIL	AGUA OXIGENADA	10 vol.env.x 440 ml	Fecofar	3.1	0.62	\N	13/07/2004
991	109	FLUMAZENIL	SOLUC.PARENT.500 ML	agua bidest.	Rigecin	3.12	0.624	\N	28/03/2014
992	24586	FLUMAZENIL	LARJANCAINA CON EPINEFRINA	1% a.x 100 x 5 ml	Veinfar	313	62.6	\N	06/09/2012
993	26128	FLUMAZENIL	KLONAFENAC	50 mg comp.x 20	Klonal	17.66	17.66	\N	23/08/2019
994	32824	FLUMAZENIL	RANIMED	300 mg comp.x 30	Lepetit	94.15	1.883	\N	16/09/2022
995	367	FLUMAZENIL	SOLUC.FISIOLOGICA APOLO	a.x 1 x 20 ml	Apolo	3.14	0.1256	\N	06/10/2025
996	3458	FLUMAZENIL	SOLVENTE INDOLORO FADA	a.x 1 x 5 ml	Fada Pharma	3.15	0.063	\N	06/10/2025
997	29324	FLUMAZENIL	FADA DICLOFENAC	50 mg comp.x 20	Fada Pharma	24.39	0.4878	\N	29/10/2025
998	24587	FLUMAZENIL	LARJANCAINA	2% a.x 100 x 5 ml	Veinfar	317	12.68	\N	15/09/2025
999	24588	FLUMAZENIL	LARJANCAINA CON EPINEFRINA	2% a.x 100 x 5 ml	Veinfar	317	63.4	\N	20/12/2025
1000	14651	FUROSEMIDA	AGUA DESTILADA	iny.x 1	Fabra	3.17	0.0634	\N	01/02/2002
1001	44734	FUROSEMIDA	DICLOFENAC 50 MG PUNTANOS	50 mg comp.x 20	Laboratorios Pu	30.15	0.603	\N	01/12/2000
1002	18841	FUROSEMIDA	DICLOFENAC DENVER FARMA	50 mg comp.x 20	Denver Farma	56.76	0.11352	\N	13/08/1996
1003	45062	FUROSEMIDA	KETOROLAC NORTHIA	20 mg comp.rec.x 20	Northia	64.32	1.072	\N	16/07/2003
1004	8535	FUROSEMIDA	ZANTAC	300 mg comp.x 10	GlaxoSmithKline	32.27	0.80675	\N	06/08/2004
1005	49027	FUROSEMIDA	VOLTAREN	50 mg comp.x 20	Novartis	75.73	2.5243332	\N	16/07/2003
1006	25831	FUROSEMIDA	SOLUC.DEXTROSA	50% a.x 100 x 20 ml	Norgreen	323.72	5.3953333	\N	01/07/2004
1007	32546	FUROSEMIDA	AQUA LENT SOLUCION SALINA FISIOLOGICA	Especial p/len.cont.x35m	Inmunolab	3.25	0.108333334	\N	01/07/2004
1008	36366	FUROSEMIDA	ALGIOXIB	50 mg comp.x 20	Ferring	149.7	7.485	\N	18/07/1995
1009	35387	FUROSEMIDA	DICLONEX 50	50 mg comp.x 30	Nexo Pharmaceut	19.9	0.995	\N	01/07/2002
1010	3040	FUROSEMIDA	SOLUC.PARENT.500 ML	dext.5% sol.fis.	Rigecin	3.27	0.0654	\N	18/07/1995
1011	30593	FUROSEMIDA	RETEP	40 mg comp.x 50	Biosintex Retai	164	8.2	\N	18/01/2003
1012	37207	FUROSEMIDA	FLEXIPLEN	50 mg comp.x 30	Vitarum	22.6	0.452	\N	01/09/2005
1013	31892	FUROSEMIDA	FLOGENAC	50 mg comp.x 30	Adium	22.87	0.4574	\N	18/01/2003
1014	40712	FUROSEMIDA	RETEP	20 mg a.x 100 x 2 ml	Fada Pharma	331.97	6.6394	\N	16/09/2002
1015	24995	FUROSEMIDA	KETOROLAC AHIMSA	iny.a.x 3 x 1 ml	Fada Pharma	9.98	0.2495	\N	01/02/2005
1016	27145	FUROSEMIDA	TENKDOL	30 mg a.x 3 x 1 ml	Biotenk	10	0.2	\N	05/09/2005
1017	24989	FUROSEMIDA	DICLOGRAND	50 mg comp.x 30	Fada Pharma	25.88	1.294	\N	18/01/2003
1018	376	FUROSEMIDA	SOLUC.PARENT.250 ML	fisiol.clor.sodio	Apolo	3.37	0.1685	\N	25/11/2011
1019	16520	FUROSEMIDA	XYLOCAINA	1% env.Polyamp.x 5 x 5ml	AstraZeneca	16.86	0.281	\N	30/09/2013
1020	14652	FUROSEMIDA	SOLUC.FISIOLOGICA	iny.x 1	Fabra	3.38	0.0676	\N	24/04/2013
1021	3043	FUROSEMIDA	SOLUC.PARENT.500 ML	dext.10% sol.fis.	Rigecin	3.38	0.0338	\N	13/06/2000
1022	8466	FUROSEMIDA	DESINFLAM	50 mg comp.x 30	Pfizer	30.3	0.606	\N	01/12/2013
1023	15605	FUROSEMIDA	DICLOFENAC SODICO RICHET	50 mg comp.x 30	Richet	36.04	0.7208	\N	10/07/2003
1024	22928	FUROSEMIDA	FUROSEMIDA DENVER FARMA	20 mg a.x 1 x 2 ml	Denver Farma	3.45	0.1725	\N	30/09/2013
1025	7756	FUROSEMIDA	METOCLOPRAMIDA	10 mg a.x 1 x 2 ml	Richmond	3.45	0.1725	\N	01/12/2005
1026	37661	FUROSEMIDA	SOLUC.FISIOLOGICA	env.x 100 ml	Zasu	3.45	0.575	\N	15/08/2002
1027	41046	FUROSEMIDA	BLOCADOL	10 mg comp.rec.x 20	Teva Argentina	69.68	0.6968	\N	25/04/2002
1028	29179	FUROSEMIDA	GASTROLETS 150	150 mg comp.rec.x 20	Lab Internacion	69.77	0.6977	\N	15/08/2000
1029	26164	FUROSEMIDA	DICLOFENAC NORTHIA	50 mg comp.x 30	Northia	46.84	0.9368	\N	26/08/2015
1030	26781	FUROSEMIDA	AGUA OXIGENADA PHARMA	10 vol.x 500 ml	Pharma del Plat	3.55	0.59166664	\N	01/02/2003
1031	24590	FUROSEMIDA	LARJANCAINA CON EPINEFRINA	1% a.x 100 x 20 ml	Veinfar	360	36	\N	28/06/2002
1032	36319	FUROSEMIDA	DOLONEITOR PLATINO	50 mg comp.x 30	Driburg	55	11	\N	30/09/2013
1033	19536	FUROSEMIDA	CLORURO DE SODIO	20% a.x 100 x 5 ml	Veinfar	362	36.2	\N	03/04/2002
1034	36539	FUROSEMIDA	LIZARONA	10 mg iny.a.x 100 x 2 ml	Northia	363	18.15	\N	18/01/2003
1035	39299	FUROSEMIDA	DICLOFENAC SANT GALL	50 mg comp.x 30	Sant Gall	74.27	0.7427	\N	05/09/2005
1036	21618	FUROSEMIDA	ORAKIT 15 SAFEJET	iny.jga.x 50 x 5 ml	Fada Pharma	182.25	36.45	\N	01/07/2002
1037	29367	FUROSEMIDA	FADA RANITIDINA/INSUFLEN FADAJET	50 mg jga.prell.x 50x5ml	Fada Pharma	182.25	1.8225	\N	21/04/2008
1038	3422	FUROSEMIDA	INSUFLEN	a.x 100 x 5 ml	Fada Pharma	364.5	364.5	\N	28/01/2003
1039	21611	FUROSEMIDA	INSUFLEN FADAJET	jga.prell.x 50 x 5 ml	Fada Pharma	182.25	182.25	\N	04/07/2007
1040	7184	FUROSEMIDA	AGUA DESTILADA	a.x 1 x 10 ml	Richmond	3.67	0.0734	\N	28/02/2018
1041	46948	FUROSEMIDA	MIDALAN	7.5 mg comp.x 20	Lafedar	74	74	\N	04/05/2015
1042	32622	FUROSEMIDA	SULFATO DE MAGNESIO DRAWER	25% a.x 50 x 5 ml	Drawer	185.9	4.131111	\N	12/11/2018
1043	35222	FUROSEMIDA	VIARTRIL NF	50 mg comp.x 30	Spedrog Caillon	88.13	1.4688333	\N	23/10/2017
1044	41440	FUROSEMIDA	FENDIBINA	300 comp.rec.x 30	Northia	112.45	2.81125	\N	10/09/2018
1045	9619	FUROSEMIDA	KEMANAT	30 mg a.x 3 x 1 ml	Finadiet	11.26	0.1126	\N	04/11/2008
1046	12371	FUROSEMIDA	ORAKIT 20	a.x 100 x 5 ml	Fada Pharma	375.44	7.5088	\N	26/04/2002
1047	35540	FUROSEMIDA	DOLVAN	50 mg comp.x 30	Gador	88.81	88.81	\N	20/01/2003
1048	7310	FUROSEMIDA	SOLVENTE INDOLORO	a.x 1 x 5 ml	Richmond	3.76	0.0752	\N	22/10/2021
1049	377	FUROSEMIDA	SOLUC.PARENT.250 ML	isot.dext.5% en agua	Apolo	3.77	0.0754	\N	09/02/2024
1050	28967	FUROSEMIDA	PASMOVIT	iny.a.x 6	Finadiet	22.63	0.2263	\N	12/08/2021
1051	22931	FUROSEMIDA	GLUCOSA HIPERTONICA DF	50% a.x 1 x 10 ml	Denver Farma	3.78	0.378	\N	31/03/2022
1052	2251	FUROSEMIDA	VOLTAREN	50 mg comp.x 30	Novartis	88.86	88.86	\N	21/10/2021
1053	14265	FUROSEMIDA	VESALION	50 mg comp.x 30	Nova Argentia	353.26	3.5326	\N	11/04/2022
1054	49765	FUROSEMIDA	KETOROLAC FABRA	10 mg comp.x 30	Fabra	113.86	3.7953334	\N	01/06/2024
1055	24589	FUROSEMIDA	LARJANCAINA	1% a.x 100 x 20 ml	Veinfar	384	7.68	\N	20/12/2025
1056	24591	FUROSEMIDA	LARJANCAINA	2% a.x 100 x 20 ml	Veinfar	384	12.8	\N	29/12/2025
1057	24592	FUROSEMIDA	LARJANCAINA CON EPINEFRINA	2% a.x 100 x 20 ml	Veinfar	384	7.68	\N	01/01/2026
1058	34443	FUROSEMIDA	DUALID	50 mg a.x 5 x 5 ml	Duncan	19.4	0.0194	\N	19/11/2025
1059	31731	FUROSEMIDA	GOBBICAINA	1% PPP a.x 4 x 5 ml	Gobbi	15.56	0.5186667	\N	02/12/2025
1060	26792	FUROSEMIDA	LIMONADA ROGE PHARMA	Inf.fco.x 25 g	Pharma del Plat	3.89	0.0778	\N	12/12/2025
1061	2452	FUROSEMIDA	FENDIBINA	50 mg iny.a.x 5	Northia	19.48	0.3896	\N	01/12/2025
1062	49028	FUROSEMIDA	VOLTAREN	50 mg comp.x 40	Novartis	135.41	4.5136666	\N	01/12/2025
1063	26988	FUROSEMIDA	TENKDOL	30 mg a.x 1 x 1 ml	Biotenk	3.9	0.065	\N	01/12/2025
1064	32912	FUROSEMIDA	IRIX SOLUCION SALINA	env.x 500 ml	Gram n	3.9	3.9	\N	13/05/2024
1065	6849	FUROSEMIDA	SOLUC.PARENT.100 ML	bicarb.sodio al 7%	Roux Ocefa	3.91	0.0391	\N	02/07/2024
1066	16521	FUROSEMIDA	XYLOCAINA	2% env.Polyamp.x 5 x 5ml	AstraZeneca	19.65	0.1965	\N	11/08/2025
1067	38296	FUROSEMIDA	DICLOFENAC NORTHIA	50 mg comp.x 495	Northia	495	4.95	\N	23/10/2025
1068	29325	FUROSEMIDA	FADA DICLOFENAC	50 mg comp.x 500	Fada Pharma	347.5	3.475	\N	13/08/2025
1069	17197	FUROSEMIDA	NOTRAB	50 mg iny.a.x 6 x 5 ml	Microsules Arg.	24.15	0.2415	\N	01/01/2025
1070	373	FUROSEMIDA	SOLUC.PARENT.100 ML	bicarb.sod.sol.molar	Apolo	4.05	0.405	\N	02/07/2024
1071	375	HIDROCORTISONA	SOLUC.PARENT.100 ML	clor.pot.sol.molar	Apolo	4.05	0.2025	\N	09/02/2002
1072	378	HIDROCORTISONA	SOLUC.PARENT.250 ML	dext.10% en agua	Apolo	4.1	0.13666667	\N	18/01/2003
1073	22460	HIDROCORTISONA	KETOROLAC NORTHIA	30 mg a.x 3 x 1 ml	Northia	12.38	1.5475	\N	18/01/2003
1074	22461	HIDROCORTISONA	KETOROLAC NORTHIA	30 mg a.x 6 x 1 ml	Northia	24.77	0.82566667	\N	30/09/2013
1075	25827	HIDROCORTISONA	SOLUC.DEXTROSA	25% a.x 100 x 20 ml	Norgreen	412.91	412.91	\N	06/11/2000
1076	25833	HIDROCORTISONA	SOLUC.DEXTROSA	50% a.x 100 x 25 ml	Norgreen	412.91	412.91	\N	30/01/2003
1077	3587	HIDROCORTISONA	SOLUC.PARENT.250 ML	dext.5% en agua	Fidex	4.17	0.0417	\N	11/07/1996
1078	26059	HIDROCORTISONA	INDOFENO	50 mg comp.x 500	Fada Pharma	347.5	347.5	\N	30/06/2017
1079	7264	HIDROCORTISONA	POTASIO CLORURO	15 mEq a.x 1 x 5 ml	Richmond	4.28	0.0856	\N	06/12/2006
1080	9460	HIDROCORTISONA	ZANTAC	300 mg comp.x 30	GlaxoSmithKline	128.69	128.69	\N	28/06/2002
1081	25801	HIDROCORTISONA	SOLUC.HIPERTONICA CLORURO DE SODIO	20% a.x 100 x 20 ml	Norgreen	436.04	436.04	\N	03/04/2002
1082	20254	HIDROCORTISONA	TOMAG	dispenser comp.x 10 x 14	Temis-Lostal	61.3	1.226	\N	10/07/2003
1083	19535	HIDROCORTISONA	CLORURO DE POTASIO	20 mEq x 100 x 5 ml	Veinfar	440	440	\N	20/11/2008
1084	28966	HIDROCORTISONA	PASMOVIT	iny.a.x 3	Finadiet	13.25	13.25	\N	01/12/2001
1085	358	HIDROCORTISONA	SOLUC.CLORURADA HIPERTONICA	20% a.x 10 ml	Apolo	4.42	0.0442	\N	25/04/2002
1086	10447	HIDROCORTISONA	NURIBAN	25 mg comp.x 45	Roux Ocefa	199.18	199.18	\N	06/12/2006
1087	31732	HIDROCORTISONA	GOBBICAINA	2% PPP a.x 4 x 5 ml	Gobbi	17.8	17.8	\N	20/02/2002
1088	23729	HIDROCORTISONA	ATLAMAC	30 mg a.x 3 x 1 ml	Casasco	13.39	13.39	\N	28/01/2003
1089	36544	HIDROCORTISONA	DICLOFENAC NORTHIA	50 mg comp.x 500	Northia	415	415	\N	01/08/2005
1090	31105	HIDROCORTISONA	DICLOFENAC ALL PRO	50 mg comp.x 500	All Pro Salud	550.74	550.74	\N	01/02/2003
1091	22459	HIDROCORTISONA	KETOROLAC NORTHIA	30 mg a.x 1 x 1 ml	Northia	4.5	4.5	\N	30/09/2013
1092	18515	HIDROCORTISONA	LIDOCAINA	1% s/epi.iny.f.a.x 25 ml	Rig	4.5	4.5	\N	30/01/2003
1093	32623	HIDROCORTISONA	VOLTAREN	50 mg comp.x 80	Novartis	136.77	2.7354	\N	06/12/2006
1094	23970	HIDROCORTISONA	DIOXAFLEX RAPID	50 mg gran.sob.x20	Bag	35492.75	35492.75	\N	06/12/2006
1095	22635	HIDROCORTISONA	AKTIOSAN	50 mg tab.rec.x 10	Investi	7.7	7.7	\N	20/02/2003
1096	30222	HIDROCORTISONA	FUROSEMIDA DENVER FARMA	40 mg comp.x 60	Denver Farma	276.01	276.01	\N	25/03/2002
1097	10603	HIDROCORTISONA	RANITIDINA LAZAR	a.x 3	Lazar	14	14	\N	28/06/2002
1098	24561	HIDROCORTISONA	NOLARAC	30 mg iny.a.x 100 x 1 ml	Fada Pharma	467	467	\N	03/04/2002
1099	26381	HIDROCORTISONA	AKTIOSAN	50 mg tab.rec.x 10 x 24	Investi	184.8	1.848	\N	04/11/2008
1100	29058	HIDROCORTISONA	AKTIOSAN	50mg rapid.comp.disp.x20	Investi	21.56	21.56	\N	27/10/2003
1101	31663	HIDROCORTISONA	LIGNOCAINA GRAY	1% a.x 5 ml	Gray	4.72	4.72	\N	31/01/2008
1102	18616	HIDROCORTISONA	KERARER	30 mg iny.a.x 5 x 1 ml	LKM	23.98	23.98	\N	28/01/2003
1103	31664	HIDROCORTISONA	LIGNOCAINA GRAY	2% a.x 5 ml	Gray	4.8	4.8	\N	20/11/2008
1104	27428	HIDROCORTISONA	METOCLOPRAMIDA SHABBA	0.2% Ni os gts.x 20 ml	Shabba	4.8	4.8	\N	21/04/2009
1105	7265	HIDROCORTISONA	POTASIO CLORURO	20 mEq a.x 1 x 5 ml	Richmond	4.81	4.81	\N	19/01/2007
1106	26793	HIDROCORTISONA	LIMONADA ROGE PHARMA	Ad.fco.x 50 g	Pharma del Plat	4.87	4.87	\N	30/09/2013
1107	25208	HIDROCORTISONA	XEDENOL	50mgcomp.rec.gastror.x15	Baliarda	7433.17	7433.17	\N	01/01/2004
1108	25822	HIDROCORTISONA	SOLUC.DEXTROSA	5% PVC/Norfl.x 50 x100ml	Norgreen	244.34	244.34	\N	09/08/2007
1109	25209	HIDROCORTISONA	XEDENOL	50mgcomp.rec.gastror.x30	Baliarda	11390.41	11390.41	\N	19/01/2007
1110	7193	HIDROCORTISONA	AGUA DESTILADA	a.x 1 x 20 ml	Richmond	4.89	4.89	\N	18/01/2003
1111	39464	HIDROCORTISONA	XEDENOL	50mgcomp.rec.gastrorx100	Baliarda	83.27	0.8327	\N	24/06/2010
1112	20181	HIDROCORTISONA	KELAC	30 mg a.x 3 x 2 ml	Richmond	14.68	14.68	\N	19/03/2016
1113	22894	HIDROCORTISONA	SOLUC.PARENT.FLEXIBLES	dext.10% sol.x 250 ml	Baxter Argentin	4.9	4.9	\N	05/03/2014
1114	37653	HIDROCORTISONA	AGUA OXIGENADA	10 vol.x 250 ml	Zasu	4.9	4.9	\N	30/09/2013
1115	11461	HIDROCORTISONA	MINITRAN	5 mg parches x 30	3 M	150.07	150.07	\N	08/04/2017
1116	32487	HIDROCORTISONA	FABOFLEM	iny.a.x 6 x 3 ml	Fabop	14	14	\N	03/09/2014
1117	13305	HIDROCORTISONA	GASTROSEDOL	50 mg iny.a.x 5	Nova Argentia	25.34	25.34	\N	03/09/2014
1118	29782	HIDROCORTISONA	LIMONADA ROGE PAGLIANO	env.x 100 g	Lacefa	5.07	5.07	\N	01/06/2020
1119	31983	HIDROCORTISONA	FADA KETOROLAC/NOLARAC	30 mg a.x 1 x 1 ml	Fada Pharma	5.1	5.1	\N	11/06/2018
1120	36270	HIDROCORTISONA	METOCLOPRAMIDA LEMAX	iny.a.x 3 x 2 ml	Lemax	15.3	0.612	\N	17/06/2020
1121	12351	HIDROCORTISONA	AGUA PARA INYECCION	a.x 50 x 20 ml	Fada Pharma	255.15	255.15	\N	03/05/2019
1122	12374	HIDROCORTISONA	SOLUC.FISIOLOGICA	3 mEq a.x 50 x 20 ml	Fada Pharma	255.15	255.15	\N	04/11/2019
1123	25438	HIDROCORTISONA	KETOROLAC AHIMSA	iny.a.x 1 x 1 ml	Fada Pharma	5.12	0.17066666	\N	30/10/2025
1124	29988	HIDROCORTISONA	SOLUC.PARENT.500 ML APIROFLEX	fisiol.clor.sodio	Roux Ocefa	5.14	0.17133333	\N	17/09/2025
1125	37846	HIDROCORTISONA	TELEDOL	10 mg comp.x 20	Casasco	103.69	3.4563334	\N	21/11/2025
1126	13268	HIDROCORTISONA	SOLUC.PARENT.250 ML	Ringer lactato	Fidex	5.2	0.26	\N	24/06/2024
1127	28388	HIDROCORTISONA	DICLOFENAC SODICO	75 mg a.x 100 x 3 ml	Norgreen	257.44	8.581333	\N	24/12/2025
1128	45064	HIDROCORTISONA	RECO	150 mg comp.rec.x 60	Trb-Pharma	321	26.75	\N	03/12/2025
1129	386	HIDROCORTISONA	SOLUC.PARENT.500 ML	fisiol.clor.sodio	Apolo	5.35	5.35	\N	15/12/2025
1130	37282	HIDROCORTISONA	UNICALM	30 mg iny.a.x 5 x 1 ml	Adium	26.76	26.76	\N	30/10/2025
1131	18323	HIDROCORTISONA	DORMICUM	15 mg comp.x 20	Investi	107.45	107.45	\N	15/12/2025
1132	39880	HIDROCORTISONA	RANITIDINA 150 VENT-3	150 mg comp.x 100	Vent 3	538.12	538.12	\N	15/12/2025
1133	395	HIDROCORTISONA	SOLUC.PARENT.500 ML	bicarb.sod.1/6 molar	Apolo	5.41	5.41	\N	12/12/2025
1134	21830	HIDROCORTISONA	KLONAFENAC	75 mg iny.a.x 6 x 3 ml	Klonal	17.66	17.66	\N	12/12/2025
1135	10448	HIDROCORTISONA	NURIBAN	50 mg comp.x 45	Roux Ocefa	244.56	244.56	\N	19/12/2025
1136	41048	HIDROCORTISONA	BLOCADOL	20 mg comp.rec.x 20	Teva Argentina	109.06	109.06	\N	12/12/2025
1137	24990	HIDROCORTISONA	DICLOGRAND	75 mg iny.a.x 6 x 3 ml	Fada Pharma	19.58	0.1958	\N	14/10/2025
1138	397	HIDROCORTISONA	SOLUC.PARENT.500 ML	agua dest.	Apolo	5.49	5.49	\N	02/01/2026
1139	369	HIDROCORTISONA	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 10 ml	Apolo	5.5	0.055	\N	06/10/2025
1140	44700	HIDROCORTISONA	KETOROLAC RICHET	20 mg comp.x 20	Richet	110.14	2.2028	\N	06/10/2025
1141	30976	HIDROCORTISONA	MAGNESIO CLORURO	pote x 100 g	Pharma del Plat	5.52	0.0552	\N	23/10/2025
1142	592	HIDROCORTISONA	LUVIER	300 mg comp.x 30	Casasco	166.15	166.15	\N	15/12/2025
1143	26782	HIDROCORTISONA	AGUA OXIGENADA PHARMA	10 vol.x 1 l	Pharma del Plat	5.54	5.54	\N	22/12/2025
1144	1385	HIDROCORTISONA	NITRADISC	5 mg disc.autoadh.x 30	Pfizer	166.3	1.663	\N	08/10/2025
1145	17110	HIDROCORTISONA	SOLVENTE INDOLORO FADA	a.x 100 x 5 ml	Fada Pharma	556	5.56	\N	04/08/2025
1146	13652	HIDROCORTISONA	XINA	75 mg a.x 6 x 3 ml	Finadiet	21.18	0.2118	\N	06/10/2025
1147	25829	HIDROCORTISONA	SOLUC.DEXTROSA	25% a.x 100 x 25 ml	Norgreen	558.26	11.1652	\N	06/10/2025
1148	29989	HIDROCORTISONA	SOLUC.PARENT.500 ML APIROFLEX	isot.dext.5% en agua	Roux Ocefa	5.68	0.1136	\N	13/08/2025
1149	4928	HIDROCORTISONA	BIOMAG	gran.sob.x 30	Baliarda	171.01	171.01	\N	22/12/2025
1150	36556	HIDROCORTISONA	KETOROLAC NORTHIA	30 mg iny.a.x 100 x 2 ml	Northia	570.58	570.58	\N	22/12/2025
1151	22921	HIDROCORTISONA	DICLOFENAC DF	75 mg/3 ml a.x 1	Denver Farma	3.9	0.039	\N	04/08/2025
1152	25503	HIDROCORTISONA	INDOFENO	75 mg a.x 100 x 3 ml	Fada Pharma	460	9.2	\N	13/08/2025
1153	11460	HIDROCORTISONA	MINITRAN	5 mg parches x 10	3 M	57.45	57.45	\N	17/09/2025
1154	7391	HIDROCORTISONA	ADITIVOS PARENTERALES	clor.pot.x 5ml L216	Rivero	5.79	5.79	\N	22/12/2025
1155	45324	HIDROCORTISONA	KETOROLAC NORTHIA	30 mg iny.a.x 50 x 2 ml	Northia	290	290	\N	22/12/2025
1156	15089	HIOSCINA N-BUTILBR	SOLUC.FISIOLOGICA	a.x 1 x 20 ml	Richmond	5.81	0.2905	\N	20/02/2002
1157	13905	HIOSCINA N-BUTILBR	VINGIONAL	50 mg iny.a.x 5	Fabra	29.25	0.02867647	\N	25/04/2002
1158	24755	HIOSCINA N-BUTILBR	DICLAC	75 mg iny.a.x 5 x 3 ml	Investi	23	1.15	\N	01/09/2007
1159	50436	HIOSCINA N-BUTILBR	CLORHYP	monods.x 24 x 1 ml	Valmax	141	7.05	\N	16/08/2013
1160	25807	HIOSCINA N-BUTILBR	LIDOCAINA	1% s/epi.a.x 100 x 5 ml	Norgreen	587.99	29.3995	\N	30/09/2013
1161	387	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	isot.dext.5% en agua	Apolo	5.89	0.9816667	\N	01/02/2003
1162	40302	HIOSCINA N-BUTILBR	SOLUC.DEXTROSA NORGREEN	25% a.x 1 x 25 ml	Norgreen	5.9	0.295	\N	01/09/2001
1163	3599	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	lact.sod.1/6 molar	Fidex	5.93	0.0593	\N	10/07/2003
1164	18416	HIOSCINA N-BUTILBR	BANOCLUS	75 mg a.x 6 x 3 ml	Laboratorios Fr	29.34	4.89	\N	15/08/2002
1165	390	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	dext.5% sol.sal.normal	Apolo	6.02	0.301	\N	05/03/2014
1166	35790	HIOSCINA N-BUTILBR	FLOGOLISIN	75 mg a.x 6 x 3 ml	Lazar	36.23	0.3623	\N	12/01/2009
1167	37190	HIOSCINA N-BUTILBR	DOXTRAN 75 MG	75 mg a.x 5 x 3 ml	Phoenix	31.61	6.322	\N	31/03/2009
1168	370	HIOSCINA N-BUTILBR	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 10 ml	Apolo	6.09	1.218	\N	30/09/2013
1169	401	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	regimen de mant.	Apolo	6.09	1.015	\N	01/09/2001
1170	399	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	regimen de rep.	Apolo	6.09	2.03	\N	01/09/2001
1171	3603	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	agua dest.para iny.	Fidex	6.09	0.0609	\N	01/08/2021
1172	388	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	dext.10% en agua	Apolo	6.1	0.061	\N	05/11/2021
1173	40287	HIOSCINA N-BUTILBR	AGUA DESTILADA NORGREEN	a.x 1 x 20 ml	Norgreen	6.1	0.061	\N	22/10/2021
1174	40303	HIOSCINA N-BUTILBR	SOLUC.DEXTROSA NORGREEN	50% a.x 1 x 20 ml	Norgreen	6.1	0.305	\N	30/12/2025
1175	11463	HIOSCINA N-BUTILBR	MINITRAN	10 mg parches x 30	3 M	183.64	9.182	\N	30/12/2025
1176	41049	HIOSCINA N-BUTILBR	BLOCADOL 10 SL	10 mg comp.subl.x 10	Teva Argentina	62.4	1.248	\N	30/12/2025
1177	24138	HIOSCINA N-BUTILBR	MIDAZOLAM LAFEDAR	5 mg/5 ml iny.a.x 10	Lafedar	62.41	0.6241	\N	11/08/2025
1178	42768	HIOSCINA N-BUTILBR	DICLOFENAC SODICO DUNCAN	75 mg a.x 100	Duncan	820.4	32.816	\N	06/10/2025
1179	20800	HIOSCINA N-BUTILBR	KEMANAT	60 mg a.x 3 x 2 ml	Finadiet	19	0.76	\N	06/10/2025
1180	15361	HIOSCINA N-BUTILBR	SOLUC.CLORURADA HIPERTONICA	20% a.x 1 x 10 ml	Richmond	6.38	2.1266668	\N	30/12/2025
1181	15362	HIOSCINA N-BUTILBR	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 1 x 10 ml	Richmond	6.38	0.0638	\N	04/08/2025
1182	9134	HIOSCINA N-BUTILBR	FIDECAINA	1% s/epi.x 25 ml	Fidex	6.43	0.0643	\N	22/12/2025
1183	24137	HIOSCINA N-BUTILBR	MIDAZOLAM LAFEDAR	5 mg/5 ml iny.a.x 2	Lafedar	12.87	0.1287	\N	23/10/2025
1184	25810	IMIPENEM+CILASTATIN	LIDOCAINA	2% s/epi.a.x 100 x 5 ml	Norgreen	644.14	644.14	\N	01/02/2003
1185	43018	IMIPENEM+CILASTATIN	SOLUC. HIPERTONICA DE CLORURO DE SODIO	20% a.x 1 x 10 ml	Norgreen	6.5	6.5	\N	26/03/2002
1186	40304	IMIPENEM+CILASTATIN	SOLUC.DEXTROSA NORGREEN	50% a.x 1 x 25 ml	Norgreen	6.5	6.5	\N	24/11/2008
1187	3601	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	electrol.balanc.	Fidex	6.51	6.51	\N	01/06/2013
1188	21116	IMIPENEM+CILASTATIN	DIASTONE	75 mg iny.a.x 6 x 3 ml	Microsules Arg.	53.01	53.01	\N	10/11/2016
1189	394	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	Ringer con lactato	Apolo	6.53	6.53	\N	05/03/2014
1190	3591	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	dext.5% en agua	Fidex	6.53	6.53	\N	16/06/2017
1191	29352	IMIPENEM+CILASTATIN	FADA METOCLOPRAMIDA	10 mg iny.a.x 100 x 2 ml	Fada Pharma	654	654	\N	05/10/2015
1192	392	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	fisiol.de ringer	Apolo	6.57	0.1314	\N	11/11/2019
1193	3595	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	dext.5% sol.sal.	Fidex	6.68	0.2672	\N	02/03/2020
1194	50718	IMIPENEM+CILASTATIN	DAFIL	40 mg comp.x 40	Sidus	267.6	267.6	\N	10/07/2019
1195	31255	IMIPENEM+CILASTATIN	KLONAFENAC	75 mg iny.a.x 3 x 3 ml	Klonal	34.46	34.46	\N	21/10/2021
1196	27426	IMIPENEM+CILASTATIN	LIDOCAINA SHABBA	viscos.fco.gotero x 50ml	Shabba	6.8	0.272	\N	11/10/2022
1197	7928	IMIPENEM+CILASTATIN	TAURAL	iny.a.x 6 x 5 ml	Roemmers	40.93	1.6372	\N	20/12/2025
1198	41047	IMIPENEM+CILASTATIN	BLOCADOL	20 mg comp.rec.x 10	Teva Argentina	69.36	0.6936	\N	11/08/2025
1199	3596	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	dext.10% sol.sal.	Fidex	6.98	6.98	\N	11/08/2025
1200	49766	IMIPENEM+CILASTATIN	KETOROLAC FABRA	20 mg comp.x 30	Fabra	210.58	4.2116	\N	06/10/2025
1201	11462	IMIPENEM+CILASTATIN	MINITRAN	10 mg parches x 10	3 M	70.22	1.4044	\N	27/06/2025
1202	1406	IMIPENEM+CILASTATIN	SOLVENTE INDOLORO EXA	iny.sol.f.a.x 1 x 5 ml	Pfizer	7.04	7.04	\N	19/01/2024
1203	1386	IMIPENEM+CILASTATIN	NITRADISC	10 mg disc.autoadh.x 30	Pfizer	211.8	211.8	\N	17/12/2025
1204	13561	IMIPENEM+CILASTATIN	TOMANIL	75 mg iny.x 3 x 3 ml	Takeda	37.03	1.4812	\N	27/06/2025
1205	9135	IMIPENEM+CILASTATIN	FIDECAINA	2% s/epi.x 25 ml	Fidex	7.18	0.2872	\N	27/06/2025
1206	42764	IMIPENEM+CILASTATIN	METOCLOPRAMIDA DUNCAN	10 mg a.x 100	Duncan	718.4	14.368	\N	12/12/2025
1207	21142	IMIPENEM+CILASTATIN	RANITIDINA LAZAR	150 mg comp.x 100	Lazar	718.45	14.369	\N	13/08/2025
1208	3598	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	Ringer lactato	Fidex	7.24	0.17238095	\N	23/10/2025
1209	42763	IMIPENEM+CILASTATIN	FURSEMIDA DUNCAN	20 mg a.x 100	Duncan	726.3	726.3	\N	20/12/2025
1210	21622	IMIPENEM+CILASTATIN	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 50 x 25 ml	Fada Pharma	364.5	7.29	\N	04/08/2025
1211	26644	KETOROLAC	MIDAZOLAN BIOCROM	5 mg/5 ml iny.a.x 10	Biocrom	73	3.65	\N	23/11/2000
1212	37534	KETOROLAC	HIERBAS DEL OASIS BAJO SODIO	Ajo sal x 70 g	Hierbas del Oas	7.3	0.365	\N	17/03/2003
1213	37533	KETOROLAC	HIERBAS DEL OASIS BAJO SODIO	Natural sal x 70 g	Hierbas del Oas	7.3	0.0146	\N	14/06/2002
1214	21633	KETOROLAC	VIAFUROX FADAJET	jga.prell.x 50 x 2 ml	Fada Pharma	365.23	0.73046	\N	14/06/2002
1215	12788	KETOROLAC	SOLUC.PARENT.1000 ML	agua dest.	Apolo	7.32	0.732	\N	17/03/2003
1216	21833	KETOROLAC	REGIOCAINA JALEA	2% pomo x 25 ml	Richmond	7.42	0.371	\N	01/05/2005
1217	27427	KETOROLAC	METOCLOPRAMIDA SHABBA	0.5% Ad.gts.x 20 ml	Shabba	7.44	0.372	\N	08/08/2008
1218	15603	KETOROLAC	DICLOFENAC SODICO RICHET	75 mg a.x 6 x 3 ml	Richet	96.76	4.838	\N	18/01/2003
1219	27801	KETOROLAC	PAXYL	60 mg a.x 1 x 2 ml	Elvetium	7.5	0.75	\N	21/04/2008
1220	51733	KETOROLAC	RANITRAL 300	300 mg comp.rec.x 20	Lepetit	150	7.5	\N	13/08/2002
1221	24996	KETOROLAC	KETOROLAC AHIMSA	iny.a.x 6 x 1 ml	Fada Pharma	45.15	4.515	\N	08/05/2007
1222	2248	KETOROLAC	VOLTAREN	75 mg a.x 6 x 3 ml	Novartis	130.07	4.3356667	\N	24/12/1999
1223	25895	KETOROLAC	NASOMICINA SALINA	gts.nasales x 30 ml	Northia	7.58	0.758	\N	26/04/2002
1224	39881	KETOROLAC	RANITIDINA 300 VENT-3	300 mg comp.x 100	Vent 3	760	38	\N	28/01/2003
1225	2212	KETOROLAC	RELIVERAN	a.x 6	Novartis	45.67	4.567	\N	01/03/2006
1226	359	KETOROLAC	SOLUC.CLORURADA HIPERTONICA	20% a.x 20 ml	Apolo	7.67	0.3835	\N	18/01/2003
1227	389	KETOROLAC	SOLUC.PARENT.500 ML	dext.25% en agua	Apolo	7.69	0.769	\N	10/10/2007
1228	37778	KETOROLAC	AGUA OXIGENADA	10 vol.x 500 ml	Zasu	7.7	0.385	\N	16/09/2013
1229	52529	KETOROLAC	DICLOMAR	75 mg a.x 50 x 3 ml	Mar	1400	140	\N	26/04/2002
1230	7143	KETOROLAC	METOCLOPRAMIDA RICHET	0.5% Ad.gts.x 20 ml	Richet	7.72	2.5733333	\N	23/11/2000
1231	24140	KETOROLAC	MIDAZOLAM LAFEDAR	15 mg/3 ml iny.a.x 10	Lafedar	77.21	7.721	\N	16/09/2013
1232	26812	KETOROLAC	SOLUC.PARENT.SOLUFLEX	hiper.cl.sod.x 50ml 637C	Rivero	7.8	0.78	\N	12/04/2011
1233	1405	KETOROLAC	SOLVENTE INDOLORO EXA	iny.liof.f.a.x 5 ml	Pfizer	7.81	0.781	\N	03/10/2003
1234	12790	KETOROLAC	AGUA DESTILADA APOLO	f.a.x 100 ml	Apolo	7.85	0.3925	\N	16/09/2013
1235	20856	KETOROLAC	FUROSEMIDA DENVER FARMA	gts.x 15 ml	Denver Farma	7.92	2.64	\N	10/01/2000
1236	24139	KETOROLAC	MIDAZOLAM LAFEDAR	15 mg/3 ml iny.a.x 2	Lafedar	15.92	5.306667	\N	07/02/2002
1237	37719	KETOROLAC	ALGIOXIB	75 mg iny.a.x 5 x 3 ml	Ferring	313.62	15.681	\N	15/12/2014
1238	15828	KETOROLAC	VINGIONAL	150 mg comp.x 20	Fabra	160	53.333332	\N	18/01/2003
1239	30580	KETOROLAC	SOFTWEAR SALINE	sol.salina x 240 ml	Ciba Vision	8	0.26666668	\N	10/11/2015
1240	34749	KETOROLAC	DICLOMAR	75 mg a.x 4 x 3 ml	Mar	400	400	\N	25/03/2002
1241	23	KETOROLAC	ALFICETIN	iny.a.x 4	Bristol	32.16	10.72	\N	03/04/2002
1242	40357	KETOROLAC	LIDOCAINA NORGREEN	1% a.x 1 x 5 ml c/epi.	Norgreen	8.08	1.3466667	\N	03/04/2002
1243	27419	KETOROLAC	HIDROCORTISONA SHABBA	100 mg f.a.x 1	Shabba	8.1	2.7	\N	18/01/2003
1244	26825	KETOROLAC	TENKDOL	60 mg a.x 1 x 2 ml	Biotenk	8.1	8.1	\N	02/10/1998
1245	3607	KETOROLAC	SOLUC.PARENT.1000 ML	agua dest.iny.	Fidex	8.12	0.0812	\N	14/06/2002
1246	29345	KETOROLAC	FADA KETOROLAC/NOLARAC	30 mg a.x 100 x 1 ml	Fada Pharma	815.35	163.07	\N	26/04/2002
1247	55135	KETOROLAC	CURINFLAM	iny.a.x 100 x 3 ml	Duncan	14287.3	4762.433	\N	28/01/2003
1248	402	KETOROLAC	SOLUC.PARENT.1000 ML	fisiol.clor.sodio	Apolo	8.27	8.27	\N	09/01/2009
1249	25688	KETOROLAC	SOLUC.PARENT.SOLUFLEX	acet.pot.mol.x100ml 635H	Rivero	8.37	8.37	\N	10/01/2000
1250	46400	KETOROLAC	DIPGIX SL	10 mg comp.subl.x 10	Lab Internacion	84.4	4.22	\N	02/03/2016
1251	368	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 20 ml	Apolo	8.55	0.4275	\N	07/05/2016
1252	3589	KETOROLAC	SOLUC.PARENT.250 ML	manitol 15% en agua	Fidex	8.59	0.0859	\N	06/07/2015
1253	62767	KETOROLAC	FABOGESIC FLEXI 75	75 mg c ps.x 10	Savant Consumer	10499	209.98	\N	24/06/2010
1254	38192	KETOROLAC	RUPEMET	0.2% gts.x 20 ml	Duncan	8.7	0.87	\N	15/12/2014
1255	2200	KETOROLAC	NITRODERM TTS	5 mg sistema x 30	Novartis	261.33	87.11	\N	18/01/2003
1256	46399	KETOROLAC	DIPGIX	20 mg comp.x 20	Lab Internacion	174.36	17.436	\N	15/12/2014
1257	12373	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 50 x 25 ml	Fada Pharma	437.4	14.58	\N	10/11/2015
1258	27081	KETOROLAC	IMANOL AP	75 mg caps.x 10	Biosintex	19.25	19.25	\N	23/11/2000
1259	13736	KETOROLAC	HIDROCORTISONA AUSTRAL	100 mg iny.liof.f.a.x 1	Austral	8.9	1.4833333	\N	01/11/2005
1260	18516	KETOROLAC	LIDOCAINA	2% s/epi.iny.f.a.x 25 ml	Rig	8.9	8.9	\N	30/09/2013
1261	9991	KETOROLAC	METOCLOPRAMIDA LARJAN	0.5% gts.x 20 ml	Veinfar	8.9	8.9	\N	07/02/2002
1262	23817	KETOROLAC	SOLUC.PARENT.1000 ML	dext.5%	Apolo	8.93	0.0893	\N	09/01/2009
1263	2199	KETOROLAC	NITRODERM TTS	10 mg sistema x 10	Novartis	90.37	9.037	\N	14/11/2016
1264	19517	KETOROLAC	HIDROCORTISONA DUNCAN	100 mg f.a.x 100	Duncan	910	45.5	\N	14/11/2016
1265	43019	KETOROLAC	SOLUC. HIPERTONICA DE CLORURO DE SODIO	20% a.x 1 x 20 ml	Norgreen	9.2	0.92	\N	31/08/2016
1266	3606	KETOROLAC	SOLUC.PARENT.1000 ML	sol.p/dial.al 7%	Fidex	9.23	0.923	\N	11/10/2016
1267	27082	KETOROLAC	IMANOL AP	75 mg caps.x 20	Biosintex	34.94	3.494	\N	15/05/2018
1268	25210	KETOROLAC	XEDENOL	75 mg comp.lib.prol.x 15	Baliarda	17120.56	5706.8535	\N	04/11/2015
1269	31792	KETOROLAC	IDENONA	cr.x 15 g	Andr maco	9.33	9.33	\N	05/01/2009
1270	3363	KETOROLAC	SOLUC.PARENT.500 ML	manitol al 15%	Rigecin	9.37	9.37	\N	08/08/2008
1271	18617	KETOROLAC	KERARER	60 mg iny.a.x 1 x 2 ml	LKM	9.43	9.43	\N	28/01/2003
1272	30504	KETOROLAC	GOBBICAINA JALEA	2% env.monods.x 10 g	Gobbi	9.69	9.69	\N	24/12/1999
1273	34163	KETOROLAC	MIDAZOLAM LARJAN	15 mg/3 ml iny.a.x 100	Veinfar	970	10.777778	\N	21/03/2022
1274	56704	KETOROLAC	DOLOFENAC 75	75 mg comp.lib.prol.x 30	Sanitas	1555.21	155.521	\N	10/05/2024
1275	29448	KETOROLAC	METOCLOPRAMIDA PHARMA	0.5% gts.x 20 ml	Pharma del Plat	9.8	9.8	\N	30/11/2015
1276	22933	KETOROLAC	RANITIDINA DENVER FARMA	50 mg a.x 1 x 5 ml	Denver Farma	9.8	9.8	\N	24/12/1999
1277	54986	KETOROLAC	NORVIKEN 75 VENT-3	75 mg comp.lib.prol.x 30	Vent 3	11426.74	380.89133	\N	10/06/2020
1278	371	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 20 ml	Apolo	9.87	3.29	\N	30/11/2015
1279	2198	KETOROLAC	NITRODERM TTS	5 mg sistema x 10	Novartis	98.81	8.234167	\N	18/01/2003
1280	23580	KETOROLAC	REM CHOBET	5 mg/5 ml a.x 10	Soubeiran Chobe	98.97	9.897	\N	03/02/2021
1281	3605	KETOROLAC	SOLUC.PARENT.1000 ML	dext.5% en agua	Fidex	9.91	0.991	\N	01/06/2020
1282	25211	KETOROLAC	XEDENOL	75 mg comp.lib.prol.x 30	Baliarda	35142.36	3514.236	\N	01/06/2020
1283	54274	KETOROLAC	MAGNESIO NATULIV	comp.x 60	Laboratorio ENA	595	198.33333	\N	24/08/2016
1284	17760	KETOROLAC	SINTEGRAN	gts.x 20 ml	Sintesina	9.92	0.992	\N	05/08/2021
1285	23816	KETOROLAC	SULFATO DE MAGNESIO APOLO	25% a.x 1 x 5 ml	Apolo	10.03	1.003	\N	10/05/2024
1286	30381	KETOROLAC	REM CHOBET	5 mg/5 ml a.x 5	Soubeiran Chobe	50.53	2.5265	\N	10/05/2024
1287	7271	KETOROLAC	SOLUC.CLORURADA HIPERTONICA	20% a.x 1 x 20 ml	Richmond	10.15	1.015	\N	10/05/2024
1288	7305	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 1 x 20 ml	Richmond	10.15	10.15	\N	01/03/2017
1289	27363	KETOROLAC	PRIMAVERA-N	Ped.gts.x 20 ml	Fabra	10.17	1.017	\N	27/11/2023
1290	19562	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 100 x 20 ml	Veinfar	1020	10.2	\N	12/08/2021
1291	46140	KETOROLAC	XEDENOL	75 mg comp.lib.prol.x 7	Baliarda	31.48	0.6296	\N	04/07/2022
1292	6082	KETOROLAC	LIZARONA	gts.x 40 ml	Northia	10.22	0.1022	\N	01/08/2021
1293	26527	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 50 x 20 ml	Fada Pharma	517.59	517.59	\N	10/10/2018
1294	45685	KETOROLAC	KETOROLAC RICHET	20 mg comp.x 10	Richet	103.91	5.1955	\N	18/06/2024
1295	36269	KETOROLAC	METOCLOPRAMIDA LEMAX	2 mg/ml Ni os gts.x 20ml	Lemax	10.4	1.04	\N	18/06/2024
1296	13270	KETOROLAC	SOLUC.PARENT.1000 ML	dext.5% sol.sal.	Fidex	10.42	10.42	\N	04/07/2022
1297	19564	KETOROLAC	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 100 x 20 ml	Veinfar	1047	52.35	\N	03/09/2025
1299	22081	KETOROLAC	CELIT	gts.x 20 ml	Fada Pharma	10.69	0.5345	\N	29/12/2025
1300	27681	KETOROLAC	FADA METOCLOPRAMIDA	gts.x 24 x 20 ml	Fada Pharma	256.56	25.656	\N	16/12/2025
1301	19968	KETOROLAC	DANTENK	4 mg comp.x 10	Biotenk	108	5.4	\N	22/12/2025
1302	7373	KETOROLAC	SOLUC.ANTICOAGULANTE ENV.VIDRIO VIAL	citr.sod.4% x 50ml C54	Rivero	10.89	0.5445	\N	18/06/2024
1303	15621	KETOROLAC	CLORURO DE SODIO	20% a.x 100 x 20 ml	Veinfar	1090	109	\N	29/12/2025
1304	13269	KETOROLAC	SOLUC.PARENT.1000 ML	dext.10% en agua	Fidex	10.94	1.094	\N	01/06/2024
1305	15636	KETOROLAC	SULFATO DE MAGNESIO	a.x 100 x 10 ml	Veinfar	1097	109.7	\N	18/06/2024
1306	26783	KETOROLAC	AGUA OXIGENADA PHARMA	10 vol.x 5 l	Pharma del Plat	11.08	0.554	\N	17/12/2025
1307	15623	KETOROLAC	LARJANCAINA	1% f.a.x 20 ml	Veinfar	11.3	0.565	\N	18/12/2025
1308	15624	KETOROLAC	LARJANCAINA	2% f.a.x 20 ml	Veinfar	11.3	0.565	\N	23/12/2025
1309	15625	KETOROLAC	LARJANCAINA CON EPINEFRINA	1% f.a.x 20 ml	Veinfar	11.3	0.565	\N	29/12/2025
1310	15626	KETOROLAC	LARJANCAINA CON EPINEFRINA	2% f.a.x 20 ml	Veinfar	11.3	1.13	\N	20/11/2025
1311	46874	KETOROLAC	ZERODOL	10 mg comp.x 10	Bag	113.02	5.651	\N	22/12/2025
1312	21813	KETOROLAC	HIDROCORTISONA	100 mg f.a.x 1	Klonal	11.31	0.5655	\N	17/12/2025
1313	16633	KETOROLAC	DORMICUM	5 mg/5 ml iny.a.x 2	Roche	22.69	2.269	\N	03/09/2025
1314	2201	KETOROLAC	NITRODERM TTS	10 mg sistema x 30	Novartis	340.54	17.027	\N	22/12/2025
1315	37660	KETOROLAC	LIMONADA ROGE	env.x 80 g	Zasu	11.45	0.5725	\N	16/12/2025
1316	6907	KETOROLAC	SOLUC.PARENT.1000 ML	sol.p/dial.per.c/2%dext.	Roux Ocefa	11.47	0.5735	\N	20/11/2025
1317	46561	KETOROLAC	DIOXAFLEX	75 mg comp.mast.x 15	Bag	1325.3	132.53	\N	16/12/2025
1318	29518	KETOROLAC	DICLAC	75 mg comp.rapirtd.x 10	Siegfried	3227.75	322.775	\N	03/09/2025
1319	29519	KETOROLAC	DICLAC	75 mg comp.rapirtd.x 20	Siegfried	5371.42	537.142	\N	18/12/2025
1320	23581	KETOROLAC	REM CHOBET	15 mg/3 ml a.x 10	Soubeiran Chobe	117.04	11.704	\N	17/12/2025
1321	42945	KETOROLAC	FLOGOLISIN	75 mg comp.rec.x 10	Lazar	38.56	3.856	\N	29/12/2025
1322	19985	KETOROLAC	ULCOTENK	150 mg comp.rec.x 60	Biotenk	707.05	70.705	\N	18/12/2025
1323	32102	KETOROLAC	RECO	150 mg comp.rec.x 30	Trb-Pharma	355	35.5	\N	22/12/2025
1324	56357	KETOROLAC	RANITIDINA HLB 150 MG	150 mg comp.x 30	HLB Pharma	355.21	35.521	\N	18/12/2025
1325	9140	KETOROLAC	FIDECAINA	1% s/epi.x 100 ml	Fidex	11.88	1.188	\N	23/12/2025
1326	37779	KETOROLAC	AGUA OXIGENADA	10 vol.x 1000 ml	Zasu	11.96	1.196	\N	01/06/2024
1327	50789	KETOROLAC	RANITIDINA LAZAR	150 mg comp.x 60	Lazar	721.23	72.123	\N	29/12/2025
1328	32547	KETOROLAC	AQUA LENT SOLUCION SALINA FISIOLOGICA	Especial p/len.con.x500m	Inmunolab	12.13	1.213	\N	16/12/2025
1329	23852	KETOROLAC	DRIM-NORTH	15 mg/3ml iny.a.x 5	Northia	60.69	6.069	\N	15/09/2025
1330	28051	KETOROLAC	LIDOCAINA	1% f.a.x 20 ml	Klonal	12.14	1.214	\N	22/12/2025
1331	28055	KETOROLAC	LIDOCAINA	1% c/epi.f.a.x 20 ml	Klonal	12.14	1.214	\N	18/12/2025
1332	30281	KETOROLAC	LIDOCAINA+EPINEFRINA KLONAL	1% f.a.x 20 ml	Klonal	12.14	0.607	\N	23/12/2025
1333	23853	KETOROLAC	DRIM-NORTH	15 mg/3ml iny.a.x 2	Northia	24.28	4.856	\N	19/04/2024
1334	25581	KETOROLAC	GOBBIZOLAM	15 mg iny.a.x 10 x 3 ml	Gobbi	122.12	12.212	\N	23/12/2025
1335	22263	KETOROLAC	DISIPAN 75 MG	75 mg comp.rec.x 10	Laboratorios Be	50.41	16.803333	\N	24/09/2025
1336	44716	KETOROLAC	VOLTAREN 75	75 mg comp.rec.x 10	Novartis	114.92	11.492	\N	23/12/2025
1337	26843	KETOROLAC	HIDROCORTISONA	0.5% cr.x 15 g	Klonal	12.35	4.116667	\N	14/04/2025
1338	8857	KETOROLAC	TOTAL MAGNESIANO	elixir fco.x 150 ml	Temis-Lostal	12.4	4.133333	\N	22/12/2025
1339	21145	KETOROLAC	MIDAZOLAN GEMEPE	5 mg/5 ml iny.a.x 2	Gemepe	25	0.25	\N	06/10/2025
1340	53976	KETOROLAC	KETOROLAC VANNIER	10 mg comp.x 10	Vannier	125.78	1.2578	\N	13/08/2025
1341	18618	KETOROLAC	KERARER	60 mg iny.a.x 3 x 2 ml	LKM	38.2	1.528	\N	27/06/2025
1342	32101	KETOROLAC	RECO	150 mg comp.rec.x 10	Trb-Pharma	129	1.29	\N	11/08/2025
1343	396	KETOROLAC	SOLUC.PARENT.500 ML	d-manitol al 15%	Apolo	12.9	0.129	\N	23/10/2025
1344	39319	KETOROLAC	HIDROCORTISONA LARJAN	100 mg f.a.x 50 x 2 ml	Veinfar	650	216.66667	\N	22/12/2025
1345	26643	KETOROLAC	MIDAZOLAN BIOCROM	15 mg/3 ml iny.a.x 5	Biocrom	65	21.666666	\N	23/12/2025
1346	41409	KETOROLAC	DISGRADON	100 mg gts.x 20 ml	Fada Pharma	13.03	13.03	\N	18/06/2024
1347	26723	KETOROLAC	HIDROCORTISONA BIOCROM	100 mg a.x 1	Biocrom	13.1	13.1	\N	15/12/2025
1348	50788	KETOROLAC	RANITIDINA LAZAR	150 mg comp.x 30	Lazar	395.2	395.2	\N	24/12/2025
1349	32736	KETOROLAC	GASTROZAC	150 mg comp.x 30	Klonal	396.45	396.45	\N	24/12/2025
1350	29349	LIDOCAINA	FADA METOCLOPRAMIDA	100 mg gts.x 20 ml	Fada Pharma	13.29	0.1329	\N	01/02/2003
1351	33714	LIDOCAINA	SULFATO DE MAGNESIO	1.25 g a.x 1 x 5 ml	Fada Pharma	13.42	0.1342	\N	03/07/2003
1352	30979	LIDOCAINA	SOLUC.SALINA	fco.gotero x 500 ml	Pharma del Plat	13.52	0.1352	\N	01/02/2003
1353	15662	LIDOCAINA	SOLUC.FISIOLOGICA APOLO	env.x 2000 ml	Apolo	13.67	0.5468	\N	09/03/2018
1354	12789	LIDOCAINA	SOLUC.PARENT.2000 ML	p/irrig.quirurg.	Apolo	13.67	0.5468	\N	09/03/2018
1355	39168	LIDOCAINA	METOCLOPRAMIDA LBA	0.4% gts.x 20 ml	Filaxis Farmac	13.69	0.1369	\N	03/07/1996
1356	17221	LIDOCAINA	DORMICUM	15 mg/3 ml iny.a.x 5	Roche	68.83	13.766	\N	28/03/2011
1357	17585	LIDOCAINA	HIDROCORTISONA NORTHIA	100 mg f.a.x 1	Northia	13.83	2.766	\N	09/11/2010
1358	398	LIDOCAINA	SOLUC.PARENT.500 ML	dext.50% en agua	Apolo	13.85	13.85	\N	03/12/2002
1359	38096	LIDOCAINA	IGLODINE 75	75 mg comp.rec.x 10	Fecofar	115.95	115.95	\N	03/12/2002
1360	55691	LIDOCAINA	ACLOXIGENAC	75 mg comp.rec.x 10	Eczane	7217.47	72.1747	\N	16/06/2005
1361	3206	LIDOCAINA	BIOMAG	comp.rec.x 20	Baliarda	281.64	281.64	\N	01/02/2003
1362	33515	LIDOCAINA	DICLOGESIC	75 mg comp.rec.x 10	Trb-Pharma	8500.01	8500.01	\N	21/04/2008
1363	3602	LIDOCAINA	SOLUC.PARENT.500 ML	manitol al 15% en agua	Fidex	14.3	0.143	\N	06/04/2022
1364	9309	LIDOCAINA	BALSAN	gts.x 15 ml	Novartis-Sandoz	14.31	2.862	\N	18/01/2003
1365	37703	LIDOCAINA	METAFLEX 75	75 mg comp.rec.x 10	Montpellier	10108.1	10108.1	\N	28/01/2003
1366	22427	LIDOCAINA	SOLUC.PARENT.2000 ML	agua dest.	Fidex	14.36	0.1436	\N	12/01/2009
1367	20292	LIDOCAINA	VANCOMICINA ABBOTT	Fliptop 0.50 g f.a.x 1	Abbott	14.36	0.1436	\N	12/01/2009
1368	42507	LIDOCAINA	DICLOFENAC NORTHIA	75 mg comp.rec.x 100	Northia	166.86	41.715	\N	11/03/2010
1369	46527	LIDOCAINA	FLOGOLISIN	75 mg comp.rec.x 100	Lazar	1948.6	389.72	\N	18/01/2003
1370	22426	LIDOCAINA	SOLUC.PARENT.2000 ML	fisiol.clor.sodio	Fidex	14.51	3.6275	\N	11/03/2010
1371	465	LIDOCAINA	GASTROSEDOL	150 mg comp.x 60	Nova Argentia	876.2	876.2	\N	01/12/1996
1372	9160	LIDOCAINA	FIDECAINA	2% s/epi.x 100 ml	Fidex	14.73	14.73	\N	04/07/2011
1373	28056	LIDOCAINA	LIDOCAINA	2% c/epi.f.a.x 20 ml	Klonal	14.74	0.1474	\N	19/05/2011
1374	30282	LIDOCAINA	LIDOCAINA+EPINEFRINA KLONAL	2% f.a.x 20 ml	Klonal	14.74	0.1474	\N	01/06/2002
1375	32600	LIDOCAINA	HIDROCORTISONA DRAWER	500 mg iny.f.a.x 50	Drawer	743.6	743.6	\N	04/05/2015
1376	22156	LIDOCAINA	LIDOCAINA LAFEDAR	2% jalea pomo x 25 ml	Lafedar	14.9	14.9	\N	26/04/2002
1377	56920	LIDOCAINA	CURINFLAM GESIC	75 mg comp.rec.x 1020	Duncan	14287.3	142.873	\N	01/06/2002
1378	36263	LIDOCAINA	HIDROCORTISONA LEMAX	100 mg f.a.x 1	Lemax	15.3	15.3	\N	06/11/2000
1379	28320	LIDOCAINA	RANITRAL 150	150 mg comp.x 10	Lepetit	153.4	153.4	\N	25/03/2002
1380	26761	LIDOCAINA	SAL INGLESA PHARMA	pote x 1000 g	Pharma del Plat	15.5	15.5	\N	07/02/2002
1381	9948	LIDOCAINA	LIDOCAINA	2% s/epi.f.a.x 20 ml	Epicaris	15.58	15.58	\N	25/03/2002
1382	9949	LIDOCAINA	LIDOCAINA	2% c/epi.f.a x 20 ml	Epicaris	15.58	15.58	\N	01/12/1996
1383	41322	LIDOCAINA	LORBIFENAC	75 mg comp.rec.x 14	Filaxis Farmac	19.78	19.78	\N	01/12/2015
1384	46538	LIDOCAINA	RANITIDINA LAZAR	300 mg comp.x 100	Lazar	1571.08	1571.08	\N	06/04/2022
1385	47688	LIDOCAINA	KERAMIX	30 mg. x 3 a.	Finadiet	47.27	47.27	\N	06/04/2022
1386	37283	LIDOCAINA	UNICALM	60 mg iny.a.x 1 x 2 ml	Adium	15.8	15.8	\N	26/04/2002
1387	16525	LIDOCAINA	SOLUC.PARENT.1000 ML	glicina al 1.5%	Rigecin	15.8	15.8	\N	01/02/2003
1388	7927	LIDOCAINA	TAURAL	150 mg comp.x 60	Roemmers	949.9	949.9	\N	01/02/2003
1389	29504	LIDOCAINA	HIDROCORTISONA PHARMA	cr.x 30 g	Pharma del Plat	15.84	15.84	\N	26/04/2002
1390	31661	LIDOCAINA	MIDAZOLAM GRAY	15 mg iny.a.x 1 x 3 ml	Gray	15.88	15.88	\N	28/06/2002
1391	21623	LIDOCAINA	SULFATO DE MAGNESIO FADAJET	25% jga.prell.x 50 x 5ml	Fada Pharma	795.34	795.34	\N	01/04/1995
1392	19518	LIDOCAINA	HIDROCORTISONA DUNCAN	500 mg f.a.x 100	Duncan	1600	1600	\N	22/01/2003
1393	39318	LIDOCAINA	HIDROCORTISONA LARJAN	100 mg f.a.x 1 x 2 ml	Veinfar	16	5.3333335	\N	07/03/2016
1394	26094	LIDOCAINA	SOLUC.SALINA	env.x 35 ml	Biotech Farma *	16	16	\N	07/03/2016
1395	21072	LIDOCAINA	HIDROCORTISONA DRAWER	500 mg iny.f.a.x 1	Drawer	16.1	0.161	\N	16/08/2016
1396	12896	LIDOCAINA	VOLTAREN 75	75 mg comp.rec.x 14	Novartis	55.25	55.25	\N	03/12/2002
1397	18615	LIDOCAINA	KERARER	30 mg iny.a.x 1 x 1 ml	LKM	16.18	16.18	\N	15/08/2000
1398	10623	LIDOCAINA	GASTROSEDOL	150 mg comp.x 30	Nova Argentia	496.5	496.5	\N	03/12/2002
1399	37165	LIDOCAINA	LORBIFENAC	75 mg comp.rec.x 15	Filaxis Farmac	17.5	17.5	\N	18/01/2003
1400	15652	LIDOCAINA	HIDROCORTISONA	100 mg f.a.x 1 est.	Richmond	16.69	16.69	\N	02/05/2016
1401	26730	LIDOCAINA	LIDOCAINA BIOCROM	2% jalea c/aplic.x 25 ml	Biocrom	16.8	16.8	\N	07/02/2002
1402	41515	LIDOCAINA	SOLVENTE INDOLORO MONSERRAT Y ECLAIR	liof.IM f.a.x 3 x 5 ml	Monserrat	50.5	50.5	\N	06/04/2022
1403	18652	LIDOCAINA	SOLVENTE INDOLORO MONSERRAT Y ECLAIR	liof.IM f.a.x 1 x 5 ml	Monserrat	16.85	16.85	\N	22/01/2003
1404	32038	LIDOCAINA	GASTROSEDOL	150 mg comp.x 20	Nova Argentia	337.94	337.94	\N	01/04/2002
1405	2455	LIDOCAINA	LIZARONA	gts.x 20 ml	Northia	17.06	17.06	\N	07/02/2002
1406	11658	LIDOCAINA	CETRON	4 mg comp.x 10	Adium	171.04	171.04	\N	04/07/2011
1407	5877	LIDOCAINA	VIZERUL	comp.x 30	Montpellier	513.72	513.72	\N	05/09/2018
1408	30880	LIDOCAINA	AGUA OXIGENADA PHARMA	100 vol.x 1 l	Pharma del Plat	17.25	17.25	\N	21/06/2003
1409	20182	LIDOCAINA	KELAC	60 mg a.x 1 x 2 ml	Richmond	17.3	17.3	\N	21/06/2003
1410	31782	LIDOCAINA	AZUTHIDRONA	cr.x 15 g	Valuge	17.4	17.4	\N	28/01/2003
1411	34165	LIDOCAINA	ONDANSETRON EPICARIS	8 mg a.x 1 x 4 ml	Epicaris	17.55	17.55	\N	16/06/2017
1412	2606	LIDOCAINA	MAGNEBE	iny.a.x 6 x 5 ml	Dom nguez	105.65	105.65	\N	04/11/2015
1413	48443	LIDOCAINA	TAURAL	150 mg comp.x 30	Roemmers	534.86	534.86	\N	04/07/2007
1414	360	LIDOCAINA	SOLUC.CLORURADA HIPERTONICA	20% f.a.x 50 ml	Apolo	17.94	17.94	\N	04/07/2007
1415	31691	LIDOCAINA	FISIOLOGICA DENVER FARMA	sol.oft.x 10 ml	Denver Farma	18.8	18.8	\N	04/07/2011
1416	15231	LIDOCAINA	MAGNESIO PAGLIANO	pvo.efer.x 100 g	Lacefa	18.9	18.9	\N	06/11/2000
1417	25362	LIDOCAINA	SINALGICO	0.5% sol.oft.x 5 ml	Laboratorios Be	19.3	19.3	\N	11/03/2010
1418	36867	LIDOCAINA	DICLOFENAC GEN MED	75 mg comp.rec.x 15	Gen Med	18.1	0.724	\N	01/06/2002
1419	38246	LIDOCAINA	DILAM	75 mg comp.rec.x 15	Lamsa	18.9	0.756	\N	01/06/2002
1420	30121	LIDOCAINA	NOREPINEFRINA NORTHIA	a.x 1 x 4 ml	Northia	19.55	19.55	\N	09/12/2015
1421	21814	LIDOCAINA	HIDROCORTISONA	500 mg f.a.x 1	Klonal	19.81	19.81	\N	04/05/2015
1422	45030	LIDOCAINA	RESPISOL	spray nasal x 25 ml	Phoenix	19.9	19.9	\N	06/11/2000
1423	6978	LIDOCAINA	FONDERYL	sol.x 20 ml	Megalabs Argent	19.93	19.93	\N	28/01/2003
1424	20470	LIDOCAINA	METOC	5% gts.x 20 ml	Oriental	19.95	19.95	\N	02/05/2016
1425	34464	LIDOCAINA	RANITIDINA DENVER FARMA	300 mg comp.x 30	Denver Farma	598.78	598.78	\N	03/11/2015
1426	43373	LIDOCAINA	SULFATO DE MAGNESIO 25% NORGREEN	25% a.x 1 x 10 ml	Norgreen	20	20	\N	09/03/2018
1427	43375	LIDOCAINA	SOLUC. HIPERTONICA DE CLOR.DE SODIO NORGREEN	20% f.a.x 1 x 50 ml	Norgreen	20	20	\N	14/07/2015
1428	350	LIDOCAINA	LIDOCAINA	1% f.a.x 20 ml s/epi.	Apolo	20.11	0.6703333	\N	21/03/2017
1429	19967	LIDOCAINA	DANTENK	4 mg/2 ml iny.f.a.x 5	Biotenk	100.8	3.36	\N	21/03/2017
1430	7411	LIDOCAINA	ADITIVOS PARENTERALES	molar acet.pot.x20ml L75	Rivero	20.3	20.3	\N	29/03/2019
1431	26727	LIDOCAINA	LIDOCAINA BIOCROM	1% f.a.x 20 ml s/epi.	Biocrom	20.45	20.45	\N	05/09/2018
1432	25687	LIDOCAINA	ONDANSETRON ASOFARMA	4 mg a.x 1 x 2 ml	Asofarma	20.62	20.62	\N	26/04/2019
1433	16750	LIDOCAINA	ONDANSETRON LAZAR	4 mg comp.x 8	Lazar	166.25	166.25	\N	14/11/2008
1434	17500	LIDOCAINA	ONDANSETRON FILAXIS	4 mg comp.x 4	Filaxis	83.43	83.43	\N	27/02/2019
1435	13664	LIDOCAINA	HIDROCORTISONA FABRA	100 mg f.a.x 1	Fabra	21.04	21.04	\N	26/04/2019
1436	31127	LIDOCAINA	AGUA OXIGENADA	100 vol.env.x 1000 ml	Eczane	21.2	1.06	\N	23/08/2019
1437	42828	LIDOCAINA	DICLOFILAB	75 mg comp.rec.x 15	Inmunolab	34.5	34.5	\N	19/04/2023
1438	13735	LIDOCAINA	HIDROCORTISONA AUSTRAL	500 mg iny.liof.f.a.x 1	Austral	21.4	21.4	\N	22/12/2025
1439	354	LIDOCAINA	LIDOCAINA	2% f.a.x 20 ml s/epi.	Apolo	21.63	21.63	\N	22/12/2025
1440	46120	LIDOCAINA	DICLOFENAC TECHSPHERE	75 mg comp.rec.x 15	Techsphere	63.25	0.6325	\N	11/08/2025
1441	8312	LIDOCAINA	SCHERICUR	pda.x 20 g	Bayer (PH)	21.79	0.2179	\N	02/07/2024
1442	36268	LIDOCAINA	METOCLOPRAMIDA LEMAX	5 mg/ml Ad.gts.x 20 ml	Lemax	21.8	0.218	\N	02/07/2024
1443	45326	LIDOCAINA	DRIM-NORTH	15 mg/3 ml iny.a.x 10	Northia	218	2.18	\N	06/10/2025
1444	48141	LIDOCAINA	IBUXIM DICLO	75 mg comp.rec.x 15	Savant Consumer	145.64	1.4564	\N	27/06/2025
1445	16327	LIDOCAINA	ESPASEVIT	4 mg comp.x 10	Richmond	218.25	2.1825	\N	11/08/2025
1446	26530	LIDOCAINA	SULFATO DE MAGNESIO	25% a.x 100 x 10 ml	Fada Pharma	2185.54	21.8554	\N	27/09/2024
1447	12791	LIDOCAINA	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 50 ml	Apolo	21.88	0.4376	\N	29/10/2025
1448	18130	LIDOCAINA	XYLOCAINA	jalea jga.prell.x 10 ml	AstraZeneca	21.93	21.93	\N	13/05/2024
1449	18651	LIDOCAINA	SOLVENTE INDOLORO MONSERRAT Y ECLAIR	sol.f.a.x 1 x 5 ml	Monserrat	22	0.44	\N	29/10/2025
1450	38878	LIDOCAINA	SAFTEN	gts.x 20 ml	Monserrat	22	1.1	\N	11/11/2025
1451	35290	LIDOCAINA	ONDANSETRON RICHET	4 mg comp.x 10	Richet	220.57	2.2057	\N	06/10/2025
1452	32104	LIDOCAINA	RECO	300 mg comp.rec.x 30	Trb-Pharma	664	6.64	\N	23/10/2025
1453	28321	LIDOCAINA	RANITRAL 300	300 mg comp.rec.x 10	Lepetit	221.94	2.2194	\N	27/06/2025
1454	34166	LIDOCAINA	ONDANSETRON EPICARIS	8 mg a.x 5 x 4 ml	Veinfar	111	1.11	\N	23/10/2025
1455	26813	LIDOCAINA	SOLUC.PARENT.SOLUFLEX	hiper.cl.sod.x100ml 637H	Rivero	22.23	0.2223	\N	01/12/2024
1456	19966	LIDOCAINA	DANTENK	4 mg/2 ml iny.f.a.x 1	Biotenk	22.5	22.5	\N	13/05/2024
1457	349	LIDOCAINA	LIDOCAINA	1% f.a.x 20 ml c/epi.	Apolo	22.61	0.2261	\N	25/07/2025
1458	55692	LIDOCAINA	ACLOXIGENAC	75 mg comp.rec.x 15	Eczane	6274.94	6274.94	\N	25/07/2025
1459	18131	LIDOCAINA	XYLOCAINA	jalea jga.prell.x 20 ml	AstraZeneca	22.98	0.9192	\N	25/07/2025
1460	13178	LIDOCAINA	LIDOCAINA	2% jalea env.x 1	Veinfar	23	23	\N	25/07/2025
1461	50630	LIDOCAINA	CLORHYP 7%	monods.x 60 x 5 ml	Valmax	1413.12	1413.12	\N	22/12/2025
1462	56356	LIDOCAINA	RANITIDINA HLB 300 MG	300 mg comp.x 30	HLB Pharma	711.61	35.5805	\N	02/01/2024
1463	33059	LIDOCAINA	CURINFLAM GESIC	75 mg comp.rec.x 15	Duncan	8843.87	8843.87	\N	16/12/2025
1464	58746	LIDOCAINA	DUPRAC	10 mg comp.x 90	Savant Generic	2140	2140	\N	22/12/2025
1465	20293	LIDOCAINA	VANCOMICINA ABBOTT	Fliptop 1 g f.a.x 1	Abbott	23.8	1.19	\N	15/11/2024
1466	7409	LIDOCAINA	SOLUC.PARENT.VIAL	molar lact.sod.x100mlL71	Rivero	23.97	23.97	\N	22/12/2025
1467	47685	LIDOCAINA	KERAMIX	10 mg comp.x 10	Finadiet	240.41	10.017083	\N	27/12/2025
1468	30475	LIDOCAINA	HIDROCORTISONA RICHET	1% cr.x 30 g	Richet	24.1	0.482	\N	04/08/2025
1469	26460	LIDOCAINA	HYPERSOL	sol.x 75 ml	Cassar	24.1	0.482	\N	04/08/2025
1470	22895	LIDOCAINA	SOLUC.PARENT.FLEXIBLES	isot.clor.sodio x 3000ml	Baxter Argentin	24.3	0.486	\N	06/10/2025
1471	33543	LIDOCAINA	NALGIFLEX 75	75 mg comp.rec.x 15	Ronnet	9605	9605	\N	01/12/2025
1472	353	LIDOCAINA	LIDOCAINA	2% f.a.x 20 ml c/epi.	Apolo	24.58	24.58	\N	16/12/2025
1473	39321	LIDOCAINA	HIDROCORTISONA LARJAN	500 mg f.a.x 50 x 4 ml	Veinfar	1246	1246	\N	27/06/2025
1474	26728	LIDOCAINA	LIDOCAINA BIOCROM	2% f.a.x 20 ml s/epi.	Biocrom	25	8.333333	\N	27/12/2025
1475	26729	LIDOCAINA	LIDOCAINA BIOCROM	2% f.a.x 20 ml c/epi.	Biocrom	25	1	\N	29/10/2025
1476	36526	LIDOCAINA	NOREPINEFRINA NORTHIA	1 mg a.x 100 x 4 ml	Northia	2500	100	\N	29/10/2025
1477	29110	LIDOCAINA	NOREPINEFRINA NORTHIA	1 mg a.x 5 x 4 ml	Northia	125	125	\N	22/12/2025
1478	10602	LIDOCAINA	RANITIDINA LAZAR	300 mg comp.x 30	Lazar	757.2	15.144	\N	06/10/2025
1479	50631	LIDOCAINA	CLORHYP 7%	monods.x 24 x 5 ml	Valmax	612.38	30.619	\N	11/09/2025
1480	32103	LIDOCAINA	RECO	300 mg comp.rec.x 10	Trb-Pharma	256	256	\N	27/06/2025
1481	13202	LIDOCAINA	LIDOCAINA DENVER FARMA	1% s/epi.f.a.x 20 ml	Denver Farma	25.74	25.74	\N	22/12/2025
1482	39320	LIDOCAINA	HIDROCORTISONA LARJAN	500 mg f.a.x 1 x 4 ml	Veinfar	26	1.3	\N	23/10/2025
1483	41272	LIDOCAINA	NORADRENALINA MAX VISION	fco.a.x 50 x 4 ml	Max Vision	2600	2600	\N	25/07/2025
1484	19986	LIDOCAINA	ULCOTENK	300 mg comp.rec.x 30	Biotenk	784.24	784.24	\N	25/07/2025
1485	9267	LIDOCAINA	XYLOCAINA	adhesiva pomo x 10 g	AstraZeneca	26.2	1.31	\N	23/10/2025
1486	35291	LIDOCAINA	ONDANSETRON RICHET	4 mg a.x 1 x 2 ml	Richet	26.52	26.52	\N	16/12/2025
1487	12020	LIDOCAINA	FINOXI	8 mg comp.x 4	Finadiet	106.18	106.18	\N	19/01/2024
1488	52671	LIDOCAINA	IGLODINE 75	75 mg comp.rec.x 15	Fecofar	9616.42	9616.42	\N	15/09/2025
1489	7410	LIDOCAINA	ADITIVOS PARENTERALES	molar cl.pot.x 20ml L73	Rivero	26.81	26.81	\N	22/12/2025
1490	34604	LIDOCAINA	MIDATENK	0.5% gts.x 60 ml	Biotenk	27	27	\N	15/09/2025
1491	7407	LIDOCAINA + ADRENALINA	ADITIVOS PARENTERALES	dext.50% hipert.20mlG72	Rivero	27.33	0.2733	\N	06/04/2022
1492	32659	LIDOCAINA + ADRENALINA	REM CHOBET	5 mg/5 ml a.x 2	Soubeiran Chobe	54.96	0.5496	\N	06/04/2022
1493	12021	LIDOCAINA + ADRENALINA	FINOXI	8 mg comp.x 10	Finadiet	275.82	2.7582	\N	15/01/2003
1494	47229	LIDOCAINA + ADRENALINA	VENZIDIAK	75 mg comp.rec.x 15	Biosintex	10403	104.03	\N	12/01/2009
1495	36278	LIDOCAINA + ADRENALINA	DIFENAC	75 mg comp.rec.x 15	Lafedar	12793.78	12793.78	\N	04/07/2007
1496	31263	LIDOCAINA + ADRENALINA	GASTROZAC	300 mg comp.x 30	Klonal	847.9	847.9	\N	06/04/2022
1497	7408	LIDOCAINA + ADRENALINA	ADITIVOS PARENTERALES	dext.25% hipert.x20mlG73	Rivero	28.5	28.5	\N	01/02/2003
1498	26814	LIDOCAINA + ADRENALINA	SOLUC.PARENT.SOLUFLEX	sol.repos.hemofilt. 3075	Rivero	28.5	28.5	\N	25/04/2002
1499	24532	LIDOCAINA + ADRENALINA	MIDATENK	10 mg comp.x 20	Biotenk	572.9	572.9	\N	03/07/2003
1500	43483	LIDOCAINA + ADRENALINA	MIDAZOLAM DENVER FARMA	15 mg/3 ml a.x 1	Denver Farma	28.71	28.71	\N	25/04/2002
1501	31666	LIDOCAINA + ADRENALINA	LIGNOCAINA 4%	sol.t pica x 25 ml	Gray	28.97	28.97	\N	01/04/1995
1502	26095	LIDOCAINA + ADRENALINA	SOLUC.SALINA	env.x 500 ml	Biotech Farma *	29	29	\N	03/12/2002
1503	11660	LIDOCAINA + ADRENALINA	CETRON	4 mg a.x 1 x 2 ml	Adium	29.12	29.12	\N	03/12/2002
1504	11661	LIDOCAINA + ADRENALINA	CETRON	4 mg a.x 5 x 2 ml	Adium	146.09	146.09	\N	21/06/2003
1505	27420	LIDOCAINA + ADRENALINA	HIDROCORTISONA SHABBA	500 mg f.a.x 1	Shabba	30	30	\N	04/07/2007
1506	26576	LIDOCAINA + ADRENALINA	ONDANSETRON CEVALLOS	8 mg iny.a.x 1 x 4 ml	Cevallos	30	30	\N	04/07/2007
1507	30702	LIDOCAINA + ADRENALINA	DHARAM SINGH	Apio env.x 70 g s/sodio	Dharam Singh	30	30	\N	27/06/2008
1508	30703	LIDOCAINA + ADRENALINA	DHARAM SINGH	Cebolla env.x 70 g s/sod	Dharam Singh	30	1.2	\N	01/06/2002
1509	42054	LIDOCAINA + ADRENALINA	DHARAM SINGH	Jam n env.x 70 g s/sodio	Dharam Singh	30	1.2	\N	01/06/2002
1510	42056	LIDOCAINA + ADRENALINA	DHARAM SINGH	Paprika env.x 70 g s/sod	Dharam Singh	30	30	\N	27/11/2015
1511	30705	LIDOCAINA + ADRENALINA	DHARAM SINGH	Pimienta env.x70 g s/sod	Dharam Singh	30	30	\N	27/11/2015
1512	42055	LIDOCAINA + ADRENALINA	DHARAM SINGH	Queso azul env.x70g s/so	Dharam Singh	30	30	\N	27/06/2025
1513	30706	LIDOCAINA + ADRENALINA	DHARAM SINGH	Queso env.x 70 g s/sodio	Dharam Singh	30	1.2	\N	13/08/2025
1514	6237	LIDOCAINA + ADRENALINA	CORTENEM	susp.x 60 ml	Pfizer	30.04	1.2016	\N	29/10/2025
1515	24562	LIDOCAINA + ADRENALINA	ORAKIT MOLAR	iny.sachet x 24 x 100 ml	Fada Pharma	723	28.92	\N	29/10/2025
1516	31083	LIDOCAINA + ADRENALINA	DALAM SOLUCION ORAL	2 mg/ml fco.x 10 ml	Penn Pharmaceut	30.33	30.33	\N	22/12/2025
1517	48320	LIDOCAINA + ADRENALINA	DISIPAN 75 MG	75 mg comp.rec.x 15	Laboratorios Be	14634.44	14634.44	\N	22/12/2025
1518	41492	LIDOCAINA + ADRENALINA	FABOACID	150 mg comp.rec.x 20	Savant Generic	608.62	608.62	\N	27/06/2025
1519	26724	MAGNESIO	HIDROCORTISONA BIOCROM	500 mg a.x 1	Biocrom	30.5	0.305	\N	18/01/2003
1520	31671	MAGNESIO	FENTANILO GRAY	iny.a.x 2 ml	Gray	30.51	0.3051	\N	01/04/2002
1521	17586	MAGNESIO	HIDROCORTISONA NORTHIA	500 mg f.a.x 1	Northia	30.82	0.3082	\N	26/07/2000
1522	32538	MAGNESIO	ONDANSETRON GOBBI	4 mg iny.a.x 1 x 2 ml	Gobbi	31.24	0.52066666	\N	18/01/2003
1523	30452	MAGNESIO	GASTROZAC	150 mg/10 ml jbe.x 120ml	Klonal	31.63	3.163	\N	18/01/2003
1524	22631	MAGNESIO	TIOSALIS	4 mg f.a.x 1	Tuteur	31.74	1.587	\N	02/06/2005
1525	42769	MAGNESIO	HIDROCORTISONA 500 DUNCAN	500 mg f.a.x 100	Duncan	3190.3	106.34333	\N	01/08/2002
1526	6422	MAGNESIO	GASTROSEDOL	300 mg comp.x 30	Nova Argentia	979.77	16.3295	\N	18/01/2003
1527	41206	MAGNESIO	OMATEX	20 mg jga.prell.x 2	Phoenix	66.33	1.3266	\N	06/05/2003
1528	19060	MAGNESIO	FENTANILO NORTHIA	iny.a.x 5 ml	Northia	33.54	1.118	\N	16/08/2010
1529	46208	MAGNESIO	XYLOCAINA	1% a.x 1 x 5 ml	AstraZeneca	33.64	1.1213334	\N	06/05/2003
1530	32039	MAGNESIO	GASTROSEDOL	300 mg comp.x 20	Nova Argentia	675.46	33.773	\N	01/05/2003
1531	15654	MAGNESIO	DANTENK	8 mg/4 ml iny.f.a.x 5	Biotenk	169	8.45	\N	01/04/2009
1532	35196	MAGNESIO	SILFOX	75 mg comp.rec.x 20	Teva Argentina	111.43	11.143	\N	01/09/2011
1533	19125	MAGNESIO	SINALGICO	60 mg a.x 1 x 2 ml	Laboratorios Be	33.94	3.394	\N	21/01/2013
1534	2049	MAGNESIO	MICROSONA	1% cr.x 60 g	Valeant Argenti	33.98	0.3398	\N	15/04/2014
1535	16573	MAGNESIO	DANTENK	8 mg/4 ml iny.f.a.x 1	Biotenk	34	34	\N	01/12/2001
1536	7929	MAGNESIO	TAURAL 300	300 mg comp.x 30	Roemmers	1043.37	104.337	\N	26/10/2015
1537	44717	MAGNESIO	VOLTAREN 75	75 mg comp.rec.x 20	Novartis	151.23	2.5205	\N	26/06/2007
1538	32415	MAGNESIO	LIDOCAINA LAFEDAR	1% f.a.x 20 ml s/epi.	Lafedar	34.9	3.49	\N	26/06/2007
1539	17453	MAGNESIO	DALAM	15 mg iny.a.x 1 x 3 ml	Richmond	35.06	0.58433336	\N	29/03/2012
1540	61840	MAGNESIO	ACLOXIGENAC	75 mg comp.rec.x 20	Eczane	12123.55	404.11835	\N	29/03/2012
1541	25603	MAGNESIO	FLUMANOVAG	0.5 mg/5 ml iny.a.x 1	Gobbi	35.73	2.382	\N	11/09/2014
1542	37892	MAGNESIO	LOCOID CRELO	0.1% emuls.x 30 g	Eurolab	35.9	35.9	\N	17/09/2002
1543	30977	MAGNESIO	MAGNESIO CLORURO	pote x 1000 g	Pharma del Plat	36.06	0.75125	\N	30/12/2016
1544	16752	MAGNESIO	ONDANSETRON LAZAR	4 mg iny.a.x 1	Lazar	36.1	1.5041667	\N	30/12/2016
1545	7374	MAGNESIO	SOLUC.ANTICOAGULANTE ENV.VIDRIO VIAL	ACD x 100 ml C55	Rivero	36.3	0.726	\N	10/07/2003
1546	25368	MAGNESIO	SINALGICO	0.5% sol.oft.x 10 ml	Laboratorios Be	36.67	36.67	\N	02/12/2003
1547	42053	MAGNESIO	FIBRINOX	20mg jga.prell.x10x0.2ml	Novartis-Sandoz	370.38	370.38	\N	02/12/2003
1548	15653	MAGNESIO	HIDROCORTISONA	500 mg f.a.x 1 est.	Richmond	37.2	37.2	\N	01/06/2002
1549	36264	MAGNESIO	HIDROCORTISONA LEMAX	500 mg f.a.x 1	Lemax	37.2	37.2	\N	17/09/2002
1550	48009	MAGNESIO	ACUVAIL	viales unids.x 30 x0.4ml	Abbvie	1118.2	37.273335	\N	20/02/2017
1551	7230	MAGNESIO	NITROGRAY	25 mg a.x 5 ml	Gray	37.54	0.6256667	\N	01/07/2021
1552	42092	MAGNESIO	FIBRINOX	20mg jga.prell.x2x0.2ml	Novartis-Sandoz	75.2	75.2	\N	03/12/2002
1553	32414	MAGNESIO	LIDOCAINA LAFEDAR	2% f.a.x 20 ml s/epi.	Lafedar	37.9	0.379	\N	06/04/2022
1554	43417	MAGNESIO	MIDAZOLAM KILAB	5 mg/ml a.x 1 x 3 ml	Kilab	37.98	37.98	\N	11/01/2011
1555	45088	MAGNESIO	MIDAZOLAM KILAB	5 mg/ml a.x 100 x 3 ml	Kilab	3798	3798	\N	18/01/2003
1556	6886	MAGNESIO	SOLUC.PARENT.500 ML	agua bidest.apirog.	Roux Ocefa	38.33	38.33	\N	25/02/2004
1557	7397	MAGNESIO	ADITIVOS PARENTERALES	sulf.cinc x 10ml G54	Rivero	38.49	38.49	\N	01/09/2000
1558	37891	MAGNESIO	LOCOID LIPOCREAM	0.1% cr.x 30 g	Eurolab	38.5	0.77	\N	26/04/2002
1559	25918	MAGNESIO	METAFLEX 75	75 mg comp.rec.x 20	Montpellier	20101.92	3350.32	\N	21/04/2015
1560	45461	MAGNESIO	ENOXAPARINA 20 DOSA	20 mg jga.prell.x 1	Dosa	39	39	\N	01/06/2002
1561	11597	MAGNESIO	EMIVOX	4 mg a.x 1	Phoenix	39.17	39.17	\N	17/04/2009
1562	45463	MAGNESIO	ENOXAPARINA 20 DOSA	20 mg jga.prell.x 2	Dosa	79	0.79	\N	26/04/2002
1563	23318	MAGNESIO	VINGIONAL	300 mg comp.x 30	Fabra	1185.07	1185.07	\N	17/09/2002
1564	45464	MAGNESIO	ENOXAPARINA 20 DOSA	20 mg jga.prell.x 10	Dosa	396	3.96	\N	28/01/2019
1565	18527	MAGNESIO	SOLUC.PARENT.FLEXIBLES	isot.clor.sodio x 1000ml	Baxter Argentin	39.8	39.8	\N	15/03/2007
1566	32413	MAGNESIO	LIDOCAINA LAFEDAR	2% f.a.x 20 ml c/epi.	Lafedar	39.9	0.399	\N	12/08/2021
1567	43268	MAGNESIO	SOLUC.PARENT.FLEXIBLES	sol.fis.p/irrig.x 3000ml	Baxter Argentin	39.9	0.665	\N	09/12/2024
1568	5075	MAGNESIO	ZOFRAN	4 mg comp.x 10	GlaxoSmithKline	399.51	6.6585	\N	09/12/2024
1569	38670	MAGNESIO	DHARAM SINGH	Apio env.x 140 g s/sodio	Dharam Singh	40	1	\N	13/11/2024
1570	38671	MAGNESIO	DHARAM SINGH	Cebolla env.x140 g s/sod	Dharam Singh	40	1.3333334	\N	02/12/2024
1571	46950	MAGNESIO	MIDALAN	5 mg iny.x 2 x 5 ml	Lafedar	80.01	1.3335	\N	29/10/2025
1572	8053	MAGNESIO	NITRO-DUR	5 mg apos.x 30	MSD Argentina S	1208.32	8.055467	\N	29/10/2025
1573	19831	MAGNESIO	FENTANILO FABRA	iny.x 1 x 5 ml	Fabra	40.4	1.3466667	\N	29/10/2025
1574	25689	MAGNESIO	ONDANSETRON ASOFARMA	8 mg a.x 1 x 4 ml	Asofarma	40.74	0.679	\N	01/11/2025
1575	47046	MAGNESIO	DORIXINA FORTE NF	60 mg a.x 3	Roemmers	123.13	4.1043334	\N	01/11/2025
1576	5882	MAGNESIO	VIZERUL	300 mg comp.x 30	Montpellier	1244.71	41.490334	\N	29/10/2025
1577	24235	MAGNESIO	STIEFCORTIL	1% cr.x 30 g	Stiefel Arg.	41.61	1.387	\N	01/08/2025
1578	17501	MAGNESIO	ONDANSETRON FILAXIS	8 mg comp.x 10	Filaxis	417.11	6.9518332	\N	10/11/2025
1579	18530	MAGNESIO	SOLUC.PARENT.FLEXIBLES	agua p/irrig.x 3000 ml	Baxter Argentin	42	1.4	\N	01/08/2025
1580	41323	MAGNESIO	LORBIFENAC	75 mg comp.rec.x 28	Filaxis Farmac	28.81	0.96033335	\N	21/08/2025
1581	32299	MAGNESIO	PRAUX	0.5% gts.x 20 ml	Savant Consumer	42.63	1.421	\N	21/08/2025
1582	16751	MAGNESIO	ONDANSETRON LAZAR	8 mg comp.x 8	Lazar	342	5.7	\N	08/07/2025
1583	12897	MAGNESIO	VOLTAREN 75	75 mg comp.rec.x 28	Novartis	110.58	3.686	\N	23/12/2025
1584	36525	MAGNESIO	DAUXONA	25 mg iny.f.a.x 50 x 5ml	Northia	2150	215	\N	21/08/2025
1585	18524	MAGNESIO	SOLUC.PARENT.FLEXIBLES	isot.clor.sodio x 100 ml	Baxter Argentin	43	1.4333333	\N	23/12/2025
1586	16328	MAGNESIO	ESPASEVIT	8 mg comp.x 10	Richmond	432.01	7.2001667	\N	30/12/2025
1587	21834	MAGNESIO	REGIOCAINA JALEA	2% estuche pomo x 25 ml	Richmond	43.21	0.4321	\N	05/11/2021
1588	23588	MAGNESIO	SOLUC.PARENT.PARENTGLASS	G85 Traximin 10% x 50 ml	Rivero	43.24	1.8016666	\N	30/12/2025
1589	35531	MAGNESIO	INDICAN GEL	5% pote x 18 g	Sidus	43.5	0.435	\N	17/12/2025
1590	7666	MAGNESIO	SOLUC.PARENT.PARENTGLASS	G69 amino .8.5%aguax50ml	Rivero	43.51	0.7251667	\N	23/12/2025
1591	40340	MAGNESIO	LIDOCAINA NORGREEN	1% a.x 1 x 20 ml	Norgreen	43.95	1.465	\N	23/12/2025
1592	40344	MAGNESIO	LIDOCAINA NORGREEN	2% a.x 1 x 20 ml	Norgreen	43.95	0.879	\N	17/12/2025
1593	40358	MAGNESIO	LIDOCAINA NORGREEN	1% a.x1 x 20 ml c/epi.	Norgreen	43.95	1.83125	\N	23/12/2025
1594	40342	MAGNESIO	LIDOCAINA NORGREEN	1% f.a.x1 x 20 ml c/epi.	Norgreen	43.95	1.465	\N	23/12/2025
1595	40359	MAGNESIO	LIDOCAINA NORGREEN	2% a.x1 x 20 ml c/epi.	Norgreen	43.95	2.1975	\N	17/12/2025
1596	40345	MAGNESIO	LIDOCAINA NORGREEN	2% f.a.x1 x 20 ml c/epi.	Norgreen	43.95	43.95	\N	21/08/2025
1597	9354	MAGNESIO	NITRO-DUR	5 mg apos.x 10	MSD Argentina S	439.92	4.3992	\N	11/08/2025
1598	14038	MAGNESIO	LIGNOCAINA GRAY	1% f.a.x 20 ml c/epi.	Gray	44	1.76	\N	06/10/2025
1599	12023	MAGNESIO	FINOXI	8 mg a.x 5	Finadiet	220.51	220.51	\N	13/05/2024
1600	10774	MAGNESIO	NITROGLICERINA RICHMOND	a.x 1 x 5 ml	Richmond	44.33	0.4433	\N	13/08/2025
1601	37676	MAGNESIO	SULFATO DE MAGNESIO BIOL	a.x 100 x 5 ml	Biol	4436.05	4436.05	\N	23/08/2024
1602	14301	MAGNESIO	LIGNOCAINA GRAY	1% f.a.x 20 ml	Gray	44.67	0.4467	\N	04/08/2025
1603	27424	MAGNESIO	LIDOCAINA SHABBA	spray x 50 g	Shabba	45	45	\N	23/12/2025
1604	7372	MAGNESIO	SOLUC.ANTICOAGULANTE ENV.VIDRIO VIAL	citr.sod.46.7% x 30mlC52	Rivero	45.38	45.38	\N	23/08/2024
1605	12022	MAGNESIO	FINOXI	8 mg a.x 1	Finadiet	45.58	45.58	\N	23/12/2025
1606	37166	MEROPENEM	LORBIFENAC	75 mg comp.rec.x 30	Filaxis Farmac	25.35	25.35	\N	06/11/1995
1607	13665	MEROPENEM	HIDROCORTISONA FABRA	500 mg f.a.x 1	Fabra	46.59	46.59	\N	01/11/1995
1608	15493	MEROPENEM	HOLOMAGNESIO	gran.efer.x 200 g	Phoenix	46.69	46.69	\N	22/02/2011
1609	26056	MEROPENEM	KETOROLAC ABBOTT	60 mg f.a.x 12 x 2 ml	Abbott	562.59	562.59	\N	18/11/2002
1610	30271	MEROPENEM	MIDAZOLAN GEMEPE	50 mg/10 ml iny.a.x 10	Gemepe	470	470	\N	12/12/2011
1611	12360	MEROPENEM	ENETEGE	a.x 1 x 5 ml	Fada Pharma	48.08	48.08	\N	22/02/2011
1612	47230	MEROPENEM	VENZIDIAK	75 mg comp.rec.x 30	Biosintex	60	60	\N	05/10/2015
1613	31557	MEROPENEM	MURO 128 5%	ung.oft.x 3.5 g	Bausch & Lomb A	48.37	48.37	\N	16/06/2017
1614	53697	MEROPENEM	RELIVERAN LP 30	30 mg comp.lib.prol.x 10	Gador	486.8	9.736	\N	11/11/2019
1615	42829	MEROPENEM	DICLOFILAB	75 mg comp.rec.x 30	Inmunolab	61.6	2.464	\N	24/09/2020
1616	30109	MEROPENEM	GOBBICAINA	1% PPP a.x 20 ml	Gobbi	48.93	1.9572	\N	10/08/2022
1617	17086	MEROPENEM	EFFICORT	Lipocrema x 30 g	Galderma	49.07	49.07	\N	23/09/2020
1618	48036	MEROPENEM	ONDANSETRON VANNIER	8 mg comp.x 10	Vannier	491.21	49.121	\N	23/09/2020
1619	5695	MEROPENEM	ZANTAC	jbe.x 120 ml	GlaxoSmithKline	49.23	49.23	\N	01/08/2021
1620	41495	MEROPENEM	FABOACID	300 mg comp.rec.x 30	Savant Generic	1514.77	60.5908	\N	24/09/2020
1621	22258	MEROPENEM	RANITIDINA BIOL	50 mg a.x 100 x 5 ml	Biol	5166.27	5166.27	\N	10/08/2022
1622	16979	MEROPENEM	VANCOTIE	500 mg iny f.a.x 1	Bioprofarma Bag	51.83	2.0732	\N	10/08/2022
1623	46121	MEROPENEM	DICLOFENAC TECHSPHERE	75 mg comp.rec.x 30	Techsphere	113.85	11.385	\N	23/09/2020
1624	46876	MEROPENEM	ZERODOL	10 mg comp.subl.x 10	Bag	520.04	520.04	\N	23/09/2020
1625	17085	MEROPENEM	EFFICORT	cr.x 30 g	Galderma	52.06	52.06	\N	01/08/2021
1626	48321	MEROPENEM	DISIPAN 75 MG	75 mg comp.rec.x 30	Laboratorios Be	1285.91	1285.91	\N	01/08/2021
1627	8054	MEROPENEM	NITRO-DUR	10 mg apos.x 30	MSD Argentina S	1575.47	1575.47	\N	10/08/2022
1628	35292	MEROPENEM	ONDANSETRON RICHET	8 mg a.x 1 x 4 ml	Richet	53.05	53.05	\N	11/08/2025
1629	24237	MEROPENEM	STIEFCORTIL	1% loc.cap.x 60 ml	Stiefel Arg.	53.17	53.17	\N	17/12/2025
1630	38097	MEROPENEM	IGLODINE 75	75 mg comp.rec.x 30	Fecofar	16552.27	1655.227	\N	13/06/2024
1631	16329	MEROPENEM	ESPASEVIT	4 mg a.x 1 x 2 ml	Richmond	53.37	1.0674	\N	06/10/2025
1632	16183	MEROPENEM	ONDANSETRON	4 mg a.x 1 x 2 ml	Richmond	53.37	2.1348	\N	06/10/2025
1633	6893	MEROPENEM	SOLUC.PARENT.500 ML	Aminocefa R	Roux Ocefa	53.51	2.1404	\N	06/10/2025
1634	41283	MEROPENEM	FENTANILO KILAB	0.25 mg iny.a.x 1 x 5 ml	Kilab	54.04	1.0808	\N	20/12/2025
1635	41285	MEROPENEM	FENTANILO KILAB	0.25 mg iny.a.x 100x 5ml	Kilab	5404.36	216.1744	\N	23/10/2025
1636	27814	MEROPENEM	FENTANILO DENVER FARMA	0.25 mg iny.a.x 5 ml	Denver Farma	54.06	54.06	\N	03/04/2024
1637	30122	MEROPENEM	ONDANSETRON NORTHIA	4 mg a.x 1 x 2 ml	Northia	54.37	54.37	\N	20/12/2025
1638	46875	MEROPENEM	ZERODOL	20 mg comp.x 10	Bag	545.71	21.8284	\N	13/08/2025
1639	7791	MEROPENEM	HIDROCORTISONA RICHET	1 g liof.f.a.x 1	Richet	54.74	54.74	\N	03/04/2024
1640	45325	MEROPENEM	HIDROCORTISONA NORTHIA	500 mg f.a.x 100	Northia	5490	5490	\N	11/08/2025
1641	44437	MEROPENEM	NALGIFLEX 75	75 mg comp.rec.x 30	Ronnet	19785	1978.5	\N	13/06/2024
1642	40046	MEROPENEM	TELEDOL	60 mg amp.x 3 x 2 ml	Casasco	165.68	6.6272	\N	27/06/2025
1643	13799	MEROPENEM	DICLOGESIC	75 mg comp.rec.x 30	Trb-Pharma	20800	832	\N	27/06/2025
1644	17195	MEROPENEM	NOTRAB	150 mg comp.rec.x 60	Microsules Arg.	3362.35	67.247	\N	12/12/2025
1645	31662	MEROPENEM	MIDAZOLAM GRAY	50 mg iny.a.x 1 x 10 ml	Gray	56.73	2.2692	\N	13/08/2025
1646	58631	MEROPENEM	FLOGOLISIN	75 mg comp.rec.x 30	Lazar	28201.07	564.0214	\N	20/12/2025
1647	16905	MEROPENEM	VANCOMICINA BIOCROM	500 mg iny.f.a.x 1	Biocrom	57.5	57.5	\N	20/12/2025
1648	25809	MEROPENEM	LIDOCAINA	1% c/epi.f.a.x 25 x 20ml	Norgreen	1444.85	34.40119	\N	23/10/2025
1649	15735	MEROPENEM	VANCOMICINA NORTHIA	500 mg iny.f.a.x 1	Northia	57.94	1.1588	\N	04/08/2025
1650	35651	MEROPENEM	FABOMICINA	500 mg iny.a.x 1	Fabop	58	1.16	\N	12/12/2025
1651	49831	MEROPENEM	GASTROSEDOL RAPID	150 mg comp.eferv.x 10	Nova Argentia	584.45	11.689	\N	04/08/2025
1652	16489	METOCLOPRAMIDA	MEROZEN	500 mg IM vial x 1	AstraZeneca	59.39	0.11878	\N	14/06/2002
1653	16540	METOCLOPRAMIDA	ZEROPENEM	500 mg IM a.x 1+dil.a.x1	Sanofi-Aventis	59.39	0.11878	\N	14/06/2002
1654	9355	METOCLOPRAMIDA	NITRO-DUR	10 mg apos.x 10	MSD Argentina S	598.39	59.839	\N	03/04/1995
1655	25808	METOCLOPRAMIDA	LIDOCAINA	1% s/epi.f.a.x 25 x 20ml	Norgreen	1502.87	75.1435	\N	18/01/2003
1656	48160	METOCLOPRAMIDA	TAURAL EFERVESCENTE	150 mg comp.eferv.x 10	Roemmers	610.34	30.517	\N	01/09/2005
1657	30474	METOCLOPRAMIDA	HIDROCORTISONA RICHET	1% cr.x 15 g	Richet	62.08	1.2416	\N	07/02/2014
1658	49572	METOCLOPRAMIDA	HYPERSOL	3% spray nasal x 28 ml	Cassar	62.22	3.111	\N	19/12/2014
1659	25813	METOCLOPRAMIDA	LIDOCAINA	2% s/epi.f.a.x 25 x 20ml	Norgreen	1560.8	1560.8	\N	08/08/2008
1660	25920	METOCLOPRAMIDA	METAFLEX 75	75 mg comp.rec.x 40	Montpellier	25832.5	2583.25	\N	15/09/2014
1661	25815	METOCLOPRAMIDA	LIDOCAINA	2% c/epi.f.a.x 25 x 20ml	Norgreen	1569.07	31.3814	\N	10/07/2003
1662	782	METOCLOPRAMIDA	XYLOCAINA	viscosa fco.got.x 50 ml	AstraZeneca	63.62	6.362	\N	15/03/2014
1663	46209	METOCLOPRAMIDA	XYLOCAINA	2% a.x 1 x 5 ml	AstraZeneca	63.79	10.631667	\N	01/02/2003
1664	27720	METOCLOPRAMIDA	KLONAM	500 mg IM f.a.x 1	Klonal	64.09	10.681666	\N	20/02/2002
1665	18003	METOCLOPRAMIDA	DALAM	15 mg iny.a.x 100 x 3 ml	Richmond	6445.66	64.4566	\N	13/06/2000
1666	22093	METOCLOPRAMIDA	FLUXIFARM	0.5 mg a.x 20 x 5 ml	Richmond	1298.4	216.4	\N	01/04/2002
1667	16492	METOCLOPRAMIDA	ONDANSETRON DENVER FARMA	8 mg/4 ml iny.a.x 5	Denver Farma	330.11	3.3011	\N	13/06/2000
1668	42094	METOCLOPRAMIDA	FIBRINOX	40mg jga.prell.x10x0.4ml	Novartis-Sandoz	670.41	670.41	\N	03/04/1995
1669	26521	METOCLOPRAMIDA	GOBBICAINA	1% c/epi.f.a.x 20 ml	Gobbi	67.3	67.3	\N	03/04/1995
1670	41208	METOCLOPRAMIDA	OMATEX	40 mg jga.prell.x 2	Phoenix	135.73	45.243332	\N	03/04/2002
1671	25580	METOCLOPRAMIDA	GOBBIZOLAM	15 mg iny.a.x 1 x 3 ml	Gobbi	67.96	11.326667	\N	03/04/2002
1672	13198	METOCLOPRAMIDA	LIDOCAINA DENVER FARMA	2% s/epi.f.a.x 20 ml (H)	Denver Farma	68.15	0.6815	\N	14/06/2002
1673	42093	METOCLOPRAMIDA	FIBRINOX	40mg jga.prell.x2x0.4ml	Novartis-Sandoz	138.11	6.9055	\N	26/06/2014
1674	25604	METOCLOPRAMIDA	FLUMANOVAG	0.5 mg/5 ml iny.a.x 5	Gobbi	347.2	347.2	\N	20/02/2003
1675	45465	METOCLOPRAMIDA	ENOXAPARINA 40 DOSA	40 mg jga.prell.x 1	Dosa	69.5	23.166666	\N	20/11/2008
1676	45466	METOCLOPRAMIDA	ENOXAPARINA 40 DOSA	40 mg jga.prell.x 2	Dosa	140	1.4	\N	27/12/2012
1677	27425	METOCLOPRAMIDA	LIDOCAINA SHABBA	spray x 82 g	Shabba	70	0.7	\N	04/11/2008
1678	45467	METOCLOPRAMIDA	ENOXAPARINA 40 DOSA	40 mg jga.prell.x 10	Dosa	702	702	\N	06/11/2000
1679	26846	METOCLOPRAMIDA	HIDROCORTISONA	2% cr.x 15 g	Klonal	71.07	11.845	\N	31/12/2013
1680	14715	METOCLOPRAMIDA	VANCOTENK	500 mg iny.f.a.x 1	Biotenk	72	72	\N	18/01/2003
1681	5040	METOCLOPRAMIDA	ZOFRAN	4 mg a.x 1	GlaxoSmithKline	73.27	73.27	\N	24/11/2010
1682	54511	METOCLOPRAMIDA	MIDAZOLAM KILAB	5 mg/ml a.x 3 x 3 ml	Kilab	220	220	\N	06/04/2022
1683	25502	METOCLOPRAMIDA	FIORITINA	4 mg a.x 5 x 4 ml	Fada Pharma	380	380	\N	01/07/2002
1684	16753	METOCLOPRAMIDA	ONDANSETRON LAZAR	8 mg iny.a.x 1	Lazar	76	76	\N	19/12/2014
1685	26522	METOCLOPRAMIDA	GOBBICAINA	2% c/epi.f.a.x 20 ml	Gobbi	76.37	76.37	\N	18/07/1995
1686	11663	METOCLOPRAMIDA	CETRON	8 mg a.x 5 x 4 ml	Adium	383.54	383.54	\N	20/11/2008
1687	11662	METOCLOPRAMIDA	CETRON	8 mg a.x 1 x 4 ml	Adium	76.71	25.57	\N	16/09/2014
1688	18025	METOCLOPRAMIDA	DAUXONA	25 mg iny.f.a.x 1 x 5 ml	Northia	76.76	76.76	\N	26/04/2002
1689	52459	METOCLOPRAMIDA	BIZILLA SOLUCION SALINA	soluc.x 240 ml	Microsules Arg.	77	3.2083333	\N	17/03/2003
1690	58676	METOCLOPRAMIDA	VENZIDIAK	75 mg comp.rec.x 900	Biosintex	23973	23973	\N	25/04/2008
1691	3451	METOCLOPRAMIDA	SOLUC.CLORURADA HIPERTONICA FADA	20% f.a.x 25 x 30 ml	Fada Pharma	1951.75	1951.75	\N	01/08/2008
1692	6880	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	fisiol.ringer c/lactato	Roux Ocefa	78.18	78.18	\N	15/04/2011
1693	20069	METOCLOPRAMIDA	VANCOMAX	1000 mg f.a.x 1	Klonal	78.48	78.48	\N	06/08/2012
1694	16724	METOCLOPRAMIDA	VAREDET	500 mg iny.f.a.x 1 x10ml	Fada Pharma	78.99	78.99	\N	28/11/2013
1695	5077	METOCLOPRAMIDA	ZOFRAN	8 mg comp.x 10	GlaxoSmithKline	799.02	799.02	\N	08/05/2008
1696	15820	METOCLOPRAMIDA	HIDROCORTISONA FABRA	1000 mg f.a.x 1	Fabra	79.97	79.97	\N	20/11/2008
1697	20834	METOCLOPRAMIDA	REGIOCAINA SPRAY	10% spray x 50 g	Richmond	81.5	81.5	\N	06/08/2004
1698	49516	METOCLOPRAMIDA	FENTANOVAG	iny.x 1 x 5 ml	Gobbi	81.52	4.076	\N	12/01/2022
1699	7370	METOCLOPRAMIDA	SOLUC.PARENT.PARENTGLASS	glic.10%dex.5% 500ml983A	Rivero	82.11	82.11	\N	05/03/2016
1700	29495	METOCLOPRAMIDA	DICLOFENAC PHARMA	75 mg comp.x 10	Pharma del Plat	15.3	0.153	\N	12/08/2021
1701	16980	METOCLOPRAMIDA	VANCOTIE	1000 mg iny f.a.x 1	Bioprofarma Bag	83.07	0.8307	\N	01/08/2021
1702	13414	METOCLOPRAMIDA	DUROGESIC	25 mcg/h parches x 5	Janssen-Cilag	416.5	20.825	\N	18/06/2024
1703	11600	METOCLOPRAMIDA	EMIVOX	8 mg a.x 5	Phoenix	431.99	21.5995	\N	16/12/2025
1704	11599	METOCLOPRAMIDA	EMIVOX	8 mg a.x 1	Phoenix	86.49	4.3245	\N	01/01/2026
1705	30435	METOCLOPRAMIDA	CEFIMEN-K	2 g iny.f.a.x 1	Klonal	87	4.35	\N	29/12/2025
1706	36959	METOCLOPRAMIDA	DIOXAFLEX	75 mg comp.x 10	Bag	71.01	3.5505	\N	29/12/2025
1707	36367	METOCLOPRAMIDA	ALGIOXIB	75 mg comp.x 10	Ferring	193.53	64.51	\N	09/02/2024
1708	5111	METOCLOPRAMIDA	VANCOCIN	500 mg f.a.x 1	Eli Lilly	88.83	8.883	\N	29/12/2025
1709	30110	METOCLOPRAMIDA	GOBBICAINA	2% PPP a.x 20 ml	Gobbi	89.25	8.925	\N	29/12/2025
1710	25757	METOCLOPRAMIDA	VANCOMICINA TUTEUR	500 mg iny.a.x 1	Tuteur	89.59	0.8959	\N	06/08/2024
1711	13336	METOCLOPRAMIDA	ENETEGE-SAFEJET	jga.prell.x 1 x 5 ml	Fada Pharma	90.39	0.9039	\N	08/02/2021
1712	21595	METOCLOPRAMIDA	ENETEGE-SAFEJET	jga.prell.x 50 x 5 ml	Fada Pharma	4519.8	45.198	\N	22/12/2025
1713	17194	METOCLOPRAMIDA	NOTRAB	150 mg comp.rec.x 20	Microsules Arg.	1809.6	18.096	\N	11/08/2025
1714	37829	METOCLOPRAMIDA	COLISTINA PERMATEC	iny.f.a.x 1+disolv.x 1	Permatec	90.85	30.283333	\N	17/12/2025
1715	6888	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	dextr n 40 10% c/dext.5%	Roux Ocefa	92.23	0.9223	\N	02/07/2024
1716	42095	METOCLOPRAMIDA	FIBRINOX	60mg jga.prell.x10x0.6ml	Novartis-Sandoz	947.87	315.95667	\N	22/12/2025
1717	20974	METOCLOPRAMIDA	ZIENAM MONOVIAL	f.a.x 1	Merck Sharp & D	95.89	31.963333	\N	10/08/2022
1718	25605	METOCLOPRAMIDA	FLUMANOVAG	0.5 mg/5 ml iny.a.x 25	Gobbi	2444.36	2444.36	\N	09/02/2024
1719	45468	METOCLOPRAMIDA	ENOXAPARINA 60 DOSA	60 mg jga.prell.x 1	Dosa	98	0.98	\N	13/08/2025
1720	45469	METOCLOPRAMIDA	ENOXAPARINA 60 DOSA	60 mg jga.prell.x 2	Dosa	197	7.88	\N	27/06/2025
1721	45470	METOCLOPRAMIDA	ENOXAPARINA 60 DOSA	60 mg jga.prell.x 10	Dosa	989.8	989.8	\N	13/05/2024
1722	54515	METOCLOPRAMIDA	DICLOFENAC TEVA	75 mg comp.x 10	Teva Argentina	550.92	91.82	\N	29/12/2025
1723	30434	METOCLOPRAMIDA	CEFIMEN-K	1 g iny.f.a.x 1	Klonal	101.53	33.843334	\N	29/12/2025
1724	16185	METOCLOPRAMIDA	ONDANSETRON	8 mg a.x 1 x 4 ml	Richmond	102.02	2.0404	\N	29/10/2025
1725	47689	METOCLOPRAMIDA	KERAMIX RAPID	10 mg comp.subl.x 10	Finadiet	1054.3	1054.3	\N	18/06/2024
1726	38853	METOCLOPRAMIDA	DOLOFENAC 75	75 mg comp.x 10	Sanitas	5000	5000	\N	15/12/2025
1727	12572	METOCLOPRAMIDA	FENTAX	a.x 1 x 5 ml	Richmond	107.24	107.24	\N	30/10/2025
1728	3065	METOCLOPRAMIDA	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	511L dext.5% aguax1000ml	Rivero	107.38	107.38	\N	18/06/2024
1729	6866	METOCLOPRAMIDA	SOLUC.PARENT.250 ML	d-manitol al 15%	Roux Ocefa	107.91	107.91	\N	20/12/2025
1730	53583	METOCLOPRAMIDA	AGUA DESTILADA	a.x 100 x 10 ml	Klonal	10796.35	107.9635	\N	04/08/2025
1731	31909	METOCLOPRAMIDA	FLUMAZENIL NORTHIA	0.5 mg iny.a.x 100 x 5ml	Northia	10800	10800	\N	30/10/2025
1732	20068	METOCLOPRAMIDA	VANCOMAX	500 mg f.a.x 1	Klonal	108.56	108.56	\N	01/01/2026
1733	22092	METOCLOPRAMIDA	FLUXIFARM	0.5 mg a.x 1 x 5 ml	Richmond	108.65	108.65	\N	17/12/2025
1734	12513	METOCLOPRAMIDA	SOLUC.P/CARDIOPLEGIA RIVERO	30mEq pot.x 500ml L43/44	Rivero	109.68	109.68	\N	29/12/2025
1735	15521	METOCLOPRAMIDA	LANEXAT	0.5 mg/5 ml iny.a.x 1	Roche	109.8	109.8	\N	29/12/2025
1736	34391	METOCLOPRAMIDA	FLUMAZENIL NORTHIA	0.5 mg iny.a.x 5 x 5 ml	Northia	549.64	549.64	\N	20/12/2025
1737	46291	METOCLOPRAMIDA	ANFLETEC	500 mg IV f.a.x 1	Permatec	110	110	\N	16/12/2025
1738	16906	METOCLOPRAMIDA	VANCOMICINA BIOCROM	1000 mg iny.f.a.x 1	Biocrom	110.5	110.5	\N	29/12/2025
1739	47053	METOCLOPRAMIDA	TOTALATLAS	spray nasal x 25 ml	Lab Internacion	111.47	111.47	\N	29/12/2025
1740	45329	MIDAZOLAM	VANCOMICINA NORTHIA	500 mg iny.f.a.x 100	Northia	11320	566	\N	25/02/2002
1741	47687	MIDAZOLAM	KERAMIX	20 mg comp.rec.x 20	Finadiet	2281.72	76.057335	\N	25/02/2002
1742	40410	MIDAZOLAM	LMX 4	pomo x 5 g + 2 ap sitos	Eurolab	115.35	11.535	\N	25/02/2002
1743	7191	MIDAZOLAM	HIDROCORTISONA RICHET	100 mg liof.f.a.x 1	Richet	115.75	3.8583333	\N	01/04/2002
1744	15736	MIDAZOLAM	VANCOMICINA NORTHIA	1000 mg iny.f.a.x 1	Northia	115.9	11.59	\N	01/04/2002
1745	15584	MIDAZOLAM	MAXCEF	1 g iny.a.x 1	Merck	119.38	3.9793334	\N	21/04/2008
1746	27385	MIDAZOLAM	DALAM SOLUCION ORAL	2 mg/ml fco.x 60 ml+jga.	Penn Pharmaceut	120.55	6.0275	\N	07/11/2015
1747	28013	MIDAZOLAM	ONDANSETRON ASOFARMA	32 mg sob.x 50 ml p/inf.	Asofarma	122.22	6.111	\N	29/07/2016
1748	38417	MIDAZOLAM	VESALION	75 mg comp.x 100	Nova Argentia	378.36	37.836	\N	25/02/2002
1749	57391	MIDAZOLAM	CLORHYP FQ	3.5% monods.x 60	Everex	7442.2	744.22	\N	28/06/2002
1750	30792	MIDAZOLAM	DIOXAFLEX	75 mg comp.x 100	Bag	449.37	224.685	\N	25/02/2002
1751	42096	MIDAZOLAM	FIBRINOX	80mg jga.prell.x10x0.8ml	Novartis-Sandoz	1274.45	12.7445	\N	06/04/2022
1752	47686	MIDAZOLAM	KERAMIX	20 mg comp.rec.x 10	Finadiet	1283.6	128.36	\N	20/01/2003
1753	17196	MIDAZOLAM	NOTRAB	300 mg comp.rec.x 30	Microsules Arg.	3852.68	770.536	\N	20/01/2003
1754	6706	MIDAZOLAM	ZIENAM	500 mg IM f.a.x 1 s/dil.	Merck Sharp & D	128.92	64.46	\N	18/01/2003
1755	16539	MIDAZOLAM	ZEROPENEM	500 mg IV a.x 1	Sanofi-Aventis	129.41	12.941	\N	20/01/2003
1756	16563	MIDAZOLAM	SIROTAMICIN HC	1% cr.x 30 g	Maigal	129.83	25.966	\N	03/04/2002
1757	16564	MIDAZOLAM	SIROTAMICIN HC	2% cr.x 15 g	Maigal	129.83	64.915	\N	03/04/2002
1758	45471	MIDAZOLAM	ENOXAPARINA 80 DOSA	80 mg jga.prell.x 1	Dosa	130	13	\N	26/04/2002
1759	45472	MIDAZOLAM	ENOXAPARINA 80 DOSA	80 mg jga.prell.x 2	Dosa	261	130.5	\N	26/04/2002
1760	45473	MIDAZOLAM	ENOXAPARINA 80 DOSA	80 mg jga.prell.x 10	Dosa	1306.8	261.36	\N	28/06/2002
1761	52601	MIDAZOLAM	DIOXAFLEX	75 mg comp.x 100 (10x10)	Bag	2448.42	489.684	\N	18/01/2003
1762	25602	MIDAZOLAM	GOBBICAINA	2% s/epi.f.a.x 20 ml	Gobbi	132.09	132.09	\N	04/07/2011
1763	47513	MIDAZOLAM	KLOPENEM	500 mg f.a.x 1	Klonal	135	13.5	\N	24/06/2010
1764	38138	MIDAZOLAM	DICLOFENAC NORTHIA	75 mg comp.x 15	Northia	40.83	1.361	\N	06/07/2021
1765	39300	MIDAZOLAM	DICLOFENAC SANT GALL	75 mg comp.x 15	Sant Gall	50.35	50.35	\N	04/05/2015
1766	20067	MIDAZOLAM	KLENAC	sol.oft.x 5 ml	Klonal	143.9	143.9	\N	16/06/2017
1767	44701	MIDAZOLAM	KETOROLAC TROMETAMINA RICHET	10 mg comp.subl.x 10	Richet	1464.18	1464.18	\N	10/11/2015
1768	39370	MIDAZOLAM	MEROTENK	500 mg iny.f.a.x 1	Biotenk	152	15.2	\N	26/04/2002
1769	13415	MIDAZOLAM	DUROGESIC	50 mcg/h parches x 5	Janssen-Cilag	763	381.5	\N	07/11/2015
1770	31868	MIDAZOLAM	VIROBRON NF	75 mg comp.x 15	Temis-Lostal	54.07	54.07	\N	04/07/2011
1771	47054	MIDAZOLAM	TOTALATLAS FORTE	spray nasal x 25 ml	Lab Internacion	155.16	1.5516	\N	18/03/2020
1772	27278	MIDAZOLAM	FADA IMIPENEM	500 mg IV f.a.x 1	Fada Pharma	157	157	\N	11/09/2018
1773	30237	MIDAZOLAM	RUPEMET	10 mg a.x 100 x 2 ml	Duncan	15723.8	5241.2666	\N	10/09/2018
1774	6911	MIDAZOLAM	SOLUC.PARENT.2000 ML	agua bidest.apirog.	Roux Ocefa	157.81	157.81	\N	01/02/2004
1775	6890	MIDAZOLAM	SOLUC.PARENT.500 ML	Aminocefa 5	Roux Ocefa	157.82	5.260667	\N	24/01/2025
1776	41204	MIDAZOLAM	OMATEX	100 mg jga.prell.x 10	Phoenix	1580.43	52.681	\N	16/12/2025
1777	50064	MIDAZOLAM	FLUMAZEN	0.5 mg/5 ml iny.a.x 5	Scott-Cassar	797	79.7	\N	24/01/2025
1778	19484	MIDAZOLAM	POTASIO CLORURO BIOQUIM	15 mEq a.x 100	Duncan	16008.65	320.173	\N	08/12/2025
1779	16725	MIDAZOLAM	VAREDET	1000 mg iny.f.a.x 1x20ml	Fada Pharma	160.98	5.366	\N	08/12/2025
1780	54281	MIDAZOLAM	FENTAX	a.x 50 x 5 ml	Richmond	8051.03	268.36768	\N	12/12/2025
1781	26805	MIDAZOLAM	DUALID	50 mg a.x 100 x 5 ml	Duncan	16576.7	165.767	\N	01/08/2021
1782	46588	MIDAZOLAM	SALINDOSA	monodosis x 60 x 0.4 ml	LKM	9947.48	994.748	\N	08/12/2025
1783	57748	MIDAZOLAM	MAGNESIO VITAL A.M.	comp. x 60	A.M. Farma Acti	10000	500	\N	12/12/2025
1784	27368	MIDAZOLAM	MAGNESIO VITAL A.M.	c ps.x 60	A.M. Farma Acti	10000	1000	\N	20/08/2025
1785	24661	MIDAZOLAM	LIDOCAINA SPRAY	10% spray x 50 g	Scott-Cassar	170.62	170.62	\N	13/05/2024
1786	53612	MIDAZOLAM	LIDOCAINA	1% f.a.x 30 x 20 ml	Klonal	5123	512.3	\N	02/01/2024
1787	53614	MIDAZOLAM	LIDOCAINA	2% f.a.x 30 x 20 ml	Klonal	5123	512.3	\N	12/12/2025
1788	36413	MIDAZOLAM	GRAY-F	100 mcg caram.x 5	Gray	878.87	43.9435	\N	02/01/2024
1789	17488	MIDAZOLAM	ONDANSETRON LKM 8	8 mg a.x 5	LKM	880	8.8	\N	13/08/2025
1790	20624	MIDAZOLAM	ICOPLAX	500 mg iny.f.a.	Richmond	176.12	176.12	\N	18/12/2023
1791	39371	MIDAZOLAM	MEROTENK	1000 mg iny.f.a.x 1	Biotenk	179	1.79	\N	06/10/2025
1792	779	MIDAZOLAM	XYLOCAINA	jalea x 25 ml	AstraZeneca	182.47	3.6494	\N	02/07/2024
1793	26820	MIDAZOLAM	DICLOFENAC HEXA 75 RETARD	75 mg comp.x 15	Fada Pharma	55.95	0.5595	\N	23/10/2025
1794	13416	MIDAZOLAM	DUROGESIC	75 mcg/h parches x 5	Janssen-Cilag	925.66	37.0264	\N	27/06/2025
1795	35223	MIDAZOLAM	VIARTRIL NF	75 mg comp.x 15	Spedrog Caillon	70.06	2.8024	\N	27/06/2025
1796	52427	MIDAZOLAM	SALINDOSA	monodosis x 12 x 0.4 ml	LKM	2240.1	89.604	\N	25/07/2025
1797	780	MIDAZOLAM	XYLOCAINA	pda.x 30 g	AstraZeneca	186.75	18.675	\N	02/01/2024
1798	7412	MIDAZOLAM	SOLUC.PARENT.PARENTGLASS	947A dext.70 6%sal.500ml	Rivero	187.98	1.8798	\N	04/08/2025
1799	12250	MIDAZOLAM	ONDANSETRON LKM 8	8 mg a.x 1	LKM	190	7.6	\N	08/12/2025
1800	31140	MIDAZOLAM	MAGNESIO	comp.x 40	Nativa	7710	77.1	\N	01/01/2025
1801	54273	MIDAZOLAM	MAGNESIO NATULIV	comp.x 30	Laboratorio ENA	5800	580	\N	24/07/2023
1802	56032	MIDAZOLAM	ALGINON	30 mg iny.a.x 100 x 1 ml	Duncan	19523.6	4880.9	\N	01/01/2026
1803	15585	MIDAZOLAM	MAXCEF	2 g iny.a.x 1	Merck	200.11	50.0275	\N	01/01/2026
1804	7415	MIDAZOLAM	SOLUC.PARENT.PARENTGLASS	950A dext.40 10% x 500ml	Rivero	200.31	50.0775	\N	01/01/2026
1805	18927	NITROGLICERINA	SOLUC.PARENT.PARENTGLASS	951A dextr.40 10%x 500ml	Rivero	200.31	6.677	\N	20/01/2003
1806	36415	NITROGLICERINA	GRAY-F	400 mcg caram.x 5	Gray	1004.93	33.497665	\N	01/06/2002
1807	12375	NITROGLICERINA	SOLUC.FISIOLOGICA FADA	1.5 mEq a.x 100 x 10 ml	Fada Pharma	20131.97	671.0657	\N	01/05/2006
1808	12352	NITROGLICERINA	AGUA PARA INYECCION FADA	a.x 100 x 10 ml	Fada Pharma	20360.31	2036.031	\N	01/06/2002
1809	55409	NITROGLICERINA	AGUA DESTILADA INYECTABLE	env.x 250 ml	B. Braun	204.5	6.8166666	\N	01/06/2002
1810	14926	NITROGLICERINA	ONDANSETRON FILAXIS	8 mg/4 ml sol.iny.x 1	Fresenius Kabi	204.64	20.464	\N	01/06/2002
1811	7376	NITROGLICERINA	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	520A isot.cl.sod.x 500ml	Rivero	207.06	6.902	\N	01/05/2006
1812	51721	NITROGLICERINA	DICLOGRAND	75 mg comp.x 15	Lab Internacion	82.18	2.7393334	\N	02/02/2015
1813	30123	NITROGLICERINA	ONDANSETRON NORTHIA	8 mg a.x 1 x 4 ml	Northia	209.97	20.997	\N	27/07/2012
1814	31766	NITROGLICERINA	MAGNESIO LAFARMEN	bl ster comp.x 60	Lafarmen	12600	1260	\N	02/02/2015
1815	6891	NITROGLICERINA	SOLUC.PARENT.500 ML	Aminocefa 7.5	Roux Ocefa	213.34	7.1113334	\N	02/02/2015
1816	17729	NITROGLICERINA	ANUSOL HC	cr.x 10 g	Elea	213.6	213.6	\N	30/09/2013
1817	36536	NITROGLICERINA	SOLUC.FISIOLOGICA NORTHIA	iny.a.x 100	Northia	21461.69	21461.69	\N	01/04/1995
1818	35388	NITROGLICERINA	DICLONEX 75	75 mg comp.x 15	Nexo Pharmaceut	128	4.266667	\N	21/06/2017
1819	50597	NITROGLICERINA	NUTRASONA	cr.x 30 g	Isdin	218.13	4.3626	\N	16/06/2005
1820	61705	NITROGLICERINA	MAGNESIO LAFARMEN	bl ster comp.x 150	Lafarmen	33000	33000	\N	28/01/2003
1821	46292	NITROGLICERINA	ANFLETEC	1000 mg IV f.a.x 1	Permatec	220	220	\N	09/01/2009
1822	4592	NITROGLICERINA	SOLUC.PARENT.SOLUFLEX	620H isot.cl.sod.x 100ml	Rivero	220.14	220.14	\N	04/07/2011
1823	778	NITROGLICERINA	XYLOCAINA	4% fco.gotero x 25 ml	AstraZeneca	220.88	7.3626666	\N	21/06/2017
1824	45400	NITROGLICERINA	DICLOFENAC SODICO RICHET	75 mg comp.x 15	Richet	139.14	13.914	\N	09/04/2018
1825	38288	NITROGLICERINA	FURITAL	20 mg a.x 1 x 2 ml	Rivero	223.98	223.98	\N	03/04/2002
1826	59711	NITROGLICERINA	FURITAL	20 mg a.x 100 x 2 ml	Rivero	22398.25	22398.25	\N	26/04/2002
1827	45330	NITROGLICERINA	VANCOMICINA NORTHIA	1000 mg iny.f.a.x 100	Northia	22460	449.2	\N	26/04/2002
1828	55485	NITROGLICERINA	DOLTEN	30 mg iny.a.x 50 x 2 ml	Pfizer	11265.57	112.6557	\N	27/06/2025
1829	36043	NITROGLICERINA	MAGNESIO LAFARMEN	bl ster comp.x 30	Lafarmen	6800	68	\N	27/06/2025
1830	33244	NITROGLICERINA	OFTALOOK	fco.gotero x 10 ml	Denver Farma	227.63	2.2763	\N	25/07/2025
1831	11179	NITROGLICERINA	SOLUC.CLORURADA HIPERTONICA FADA	20% a.x 50 x 20 ml	Fada Pharma	11417	456.68	\N	25/07/2025
1832	55407	NITROGLICERINA	SOL.MOLAR CLORURO DE POTASIO	env.x 100 ml	B. Braun	229.15	4.583	\N	18/12/2024
1833	4415	NITROGLICERINA	ZIENAM	500 mg IV f.a.x 1	MSD Argentina S	229.66	2.2966	\N	13/08/2025
1834	7385	NITROGLICERINA	SOLUC.PARENT.SOLUFLEX	620Q isot.cl.sod.x 250ml	Rivero	229.7	229.7	\N	18/12/2024
1835	21792	NITROGLICERINA	MAGNESIO 100	c ps.x 60	Natufarma	13831	13831	\N	02/09/2024
1836	33724	NITROGLICERINA	FENTANILO LAZAR	0.25 mg/5 ml iny.a.x 3	Lazar	695.96	695.96	\N	30/12/2025
1837	55290	NORADRENALINA	SOL.DEXTROSA AL 10% EN AGUA	env.x 250 ml	B. Braun	232.49	232.49	\N	03/04/2002
1838	43005	NORADRENALINA	MAGNESIO SPORT	comp.x 30	Natufarma	7084	1416.8	\N	16/06/2005
1839	27721	NORADRENALINA	KLONAM	500 mg IV f.a.x 1	Klonal	236.26	2.3626	\N	25/01/2012
1840	18167	NORADRENALINA	LIDOCAINA 5% HIPERBARICA	a.x 5 x 2 ml	Scott-Cassar	238.3	47.66	\N	19/05/2011
1841	4585	NORADRENALINA	SOLUC.PARENT.SOLUFLEX	611H dext.5% agua x100ml	Rivero	240.53	2.4053	\N	10/01/2022
1842	7384	NORADRENALINA	SOLUC.PARENT.SOLUFLEX	620A isot.cl.sod.x 500ml	Rivero	240.53	2.4053	\N	01/08/2021
1843	10446	NORADRENALINA	NURIBAN	gts.x 15 ml	Roux Ocefa	243.23	4.8646	\N	03/11/2021
1844	19598	NORADRENALINA	DISMOLAN	4 mg iny.a.x 1 x 2 ml	Rivero	246.4	2.464	\N	02/07/2024
1845	55283	NORADRENALINA	SOL.FISIOLOGICA CLORURO DE SODIO	env.x 250 ml	B. Braun	248.08	2.4808	\N	22/12/2025
1846	36924	NORADRENALINA	MEROEFECTIL NORTHIA	500 mg IV iny.f.a.x 1	Northia	249.37	24.937	\N	22/12/2025
1847	61822	NORADRENALINA	CITRATO DE MAGNESIO	comp.x 150	Lafarmen	37500	1500	\N	25/07/2025
1848	37245	NORADRENALINA	MERPEM	500 mg iny.f.a.x 1	Richmond	250.19	2.5019	\N	25/07/2025
1849	7379	NORADRENALINA	SOLUC.PARENT.SOLUFLEX	611Q dext.5% agua x250ml	Rivero	251.29	125.645	\N	20/12/2025
1850	46346	NORADRENALINA	FLEXIPLEN	75 mg comp.x 15	Savant Consumer	340.98	13.6392	\N	06/10/2025
1851	51997	NORADRENALINA	DISGRADON	10 mg iny.a.x 100 x 2 ml	Fada Pharma	25312.68	1012.5072	\N	06/10/2025
1852	16541	NORADRENALINA	ZEROPENEM	1 g IV a.x 1	Sanofi-Aventis	253.44	2.5344	\N	13/08/2025
1853	61862	NORADRENALINA	CITRATO DE MAGNESIO	comp.x 30	Lafarmen	7700	7700	\N	23/02/2023
1854	23913	ONDANSETRON	FADAFLUMAZ	0.5 mg iny.a.x 5 x 5 ml	Fada Pharma	1294	129.4	\N	07/02/2002
1855	32111	ONDANSETRON	DICLOFENAC DENVER FARMA	75 mg comp.x 15	Denver Farma	578.13	57.813	\N	05/01/2009
1856	60001	ONDANSETRON	DAFUROSE	40 mg comp.rec.x 50	HLB Pharma	12994.66	12994.66	\N	06/12/2006
1857	35541	ONDANSETRON	DOLVAN	75 mg comp.x 15	Gador	1586.49	317.298	\N	07/02/2002
1858	62568	ONDANSETRON	MAGNESIO 400 NATULIV	comp.x 30	Laboratorio ENA	7850	7850	\N	01/03/2000
1859	51813	ONDANSETRON	DIPGIX	30 mg iny.a.x 100 x 2 ml	Northia	26259.52	3282.44	\N	26/06/2014
1860	13668	ONDANSETRON	ONDANSETRON FILAXIS	8 mg/4 ml sol.iny.x 5	Fresenius Kabi	1316.16	329.04	\N	20/01/2003
1861	7378	ONDANSETRON	SOLUC.PARENT.SOLUFLEX	611A dext.5% agua x500ml	Rivero	263.35	26.335	\N	28/01/2003
1862	25601	ONDANSETRON	GOBBICAINA	1% s/epi.f.a.x 20 ml	Gobbi	263.98	26.398	\N	23/12/2015
1863	55287	ONDANSETRON	SOL.DEXTROSA AL 5% EN AGUA	env.x 250 ml	B. Braun	264.04	52.808	\N	06/04/2022
1864	54303	ONDANSETRON	ICOPLAX	500 mg iny.f.a.caja x 50	Richmond	13221.45	13221.45	\N	02/02/2015
1865	21114	ONDANSETRON	DIASTONE	75 mg comp.x 15	Microsules Arg.	9266.94	9266.94	\N	05/01/2009
1866	6892	ONDANSETRON	SOLUC.PARENT.500 ML	Aminocefa 10	Roux Ocefa	268.86	268.86	\N	19/01/2003
1867	15886	ONDANSETRON	DIOXAFLEX 75	75 mg comp.x 15	Bag	14861.75	14861.75	\N	30/05/2008
1868	39921	ONDANSETRON	ONDANSETRON GOBBI	8 mg comp.rec.x 10	Gobbi	2719.38	2719.38	\N	01/11/2008
1869	37739	ONDANSETRON	IMISTATIN 500 IV	500 mg IV f.a.x 1	Richmond	272.01	54.402	\N	07/02/2002
1870	56763	ONDANSETRON	TRIMPOL	10 mg comp.x 20	HLB Pharma	5523.42	5523.42	\N	26/06/2014
1871	40201	ONDANSETRON	FLEXIPLEN	75 mg comp.x 210	Vitarum	232.47	23.247	\N	01/03/2014
1872	62909	ONDANSETRON	ZENTRO MAGNESIO	comp. x 60	ISA	16848	16848	\N	01/03/2000
1873	35818	ONDANSETRON	SOLUC.PARENT.SOLUFLEX	613Q dext.10% aguax250ml	Rivero	282.04	28.204	\N	20/01/2003
1874	62564	ONDANSETRON	MAGNESIO PLUS NATULIV	c ps.x 30	Laboratorio ENA	8550	1068.75	\N	26/06/2014
1875	35389	ONDANSETRON	DICLONEX 75	75 mg comp.x 30	Nexo Pharmaceut	26.02	2.602	\N	28/01/2003
1876	7375	ONDANSETRON	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	511A dext.5% agua x500ml	Rivero	292	58.4	\N	26/06/2014
1877	55284	ONDANSETRON	SOL.FISIOLOGICA CLORURO DE SODIO	env.x 500 ml	B. Braun	295.87	295.87	\N	26/06/2014
1878	53597	ONDANSETRON	HIDROCORTISONA	100 mg f.a.x 25	Klonal	7486.3	748.63	\N	12/01/2015
1879	58184	ONDANSETRON	DISMOLAN	8 mg iny.a.x50 x4ml (EH)	Rivero	14973.27	14973.27	\N	02/02/2015
1880	57747	ONDANSETRON	MAGNESIO VITAL A.M.	comp. x 30	A.M. Farma Acti	9000	9000	\N	28/01/2003
1881	24287	ONDANSETRON	MAGNESIO VITAL A.M.	c ps.x 30	A.M. Farma Acti	9000	9000	\N	28/01/2003
1882	6887	ONDANSETRON	SOLUC.PARENT.500 ML	dextr n 40 10% sol.fis.	Roux Ocefa	300.96	300.96	\N	17/04/2006
1883	7364	ONDANSETRON	SOLUC.PARENT.PARENTGLASS	969Q aa.esen.5.4% x250ml	Rivero	304.12	60.824	\N	21/04/2009
1947	59285	POTASIO CLORURO	FLEXANA	iny.a.x 3 x 3 ml	HLB Pharma	1200	1200	\N	04/06/2012
1884	19592	ONDANSETRON	SOLUC.PARENT.PARENTGLASS	aa.esen.5.4% x500ml 969A	Rivero	304.12	304.12	\N	01/03/2014
1885	26165	ONDANSETRON	DICLOFENAC NORTHIA	75 mg comp.x 30	Northia	84.08	84.08	\N	26/06/2014
1886	7366	ONDANSETRON	SOLUC.PARENT.PARENTGLASS	972A amino c.8% x 500 ml	Rivero	309.28	309.28	\N	12/08/2011
1887	55289	ONDANSETRON	SOL.DEXTROSA AL 5% EN AGUA	env.x 1000 ml	B. Braun	311.06	31.106	\N	01/03/2014
1888	18411	ONDANSETRON	SOLUC.PARENT.2000 ML	glicina al 1.5%	Roux Ocefa	312.78	62.556	\N	21/07/2004
1889	26819	ONDANSETRON	DICLOFENAC HEXA 75 RETARD	75 mg comp.x 30	Fada Pharma	109.06	109.06	\N	21/07/2004
1890	35224	ONDANSETRON	VIARTRIL NF	75 mg comp.x 30	Spedrog Caillon	140.75	140.75	\N	28/01/2003
1891	62843	ONDANSETRON	STAR NUTRITION MAGNESIO 500	c ps. x 60	Lesag	19017.1	19017.1	\N	01/01/2001
1892	61912	ONDANSETRON	CITRATO DE MAGNESIO 500	comp.x 30	Provefarma	9555	1911	\N	29/04/2016
1893	51836	ONDANSETRON	DICLOGRAND	75 mg comp.x 30	Lab Internacion	160.19	160.19	\N	29/04/2016
1894	31654	ONDANSETRON	MAGNESIO 400 GARDEN HOUSE	comp.x 30	Garden House Ar	9590	9590	\N	23/03/2016
1895	19969	ONDANSETRON	DANTENK	8 mg comp.x 10	Biotenk	3197.06	3197.06	\N	06/07/2015
1896	54708	ONDANSETRON	BIZILLIA PLUS SOLUCION SALINA	sol.x 500 ml	Microsules Arg.	320	320	\N	21/10/2021
1897	35542	ONDANSETRON	DOLVAN	75 mg comp.x 30	Gador	203.12	40.624	\N	23/03/2016
1898	55291	ONDANSETRON	SOL.DEXTROSA AL 10% EN AGUA	env.x 500 ml	B. Braun	328.11	32.811	\N	30/04/2022
1899	20693	ONDANSETRON	PRIMPERIL	comp.x 20	Lafedar	6579.81	131.5962	\N	21/10/2021
1900	55285	ONDANSETRON	SOL.FISIOLOGICA CLORURO DE SODIO	env.x 1000 ml	B. Braun	329.46	32.946	\N	18/02/2020
1901	56040	ONDANSETRON	FENTANILO DENVER FARMA	0.25 mg iny.a.x 25 x 5ml	Denver Farma	8327.17	8327.17	\N	21/10/2021
1902	19599	ONDANSETRON	DISMOLAN	8 mg iny.a.x 1 x 4 ml	Rivero	334.05	66.81	\N	09/02/2022
1903	55411	ONDANSETRON	AGUA DESTILADA INYECTABLE	env.x 1000 ml	B. Braun	335.57	335.57	\N	09/02/2022
1904	7367	ONDANSETRON	SOLUC.PARENT.PARENTGLASS	974A amino c.6.9% x500ml	Rivero	337.96	3.3796	\N	05/11/2021
1905	45401	ONDANSETRON	DICLOFENAC SODICO RICHET	75 mg comp.x 30	Richet	240.34	24.034	\N	07/06/2023
1906	36368	ONDANSETRON	ALGIOXIB	75 mg comp.x 30	Ferring	415.64	41.564	\N	07/06/2023
1907	32112	ONDANSETRON	DICLOFENAC DENVER FARMA	75 mg comp.x 30	Denver Farma	909.98	909.98	\N	07/06/2023
1908	54516	ONDANSETRON	DICLOFENAC TEVA	75 mg comp.x 30	Teva Argentina	1015.44	101.544	\N	17/12/2025
1909	55288	ONDANSETRON	SOL.DEXTROSA AL 5% EN AGUA	env.x 500 ml	B. Braun	348.41	34.841	\N	20/12/2025
1910	21115	ONDANSETRON	DIASTONE	75 mg comp.x 30	Microsules Arg.	16480.76	1648.076	\N	18/12/2025
1911	29640	ONDANSETRON	HYPERSOL UNIDOSIS	unidosis est riles x 25	Cassar	8730	873	\N	16/12/2025
1912	38084	ONDANSETRON	IMIPECIL	500 mg IV f.a.x 1	Northia	349.32	349.32	\N	29/10/2025
1913	58719	ONDANSETRON	FLEXANA	75 mg comp.x 30	HLB Pharma	24189.34	483.7868	\N	29/10/2025
1914	7381	ONDANSETRON	SOLUC.PARENT.SOLUFLEX	613A dext.10% aguax500ml	Rivero	355.97	71.194	\N	01/01/2026
1915	14730	ONDANSETRON	KETOPHARM	gts.oft.x 5 ml	Max Vision	356	35.6	\N	12/12/2025
1916	15887	ONDANSETRON	DIOXAFLEX 75	75 mg comp.x 30	Bag	31303.62	313.0362	\N	11/08/2025
1917	7380	ONDANSETRON	SOLUC.PARENT.SOLUFLEX	611L dext.5% aguax1000ml	Rivero	361.07	14.4428	\N	06/10/2025
1918	57941	ONDANSETRON	FUROSEMIDA VENT-3	comp. x 30	Vent 3	10928.42	10928.42	\N	17/12/2025
1919	14266	ONDANSETRON	VESALION	75 mg comp.x 30	Siegfried	33390.87	1335.6348	\N	21/11/2025
1920	21308	ONDANSETRON	RILAQUIN	10 mg comp.x 20	Microsules Arg.	7421.21	7421.21	\N	16/12/2025
1921	54300	ONDANSETRON	MERPEM	500 mg iny.f.a.x 50	Richmond	18782.97	187.8297	\N	13/08/2025
1922	54188	ONDANSETRON	FENTORA 800	800 mcg comp.dis.buc.x28	Teva Argentina	10556.55	10556.55	\N	30/12/2025
1923	60386	ONDANSETRON	REM CHOBET	7.5 mg comp.x 30	Soubeiran Chobe	11385.32	11385.32	\N	21/11/2025
1924	21237	ONDANSETRON	BLOKIUM	75 mg comp.x 30	Casasco	34781.8	34781.8	\N	01/01/2026
1925	41190	ONDANSETRON	MAGNESIO VITAL A.M.	bl st.x 20 x 10 c ps.c/u	A.M. Farma Acti	3800	380	\N	02/12/2025
1926	38297	ONDANSETRON	DICLOFENAC NORTHIA	75 mg comp.x 495	Northia	544.5	544.5	\N	02/12/2025
1927	55292	POTASIO CLORURO	SOL.DEXTROSA AL 5% EN SALINA NORMAL	env.x 500 ml	B. Braun	381.89	3.8189	\N	04/06/2012
1928	62597	POTASIO CLORURO	SOLUC. CLORURO DE SODIO 0.9%	a.pl st.x 5 ml	Laboratorios Te	7678.44	153.5688	\N	10/07/2003
1929	36545	POTASIO CLORURO	DICLOFENAC NORTHIA	75 mg comp.x 500	Northia	475	23.75	\N	01/08/1995
1930	9201	POTASIO CLORURO	SOLUC.PARENT.SOLUFLEX	613H dext.10% aguax100ml	Rivero	389.96	3.8996	\N	04/04/2002
1931	62210	POTASIO CLORURO	FABOGESIC FLEXI 75	75 mg comp.x 90	Savant Consumer	18887.13	188.8713	\N	12/02/2007
1932	14702	POTASIO CLORURO	VANCOMICINA FILAXIS	500 mg iny.liof.f.a.x 1	Filaxis Farmac	390	3.9	\N	01/06/2002
1933	45392	POTASIO CLORURO	FUROSEMIDA FECOFAR	comp.x 50	Fecofar	19583.63	6527.8765	\N	01/12/1996
1934	44769	POTASIO CLORURO	LOPARINE 100 MG	100 mg jga.prell.x10x1ml	Rivero	3989.17	39.8917	\N	01/06/2002
1935	37378	POTASIO CLORURO	DICLOGESIC	75 mg IM iny.a.x 5 x 3ml	Trb-Pharma	28.6	0.286	\N	15/08/2000
1936	19494	POTASIO CLORURO	SOLUC.CLORURADA HIPERTONICA	20% a.x 100 x 10 ml	Duncan	40142.08	802.8416	\N	09/08/2012
1937	7386	POTASIO CLORURO	SOLUC.PARENT.SOLUFLEX	620L isot.cl.sod.x1000ml	Rivero	402.05	402.05	\N	09/02/2002
1938	56752	POTASIO CLORURO	KPAN	10 mg comp.x 20	HLB Pharma	8121.06	8121.06	\N	28/06/2002
1939	54298	POTASIO CLORURO	IMISTATIN 500 IV	500 mg IV f.a.x 50	Richmond	20421.06	1021.053	\N	09/08/2012
1940	16343	POTASIO CLORURO	DICLOGESIC	75 mg IM iny.a.x 6 x 3ml	Trb-Pharma	19.55	3.2583334	\N	25/04/2002
1941	58784	POTASIO CLORURO	EZETIMAR	75 mg a.x 4 x 3 ml	Mar	1380	1380	\N	03/04/2002
1942	29326	POTASIO CLORURO	FADA DICLOFENAC	75 mg a.x 100 x 3 ml	Fada Pharma	35792.29	715.8458	\N	26/04/2002
1943	3546	POTASIO CLORURO	FUROSEMIDA FECOFAR	comp.x 30	Fecofar	12598.79	12598.79	\N	28/01/2003
1944	55408	POTASIO CLORURO	SOL.RINGER CON LACTATO	env.x 500 ml	B. Braun	422.67	4.2267	\N	06/04/2022
1945	59286	POTASIO CLORURO	FLEXANA	iny.a.x 5 x 3 ml	HLB Pharma	1950	1950	\N	28/01/2003
1946	46949	POTASIO CLORURO	MIDALAN	15 mg comp.x 30	Lafedar	12929.82	12929.82	\N	20/07/2007
1948	36543	POTASIO CLORURO	DICLOCALM	75 mg a.x 100 x 3 ml	Northia	43333.43	43333.43	\N	04/06/2012
1949	10493	POTASIO CLORURO	TRANSDERMA H	cr.x 20 g	Szama	433.97	433.97	\N	04/06/2012
1950	55410	POTASIO CLORURO	AGUA DESTILADA INYECTABLE	env.x 500 ml	B. Braun	436.86	436.86	\N	04/06/2012
1951	2754	POTASIO CLORURO	CURINFLAM	iny.a.x 6 x 3 ml	Duncan	9930.84	9930.84	\N	04/06/2012
1952	18526	POTASIO CLORURO	SOLUC.PARENT.FLEXIBLES BAXTER	isot.clor.sodio x 500 ml	Aponor	451.19	451.19	\N	04/06/2012
1953	18525	POTASIO CLORURO	SOLUC.PARENT.FLEXIBLES BAXTER	isot.clor.sodio x 250 ml	Aponor	451.34	18.805834	\N	19/05/2011
1954	51941	POTASIO CLORURO	ISOFUNDIN	ecoflac.env.x 10 x1000ml	B. Braun	4621.36	4621.36	\N	04/06/2012
1955	15870	POTASIO CLORURO	MEDROCIL	2% pomo x 30 g	Fortbenton	464.84	464.84	\N	04/06/2012
1956	39204	POTASIO CLORURO	COLISTINA TECHSPHERE	iny.f.a.x 1+ solv.x 2ml	Techsphere	472.15	4.7215	\N	12/08/2021
1957	9272	POTASIO CLORURO	DIOXAFLEX INY	iny.a.x 5 x 3 ml	Bag	17147.9	285.79834	\N	30/06/2025
1958	21239	POTASIO CLORURO	BLOKIUM	75 mg iny.a.x 5 x 3 ml	Casasco	17840.81	17840.81	\N	02/01/2024
1959	33094	POTASIO CLORURO	BLOKIUM	75 mg iny.a.x 3 x 3 ml	Casasco	10713.84	178.564	\N	17/12/2025
1960	52385	POTASIO CLORURO	SOLUC.PARENT.FLEXIBLES BAXTER	isot.clor.sodio x 100 ml	Aponor	485.4	16.18	\N	17/12/2025
1961	18519	POTASIO CLORURO	SOLUC.PARENT.FLEXIBLES BAXTER	dext.5% agua x 100 ml	Aponor	486.52	486.52	\N	15/11/2024
1962	25212	POTASIO CLORURO	XEDENOL	75 mg iny.a.x 5 x 3 ml	Baliarda	18233.11	18233.11	\N	15/11/2024
1963	43449	POTASIO CLORURO	FUROTRAL	40 mg comp.x 30	Lepetit	14930	14930	\N	20/11/2024
1964	58622	POTASIO CLORURO	DIOXAFLEX INY	iny.a.x 200 x 3 ml	Bag	832332.2	832332.2	\N	15/11/2024
1965	1048	POTASIO CLORURO	HIDROCORTISONA RICHET	10 mg comp.x 30	Richet	15016.65	250.2775	\N	15/08/2024
1966	54187	POTASIO CLORURO	FENTORA 600	600 mcg comp.dis.buc.x28	Teva Argentina	14105.67	14105.67	\N	19/01/2024
1967	21319	POTASIO CLORURO	CLEXANE	20 mg jga.prell.x 2	Sanofi-Aventis	1015.07	40.6028	\N	06/10/2025
1968	55295	POTASIO CLORURO	SOL.MANITOL AL 15% EN AGUA	env.x 250 ml	B. Braun	508.2	20.328	\N	06/10/2025
1969	18520	POTASIO CLORURO	SOLUC.PARENT.FLEXIBLES BAXTER	dext.5% agua x 250 ml	Aponor	509.31	5.0931	\N	11/08/2025
1970	56751	POTASIO CLORURO	KPAN	10 mg comp.x 10	HLB Pharma	5198.52	51.9852	\N	04/08/2025
1971	60385	POTASIO CLORURO	REM CHOBET	7.5 mg comp.x 10	Soubeiran Chobe	5306.84	5306.84	\N	21/07/2025
1972	9607	POTASIO CLORURO	DOLTEN	60 mg iny.a.x 1 x 2 ml	Pfizer	542.58	542.58	\N	21/07/2025
1973	50529	POTASIO CLORURO	XEDENOL CB	75mg c ps.bl.gastror.x15	Baliarda	13395.58	13395.58	\N	21/07/2025
1974	56600	POTASIO CLORURO	NORADRENALINA GP PHARM	1 mg/ml a.x 100 x 4 ml	Filaxis Farmac	55041.45	55041.45	\N	21/07/2025
1975	52130	POTASIO CLORURO	KETOROLAC LABSA	10 mg comp.rec.x 20	Labsa	11165.82	11165.82	\N	28/05/2025
1976	12818	POTASIO CLORURO	ERROLON	comp.x 50	Siegfried	28062.81	28062.81	\N	28/05/2025
1977	20202	POTASIO CLORURO	KETOROLAC FABRA	10 mg comp.x 20	Fabra	11350	11350	\N	29/02/2024
1978	45002	RANITIDINA	METAFLEX 50 CB	c ps.blandas x 15	Montpellier	4035.67	4.03567	\N	22/01/2014
1979	45301	RANITIDINA	DIOXAFLEX 75 CB	c ps.blandas x 15	Bag	16513.06	330.2612	\N	01/05/1999
1980	50302	RANITIDINA	METAFLEX 75 CB	c ps.blandas x 15	Montpellier	23636.29	196.96909	\N	12/04/2007
1981	58909	RANITIDINA	ANAFLEX	c ps.blandas x 16	Bag	4176.22	208.811	\N	18/01/2003
1982	21805	RANITIDINA	FLUMAZENIL RICHET	0.5 mg iny.a.x 1	Richet	592.81	19.760334	\N	31/07/2004
1983	40635	RANITIDINA	BUSCAPINA PERLAS	c ps.blandas x 10	Opella Healthca	5932.95	296.6475	\N	06/11/2000
1984	47457	RANITIDINA	BUSCAPINA PERLAS	c ps.blandas x 50	Opella Healthca	29664.75	1483.2375	\N	15/08/2002
1985	37954	RANITIDINA	TAURAL	Oral susp.x 200 ml	Roemmers	594.93	29.7465	\N	01/07/2004
1986	25126	RANITIDINA	ALFACORT UNIDOSIS	env.x 20 unidosis	Cassar	12000	400	\N	17/03/2003
1987	45003	RANITIDINA	METAFLEX 50 CB	c ps.blandas x 30	Montpellier	7960.71	796.071	\N	17/02/2003
1988	49836	RANITIDINA	DIOXAFLEX 75 CB	c ps.blandas x 30	Bag	34781.8	1159.3933	\N	17/02/2003
1989	54130	RANITIDINA	VAREDET	500 mg iny.f.a.x 50x10ml	Fada Pharma	30957.5	221.125	\N	28/12/2007
1990	62189	RANITIDINA	TOTAL MAGNESIANO+50	comp.rec.x 30	Temis-Lostal	18580.07	929.0035	\N	01/02/2007
1991	34342	RANITIDINA	SOLUC.PARENT.SOLUFLEX	631HD dext.5% aguax100ml	Rivero	621.01	12.4202	\N	26/04/2002
1992	50303	RANITIDINA	METAFLEX 75 CB	c ps.blandas x 30	Montpellier	43147.24	862.9448	\N	26/04/2002
1993	47041	RANITIDINA	DORIXINA FORTE NF	10 mg comp.rec.x 10	Roemmers	6305	12.61	\N	26/04/2002
1994	58930	RANITIDINA	ANAFLEX	c ps.blandas x 8	Bag	2246.32	22.4632	\N	24/08/2004
1995	2752	RANITIDINA	CURINFLAM A.P.	c ps.x 15	Duncan	14576.23	485.87433	\N	19/06/2002
1996	11961	RANITIDINA	SINALGICO	10 mg comp.x 20	Laboratorios Be	12891.59	107.42992	\N	11/06/2007
1997	22896	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	dext.5% clor.sod.x 500ml	Aponor	645.37	21.512333	\N	23/09/2003
1998	45148	RANITIDINA	DICLOLABSA 100 RETARD	c ps.x 15	Labsa	15587.6	31.1752	\N	16/09/2005
1999	20502	RANITIDINA	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	513A dext.10% aguax500ml	Rivero	654	65.4	\N	23/09/2003
2000	39863	RANITIDINA	CALMOFLEX RAPIDA ACCION	caps.blandas x 10	E. J. Gezzi	13.28	0.22133334	\N	01/07/2007
2001	56754	RANITIDINA	KPAN	20 mg comp.x 20	HLB Pharma	13223.72	220.39534	\N	19/12/2003
2002	39239	RANITIDINA	ZIENAM	500 mg IV f.a.x 25	MSD Argentina S	16530.83	330.6166	\N	01/02/2005
2003	39791	RANITIDINA	ANAFLEX MUJER PERLAS	caps.blandas x 10	Bag	20.68	0.34466666	\N	02/11/2007
2004	7492	RANITIDINA	DORMICUM	15 mg comp.x 30	Siegfried	20687.02	344.78366	\N	17/07/2008
2005	32200	RANITIDINA	ANAFLEX	caps.blandas x 10	Bag	155.96	0.31192	\N	14/07/2003
2006	32202	RANITIDINA	ANAFLEX	caps.blandas x 100	Bag	51	1.7	\N	01/09/2003
2007	40903	RANITIDINA	CALMOFLEX RAPIDA ACCION	caps.blandas x 20	E. J. Gezzi	24	1.2	\N	19/12/2003
2008	34343	RANITIDINA	SOLUC.PARENT.SOLUFLEX	632HD dext.10%aguax100ml	Rivero	698.86	11.647667	\N	30/01/2003
2009	32594	RANITIDINA	DILUTOL	20mg jga.prell.x10x0.2ml	Lazar	7046.64	234.888	\N	05/01/2009
2010	39792	RANITIDINA	ANAFLEX MUJER PERLAS	caps.blandas x 20	Bag	27.63	1.3815	\N	01/07/2007
2011	32201	RANITIDINA	ANAFLEX	caps.blandas x 20	Bag	289.95	14.4975	\N	05/09/2002
2012	18521	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	dext.5% agua x 500 ml	Aponor	726.23	36.3115	\N	17/07/2008
2013	32593	RANITIDINA	DILUTOL	20 mg jga.prell.x2x0.2ml	Lazar	1475.02	73.751	\N	01/11/2005
2014	55294	RANITIDINA	SOL.DEXTROSA AL 50% EN AGUA	env.x 500 ml	B. Braun	740.73	37.0365	\N	28/12/2007
2015	52386	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	isot.clor.sodio x 1000ml	Aponor	741.78	37.089	\N	01/02/2003
2016	55293	RANITIDINA	SOL.DEXTROSA AL 25% EN AGUA	env.x 500 ml	B. Braun	758.12	37.906	\N	17/11/2006
2017	56724	RANITIDINA	KETOROLAC 10 MG SL	10 mg comp.subl.x 10	Vent 3	7649.9	127.49834	\N	30/01/2008
2018	18522	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	dext.5% agua x 1000 ml	Aponor	782.62	39.131	\N	30/01/2003
2019	2608	RANITIDINA	MAGNEBE	comp.x 60	Dom nguez	47014.56	2350.728	\N	26/03/2007
2020	55507	RANITIDINA	OPTI FREE PUREMOIST REWETTING	env.x 10 ml	Alcon	786.5	39.325	\N	18/01/2003
2021	43306	RANITIDINA	ANAFLEX MUJER PERLAS	caps.blandas x 4	Bag	7.93	0.08811111	\N	30/01/2008
2022	53627	RANITIDINA	VANCOMAX	500 mg f.a.x 25	Klonal	20057.25	1002.8625	\N	18/06/2002
2023	20623	RANITIDINA	LEVEDAD	colirio x 10 ml	Max Vision	266.89	4.448167	\N	01/02/2003
2024	36594	RANITIDINA	PRONIX	colirio x 5 ml	Vannier	21.27	0.53175	\N	26/03/2007
2025	45502	RANITIDINA	ENOXANORTH	100 mg jga.prell.x 10	Northia	8169.3	408.465	\N	29/12/2010
2026	20183	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	dext.10% sol.x 500 ml	Aponor	822.39	41.1195	\N	08/05/2008
2027	35861	RANITIDINA	AKTIOSAN 75	comp.Rapiretard x 10	Investi	19.96	0.998	\N	24/11/2010
2028	56753	RANITIDINA	KPAN	20 mg comp.x 10	HLB Pharma	8285.13	414.2565	\N	20/01/2003
2029	52052	RANITIDINA	LIDOCAINA B.BRAUN	1% f.a.x 20 ml x 20 u.	B. Braun	16741.8	334.836	\N	08/03/2010
2030	55286	RANITIDINA	SOL.FISIOLOGICA CLORURO DE SODIO	env.x 2000 ml	B. Braun	841.52	42.076	\N	15/04/2011
2031	35862	RANITIDINA	AKTIOSAN 75	comp.Rapiretard x 20	Investi	33.3	1.665	\N	01/10/2000
2032	47572	RANITIDINA	FADA MIDAZOLAM	15 mg/3 ml iny.a.x 100	Fada Pharma	84900.13	4245.0063	\N	01/07/2004
2033	35252	RANITIDINA	DOXTRAN 75 MG	comp.rec.lib.prol.x 10	Phoenix	60.65	6.065	\N	07/01/2008
2034	32408	RANITIDINA	ALDORON NF	comp.rec.lib.prol.x 20	Teva Argentina	62.62	2.0873334	\N	06/11/2000
2035	35197	RANITIDINA	SILFOX 100 AP	comp.rec.lib.prol.x 20	Teva Argentina	64.71	0.6471	\N	20/07/2009
2036	35147	RANITIDINA	DOXTRAN 75 MG	comp.rec.lib.prol.x 20	Phoenix	108.6	2.172	\N	10/07/2003
2037	18523	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	dext.5% clor.sod.x1000ml	Aponor	862.72	8.6272	\N	16/09/2013
2038	39265	RANITIDINA	CALMOFLEX	comp.rec.x 10	E. J. Gezzi	14.91	0.2485	\N	19/03/2009
2039	39409	RANITIDINA	VOLFORTE 50	comp.rec.x 10	Omicron	4100.86	102.5215	\N	26/04/2002
2040	55441	RANITIDINA	SOL.DEXTROSA AL 5% SIST.CERRADO EP	env.x 250 ml	B. Braun	883.56	44.178	\N	15/12/2014
2041	22508	RANITIDINA	ORALSONE	comp.x 12	Laboratorio Mil	10662.21	533.1105	\N	29/07/2005
2042	52499	RANITIDINA	REM CHOBET	15 mg comp.x 10	Soubeiran Chobe	8915.62	891.562	\N	01/02/2007
2043	39411	RANITIDINA	VOLFORTE 75	comp.rec.x 10	Omicron	5858.3	292.915	\N	19/09/2003
2044	34373	RANITIDINA	OXA 75 RAPILENT	comp.rec.x 100	Beta	796.4	5.6885715	\N	11/06/2007
2045	9936	RANITIDINA	DOLTEN	10 mg comp.x 20	Pfizer	17975.65	898.7825	\N	25/11/2011
2046	63575	RANITIDINA	SOLUCION MOLAR JAYOR	bols.flex. x 100 ml x 60	Jayor	53993.04	899.884	\N	05/03/2014
2047	2607	RANITIDINA	MAGNEBE	comp.x 24	Dom nguez	21605.34	1080.267	\N	01/03/2014
2048	35810	RANITIDINA	UNICALM	10 mg comp.x 10	Adium	9074.05	151.23416	\N	01/07/2007
2049	2753	RANITIDINA	CURINFLAM	comp.rec.x 15	Duncan	44.94	2.247	\N	06/08/2004
2050	10162	RANITIDINA	OXA RETARD	comp.rec.x 15	Beta	522.18	26.109	\N	08/03/2010
2051	37441	RANITIDINA	OXA 100	comp.rec.x 15	Beta	533.8	17.793333	\N	01/07/2007
2052	13543	RANITIDINA	OXA 75 RAPILENT	comp.rec.x 15	Beta	787.39	39.3695	\N	19/03/2009
2053	58079	RANITIDINA	SOLUC.DEXTROSA NORGREEN	5% sachet x 1 x 2000 ml	Norgreen	945.45	31.515	\N	16/10/2003
2054	11962	RANITIDINA	SINALGICO	20 mg comp.x 20	Laboratorios Be	18944.87	189.4487	\N	24/08/2004
2055	55101	RANITIDINA	KETOROLAC FABRA SL	10 mg comp.subl.x 20	Fabra	19136	637.86664	\N	17/02/2003
2056	49363	RANITIDINA	DICLOLABSA 75 R	comp.rec.x 15	Labsa	12914.83	645.7415	\N	01/07/2007
2057	57006	RANITIDINA	OXA 75	comp.rec.x 15	Beta	15161.94	758.097	\N	05/09/2002
2058	55438	RANITIDINA	SOL.FISIOLOGICA 0.9% SIST.CERRADO EP	env.x 250 ml	B. Braun	966.85	48.3425	\N	28/11/2013
2059	44883	RANITIDINA	DICLOLABSA 75 AP	comp.rec.x 15	Labsa	17500.77	1750.077	\N	11/06/2007
2060	39266	RANITIDINA	CALMOFLEX	comp.rec.x 20	E. J. Gezzi	29.62	0.98733336	\N	02/11/2007
2061	52132	RANITIDINA	KETOROLAC LABSA	10 mg comp.subl.x 10	Labsa	9807.22	108.96911	\N	30/01/2008
2062	22900	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	Ringer lact.x 500 ml	Aponor	981.64	19.6328	\N	01/03/2014
2063	55296	RANITIDINA	SOL.MANITOL AL 15% EN AGUA	env.x 500 ml	B. Braun	981.85	32.728333	\N	30/01/2003
2064	13544	RANITIDINA	OXA 75 RAPILENT	comp.rec.x 30	Beta	1464.6	69.74286	\N	28/11/2013
2065	55412	RANITIDINA	AGUA DESTILADA P/IRRIGACION QUIRURGICA	env.x 2000 ml	B. Braun	991.54	33.051334	\N	05/01/2009
2066	57763	RANITIDINA	SOLUCION FISIOLOGICA ISOTONICA UGAL	sistema cerrado x 500 ml	Ugal Farmac uti	999.46	1.99892	\N	14/07/2003
2067	1395	RANITIDINA	OXA RETARD	comp.rec.x 30	Beta	1709.06	85.453	\N	30/09/2013
2068	25369	RANITIDINA	SINALGICO SL	10 mg comp.subl.x 20	Laboratorios Be	20003.46	666.782	\N	15/02/2003
2069	36528	RANITIDINA	FENTANILO NORTHIA	0.25 mg iny.a.x 100 x5ml	Northia	100309.27	3343.6423	\N	15/04/2011
2070	20175	RANITIDINA	NAFLUVENT	250 mcg a.x 50 x 5 ml	Fada Pharma	50154.64	5015.464	\N	24/08/2004
2071	47044	RANITIDINA	DORIXINA FORTE NF	10 mg comp.subl.x 20	Roemmers	20090	2009	\N	18/06/2002
2072	37442	RANITIDINA	OXA 100	comp.rec.x 30	Beta	2657.98	88.599335	\N	18/06/2002
2073	39410	RANITIDINA	VOLFORTE 50	comp.rec.x 30	Omicron	6489.23	108.15383	\N	21/12/2015
2074	39412	RANITIDINA	VOLFORTE 75	comp.rec.x 30	Omicron	10536.13	526.8065	\N	01/03/2014
2075	35812	RANITIDINA	UNICALM	20 mg comp.x 20	Adium	20278.14	675.938	\N	20/01/2003
2076	16286	RANITIDINA	DORMICUM	7.5 mg comp.x 20	Siegfried	20444.94	340.749	\N	04/11/2015
2077	47043	RANITIDINA	DORIXINA FORTE NF	10 mg comp.subl.x 10	Roemmers	10347	1034.7	\N	30/12/2016
2078	52131	RANITIDINA	KETOROLAC LABSA	20 mg comp.rec.x 10	Labsa	10371.76	345.72534	\N	04/11/2015
2079	57007	RANITIDINA	OXA 75	comp.rec.x 30	Beta	28739.46	574.7892	\N	31/01/2007
2080	40044	RANITIDINA	TELEDOL SL	10 mg comp.subl.x 10	Casasco	10392.61	519.6305	\N	17/01/2014
2081	55100	RANITIDINA	KETOROLAC FABRA SL	10 mg comp.subl.x 10	Fabra	10396	519.8	\N	24/11/2010
2082	8135	RANITIDINA	FLUXPIREN	comp.x 10	Ariston	18.13	1.813	\N	01/10/2005
2083	45154	RANITIDINA	VOLTAREN RETARD	comp.x 10	Novartis	86.67	8.667	\N	14/06/2002
2084	35837	RANITIDINA	TALNUR	25 mcg/h parches x 5	Novartis-Sandoz	5357.45	53.5745	\N	16/09/2013
2085	57185	RANITIDINA	CLORURO DE POTASIO B.BRAUN	2 mEq/ml a.x1 x 10ml	B. Braun	1073.25	53.6625	\N	04/11/2015
2086	37883	RANITIDINA	ONDANSETRON GLENMARK	8 mg iny.a. x 5 x 4 ml	Glenmark	5372.75	179.09166	\N	25/11/2011
2087	25398	RANITIDINA	KEMANAT	sublingual comp.x 10	Microsules Arg.	10782.81	513.46716	\N	28/10/2009
2088	18528	RANITIDINA	SOLUC.PARENT.FLEXIBLES BAXTER	Ringer lact.x 1000 ml	Aponor	1081.44	54.072	\N	31/01/2007
2089	37847	RANITIDINA	TELEDOL	20 mg comp.x 10	Casasco	10896.06	544.803	\N	06/09/2013
2090	39408	RANITIDINA	VOLFORTE 25	comp.x 10	Omicron	2793.97	279.397	\N	15/04/2011
2091	52901	RANITIDINA	RODINAC 75	comp.x 10	G minis Farmac	8134.91	271.16367	\N	29/11/2013
2092	47368	RANITIDINA	HYPERSOL SOLUCION	3%sol.est rilx12mds.x5ml	Cassar	13260	442	\N	15/12/2014
2093	25367	RANITIDINA	SINALGICO SL	10 mg comp.subl.x 10	Laboratorios Be	11097.88	554.894	\N	09/05/2013
2094	35809	RANITIDINA	UNICALM	10 mg comp.subl.x 10	Adium	11128.62	370.954	\N	07/03/2012
2095	30638	RANITIDINA	DIOXAFLEX	comp.x 100	Bag	1441.83	144.183	\N	30/03/2012
2096	56725	RANITIDINA	KETOROLAC 20 MG	20 mg comp.x 10	Vent 3	11259.59	187.65984	\N	01/03/2014
2097	20912	RANITIDINA	D.F.N.	comp.x 15	Laboratorios Fe	24.14	1.207	\N	05/03/2014
2098	4315	RANITIDINA	LASIX	40 mg comp.x 50	Sanofi-Aventis	57143.26	1904.7754	\N	06/07/2015
2099	49436	RANITIDINA	LASIX	40 mg comp.x 30	Sanofi-Aventis	34286.37	1714.3185	\N	14/11/2016
2100	47042	RANITIDINA	DORIXINA FORTE NF	20 mg comp.rec.x 10	Roemmers	11449	572.45	\N	01/03/2014
2101	49362	RANITIDINA	DICLOLABSA 75	comp.x 15	Labsa	43.8	2.19	\N	01/11/2015
2102	2252	RANITIDINA	VOLTAREN RETARD	comp.x 15	Novartis	73.16	14.632	\N	26/04/2002
2103	54963	RANITIDINA	ELGYDOL	10 mg comp.x 10	Sidus	11632.98	1938.83	\N	20/02/2002
2104	11709	RANITIDINA	SINALGICO	20 mg comp.x 10	Laboratorios Be	11701.52	1170.152	\N	01/11/2014
2105	13559	RANITIDINA	TOMANIL	comp.x 20	Takeda	40.25	0.67083335	\N	27/12/2017
2106	6351	RANITIDINA	DIOXAFLEX RETARD	comp.x 20	Bag	1552.27	258.71167	\N	01/02/2003
2107	5453	RANITIDINA	DIOXAFLEX 50	comp.x 20	Bag	8534.59	406.40906	\N	28/10/2009
2108	48614	RANITIDINA	RILAQUIN SL	10 mg comp.subl.x 10	Microsules Arg.	11993.28	1998.88	\N	24/11/2003
2109	47573	RANITIDINA	FIORITINA	4 mg a.x 50 x 4 ml	Fada Pharma	60480.46	3024.023	\N	04/05/2012
2110	46783	RANITIDINA	RODINAC 75	comp.x 20	G minis Farmac	17952.5	598.4167	\N	06/09/2013
2111	18785	RANITIDINA	D.F.N.	comp.x 30	Laboratorios Fe	45.72	4.572	\N	27/06/2008
2112	7016	RANITIDINA	FLUXPIREN	comp.x 30	Ariston	48.51	2.4255	\N	14/11/2016
2113	35811	RANITIDINA	UNICALM	20 mg comp.x 10	Adium	12520.11	250.4022	\N	26/04/2002
2114	17396	RANITIDINA	RELIVERAN SUBLINGUAL	comp.x 10	Gador	12588.41	125.8841	\N	26/04/2002
2115	43027	RANITIDINA	ONDANSETRON GLENMARK	8 mg iny.a. x 1 x 4 ml	Glenmark	1349.16	44.972	\N	14/11/2016
2116	44765	RANITIDINA	LOPARINE 20 MG	20mg jga.prell.x10x0.2ml	Rivero	13543.26	2708.652	\N	25/03/2008
2117	49361	RANITIDINA	DICLOLABSA 50	comp.x 30	Labsa	79.4	13.233334	\N	05/12/2008
2118	13205	RANITIDINA	LIDOCAINA DENVER FARMA	2% viscosa fco.got.x50ml	Denver Farma	1409.55	46.985	\N	01/03/2014
2119	37184	RANITIDINA	RODINAC 75	comp.x 30	G minis Farmac	21471.35	1533.6678	\N	18/02/2002
2120	18161	RANITIDINA	LIDOCAINA	1% s/epi.a.x 5 ml	Scott-Cassar	1465	293	\N	03/09/2013
2121	44766	RANITIDINA	LOPARINE 40 MG	40mg jga.prell.x10x0.4ml	Rivero	15091.15	3018.23	\N	19/12/2014
2122	6474	RANITIDINA	HOLOMAGNESIO	comp.rec.x 50	Elea	76162.21	12693.702	\N	18/12/2015
2123	8854	RANITIDINA	TOTAL MAGNESIANO EFERVESCENTE	comp.x 24	Temis-Lostal	36974.25	369.7425	\N	04/12/2020
2124	60393	RANITIDINA	CLORURO DE POTASIO UNC	a. x 100 x 5 ml	Hemoderivados	154700	7735	\N	01/06/2018
2125	8041	RANITIDINA	HOLOMAGNESIO	comp.rec.x 20	Elea	31123.11	1556.1555	\N	09/11/2018
2126	5454	RANITIDINA	DIOXAFLEX	comp.x 40	Bag	1114.45	18.574167	\N	02/12/2019
2127	35838	RANITIDINA	TALNUR	50 mcg/h parches x 5	Novartis-Sandoz	7992.86	133.21434	\N	13/03/2021
2128	60395	RANITIDINA	RANITIDINA UNC	a. x 100 x 5 ml	Hemoderivados	160050	16005	\N	21/12/2020
2129	17633	RANITIDINA	VOLTAREN COLIRIO	fco.cuentagotas x 5 ml	Novartis	82.95	8.295	\N	17/05/2021
2130	44767	RANITIDINA	LOPARINE 60 MG	60mg jga.prell.x10x0.6ml	Rivero	16639.02	277.317	\N	05/01/2021
2131	38540	RANITIDINA	QUER-OUT	gel t pico x 25 g	Lab Internacion	696.14	23.204666	\N	20/11/2020
2132	35822	RANITIDINA	RIVEPIME	1 g f.a.x 1	Rivero	1679.43	83.9715	\N	20/11/2020
2133	9937	RANITIDINA	DOLTEN	20 mg comp.x 10	Pfizer	17223.57	574.119	\N	20/02/2021
2134	47540	RANITIDINA	CONTROL K	c ps.x 30	Elea	52594.16	1753.1387	\N	05/01/2021
2135	59284	RANITIDINA	FLEXANA	gel t pico x 50 g	HLB Pharma	500	16.666666	\N	01/09/2020
2136	43903	RANITIDINA	ZOFRAN DR	4 mg comp.disol.rap.x 10	Novartis-Sandoz	18382.37	612.74567	\N	21/12/2020
2137	44768	RANITIDINA	LOPARINE 80 MG	80mg jga.prell.x10x0.8ml	Rivero	18573.2	1857.32	\N	17/05/2021
2138	35999	RANITIDINA	FADA CEFEPIME	1 g f.a.x 1	Fada Pharma	1950.87	65.029	\N	28/08/2020
2139	30938	RANITIDINA	CEFEPIME	1 g f.a.x 1	Northia	1950.87	65.029	\N	13/03/2021
2140	48821	RANITIDINA	HYPERSOL NEBU	sol.neb.unids.est r.x 12	Cassar	24830	2483	\N	21/12/2020
2141	40045	RANITIDINA	TELEDOL	30 mg a.x 3 x 2 ml	Casasco	6329.25	210.975	\N	12/02/2021
2142	52377	RANITIDINA	SUBLIMAZE S/CONSERVADOR	iny.x 5 x 2 ml	Janssen-Cilag	11286.79	11286.79	\N	05/03/2014
2143	61794	RANITIDINA	CLORURO DE POTASIO B. BRAUN EN SF 0.9%	1.5mg/ml x 1 x 500 ml	B. Braun	2318.6	77.28667	\N	20/11/2020
2144	35839	RANITIDINA	TALNUR	75 mcg/h parches x 5	Novartis-Sandoz	11830.07	591.5035	\N	20/11/2020
2145	61796	RANITIDINA	CLORURO DE POTASIO B. BRAUN EN SF 0.9%	3mg/ml x 1 x 500 ml	B. Braun	2382.1	79.403336	\N	05/01/2021
2146	40285	RANITIDINA	AGUA DESTILADA INYECTABLE NORGREEN	a.x 100 x 5 ml	Norgreen	241189.84	8039.661	\N	20/02/2021
2147	23465	RANITIDINA	SOLUC.PARENT.SOLUFLEX	612L glucoclorur.x1000ml	Rivero	2467.22	82.24067	\N	03/02/2021
2148	61795	RANITIDINA	CLORURO DE POTASIO B. BRAUN EN GLUC.5%	1.5mg/ml x 1 x 500 ml	B. Braun	2572.7	25.727	\N	19/12/2019
2149	57518	RANITIDINA	ALFACOLIN	pvo.iny. f.a.x 25 x100mg	Pint Pharma	65062	1084.3667	\N	10/05/2024
2150	54186	RANITIDINA	FENTORA 400	400 mcg comp.dis.buc.x28	Teva Argentina	76353.16	7635.316	\N	05/01/2021
2151	59100	RANITIDINA	SUERO FISIOLOGICO	a. x 100 x 5 ml	HLB Pharma	275400	13770	\N	10/05/2024
2152	61797	RANITIDINA	CLORURO DE POTASIO B. BRAUN EN GLUC.5%	3mg/ml x 1 x 500 ml	B. Braun	2826.8	2826.8	\N	05/01/2021
2153	53282	RANITIDINA	REPAK	gel x 30 g	Cassar	30290	302.9	\N	11/08/2025
2154	26887	RANITIDINA	DORMID	15 mg/3 ml iny.a.x 10	Scott-Cassar	28960	28960	\N	13/05/2024
2155	24585	RANITIDINA	LARJANCAINA	1% a.x 100 x 5 ml	Veinfar	297100	2971	\N	06/10/2025
2156	60085	RANITIDINA	ARTROSTOP MANOS	gel x 50 g	Excelentia	15000	150	\N	06/10/2025
2157	59095	RANITIDINA	SOLUC. DE LIDOCAINA	1% a.x 100 x 5 ml	HLB Pharma	297432	2974.32	\N	13/08/2025
2158	62206	SODIO CLORURO	SOLUC. MOLAR UPL	env.x 100 ml x 60 unid.	Ultra Pharma	179640	179640	\N	09/09/2004
2159	56877	SODIO CLORURO	MEROPENEM PHARMAVIAL	500 mg f.a.x 25 E.H.	IBC	75936.37	75936.37	\N	09/09/2004
2160	40299	SODIO CLORURO	CLORURO DE POTASIO NORGREEN	20 mEq a.x 1 x 5 ml	Norgreen	3111.11	3111.11	\N	01/10/2003
2161	11710	SODIO CLORURO	SINALGICO	30 mg a.x 3 x 1 ml	Laboratorios Be	9340.88	389.20334	\N	01/04/2019
2162	19551	SODIO CLORURO	HIOSCINA	a.x 100 x 1 ml	Veinfar	311920	311920	\N	12/01/2009
2163	40298	SODIO CLORURO	CLORURO DE POTASIO NORGREEN	15 mEq a.x 1 x 5 ml	Norgreen	3143.08	3143.08	\N	01/07/2001
2164	48670	SODIO CLORURO	NADRION	7% a. mds.x 60 x 5ml	Lafedar	190536.31	190536.31	\N	16/09/2003
2165	36000	SODIO CLORURO	FADA CEFEPIME	2 g f.a.x 1	Fada Pharma	3190.48	3190.48	\N	12/01/2009
2166	30939	SODIO CLORURO	CEFEPIME	2 g f.a.x 1	Northia	3190.48	3190.48	\N	09/01/2012
2167	56876	SODIO CLORURO	KETOROLAC PHARMAVIAL	30 mg iny.a.x 100 x 1 ml	IBC	322870.88	322870.88	\N	24/09/2003
2168	44205	SODIO CLORURO	RIVEPIME	2 g f.a.x 1	Rivero	3294.63	3294.63	\N	10/03/2014
2169	48669	SODIO CLORURO	NADRION	7% a. mds.x 30 x 5ml	Lafedar	98891.48	98891.48	\N	17/02/2003
2170	15620	SODIO CLORURO	CLORURO DE SODIO	20% a.x 100 x 10 ml	Veinfar	331990	5533.1665	\N	07/03/2017
2171	15631	SODIO CLORURO	SOLUC.FISIOLOGICA VEINFAR	a.x 100 x 5 ml	Veinfar	335590	335590	\N	01/04/2003
2172	60004	SODIO CLORURO	TRIMPOL	10 mg a. x 3 x 2 ml	HLB Pharma	10120	10120	\N	10/03/2014
2173	45040	SODIO CLORURO	IMIPENEM DRAWER	500 mg f.a.x 1	Drawer	3400	3400	\N	20/03/2008
2174	57625	SODIO CLORURO	LIDOCAINA PHARMAVIAL	1% s/epi.f.a.x 100 x 5ml	IBC	345818.6	345818.6	\N	06/07/2017
2175	57200	SODIO CLORURO	AGUA DESTILADA GEMEPE	a.x 100 x 3 ml	Gemepe	346427.03	346427.03	\N	11/10/2018
2176	56823	SODIO CLORURO	AGUA DESTILADA GEMEPE	a.x 100 x 5 ml	Gemepe	346427.03	5773.7837	\N	15/08/2022
2177	7388	SODIO CLORURO	SOLUC.PARENT.SOLUFLEX	625A Ring.3cl.isot.500ml	Rivero	3466.68	3466.68	\N	11/10/2018
2178	57215	SODIO CLORURO	LIDOCAINA GEMEPE	1% f.a.x 100 x 5 ml	Gemepe	350143.38	5835.723	\N	11/06/2021
2179	32655	SODIO CLORURO	RUPEMET	0.5% gts.x 20 ml	Duncan	3529.29	35.2929	\N	05/11/2021
24	63398	SODIO CLORURO	METOCLOPRAMIDA CELTYC	10 mg a.x 2 ml x 100	Celtyc	355100	355100	\N	02/04/2020
2181	39414	SODIO CLORURO	VOLFORTE GEL 5%	gel x 50 g	Omicron	18500	740	\N	15/12/2025
2182	44894	SODIO CLORURO	DIOXAFLEX GEL	gel x 50 g	Bag	19367.13	403.48187	\N	11/08/2021
2183	23534	SODIO CLORURO	HYANAC	gts.oft.unidosis x 20	Bausch & Lomb A	32.23	2.1486666	\N	11/08/2021
2184	43904	SODIO CLORURO	ZOFRAN DR	8 mg comp.disol.rap.x 10	Novartis-Sandoz	36762.6	3063.55	\N	23/09/2024
2185	40308	SODIO CLORURO	METOCLOPRAMIDA NORGREEN	10 mg a.x 2 ml	Norgreen	3689.28	307.44	\N	15/12/2025
2186	7418	SODIO CLORURO	SOLUC.PARENT.PARENTGLASS	956A agua p/iny.x 500 ml	Rivero	3704.1	37.041	\N	02/07/2024
2187	15632	SODIO CLORURO	SOLUC.FISIOLOGICA VEINFAR	a.x 100 x 10 ml	Veinfar	371300	371300	\N	13/05/2024
2188	47168	SODIO CLORURO	COTRELAN 100	iny.f.a.x 1+disolv.x 1	Rivero	3719.7	37.197	\N	11/08/2025
2189	7422	SODIO CLORURO	SOLUC.PARENT.PARENTGLASS	911Q dext.5% agua x250ml	Rivero	3753.74	37.5374	\N	11/08/2025
2190	56213	SODIO CLORURO	MIDAZOLAM B.BRAUN	5 mg/ml a.x 10 x 3 ml	B. Braun	37578	375.78	\N	02/09/2025
2191	56864	SODIO CLORURO	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	a.x 100 x 5ml	Rigecin	378741	12624.7	\N	01/01/2026
2192	61790	SODIO CLORURO	ANESTEX	iny.a. x100 x 5 ml	Klonal	379535.5	6325.592	\N	01/01/2026
2193	57746	SODIO CLORURO	MAGNESIO VITAL A.M.	bl ster x 10 comp.	A.M. Farma Acti	3800	3800	\N	13/05/2024
18	62416	SODIO CLORURO	LIDOCAINA CELTYC	2% a.x 100 x 5 ml	Celtyc	385000	3850	\N	23/10/2025
2195	55075	SODIO CLORURO	GOBBICAINA	1% s/epi.a.x 50 x 5 ml	Gobbi	192510.22	1925.1022	\N	02/07/2024
2196	52483	SODIO CLORURO	RELIVERAN INYECTABLE	10 mg a.x 6 x 2 ml	Gador	23127.43	23127.43	\N	02/12/2024
2197	59433	SODIO CLORURO	AGUA DESTILADA NORTHIA	a.x 25 x 5 ml	Northia	97509.99	24377.498	\N	04/11/2025
2198	45153	SODIO CLORURO	NACLIN	a.x 60 x 5 ml	Qu mica Luar	234570.64	3909.5107	\N	01/01/2026
2199	59300	SODIO CLORURO	MEROPENEM HLB	500 mg f.a.x 25	HLB Pharma	97800	97800	\N	30/10/2025
2200	40339	SODIO CLORURO	LIDOCAINA NORGREEN	1% a.x 1 x 5 ml	Norgreen	3947.11	3947.11	\N	25/09/2024
2201	7434	SODIO CLORURO	SOLUC.PARENT.PARENTGLASS	920A isot.cl.sod.x 500ml	Rivero	3958.3	131.94333	\N	01/01/2026
2202	56944	SODIO CLORURO	FADA CEFEPIME	2 g f.a.x 25	Fada Pharma	99464.15	994.6415	\N	02/09/2025
2203	7421	SODIO CLORURO	SOLUC.PARENT.PARENTGLASS	911A dext.5% agua x500ml	Rivero	4056.43	4056.43	\N	12/12/2025
2204	52482	SODIO CLORURO	RELIVERAN INYECTABLE	10 mg a.x 3 x 2 ml	Gador	12173.97	121.7397	\N	04/08/2025
2205	32091	SODIO CLORURO	GENTISALYL	gts.oft.x 5 ml	Maigal	131.58	131.58	\N	15/12/2025
2206	55894	SODIO CLORURO	MEROZEN	500 mg IV vial x 10	Pfizer	42604.41	42604.41	\N	15/12/2025
2207	57628	SODIO CLORURO	LIDOCAINA PHARMAVIAL	2% s/epi.f.a.x 100 x 5ml	IBC	443414.72	443414.72	\N	02/12/2024
2208	18529	SODIO CLORURO	SOLUC.PARENT.FLEXIBLES BAXTER	glicina 1.5% x 3000 ml	Aponor	4435.49	4435.49	\N	02/07/2024
2209	61308	SODIO CLORURO	FENTANILO LARJAN	100 mcg a.x 100 x 2 ml	Veinfar	445610	14853.667	\N	02/09/2025
2210	58082	SODIO CLORURO	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	sachet x 1 x 250 ml	Norgreen	4543.71	4543.71	\N	02/07/2024
2211	60748	SODIO CLORURO	METOCLOPRAMIDA GOBBI	10 mg iny.a.x 50	Gobbi	228789.38	228789.38	\N	02/12/2024
2212	53613	SODIO CLORURO	LIDOCAINA KLONAL	1% f.a.x 100 x 5 ml	Klonal	457874.44	457874.44	\N	15/12/2025
2213	57217	SODIO CLORURO	LIDOCAINA GEMEPE	2% a.x 100 x 5 ml	Gemepe	458976.1	458976.1	\N	02/12/2024
2214	53979	SODIO CLORURO	CLORHYP FQ	7% monods.x 60	Everex	275524.12	22960.342	\N	02/09/2025
2215	58831	SODIO CLORURO	ORAKIT 15	a.x 25 x 5 ml	Fada Pharma	116107.85	116107.85	\N	17/06/2025
33	63570	SODIO CLORURO	AGUA PARA INYECTABLE CELTYC	a.x 100 x 5 ml	Celtyc	465360	38780	\N	02/09/2025
2217	58607	SODIO CLORURO	HIOSCINA FADA	20 mg a.x 25 x 1 ml	Fada Pharma	117575.53	14696.941	\N	02/09/2025
2218	61442	SODIO CLORURO	DORMICUM	15 mg/3 ml iny.a.x 10	Siegfried	47069.29	47069.29	\N	17/06/2025
2219	63196	SODIO CLORURO	CLORURO DE SODIO 20% PHARMAVIAL	20% a.x 100 x 10 ml	IBC	470827.4	470827.4	\N	17/06/2025
2220	58060	SODIO CLORURO	AGUA DESTILADA INYECTABLE NORGREEN	a.x 100 x 20 ml	Norgreen	473127.22	118281.805	\N	02/09/2025
2221	40290	SODIO CLORURO	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	0.9% a.x 1 x 20 ml	Norgreen	4759.65	4759.65	\N	17/06/2025
2222	43020	SODIO CLORURO	RANITIDINA NORGREEN	50 mg a.x 1 x 5 ml	Norgreen	4786.6	4786.6	\N	19/12/2025
2223	58812	SODIO CLORURO	FENTANILO B.BRAUN	0.05 mg/ml a.x 10 x 5 ml	B. Braun	48273.53	48273.53	\N	23/09/2025
2224	57611	SODIO CLORURO	ARLYT FILL	fco.x 4 x 35 ml	Poen	19384.37	19384.37	\N	04/11/2025
2225	29366	SOLUCION PARENTERAL	FADA RANITIDINA	50 mg a.x 100 x 5 ml	Fada Pharma	485095.06	40424.59	\N	15/04/2002
2226	58102	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G51 sulf.mag. a.x100x5ml	Rivero	509616.28	84936.05	\N	31/05/2002
2227	58056	SOLUCION PARENTERAL	AGUA DESTILADA NORGREEN	sachet x 1 x 250 ml	Norgreen	5219.45	52.1945	\N	13/06/2000
2228	58474	SOLUCION PARENTERAL	CLEXANE	60 mg jga.prell.x 2	Sanofi-Aventis	10591.67	105.9167	\N	13/06/2000
2229	36408	SOLUCION PARENTERAL	FADA MEROPENEM	500 mg f.a.x 1	Fada Pharma	5382.04	5382.04	\N	03/12/2002
2230	51814	SOLUCION PARENTERAL	MEROEFECTIL	500 mg iny.f.a.x 5	Northia	26910.21	269.1021	\N	13/06/2000
2231	25982	SOLUCION PARENTERAL	NATURA FENAC	gts.oft.x 5 ml	Ariston	10850.44	108.5044	\N	13/06/2000
2232	56879	SOLUCION PARENTERAL	MEROPENEM PHARMAVIAL	1000 mg f.a.x 25 E.H.	IBC	138160.44	23026.738	\N	31/05/2002
2233	59299	SOLUCION PARENTERAL	MEROPENEM HLB	500 mg f.a.x 1	HLB Pharma	5600	466.66666	\N	01/04/2003
2234	43940	SOLUCION PARENTERAL	BUSCAPINA	a.x 3	Opella Healthca	16860.97	2810.1616	\N	01/04/2003
2235	46813	SOLUCION PARENTERAL	SOLUC. HIPERSALINA TECHSPERE 7%	a.x 60 x 4 ml	Biosintex Tr. E	337710.84	56285.137	\N	01/04/2003
2236	31524	SOLUCION PARENTERAL	RELENTE	sol.oft.x 10 ml	Klonal	5644.94	112.8988	\N	10/07/2003
2237	40297	SOLUCION PARENTERAL	DICLOFENAC NORGREEN	75 mg a.x 1 x 3 ml	Norgreen	5797.61	966.2683	\N	01/04/2003
2238	58825	SOLUCION PARENTERAL	FADA DICLOFENAC	75 mg a.x 25 x 3 ml	Fada Pharma	145047.34	1450.4734	\N	03/01/2008
2239	40570	SOLUCION PARENTERAL	SUAVILER	sol.oft.x 10 ml	Austral	5965	994.1667	\N	01/02/2003
2240	61309	SOLUCION PARENTERAL	FENTANILO LARJAN	250 mcg a.x 100 x 5 ml	Veinfar	597160	5971.6	\N	10/03/1997
2241	46812	SOLUCION PARENTERAL	SOLUC. HIPERSALINA TECHSPERE 7%	a.x 30 x 4 ml	Biosintex Tr. E	181025.23	1810.2523	\N	10/03/1997
2242	26526	SOLUCION PARENTERAL	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 50 x 20 ml	Fada Pharma	306573.66	306573.66	\N	26/03/2003
2243	51817	SOLUCION PARENTERAL	IMIPECIL	500 mg IV f.a.x 5	Northia	30824.69	308.2469	\N	01/06/2002
2244	61818	SOLUCION PARENTERAL	HIOSCINA SCOTT	20 mg iny.a.x 100 x 1 ml	Scott Pharma	628900	6289	\N	12/01/2009
2245	40315	SOLUCION PARENTERAL	AGUA DESTILADA NORGREEN	sachet x 1 x 100 ml	Norgreen	6290.18	2096.7266	\N	01/12/1996
2246	56169	SOLUCION PARENTERAL	TRIMPOL	0.2% gts.x 20 ml	HLB Pharma	6335.69	2111.8967	\N	01/12/1996
2247	60579	SOLUCION PARENTERAL	LIGNOCAINA GRAY	1% a.x 100 x 5 ml	Gray	633979.5	6339.795	\N	17/11/2006
2248	59741	SOLUCION PARENTERAL	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 25 x 20 ml	Fada Pharma	161249.72	161249.72	\N	18/01/2003
2249	1219	SOLUCION PARENTERAL	LIGNOCAINA VISCOSA	2% fco.got.x 50 ml	Gray	6469.18	2156.3933	\N	01/12/1996
2250	5061	SOLUCION PARENTERAL	ZOFRAN LIAM	8 mg a.x 1	Novartis-Sandoz	6472.7	2157.5667	\N	01/12/1996
2251	52378	SOLUCION PARENTERAL	SUBLIMAZE S/CONSERVADOR	iny.x 5 x 5 ml	Janssen-Cilag	32549.62	325.4962	\N	03/01/2008
2252	56824	SOLUCION PARENTERAL	AGUA DESTILADA GEMEPE	a.x 100 x 10 ml	Gemepe	660433.4	220144.47	\N	01/12/1996
2253	58083	SOLUCION PARENTERAL	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	sachet x 1 x 500 ml	Norgreen	6622.17	66.2217	\N	01/06/2002
2254	58076	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	5% sachet x 1 x 250 ml	Norgreen	6859.29	6859.29	\N	05/09/2002
2255	58969	SOLUCION PARENTERAL	CLEXANE	80 mg jga.prell.x 2	Sanofi-Aventis	13990.15	4663.3833	\N	01/12/1996
2256	19126	SOLUCION PARENTERAL	SINALGICO	60 mg a.x 3 x 2 ml	Laboratorios Be	21366.58	7122.1934	\N	01/12/1996
2257	62598	SOLUCION PARENTERAL	AGUA ESTERIL PARA INYECTABLES	a.pl st.x 5 ml	Laboratorios Te	7148.26	7148.26	\N	17/09/2002
2258	7394	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G15hipert.cl.sod.20%20ml	Rivero	7228	7228	\N	03/12/2002
2259	28233	SOLUCION PARENTERAL	HYPERSOL	3% spray nasal x 25 ml	Cassar	7270	72.7	\N	03/07/1996
2260	56762	SOLUCION PARENTERAL	TRIMPOL	0.5% gts.x 20 ml	HLB Pharma	7310.41	7310.41	\N	03/12/2002
2261	24103	SOLUCION PARENTERAL	ONDANSETRON FABRA	8 mg comp.x 10	Fabra	73558	73558	\N	01/11/1998
2262	60580	SOLUCION PARENTERAL	LIGNOCAINA JALEA	2% pomo c/aplic.x25x25ml	Gray	188182.94	1881.8293	\N	03/07/1996
2263	1220	SOLUCION PARENTERAL	LIGNOCAINA JALEA	2% pomo c/aplic.x 25 ml	Gray	7527.32	75.2732	\N	29/12/2009
2264	38293	SOLUCION PARENTERAL	DIXABIOX	500 mg IV f.a.x 1	Rivero	7531.48	7531.48	\N	28/01/2003
2265	56828	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA GEMEPE	90 mg a.x 100 x 10 ml	Gemepe	761877.2	761877.2	\N	01/04/2003
2266	56827	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA GEMEPE	45 mg a.x 100 x 5 ml	Gemepe	768661	768661	\N	01/09/2000
2267	57222	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA GEMEPE	a.x 100 x 3 ml	Gemepe	768661	768661	\N	03/04/2002
2268	11485	SOLUCION PARENTERAL	DOLTEN	60 mg iny.a.x 3 x 2 ml	Pfizer	23175.34	23175.34	\N	03/04/1995
2269	43374	SOLUCION PARENTERAL	MIDAZOLAM NORGREEN	50 mg a.x 1 x 10 ml	Norgreen	7740.12	7740.12	\N	01/11/1998
2270	59446	SOLUCION PARENTERAL	SOLUC.FISIOLOGICA	1.5 mEq a.x 25	Northia	194376.69	194376.69	\N	05/09/2002
2271	59302	SOLUCION PARENTERAL	MEROPENEM HLB	1000 mg f.a.x 25	HLB Pharma	199800	199800	\N	01/11/1998
2272	59291	SOLUCION PARENTERAL	IMIPENEM CILASTATINA HLB	500 mg f.a.x 25 x 2 ml	HLB Pharma	202000	202000	\N	22/01/2007
2273	52051	SOLUCION PARENTERAL	LIDOCAINA B.BRAUN	2% f.a.x 20 ml x20 unid.	B. Braun	164012.12	164012.12	\N	01/10/1992
2274	54120	SOLUCION PARENTERAL	MEROZEN	1 g IV vial x 10	Pfizer	82198.75	821.9875	\N	01/06/2002
2275	16490	SOLUCION PARENTERAL	MEROZEN	1 g IV vial x 1	Pfizer	8219.88	8219.88	\N	03/12/2002
2276	54041	SOLUCION PARENTERAL	CLORHYP ATOM	3% nasal spray x 25 ml	Valmax	8300	83	\N	29/12/2009
2277	18556	SOLUCION PARENTERAL	METOCLOPRAMIDA VANNIER	ad.gts.x 20 ml	Vannier	8322.11	8322.11	\N	03/12/2002
2278	27361	SOLUCION PARENTERAL	PRIMAVERA-N	ad.gts.x 20 ml	Fabra	8337	8337	\N	01/11/1998
2279	2217	SOLUCION PARENTERAL	RELIVERAN	n .gts.x 20 ml	Gador	8493.57	84.9357	\N	01/06/2002
2280	11659	SOLUCION PARENTERAL	CETRON	8 mg comp.x 10	Adium	85039.2	850.392	\N	01/06/2002
2281	21309	SOLUCION PARENTERAL	RILAQUIN	ad.gts.x 20 ml	Microsules Arg.	8511.61	8511.61	\N	03/12/2002
2282	58077	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	5% sachet x 1 x 500 ml	Norgreen	8517.87	8517.87	\N	11/01/2011
2283	40301	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	25% a.x 1 x 20 ml	Norgreen	8532.01	8532.01	\N	26/04/2002
2284	35820	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	520H isot.cl.sod.x 100ml	Rivero	8578.15	8578.15	\N	21/04/2009
2285	25613	SOLUCION PARENTERAL	MIDATENK	0.5% gts.adultos x 20 ml	Biotenk	8691.24	434.562	\N	19/07/2002
2286	23548	SOLUCION PARENTERAL	NORADRENALINA BIOL	1 mg/ml a.x 10 x 4 ml	Biol	88561.37	88561.37	\N	28/01/2003
2287	55900	SOLUCION PARENTERAL	SOL.FISIOLOGICA 0.9% FRESENIUS KAVI	env.x 100 ml	Fresenius Kabi	8881.21	8881.21	\N	01/11/1998
2288	58075	SOLUCION PARENTERAL	SOLUC. RINGER LACTATO NORGREEN	sachet x 250 ml	Norgreen	8894.24	8894.24	\N	22/01/2007
2289	60000	SOLUCION PARENTERAL	DAFUROSE	20 mg a.x 10 x 2 ml	HLB Pharma	89229.6	89229.6	\N	01/11/1992
2290	51942	SOLUCION PARENTERAL	ISOFUNDIN	ecoflac.env.x 10 x 500ml	B. Braun	89289.8	89289.8	\N	30/09/2013
2291	58832	SOLUCION PARENTERAL	SOLUC.CLORURADA HIPERTONICA FADA	20% a.x 25 x 10 ml	Fada Pharma	223799.27	223799.27	\N	01/11/1992
2292	56884	SOLUCION PARENTERAL	MIDAZOLAM PHARMAVIAL	15 mg/3 ml iny.a.x 100	IBC	900385.56	9003.855	\N	01/06/2002
2293	59373	SOLUCION PARENTERAL	LIDOCAINA B.BRAUN	2% f.a.x 5 ml x 20 unid.	B. Braun	182626.7	182626.7	\N	01/11/1992
2294	18339	SOLUCION PARENTERAL	RIVERVAN	500 mg f.a.x 1	Rivero	9230.05	9230.05	\N	15/07/2005
2295	21146	SOLUCION PARENTERAL	MIDAZOLAN GEMEPE	15 mg/3 ml iny.a.x 100	Gemepe	928830	928830	\N	30/09/2013
2296	26462	SOLUCION PARENTERAL	ALFACORT	1% emuls.x 15 ml	Cassar	9390	9390	\N	01/11/1992
2297	20881	SOLUCION PARENTERAL	LIDOCAINA 4%	sol.t pica x 25 ml	Scott-Cassar	9520	9520	\N	11/01/2011
2298	61793	SOLUCION PARENTERAL	SOLVENTE INDOLORO MONSERRAT Y ECLAIR	sol.f.a.x 24 x 5 ml	Monserrat	230800	230800	\N	02/12/2003
2299	59198	SOLUCION PARENTERAL	CLORHIDRATO DE LIDOCAINA	1% s/epi.f.a.x 50x 25 ml	Drawer	487687.2	487687.2	\N	15/07/2005
2300	2219	SOLUCION PARENTERAL	RELIVERAN	ad.gts.x 20 ml	Gador	10010.32	10010.32	\N	18/01/2003
2301	34346	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	520Q isot.cl.sod.x 250ml	Rivero	10023.6	10023.6	\N	01/11/1992
2302	58101	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G50 sulf.mag. a.x50 x5ml	Rivero	509616.28	509616.28	\N	03/12/2002
2303	59960	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	642H bicar.sod.molx100ml	Rivero	10278.85	102.7885	\N	01/06/2002
2304	58057	SOLUCION PARENTERAL	AGUA DESTILADA NORGREEN	sachet x 1 x 500 ml	Norgreen	10317.31	103.1731	\N	01/06/2002
2305	55440	SOLUCION PARENTERAL	SOLUC.DEXTROSA AL 5% SIST.CERRADO EP	env.x 100 ml	B. Braun	10328.8	10328.8	\N	26/04/2002
2306	24471	SOLUCION PARENTERAL	DIOXAFLEX	iny.jga.prell.x 1	Bag	14.3	14.3	\N	26/04/2002
2307	55896	SOLUCION PARENTERAL	SOL.DEXTROSA AL 5% FRESENIUS KABI	env.x 100 ml	Fresenius Kabi	10349.87	10349.87	\N	26/04/2002
2308	57626	SOLUCION PARENTERAL	LIDOCAINA PHARMAVIAL	1% s/epi.f.a.x 50 x 20ml	IBC	523419	5234.19	\N	01/06/2002
2309	37024	SOLUCION PARENTERAL	FADA MEROPENEM	1 g f.a.x 1	Fada Pharma	10501.2	10501.2	\N	03/12/2002
2310	37620	SOLUCION PARENTERAL	MEROEFECTIL NORTHIA	1000 mg IV iny.f.a.x 1	Northia	10501.2	10501.2	\N	01/11/1992
2311	56755	SOLUCION PARENTERAL	KPAN	gts.x 5 ml	HLB Pharma	10559.48	10559.48	\N	26/04/2002
2312	24231	SOLUCION PARENTERAL	ALFACORT	1% cr.x 30 g	Cassar	10570	211.4	\N	01/06/2002
2313	2047	SOLUCION PARENTERAL	MICROSONA	0.5% cr.x 15 g	Siegfried	10774.24	215.4848	\N	26/04/2002
2314	59484	SOLUCION PARENTERAL	DIOXAFLEX PARCHES	parches x 2	Bag	24454.49	24454.49	\N	30/09/2005
2315	54184	SOLUCION PARENTERAL	FENTORA 100	100 mcg comp.dis.buc.x28	Teva Argentina	306300.34	306300.34	\N	26/04/2002
2316	54185	SOLUCION PARENTERAL	FENTORA 200	200 mcg comp.dis.buc.x28	Teva Argentina	306300.34	306300.34	\N	03/12/2002
2317	58058	SOLUCION PARENTERAL	AGUA DESTILADA NORGREEN	sachet x 1 x 1000 ml	Norgreen	11057.25	11057.25	\N	03/12/2002
2318	57216	SOLUCION PARENTERAL	LIDOCAINA GEMEPE	1% f.a.x 1 x 20 ml	Gemepe	11148.03	11148.03	\N	01/11/1992
2319	35819	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	511H dext.5% aguax 100ml	Rivero	11156.47	111.5647	\N	01/06/2002
2320	59737	SOLUCION PARENTERAL	FENTANILO KABI	0.1 mg a.x 20 x 2 ml	Fresenius Kabi	225197.34	2251.9734	\N	26/04/2002
2321	32483	SOLUCION PARENTERAL	FENTANILO GEMEPE	0.05 mg/ml a.x 25 x 5 ml	Gemepe	282382	282382	\N	28/01/2003
2322	62494	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env.flex.x100ml dob.bol.	Laboratorios Te	11384.09	11384.09	\N	09/01/2009
2323	59442	SOLUCION PARENTERAL	SULFATO DE MAGNESIO	25% a.x 25 x 5 ml	Fada Pharma	288349.28	288349.28	\N	26/04/2002
2324	59301	SOLUCION PARENTERAL	MEROPENEM HLB	1000 mg f.a.x 1	HLB Pharma	11600	11600	\N	26/04/2002
2325	52102	SOLUCION PARENTERAL	CITRATO DE FENTANILO	a.x 5 x 5 ml	Filaxis Farmac	58707.52	58707.52	\N	03/12/2002
2326	17227	SOLUCION PARENTERAL	DIOXAFLEX PARCHES	parches x 5	Bag	58836.38	58836.38	\N	03/12/2002
2327	41516	SOLUCION PARENTERAL	SOLVENTE INDOLORO MONSERRAT Y ECLAIR	sol.f.a.x 3 x 5 ml	Monserrat	35850	35850	\N	03/12/2002
2328	57213	SOLUCION PARENTERAL	LIDOCAINA EPINEFRINA GEMEPE	1% f.a.x 20 ml	Gemepe	12063.66	12063.66	\N	26/04/2002
2329	44513	SOLUCION PARENTERAL	DICLOREUMOL FORTE GEL	pomo x 50 g	Cabuchi	46.06	46.06	\N	09/01/2009
2330	58802	SOLUCION PARENTERAL	UNIFRESH SOLUCION SALINA	fco.x 360 ml	Max Vision	12190	12190	\N	09/01/2009
2331	63340	SOLUCION PARENTERAL	DICLOLAM GEL T PICO AL 1%	pomo x 50 g	Austral	7084.8	70.848	\N	26/04/2002
2332	55893	SOLUCION PARENTERAL	GOBBICAINA	1% s/epi.f.a.x 25 x 20ml	Gobbi	306191.7	306191.7	\N	28/01/2003
2333	40291	SOLUCION PARENTERAL	CLORURO DE SODIO 20% NORGREEN	20% a.x 1 x 10 ml	Norgreen	12258.93	12258.93	\N	28/01/2003
2334	55902	SOLUCION PARENTERAL	SOL.FISIOLOGICA 0.9% FRESENIUS KAVI	env.x 500 ml	Fresenius Kabi	12425.05	12425.05	\N	09/01/2009
2335	19712	SOLUCION PARENTERAL	NAFLUVENT	250 mcg f.a.x 25 x 5 ml	Fada Pharma	312731.62	312731.62	\N	26/04/2002
2336	44202	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	611CD dext.5% agua x50ml	Rivero	12816	12816	\N	26/04/2002
2337	47124	SOLUCION PARENTERAL	REUMOL DICLO FORTE GEL	pomo x 50 g	Cabuchi	14900.32	14900.32	\N	26/04/2002
2338	19594	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	556A agua p/iny.x 500 ml	Rivero	12970.94	259.4188	\N	26/04/2002
2339	58059	SOLUCION PARENTERAL	AGUA DESTILADA NORGREEN	sachet x 1 x 2000 ml	Norgreen	13183.75	13183.75	\N	26/04/2002
2340	60581	SOLUCION PARENTERAL	MIDAZOLAM GRAY	15 mg iny.a.x 25 x 3 ml	Gray	329940.28	329940.28	\N	03/12/2002
2341	55897	SOLUCION PARENTERAL	SOL.DEXTROSA AL 5% FRESENIUS KABI	env.x 250 ml	Fresenius Kabi	13269.08	13269.08	\N	11/01/2011
2342	58404	SOLUCION PARENTERAL	NACLOR	0.9% sol. oft. x 10 ml	Novoplos	13320	13320	\N	18/02/2005
2343	58609	SOLUCION PARENTERAL	SOLUC.CLORURADA HIPERTONICA FADA	20% a.x 25 x 20 ml	Fada Pharma	335082.28	335082.28	\N	03/12/2002
2344	60584	SOLUCION PARENTERAL	NOREPINEFRINA GRAY	1 mg a.x 25 x 4 ml	Gray	336861	336861	\N	03/12/2002
2345	60585	SOLUCION PARENTERAL	NOREPINEFRINA GRAY	1 mg a.x 100 x 4 ml	Gray	1.347444e+06	1.347444e+06	\N	18/05/2006
2346	2050	SOLUCION PARENTERAL	MICROSONA	2% cr.x 15 g	Siegfried	13531.68	13531.68	\N	26/04/2002
2347	7377	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	520L isot.cl.sod.x1000ml	Rivero	13667.62	13667.62	\N	03/12/2002
2348	28821	SOLUCION PARENTERAL	NORADRENALINA RICHET	1 mg/ml a.x 2 x 4 ml	Richet	27396.42	27396.42	\N	26/04/2002
2349	58920	SOLUCION PARENTERAL	OXA GEL PLUS	roll-on gel x 50 g	Beta	12142.74	242.8548	\N	26/04/2002
2350	34345	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	511Q dext.5% agua x250ml	Rivero	13734.85	13734.85	\N	03/12/2002
2351	31670	SOLUCION PARENTERAL	FENTANILO GRAY	iny.a.x 5 ml	Gray	13755.42	13755.42	\N	26/04/2002
2352	58686	SOLUCION PARENTERAL	NOREPINEFRINA NORTHIA	4 mg a.x 25 x 4 ml	Northia	345216.2	345216.2	\N	01/11/1992
2353	18159	SOLUCION PARENTERAL	LIDOCAINA	1% s/epi.f.a.x 20 ml	Scott-Cassar	13930	13930	\N	26/04/2002
2354	57627	SOLUCION PARENTERAL	LIDOCAINA PHARMAVIAL	2% s/epi.f.a.x 50 x 20ml	IBC	702374.4	702374.4	\N	28/01/2003
2355	54299	SOLUCION PARENTERAL	REGIOCAINA JALEA	pomo x 25 ml caja x 20	Richmond	282457.06	282457.06	\N	28/01/2003
2356	56311	SOLUCION PARENTERAL	ARLYT SOLUCION SALINA	env.x 500 ml	Poen	14209.73	284.1946	\N	26/04/2002
2357	38925	SOLUCION PARENTERAL	DEMACORT	cr.x 15 g	Andr maco	14427.74	14427.74	\N	18/02/2005
2358	57218	SOLUCION PARENTERAL	LIDOCAINA GEMEPE	2% f.a.x 1 x 20 ml	Gemepe	14457.09	144.5709	\N	06/04/2022
2359	44204	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	620CD isot.cl.sod.x 50ml	Rivero	14482.09	14482.09	\N	26/04/2002
2360	55439	SOLUCION PARENTERAL	SOLUC.FISIOLOGICA 0.9% SIST.CERRADO EP	env.x 500 ml	B. Braun	14566.8	14566.8	\N	02/12/2003
2361	56630	SOLUCION PARENTERAL	GOBBICAINA	1% c/epi.a.x 25 x 20 ml	Gobbi	367429.72	367429.72	\N	11/01/2011
2362	32539	SOLUCION PARENTERAL	ONDANSETRON GOBBI	8 mg iny.a. x 1 x 4 ml	Gobbi	14849.48	14849.48	\N	03/12/2002
2363	57424	SOLUCION PARENTERAL	VOLFORTE GEL ROLL-ON 5 %	roll-on x 50 g	Omicron	17445.55	17445.55	\N	17/09/2002
2364	55899	SOLUCION PARENTERAL	SOL.DEXTROSA AL 5% FRESENIUS KABI	env.x 1000 ml	Fresenius Kabi	14917.93	14917.93	\N	03/12/2002
2365	14267	SOLUCION PARENTERAL	VESALION	Rtd.100 mg comp.x 30	Nova Argentia	58.71	58.71	\N	03/12/2002
2366	30701	SOLUCION PARENTERAL	SALDIET DHARAM SINGH	Ajo env.x 70 g s/sodio	Dharam Singh	15000	15000	\N	03/12/2002
2367	30704	SOLUCION PARENTERAL	SALDIET DHARAM SINGH	natural env.x 70g s/sod.	Dharam Singh	15000	15000	\N	26/04/2002
2368	40295	SOLUCION PARENTERAL	CLORURO DE SODIO 20% NORGREEN	20% a.x 1 x 20 ml	Norgreen	15242.7	15242.7	\N	26/04/2002
2369	55903	SOLUCION PARENTERAL	SOL.FISIOLOGICA 0.9% FRESENIUS KAVI	env.x 1000 ml	Fresenius Kabi	15515.92	15515.92	\N	05/09/2002
2370	55901	SOLUCION PARENTERAL	SOL.FISIOLOGICA 0.9% FRESENIUS KAVI	env.x 250 ml	Fresenius Kabi	15624.38	15624.38	\N	03/12/2002
2371	40323	SOLUCION PARENTERAL	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	sachet x 1 x 100 ml	Norgreen	15820.56	15820.56	\N	03/10/2002
2372	60958	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	30 sach. x 100ml	Rigecin	481201.8	481201.8	\N	03/10/2002
2373	58074	SOLUCION PARENTERAL	SOLUC. RINGER LACTATO NORGREEN	sachet x 1000 ml	Norgreen	16224	16224	\N	18/05/2006
2374	29213	SOLUCION PARENTERAL	OPTI FREE EXPRESS	env.x 120 ml	Alcon	16389	16389	\N	18/05/2006
2375	22423	SOLUCION PARENTERAL	RIVERVAN	1 g f.a.x 1	Rivero	16552.56	16552.56	\N	18/05/2006
2376	12565	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	611HD dext.5% aguax100ml	Rivero	16591.53	16591.53	\N	01/07/2000
2377	60268	SOLUCION PARENTERAL	LIDOCAINA KLONAL	1% f.a.x 20 x 20 ml	Klonal	336043.4	336043.4	\N	18/05/2017
2378	12566	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	611QD dext.5% aguax250ml	Rivero	17101.74	17101.74	\N	18/02/2005
2379	14099	SOLUCION PARENTERAL	POENKERAT	0.5% colirio x 5 ml	Poen	17180.55	17180.55	\N	18/05/2017
2380	24753	SOLUCION PARENTERAL	DICLAC	Rtd.150 mg ID comp.x 20	Investi	38.9	38.9	\N	18/05/2006
2381	55898	SOLUCION PARENTERAL	SOL.DEXTROSA AL 5% FRESENIUS KABI	env.x 500 ml	Fresenius Kabi	17516.73	17516.73	\N	06/05/2014
2382	50704	SOLUCION PARENTERAL	ALFACORT	ung.est ril x 5 g	Cassar	17840	17840	\N	18/05/2017
2383	61559	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env. flex.x 250 ml	Laboratorios Te	18138.78	18138.78	\N	02/09/2008
2384	15467	SOLUCION PARENTERAL	ACULAR	sol.oft.x 5 ml	Abbvie	18158.44	18158.44	\N	02/09/2008
2385	55505	SOLUCION PARENTERAL	OPTI FREE PUREMOIST	env.x 120 ml	Alcon	18186	18186	\N	18/02/2005
2386	61556	SOLUCION PARENTERAL	AGUA ESTERIL PARA INYECTABLES	env.flex.x 1000 ml	Laboratorios Te	18243.56	18243.56	\N	18/05/2017
2387	62493	SOLUCION PARENTERAL	AGUA ESTERIL PARA INYECTABLES	env.flex.x1000ml dob.bol	Laboratorios Te	18248.65	18248.65	\N	18/05/2017
2388	24751	SOLUCION PARENTERAL	DICLAC	Rtd.75 mg ID comp.x 10	Investi	15.9	0.159	\N	05/11/2021
2389	24752	SOLUCION PARENTERAL	DICLAC	Rtd.75 mg ID comp.x 20	Investi	27.5	27.5	\N	18/05/2017
2390	62165	SOLUCION PARENTERAL	PROAVENAL H	cr.x 20 g	Panalab	18539.21	18539.21	\N	18/05/2017
2391	57214	SOLUCION PARENTERAL	LIDOCAINA EPINEFRINA GEMEPE	2% f.a.x 20 ml	Gemepe	18555.17	18555.17	\N	18/05/2017
6	61926	SOLUCION PARENTERAL	ENOXAPARINA CELTYC	20 mg jga.prell.x 10	Celtyc	188600	7544	\N	31/05/2016
2393	18337	SOLUCION PARENTERAL	SOLUC.PARENT.PLASTICOS SEMIRRIGIDOS	524A Ringer lact.x 500ml	Rivero	19064.05	19064.05	\N	03/10/2002
2394	14466	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	611LD dext.5%aguax1000ml	Rivero	19142.59	19142.59	\N	18/05/2017
2395	61555	SOLUCION PARENTERAL	AGUA ESTERIL PARA INYECTABLES	env. flex.x 500 ml	Laboratorios Te	19158.47	19158.47	\N	30/09/2005
2396	62492	SOLUCION PARENTERAL	AGUA ESTERIL PARA INYECTABLES	env.flex.x500ml dob.bol.	Laboratorios Te	19350.06	19350.06	\N	02/05/2018
2397	37403	SOLUCION PARENTERAL	INGECLOF	sol.oft.x 5 ml	Ingens	48.15	48.15	\N	18/05/2017
2398	30813	SOLUCION PARENTERAL	DIOXAFLEX	Spraygel x 25 g	Bag	30	0.3	\N	17/06/2020
2399	34340	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	613HD dext.10%aguax100ml	Rivero	19540.94	19540.94	\N	03/10/2002
2400	60582	SOLUCION PARENTERAL	NITROGRAY	25 mg a.x 25 x 5 ml	Gray	500495.16	500495.16	\N	20/05/2008
2401	8858	SOLUCION PARENTERAL	TOTAL MAGNESIANO	gran.fco.x 50 g	Temis-Lostal	20023.58	20023.58	\N	20/05/2008
2402	58084	SOLUCION PARENTERAL	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	sachet x 1 x 1000 ml	Norgreen	20075.71	200.7571	\N	01/08/2021
2403	61558	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env. flex.x 100 ml	Laboratorios Te	20288.48	202.8848	\N	01/08/2021
2404	58073	SOLUCION PARENTERAL	SOLUC. RINGER LACTATO NORGREEN	sachet x 500 ml	Norgreen	20530	20530	\N	16/10/2019
2405	58405	SOLUCION PARENTERAL	NACLOR	5% sol. oft. x 10 ml	Novoplos	21030	21030	\N	06/07/2015
2406	26799	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	613AD dext.10%aguax500ml	Rivero	21071.57	421.4314	\N	01/08/2021
2407	58085	SOLUCION PARENTERAL	SOLUC.FISIOL.DE CLORURO DE SODIO NORGREEN	sachet x 1 x 2000 ml	Norgreen	21239.34	21239.34	\N	15/05/2019
2408	44062	SOLUCION PARENTERAL	VANCOMICINA ENTEROCAPS SCHAFER	250 mg c ps.x 10	Schafer	212446.08	212446.08	\N	21/10/2021
2409	58180	SOLUCION PARENTERAL	NIGLINAR	25 mg iny.a.x50x5ml (EH)	Rivero	1.0736595e+06	1.0736595e+06	\N	15/05/2019
2410	7382	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	613Ldext.10% aguax1000ml	Rivero	21734.86	21734.86	\N	15/05/2019
2411	34344	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	656Q agua p/iny.x 250 ml	Rivero	21735.33	21735.33	\N	21/10/2021
2412	38945	SOLUCION PARENTERAL	ACULAR LS	sol.oft.x 5 ml	Abbvie	21786.65	21786.65	\N	15/05/2019
2413	40320	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	5% sachet x 1 x 100 ml	Norgreen	21908.78	219.0878	\N	01/02/2022
2414	15835	SOLUCION PARENTERAL	VANCOMICINA FABRA	500 mg iny.f.a.x 1	Fabra	21947	21947	\N	06/07/2015
2415	61397	SOLUCION PARENTERAL	CITRATO DE MAGNESIO	pvo.x 200 g	Lafarmen	22000	22000	\N	21/10/2021
2416	60970	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA ISOTONICA RIGECIN	12 sach. x 500ml	Rigecin	264460.2	264460.2	\N	21/10/2021
2417	7455	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	1056 agua p/irri.x2000ml	Rivero	22042.69	22042.69	\N	06/07/2015
2418	41205	SOLUCION PARENTERAL	OMATEX	20 mg jga.prell.x 10	Elea	222327.53	222327.53	\N	29/07/2008
2419	14469	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	620LD isot.cl.sod.x1000m	Rivero	23074.74	23074.74	\N	18/05/2017
2420	14337	SOLUCION PARENTERAL	VANCOMICINA RICHET	500 mg iny.IV f.a.x 1	Richet	23542.69	23542.69	\N	15/05/2019
2421	7383	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	617Adext.5% salinax500ml	Rivero	23868.53	23868.53	\N	15/05/2019
2422	61560	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env. flex.x 500 ml	Laboratorios Te	23986.13	23986.13	\N	21/10/2021
2423	29015	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	645Q manitol 15% x 250ml	Rivero	24457.28	24457.28	\N	21/10/2021
2424	29214	SOLUCION PARENTERAL	OPTI FREE EXPRESS	env.x 355 ml	Alcon	24640	24640	\N	21/10/2021
2425	58080	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	25% sachet x 1 x 500 ml	Norgreen	24702.14	24702.14	\N	15/05/2019
2426	59769	SOLUCION PARENTERAL	SOLUC.PARENT. MAXFUSOR PLUS	513AP dext.10%aguax500ml	Rivero	24814.39	24814.39	\N	28/01/2022
2427	38669	SOLUCION PARENTERAL	SALDIET DHARAM SINGH	ajo env.x 140 g s/sodio	Dharam Singh	25000	25000	\N	28/01/2022
2428	38668	SOLUCION PARENTERAL	SALDIET DHARAM SINGH	natural env.x140g s/sod.	Dharam Singh	25000	2500	\N	06/05/2020
2429	62495	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env.flex.x500ml dob.bol.	Laboratorios Te	25251.48	25251.48	\N	28/01/2022
2430	58081	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	50% sachet x 1 x 500 ml	Norgreen	25354.16	1267.708	\N	10/04/2025
2431	7387	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	624A Ringer lact.x 500ml	Rivero	25425.2	25425.2	\N	15/05/2019
2432	55506	SOLUCION PARENTERAL	OPTI FREE PUREMOIST	env.x 300 ml	Alcon	25791	257.91	\N	01/08/2021
2433	2220	SOLUCION PARENTERAL	RELIVERAN	ad.gts.x 60 ml	Gador	25967.92	25967.92	\N	21/10/2021
2434	57853	SOLUCION PARENTERAL	SOLUC. DEXTROSA 5% JAYOR BOLSA SIMPLE	sachet x 50 ml	Jayor	26065.26	26065.26	\N	28/01/2022
2435	62334	SOLUCION PARENTERAL	LAMUNA	25mcg/h parche matriz.x5	Amarin Technolo	130570.98	130570.98	\N	21/10/2021
2436	47637	SOLUCION PARENTERAL	RIVERVAN	2 g f.a.x 1	Rivero	26438.97	26438.97	\N	28/01/2022
2437	7161	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	631H dext.5% agua x100ml	Rivero	26462.93	26462.93	\N	15/05/2019
2438	62499	SOLUCION PARENTERAL	SOLUC. DEXTROSA 25% EN AGUA	env.flex.x500ml dob.bol.	Laboratorios Te	26728.49	26728.49	\N	28/01/2022
2439	15341	SOLUCION PARENTERAL	INDICAN	spray x 60 ml	Sidus	26760.89	26760.89	\N	10/01/2022
2440	18929	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	3054 isot.cl.sod.x3000ml	Rivero	27067.63	27067.63	\N	28/06/2021
2441	23464	SOLUCION PARENTERAL	NIGLINAR 50	200 mcg/ml f.a.x 250 ml	Rivero	27085.08	27085.08	\N	28/03/2023
2442	58105	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	625AD Ring3cl.isot.500ml	Rivero	27270.09	27270.09	\N	28/01/2022
2443	60963	SOLUCION PARENTERAL	SOLUC. DEXTROSA 5% EN SOLUC. FISIOL. RIGECIN	sach. x 500 ml x 12	Rigecin	331935.38	331935.38	\N	16/10/2019
2444	34167	SOLUCION PARENTERAL	ONDANSETRON	8 mg a.x 100 x 4 ml	Veinfar	2.77485e+06	2.77485e+06	\N	28/01/2022
2445	22960	SOLUCION PARENTERAL	FRIDALIT 500	500 mg f.a.x 100 x 10 ml	Fada Pharma	2.803213e+06	28032.129	\N	13/05/2024
2446	54519	SOLUCION PARENTERAL	VANCOMICINA ENTEROCAPS SCHAFER	250 mg c ps.x 12	Schafer	341431.2	3414.312	\N	11/08/2025
2447	58078	SOLUCION PARENTERAL	SOLUC.DEXTROSA NORGREEN	5% sachet x 1 x 1000 ml	Norgreen	28471.99	28471.99	\N	15/11/2024
2448	57852	SOLUCION PARENTERAL	SOLUC. FISIOLOGICA JAYOR BOLSA SIMPLE	sachet x 50 ml	Jayor	29035.52	290.3552	\N	22/10/2025
2449	7164	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	632H dext.10% aguax100ml	Rivero	29287.97	292.8797	\N	22/10/2025
2450	25922	SOLUCION PARENTERAL	METAFLEX N.F.	sup.x 10	Montpellier	25.56	25.56	\N	21/12/2023
2451	28761	SOLUCION PARENTERAL	MURO 128 5%	sol.oft.x 15 ml	Bausch & Lomb A	30380.26	30380.26	\N	15/11/2024
2452	58440	SOLUCION PARENTERAL	ESPIROTECH INYECTABLE	f.a.x 50+disolv.x50	Biosintex Tr. E	1.5337719e+06	61350.875	\N	16/10/2025
2453	7396	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G52 sulf.mag.x 10 ml	Rivero	30833.28	30833.28	\N	08/07/2022
2454	7399	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G58 clor.cromo x 10 ml	Rivero	30833.29	308.3329	\N	02/07/2024
2455	7400	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G59 sulf.mang.x 10 ml	Rivero	30833.29	308.3329	\N	23/10/2025
2456	7401	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G60 molib.amon.x 10 ml	Rivero	30833.29	30833.29	\N	28/01/2022
2457	24232	SOLUCION PARENTERAL	ALFACORT	1% emuls.x 100 ml	Cassar	31200	312	\N	13/08/2025
2458	59660	SOLUCION PARENTERAL	DIANEAL BAXTER	1.5% PD2 bolsa x 2000 ml	Aponor	31323.72	313.2372	\N	11/08/2025
2459	21224	SOLUCION PARENTERAL	TOTAL MAGNESIANO LIMON	pvo.gran.x 50 g	Temis-Lostal	31495.78	314.9578	\N	06/10/2025
2460	62496	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env.flex.x250ml dob.bol.	Laboratorios Te	31896.72	318.9672	\N	13/05/2024
2461	7389	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	626A elect.balanc.x500ml	Rivero	32170.59	321.7059	\N	02/09/2024
2462	14479	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G55 sulf.cobre x 10 ml	Rivero	32320.1	32320.1	\N	02/12/2024
2463	59665	SOLUCION PARENTERAL	DIANEAL BAXTER	2.5% PD2 bolsa x 2000 ml	Aponor	32379.22	32379.22	\N	02/12/2024
2464	14470	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	620LDDBisot.cl.sod.x1000	Rivero	32873.52	32873.52	\N	28/05/2025
2465	51430	SOLUCION PARENTERAL	INDICAN GEL	5% pote x 20 g	Sidus	33218.59	33218.59	\N	02/09/2024
2466	62506	SOLUCION PARENTERAL	SOLUC. MOLAR CLORURO DE POTASIO	env.flex.x100ml dob.bol.	Laboratorios Te	33389.11	33389.11	\N	02/12/2024
2467	59107	SOLUCION PARENTERAL	MIDAZOLAM B.BRAUN	1 mg/ml EP x 10 x 100 ml	B. Braun	336091.75	336091.75	\N	19/01/2024
2468	47166	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	parent.gliserof.sodx20ml	Rivero	33724.87	33724.87	\N	19/04/2024
2469	43806	SOLUCION PARENTERAL	PROAVENAL H	emuls.x 50 g	Panalab	34131.88	34131.88	\N	13/05/2024
2470	4243	SOLUCION PARENTERAL	SOLUC.PARENT.PARENTGLASS	963A amino c.5% x 500 ml	Rivero	34463.14	3446.314	\N	15/11/2024
2471	59670	SOLUCION PARENTERAL	DIANEAL BAXTER	4.25% PD2 bolsa x 2000ml	Aponor	34843.23	1393.7292	\N	27/06/2025
2472	58856	SOLUCION PARENTERAL	SOLUC.FISIOL.CLORURO DE SODIO BINA PHARMA	sachet x 1 x 500 ml	Bina Pharma S.A	35438	35438	\N	28/05/2025
2473	18930	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	3056agua p/irrig.x3000ml	Rivero	35991.9	35991.9	\N	15/01/2024
2474	61571	SOLUCION PARENTERAL	SOLUC. DEXTROSA 25% EN AGUA	env. flex. x 500 ml	Laboratorios Te	36364.86	36364.86	\N	02/12/2024
2475	7402	SOLUCION PARENTERAL	ADITIVOS PARENTERALES	G62  c.selenioso x 10 ml	Rivero	36606.2	36606.2	\N	01/01/2024
2476	57223	SOLUCION PARENTERAL	VANCOMICINA GEMEPE	500 mg f.a.x 50	Gemepe	1.8329331e+06	1.8329331e+06	\N	02/12/2024
2477	55065	SOLUCION PARENTERAL	ESPASEVIT	8 mg a.x 25 x 4 ml	Richmond	921602.6	921602.6	\N	01/08/2025
2478	45499	SOLUCION PARENTERAL	ENOXANORTH	40 mg jga.prell.x 10	Lab Internacion	369552.7	369552.7	\N	13/05/2024
2479	61561	SOLUCION PARENTERAL	SOLUC. CLORURO DE SODIO 0.9%	env. flex.x 1000 ml	Laboratorios Te	37362.48	37362.48	\N	15/11/2024
2480	21629	SOLUCION PARENTERAL	VAREDET	500 mg iny.f.a.x 25x10ml	Fada Pharma	936737.9	936737.9	\N	02/09/2024
2481	8859	SOLUCION PARENTERAL	TOTAL MAGNESIANO	gran.fco.x 100 g	Temis-Lostal	37556.74	37556.74	\N	19/04/2024
2482	38684	SOLUCION PARENTERAL	NOREPINEFRINA GRAY	1 mg a.x 1 x 4 ml	Gray	37582.66	37582.66	\N	02/12/2024
2483	61572	SOLUCION PARENTERAL	SOLUC. DEXTROSA 50% EN AGUA	env. flex. x 500 ml	Laboratorios Te	37956.98	1518.2792	\N	06/10/2025
2484	62504	SOLUCION PARENTERAL	SOLUC. DEXTROSA 50% EN AGUA	env.flex.x500ml dob.bol.	Laboratorios Te	38336.54	38336.54	\N	14/05/2024
2485	9219	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	624L Ringer lact.x1000ml	Rivero	38627.83	38627.83	\N	02/09/2024
2486	60273	SOLUCION PARENTERAL	ENOXANORTH	40 mg jga.prell.x 2	Lab Internacion	77773.08	77773.08	\N	14/05/2024
2487	32595	SOLUCION PARENTERAL	DILUTOL	40mg jga.prell.x 2x0.4ml	Lazar	78104.52	78104.52	\N	29/02/2024
2488	11808	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	615A dext.25% aguax500ml	Rivero	39961.49	39961.49	\N	01/12/2025
2489	14338	SOLUCION PARENTERAL	VANCOMICINA RICHET	1 g iny.IV f.a.x 1	Richet	40204.56	40204.56	\N	02/09/2024
2490	34341	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	631A dext.5% agua x500ml	Rivero	40530.39	40530.39	\N	02/09/2024
2491	40317	SOLUCION PARENTERAL	CLORURO DE POTASIO NORGREEN	1Molar sachet x1 x100 ml	Norgreen	41682.02	41682.02	\N	01/12/2025
2492	26800	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	634H cl.pot.mol.x 100 ml	Rivero	42202.3	42202.3	\N	01/08/2025
2493	61851	SOLUCION PARENTERAL	CEFEPIME KILAB	1g f.a.x 100	Kilab	4.235e+06	4.235e+06	\N	02/09/2024
2494	59669	SOLUCION PARENTERAL	DIANEAL BAXTER	2.5% PD4 bolsa x 2500 ml	Aponor	43465.5	43465.5	\N	10/04/2025
2495	59664	SOLUCION PARENTERAL	DIANEAL BAXTER	1.5% PD4 bolsa x 2500 ml	Aponor	44169.16	44169.16	\N	01/08/2025
2496	42451	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	623A hiper.cl.sod.x500ml	Rivero	44796.7	44796.7	\N	02/12/2024
2497	58627	SOLUCION PARENTERAL	CEFEPIME PHARMAVIAL	1 g f.a.x 100	IBC	4.5002445e+06	4.5002445e+06	\N	14/05/2024
2498	58106	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	637H hiper.cl.sod.x100ml	Rivero	45488.54	45488.54	\N	02/09/2024
2499	59662	SOLUCION PARENTERAL	DIANEAL BAXTER	1.5% PD2 bolsa x 2500 ml	Aponor	45753.58	45753.58	\N	02/09/2024
2500	63402	SOLUCION PARENTERAL	NOLISIM	100 mg/2ml IM/IV f.a.x25	Fada Pharma	1.1444222e+06	1.1444222e+06	\N	02/09/2024
2501	59667	SOLUCION PARENTERAL	DIANEAL BAXTER	2.5% PD2 bolsa x 2500 ml	Aponor	46633.16	46633.16	\N	02/12/2024
2502	61449	SOLUCION PARENTERAL	SOLUC. GLICINA BAXTER	1.5% bolsa x 3000 ml	Aponor	46998	46998	\N	02/09/2024
2503	62335	SOLUCION PARENTERAL	LAMUNA	50mcg/h parche matrizx5	Amarin Technolo	235010.75	235010.75	\N	02/09/2024
2504	59672	SOLUCION PARENTERAL	DIANEAL BAXTER	4.25% PD2 bolsa x 2500ml	Aponor	48040.5	48040.5	\N	01/12/2025
2505	7362	SOLUCION PARENTERAL	SOLUC.PARENT.PARENTGLASS	966A amino c.8.5% x500ml	Rivero	48500.64	48500.64	\N	02/12/2024
2506	38282	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	641H acet.pot.mol.x100ml	Rivero	50619.68	50619.68	\N	02/09/2024
2507	58561	SOLUCION PARENTERAL	NAUSEDRON	8 mg/4 ml a. x 1	IMA	50701.19	50701.19	\N	02/09/2024
2508	18931	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	3062 glicina 1.5%x3000ml	Rivero	52111.88	52111.88	\N	02/09/2024
2509	59661	SOLUCION PARENTERAL	DIANEAL BAXTER	1.5% PD2 bolsa x 6000 ml	Aponor	52359.75	52359.75	\N	02/09/2024
2510	59663	SOLUCION PARENTERAL	DIANEAL BAXTER	1.5% PD4 bolsa x 6000 ml	Aponor	52549.55	52549.55	\N	02/09/2024
2511	21320	SOLUCION PARENTERAL	CLEXANE	40 mg jga.prell.x 2	Sanofi-Aventis	105457.73	105457.73	\N	02/09/2024
2512	59668	SOLUCION PARENTERAL	DIANEAL BAXTER	2.5% PD4 bolsa x 6000 ml	Aponor	52740.51	52740.51	\N	02/09/2024
2513	63576	SOLUCION PARENTERAL	AGUA DESTILADA INYECTABLE JAYOR	bolsa x 12 x 1000 ml	Jayor	53441.96	53441.96	\N	02/12/2024
2514	59666	SOLUCION PARENTERAL	DIANEAL BAXTER	2.5% PD2 bolsa x 6000 ml	Aponor	53882.82	53882.82	\N	02/09/2024
2515	7363	SOLUCION PARENTERAL	SOLUC.PARENT.PARENTGLASS	967A amino c.11.5%x500ml	Rivero	54878.53	54878.53	\N	01/08/2025
2516	45500	SOLUCION PARENTERAL	ENOXANORTH	60 mg jga.prell.x 10	Lab Internacion	549731.8	549731.8	\N	02/09/2024
2517	58857	SOLUCION PARENTERAL	SOLUC.FISIOL.CLORURO DE SODIO BINA PHARMA	sachet x 1 x 1000 ml	Bina Pharma S.A	55688	55688	\N	02/09/2024
2518	61450	SOLUCION PARENTERAL	CLORURO DE SODIO BAXTER	0,9% bolsa x 1000 ml	Aponor	56725	56725	\N	02/09/2024
2519	59671	SOLUCION PARENTERAL	DIANEAL BAXTER	4.25% PD2 bolsa x 6000ml	Aponor	57118.77	57118.77	\N	02/09/2024
2520	38280	SOLUCION PARENTERAL	SOLUC.PARENT.PARENTGLASS	978Q traximin 10% x250ml	Rivero	58200.77	58200.77	\N	02/09/2024
2521	57224	SOLUCION PARENTERAL	VANCOMICINA GEMEPE	1000 mg f.a.x 50	Gemepe	2.9114252e+06	2.9114252e+06	\N	02/09/2024
2522	62190	SOLUCION PARENTERAL	CEFEPIME RICHET	1 g f.a.x 25	Richet	1.4836474e+06	1.4836474e+06	\N	28/05/2025
2523	16330	SOLUCION PARENTERAL	ESPASEVIT	8 mg a.x 1 x 4 ml	Richmond	62146.28	62146.28	\N	01/08/2025
2524	21226	SOLUCION PARENTERAL	TOTAL MAGNESIANO LIMON	pvo.gran.x 100 g	Temis-Lostal	62974.94	62974.94	\N	02/09/2024
2525	49045	SOLUCION PARENTERAL	PROAVENAL H	cr.x 100 g	Panalab	64525	64525	\N	02/09/2024
2526	44791	SOLUCION PARENTERAL	PROAVENAL H	emuls.x 100 g	Panalab	64525	64525	\N	02/09/2024
2527	22632	SOLUCION PARENTERAL	TIOSALIS	8 mg f.a.x 1	Tuteur	64947.99	64947.99	\N	02/09/2024
2528	59074	SOLUCION PARENTERAL	SOLUC.FISIOL. DE CLORURO DE SODIO	sachet x 2000 ml	HLB Pharma	65831.62	65831.62	\N	02/09/2024
2529	13423	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	679A sol.ACD for.A 500ml	Rivero	67146.43	67146.43	\N	12/11/2025
2530	55620	SOLUCION PARENTERAL	SOLUC. GLUCOSALINA BOLSA SIMPLE	sachet x 500 ml	Jayor	67930.64	67930.64	\N	17/06/2025
2531	13421	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	629A Coropar x 500 ml	Rivero	68377	68377	\N	12/11/2025
2532	62508	SOLUCION PARENTERAL	SOLUC. GLICINA 1.5% EN AGUA	env. flex. 1000 ml	Laboratorios Te	69587	69587	\N	02/09/2024
2533	58628	SOLUCION PARENTERAL	CEFEPIME PHARMAVIAL	2 g f.a.x 50	IBC	3.511915e+06	3.511915e+06	\N	17/06/2025
2534	38281	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	627A isot.poliel.x 500ml	Rivero	71951.47	71951.47	\N	02/09/2024
2535	60170	SOLUCION PARENTERAL	IMIPENEM CILASTATIN RICHET	500 mg IV f.a.x 25	Richet	1.8257369e+06	1.8257369e+06	\N	17/06/2025
2536	61349	SOLUCION PARENTERAL	ONDANSETRON KABI	8 mg/4 ml sol.iny.x 10	Fresenius Kabi	746461.56	746461.56	\N	12/11/2025
2537	60902	SOLUCION PARENTERAL	ONDANSETRON KABI	8 mg/4 ml sol.iny.x 1	Fresenius Kabi	74646.16	74646.16	\N	12/11/2025
2538	59771	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	2079 sol.ACD x 2000 ml	Rivero	75846.64	75846.64	\N	30/06/2025
2539	61852	SOLUCION PARENTERAL	CEFEPIME KILAB	2g f.a.x 50	Kilab	4.1125e+06	4.1125e+06	\N	12/11/2025
2540	52825	SOLUCION PARENTERAL	MERANT 500	500 mg f.a.x 10	Schafer	825000	825000	\N	02/09/2024
2541	58107	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	3075Certesol negrx3000ml	Rivero	83858.8	83858.8	\N	17/06/2025
2542	58108	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	3076Certesol0/2.5x3000ml	Rivero	83858.8	83858.8	\N	02/09/2024
2543	58109	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	3077Certesol2/3.5x3000ml	Rivero	83858.8	83858.8	\N	02/09/2024
2544	60411	SOLUCION PARENTERAL	IMIPENEM CILASTATINA LARJAN	a.x 100	Veinfar	8.41013e+06	8.41013e+06	\N	17/06/2025
2545	17107	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	618A dext.70% aguax500ml	Rivero	85818.89	85818.89	\N	17/06/2025
2546	56878	SOLUCION PARENTERAL	MEROPENEM PHARMAVIAL	500 mg f.a.x 50 E.H.	IBC	4.2996305e+06	4.2996305e+06	\N	02/09/2024
2547	51345	SOLUCION PARENTERAL	COLISTYN	100mg/4ml sol.p/inh. x30	Lafedar	2.5848522e+06	2.5848522e+06	\N	02/09/2024
2548	18928	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	679Ssol.ACD form.A 600ml	Rivero	86526.62	86526.62	\N	02/09/2024
2549	38283	SOLUCION PARENTERAL	LORIHESS	130/0.4 6% sol.x 500 ml	Rivero	90786.8	90786.8	\N	02/09/2024
2550	57561	SOLUCION PARENTERAL	FADA MEROPENEM	500 mg f.a.x 25	Fada Pharma	2.275537e+06	2.275537e+06	\N	02/09/2024
2551	62192	SOLUCION PARENTERAL	MEROPENEM RICHET	500 mg IV iny.f.a.x 50	Richet	4.681901e+06	4.681901e+06	\N	02/09/2024
2552	56875	SOLUCION PARENTERAL	IMIPENEM CILASTATINA PHARMAVIAL	500 mg f.a.x 50	IBC	4.6882205e+06	4.6882205e+06	\N	23/09/2025
2553	57207	SOLUCION PARENTERAL	CILASTATINA GEMEPE	500 mg f.a.x 50	Gemepe	4.825331e+06	4.825331e+06	\N	02/09/2024
2554	20501	SOLUCION PARENTERAL	SOLUC.PARENT.PARENTGLASS	978A traximin 10% x500ml	Rivero	101389.93	101389.93	\N	02/09/2024
2555	40306	SOLUCION PARENTERAL	IMIPENEM CILASTATINA NORGREEN	500 mg f.a.x 1 x 20 ml	Norgreen	103398.72	103398.72	\N	02/09/2024
2556	37475	SOLUCION PARENTERAL	MEROPENEM RICHET	500 mg IV iny.f.a.x 1	Richet	105589.94	105589.94	\N	02/09/2024
2557	58104	SOLUCION PARENTERAL	SOLUC.PARENT.SOLUFLEX	618L dext.70%aguax1000ml	Rivero	107175.39	107175.39	\N	02/09/2024
2558	62191	SOLUCION PARENTERAL	CEFEPIME RICHET	2 g f.a.x 25	Richet	2.8040935e+06	280409.34	\N	02/12/2025
2559	54522	VANCOMICINA	ESPIROTECH INHALATORIO	f.a.x 30+disolv.x30	Biosintex Tr. E	3.4889942e+06	3.4889942e+06	\N	01/12/1995
23	62836	VANCOMICINA	MEROPENEM CELTYC	500 mg f.a.x 25	Celtyc	2.9177e+06	2.9177e+06	\N	23/04/2002
2561	38284	VANCOMICINA	HESSICO	200/0.5 6% sol.x 500 ml	Rivero	118929.07	118929.07	\N	13/01/2005
2562	63010	VANCOMICINA	BUCCOLAM	10 mg jer.prell. x 4	Tuteur	498284.8	498284.8	\N	21/04/2008
2563	63008	VANCOMICINA	BUCCOLAM	5 mg jer.prell. x 4	Tuteur	498284.8	498284.8	\N	01/12/1995
2564	63009	VANCOMICINA	BUCCOLAM	7.5 mg jer.prell. x 4	Tuteur	498284.8	498284.8	\N	11/02/2003
2565	14464	VANCOMICINA	SOLUC.PARENT.PARENTGLASS	DB70 arginina 10%x 250ml	Rivero	138137.38	138137.38	\N	28/06/2002
2566	40314	VANCOMICINA	MEROPENEM NORGREEN	1000 mg f.a.x 1 x 20 ml	Norgreen	138342.61	1383.4261	\N	24/06/2010
2567	56880	VANCOMICINA	MEROPENEM PHARMAVIAL	1000 mg f.a.x 50 E.H.	IBC	7.92593e+06	7.92593e+06	\N	16/06/2017
2568	52826	VANCOMICINA	MERANT 1000	1000 mg f.a.x 10	Schafer	1.625e+06	16250	\N	24/06/2010
21	62866	VANCOMICINA	MEROPENEM CELTYC	1000 mg f.a.x 25	Celtyc	4.6521e+06	4.6521e+06	\N	02/09/2024
2570	62193	VANCOMICINA	MEROPENEM RICHET	1 g IV iny.f.a.x 50	Richet	9.655754e+06	965575.4	\N	01/06/2024
2571	37476	VANCOMICINA	MEROPENEM RICHET	1 g IV iny.f.a.x 1	Richet	195295.22	195295.22	\N	17/12/2025
2572	55963	VANCOMICINA	AMUCHINA 100%	bid n x 5000 ml	Iraola	249158.62	4983.1724	\N	27/06/2025
2573	17109	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-58 Eurocollins x1000ml	Rivero	281242.22	281242.22	\N	17/12/2025
2574	12514	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-51 sol.p/ind.x 830 ml	Rivero	356525.88	14261.035	\N	06/10/2025
2575	12515	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-52 sol.p/mant.x 815 ml	Rivero	356525.88	7130.5176	\N	06/10/2025
2576	12516	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-53 sol.p/rep.x 500 ml	Rivero	356525.88	356525.88	\N	20/12/2025
2577	14473	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-54 sol.p/rep.x 500 ml	Rivero	356525.88	7130.5176	\N	13/08/2025
2578	17597	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-55 sol.p/mant.x 815 ml	Rivero	356525.88	3565.2588	\N	23/10/2025
2579	38286	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-64 kantrilex x 500 ml	Rivero	356525.88	7130.5176	\N	27/06/2025
2580	14471	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-45/44 St.Thom. x1000ml	Rivero	427831.06	8556.621	\N	06/10/2025
2581	51720	VANCOMICINA	SOLUC.P/CARDIOPLEGIA RIVERO	L-65 kantrilex x 1000 ml	Rivero	427831.06	17113.242	\N	06/10/2025
2582	61350	VANCOMICINA	SMOFLIPID 20% 500 ML	env.x 500 ml x 10	Fresenius Kabi	6.8117165e+06	136234.33	\N	13/08/2025
2583	61348	VANCOMICINA	SMOFLIPID 20% 500 ML	env.x 500 ml	Fresenius Kabi	681171.6	13623.433	\N	04/08/2025
2584	18896	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 100 x 5 ml	Welt	84.06	4.203	\N	01/02/2003
2585	48373	DICLOFENAC SODICO	VOLTAREN 24 HS	15 mg parches x 2	Novartis Consum	95.11	15.851666	\N	27/08/2015
2586	25794	DICLOFENAC SODICO	AGUA DESTILADA	a.x 100 x 5 ml	Norgreen	112.31	8.022142	\N	15/04/2011
2587	25797	DICLOFENAC SODICO	SOLUC.FISIOLOGICA	a.x 100 x 5 ml	Norgreen	112.31	8.022142	\N	16/04/2012
2588	25795	DICLOFENAC SODICO	AGUA DESTILADA	a.x 100 x 10 ml	Norgreen	135.44	4.5146666	\N	17/02/2020
2589	22542	DICLOFENAC SODICO	SOLUC.PARENT.250 ML	fisiol.clor.sodio	Landi	1.64	0.05466667	\N	08/04/2025
2590	15617	DICLOFENAC SODICO	AGUA DESTILADA	a.x 100 x 10 ml	Veinfar	185	185	\N	03/09/2014
2591	22543	ENOXAPARINA SODICA	SOLUC.PARENT.250 ML	isot.dext.5% en agua	Landi	2.1	2.1	\N	03/08/2010
2592	22544	ENOXAPARINA SODICA	SOLUC.PARENT.250 ML	dext.10% en agua	Landi	2.18	1.09	\N	03/08/2010
2593	22546	ENOXAPARINA SODICA	SOLUC.PARENT.500 ML	fisiol.clor.sodio	Landi	2.32	1.16	\N	30/09/2022
2594	22547	ENOXAPARINA SODICA	SOLUC.PARENT.500 ML	isot.dext.5% en agua	Landi	2.59	0.259	\N	01/12/2025
2595	25796	FENTANILO	AGUA DESTILADA	a.x 100 x 20 ml	Norgreen	260.96	260.96	\N	03/04/2002
2596	13266	FENTANILO	SOLUC.PARENT.100 ML	fisiol.clor.sodio	Fidex	2.74	0.1096	\N	30/09/2019
2597	22545	FLUMAZENIL	SOLUC.PARENT.500 ML	dext.10% en agua	Landi	3.06	0.153	\N	14/09/2000
2598	40351	FLUMAZENIL	FUROSEMIDA NORGREEN	20 mg a.x 1 x 2 ml	Norgreen	3.1	3.1	\N	28/01/2003
2599	2794	FUROSEMIDA	SOLUC.PARENT.500 ML	dext.5% en agua	Rigecin	3.17	0.00317	\N	25/04/2002
2600	6871	FUROSEMIDA	SOLUC.PARENT.500 ML	fisiol.clor.sodio	Roux Ocefa	3.32	0.166	\N	18/01/2003
2601	2898	FUROSEMIDA	SOLUC.PARENT.500 ML	dext.10% en agua	Rigecin	3.5	0.175	\N	18/01/2003
2602	6872	FUROSEMIDA	SOLUC.PARENT.500 ML	isot.dext.5% en agua	Roux Ocefa	3.68	0.0368	\N	09/01/2009
2603	3586	FUROSEMIDA	SOLUC.PARENT.250 ML	fisiol.clor.sodio	Fidex	3.74	0.083111115	\N	12/11/2018
2604	3046	FUROSEMIDA	SOLUC.PARENT.500 ML	electrol.balanc.	Rigecin	4.01	0.0401	\N	22/12/2025
2605	3345	FUROSEMIDA	SOLUC.PARENT.500 ML	fisiol.de ringer	Rigecin	4.01	0.0401	\N	04/08/2025
2606	3585	HIDROCORTISONA	SOLUC.PARENT.100 ML	bicarb.sod.sol.molar	Fidex	4.22	4.22	\N	01/02/2003
2607	3584	HIDROCORTISONA	SOLUC.PARENT.100 ML	clor.pot.sol.molar	Fidex	4.22	4.22	\N	01/02/2003
2608	3364	HIDROCORTISONA	SOLUC.PARENT.500 ML	Ringer lactato	Rigecin	4.53	4.53	\N	20/11/2007
2609	3588	HIDROCORTISONA	SOLUC.PARENT.250 ML	dext.10% en agua	Fidex	4.55	4.55	\N	13/04/2011
2610	2900	HIDROCORTISONA	SOLUC.PARENT.500 ML	dext.25% en agua	Rigecin	5.56	0.0556	\N	23/10/2025
2611	26528	HIDROCORTISONA	SOLUC.GLUCOSADA HIPERTONICA	25% a.x 100 x 10 ml	Fada Pharma	568.62	568.62	\N	15/12/2025
2612	3590	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	fisiol.clor.sodio	Fidex	5.93	0.98833334	\N	03/04/2002
2613	3600	HIOSCINA N-BUTILBR	SOLUC.PARENT.500 ML	bicarb.sod.1/6 molar	Fidex	6.01	0.1202	\N	10/07/2003
2614	3592	IMIPENEM+CILASTATIN	SOLUC.PARENT.500 ML	dext.10% en agua	Fidex	6.77	1.354	\N	28/06/2021
2615	3597	KETOROLAC	SOLUC.PARENT.500 ML	fisiol.de ringer	Fidex	7.29	0.3645	\N	23/11/2000
2616	3593	KETOROLAC	SOLUC.PARENT.500 ML	dext.25% en agua	Fidex	8.52	1.704	\N	05/01/2009
2617	3604	KETOROLAC	SOLUC.PARENT.1000 ML	fisiol.clor.sodio	Fidex	9.17	9.17	\N	08/08/2008
2618	2927	KETOROLAC	SOLUC.PARENT.500 ML	dext.50% en agua	Rigecin	9.29	3.0966666	\N	26/04/2002
2619	3594	LIDOCAINA	SOLUC.PARENT.500 ML	dext.50% en agua	Fidex	15.36	15.36	\N	26/04/2002
2620	41928	LIDOCAINA	SOLVENTE INDOLORO DRAWER	iny.a.x 100 x 5 ml	Drawer	1905	1905	\N	28/01/2003
2621	12903	LIDOCAINA + ADRENALINA	SOLUC.PARENT.100 ML	fisiol.clor.sodio	Roux Ocefa	28.12	28.12	\N	06/04/2022
2622	6854	LIDOCAINA + ADRENALINA	SOLUC.PARENT.250 ML	fisiol.clor.sodio	Roux Ocefa	29.14	29.14	\N	15/08/2000
2623	12904	LIDOCAINA + ADRENALINA	SOLUC.PARENT.100 ML	isot.dext.5% en agua	Roux Ocefa	29.84	29.84	\N	04/07/2007
2624	6855	MAGNESIO	SOLUC.PARENT.250 ML	isot.dext.5% en agua	Roux Ocefa	32.8	0.656	\N	01/12/1997
2625	29986	MAGNESIO	SOLUC.PARENT.500 ML	fisiol.clor.sodio	Roux Ocefa	38.41	1.9205	\N	27/11/2018
2626	7248	MAGNESIO	LIDOCAINA	1% f.a.x 20 ml	Richmond	41.21	0.27473333	\N	29/10/2025
2627	29987	MAGNESIO	SOLUC.PARENT.500 ML	isot.dext.5% en agua	Roux Ocefa	42.83	1.4276667	\N	04/08/2025
2628	6856	MAGNESIO	SOLUC.PARENT.250 ML	dext.10% en agua	Roux Ocefa	44.87	44.87	\N	21/08/2025
2629	7252	MEROPENEM	LIDOCAINA	2% f.a.x 20 ml	Richmond	47.45	47.45	\N	19/12/2006
2630	44146	MEROPENEM	NITROGRAY	25 mg a.x 5 ml	Gray	49.95	9.99	\N	01/08/2021
2631	6847	MEROPENEM	SOLUC.PARENT.100 ML	clor.pot.sol.molar	Roux Ocefa	54.92	1.0984	\N	06/10/2025
2632	6878	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	fisiol.de ringer	Roux Ocefa	66.09	33.045	\N	01/02/2003
2633	6873	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	dext.10% en agua	Roux Ocefa	66.33	3.3165	\N	06/02/2018
2634	6876	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	dext.5% sol.sal.normal	Roux Ocefa	69.35	0.6935	\N	16/06/2005
2635	6894	METOCLOPRAMIDA	SOLUC.PARENT.1000 ML	fisiol.clor.sodio	Roux Ocefa	74.6	74.6	\N	05/09/2002
2636	6884	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	electrol.balanc.	Roux Ocefa	80.52	80.52	\N	10/09/2014
2637	6874	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	dext.25% en agua	Roux Ocefa	82.55	8.255	\N	03/03/2020
2638	6875	METOCLOPRAMIDA	SOLUC.PARENT.500 ML	dext.50% en agua	Roux Ocefa	108.48	108.48	\N	05/12/2025
2639	6885	MIDAZOLAM	SOLUC.PARENT.500 ML	d-manitol al 15%	Roux Ocefa	150.86	75.43	\N	07/11/2015
2640	6910	MIDAZOLAM	SOLUC.PARENT.2000 ML	fisiol.clor.sodio	Roux Ocefa	164.78	1.6478	\N	01/08/2021
2641	63812	POTASIO CLORURO	FURTENK	40 mg comp.x 30	Biotenk	12385	12385	\N	01/04/2002
2642	64266	POTASIO CLORURO	KOLKIN	40 mg comp.x 1000	Duncan	474000	4740	\N	01/08/2021
2643	24575	POTASIO CLORURO	DICLOFENAC SODICO	75 mg a.x 100 x 3 ml	Veinfar	541250	5412.5	\N	02/07/2024
2644	63752	RANITIDINA	HIDROCORT	10 mg comp.x 30	Montpellier	17305.48	576.8493	\N	01/10/2000
2645	59283	RANITIDINA	FLEXANA	gel t pico x 50 g	HLB Pharma	6498.14	216.60466	\N	28/04/2022
2646	15616	RANITIDINA	AGUA DESTILADA	a.x 100 x 5 ml	Veinfar	268210	26821	\N	20/11/2020
2647	15627	SODIO CLORURO	SOLVENTE INDOLORO	1% a.x 100 x 5 ml	Veinfar	357240	357240	\N	19/10/2020
2648	19563	SODIO CLORURO	SOLUC.GLUCOSADA HIPERTONICA	50% a.x 100 x 10 ml	Veinfar	478720	478720	\N	02/07/2024
2649	64115	SOLUCION PARENTERAL	HIDROCORTISONA PHARMAVIAL	100 mg f.a.x 100	IBC	1.4151542e+06	14151.543	\N	06/04/2022
2650	18163	SOLUCION PARENTERAL	LIDOCAINA	2% s/epi.f.a.x 20 ml	Scott-Cassar	14650	14650	\N	30/09/2005
2651	18160	SOLUCION PARENTERAL	LIDOCAINA	1% c/epi.f.a.x 20 ml	Scott-Cassar	16450	16450	\N	18/05/2017
2652	18164	SOLUCION PARENTERAL	LIDOCAINA	2% c/epi.f.a.x 20 ml	Scott-Cassar	17260	17260	\N	18/05/2017
2653	64329	SOLUCION PARENTERAL	ENOPARIN	20 mg jga.prell.x 10	Biofactor	238639.4	238639.4	\N	29/07/2008
11	63836	SOLUCION PARENTERAL	FLUMAZENIL CELTYC	0.5 mg/5 ml a.x 25	Celtyc	604249.5	30212.475	\N	28/05/2025
2655	64073	SOLUCION PARENTERAL	HIDROCORTISONA PHARMAVIAL	500 mg f.a.x 100	IBC	2.6166338e+06	2.6166338e+06	\N	21/10/2021
2656	56201	SOLUCION PARENTERAL	OMATEX	40 mg jga.prell.x 2	Elea	84458.13	84458.13	\N	19/04/2024
2657	56465	SOLUCION PARENTERAL	HEPARINOX	40 mg jga.prell.x 10	Denver Farma	470000	470000	\N	02/09/2024
2658	64328	SOLUCION PARENTERAL	ENOPARIN	40 mg jga.prell.x 10	Biofactor	477278.78	477278.78	\N	02/09/2024
2659	64333	SOLUCION PARENTERAL	ENOPARIN	60 mg jga.prell.x 10	Biofactor	715918.2	715918.2	\N	12/11/2025
2660	56467	SOLUCION PARENTERAL	HEPARINOX	80 mg jga.prell.x 10	Denver Farma	902000	902000	\N	02/09/2024
2661	64331	SOLUCION PARENTERAL	ENOPARIN	80 mg jga.prell.x 10	Biofactor	954557.56	954557.56	\N	02/09/2024
2662	63879	SOLUCION PARENTERAL	AGUA DESTILADA BOLSA SIMPLE	sachet x 2000 ml	Jayor	112342.27	112342.27	\N	02/12/2025
2663	63878	VANCOMICINA	SOLUC. FISIOLOGICA JAYOR BOLSA SIMPLE	sachet x 2000 ml	Jayor	168498.17	3369.9634	\N	11/11/2019
\.


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes (id, nombre, razon_social, cuit, direccion, telefono, email, organismo_jurisdiccion, activo) FROM stdin;
4	CMI	CMI					Hospital	t
\.


--
-- Data for Name: formas_pago; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formas_pago (id, nombre, activo) FROM stdin;
1	30 días	t
2	60 días	t
3	90 días	t
4	120 días	t
5	Contra entrega	t
6	Tesorería pública	t
\.


--
-- Data for Name: licitaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.licitaciones (id, numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador, portal_origen, modalidad_entrega, forma_pago, requiere_poliza, monto_poliza, observaciones, mantenimiento_oferta, numero_presupuesto, tipo_adjudicacion) FROM stdin;
1	2580	4	1	2026-02-07 10:00			\N	COMPR.AR	Abierto por demanda	120 días	t	6075		30 dias	3	Total
\.


--
-- Data for Name: mantenimientos_oferta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mantenimientos_oferta (id, nombre, activo) FROM stdin;
1	30 dias	t
\.


--
-- Data for Name: marcas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marcas (id, nombre, activo) FROM stdin;
1	Drawer	t
2	Celty	t
\.


--
-- Data for Name: modalidades_entrega; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modalidades_entrega (id, nombre, activo) FROM stdin;
1	Entrega total	t
2	Entregas parciales	t
3	Abierto por demanda	t
\.


--
-- Data for Name: motivos_perdida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.motivos_perdida (id, nombre, activo) FROM stdin;
1	Precio más alto	t
2	Marca no priorizada	t
3	No cumplía especificación	t
4	Error administrativo	t
5	Otro	t
\.


--
-- Data for Name: oferentes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oferentes (id, nombre, activo) FROM stdin;
1	Drawer	t
2	Medpharma	t
3	DNM	t
4	Suizo Barracas	t
5	CMI	t
\.


--
-- Data for Name: ofertas_productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ofertas_productos (id, producto_id, oferente, laboratorio, precio) FROM stdin;
3	1	DNM	Drawer	1500
4	1	Drawer	Northia	980
\.


--
-- Data for Name: organismos_jurisdiccion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organismos_jurisdiccion (id, nombre, activo) FROM stdin;
1	Nacional	t
2	Provincial	t
3	Municipal	t
4	Hospital	t
5	OS	t
\.


--
-- Data for Name: portales_origen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.portales_origen (id, nombre, activo) FROM stdin;
1	COMPR.AR	t
2	BAC	t
3	PBAC	t
4	Portal propio	t
5	Mail	t
6	Otro	t
\.


--
-- Data for Name: presupuestos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.presupuestos (id, numero, licitacion_id, fecha_generacion) FROM stdin;
1	1	1	2026-02-07 21:17:14.4003
2	2	1	2026-02-07 21:20:07.46643
3	3	1	2026-02-07 21:43:52.530895
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (id, licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora, motivo_perdida, numero_renglon, costo_unitario, margen_porcentaje, observaciones, producto_cotizar) FROM stdin;
3	1	fentanilo	FENTANILO CELTYC	0.25 mg a.x 50 x 5ml	100	550	Adjudicado	550		Celtyc			\N	500	25		alt-3-0
1	1	Diclofenac Sodico	DICLOFENAC CELTYC	75 mg a.x 100 x 3 ml	100	110	No Adjudicado	980	Drawer	Celtyc			5	100	10		principal
2	1	Imipenem+Cilastatin	IMIPENEM CELTYC	500 mg IV f.a.x 50	200	240	Adjudicado	240		Celtyc			2	200	20		principal
\.


--
-- Data for Name: tipos_licitacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipos_licitacion (id, nombre, activo) FROM stdin;
1	Privada	t
2	Publica	t
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, username, email, password_hash, activo, fecha_creacion) FROM stdin;
1	admin	admin@licitarte.com	scrypt:32768:8:1$zZDTnsfUXl7Mpsii$fa10cbc8efd5bd8dd48db2883595f9c78839d05f727096728f0590667cf9bda54342fbc02a9b1e50ce95e14d0f38baad15d0dc32613cdf9fdc28785f4172f754	t	2026-02-08 22:32:12.836816
\.


--
-- Name: alternativas_productos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alternativas_productos_id_seq', 16, true);


--
-- Name: celty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.celty_id_seq', 2663, true);


--
-- Name: clientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clientes_id_seq', 4, true);


--
-- Name: formas_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formas_pago_id_seq', 6, true);


--
-- Name: licitaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.licitaciones_id_seq', 1, true);


--
-- Name: mantenimientos_oferta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mantenimientos_oferta_id_seq', 1, true);


--
-- Name: marcas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marcas_id_seq', 2, true);


--
-- Name: modalidades_entrega_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modalidades_entrega_id_seq', 3, true);


--
-- Name: motivos_perdida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.motivos_perdida_id_seq', 5, true);


--
-- Name: oferentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.oferentes_id_seq', 5, true);


--
-- Name: ofertas_productos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ofertas_productos_id_seq', 4, true);


--
-- Name: organismos_jurisdiccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organismos_jurisdiccion_id_seq', 5, true);


--
-- Name: portales_origen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.portales_origen_id_seq', 6, true);


--
-- Name: presupuestos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.presupuestos_id_seq', 3, true);


--
-- Name: productos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_id_seq', 3, true);


--
-- Name: tipos_licitacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipos_licitacion_id_seq', 2, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 1, true);


--
-- Name: alternativas_productos alternativas_productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alternativas_productos
    ADD CONSTRAINT alternativas_productos_pkey PRIMARY KEY (id);


--
-- Name: celty celty_numero_registro_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celty
    ADD CONSTRAINT celty_numero_registro_key UNIQUE (numero_registro);


--
-- Name: celty celty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.celty
    ADD CONSTRAINT celty_pkey PRIMARY KEY (id);


--
-- Name: clientes clientes_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_nombre_key UNIQUE (nombre);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id);


--
-- Name: formas_pago formas_pago_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formas_pago
    ADD CONSTRAINT formas_pago_nombre_key UNIQUE (nombre);


--
-- Name: formas_pago formas_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formas_pago
    ADD CONSTRAINT formas_pago_pkey PRIMARY KEY (id);


--
-- Name: licitaciones licitaciones_numero_licitacion_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licitaciones
    ADD CONSTRAINT licitaciones_numero_licitacion_key UNIQUE (numero_licitacion);


--
-- Name: licitaciones licitaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licitaciones
    ADD CONSTRAINT licitaciones_pkey PRIMARY KEY (id);


--
-- Name: mantenimientos_oferta mantenimientos_oferta_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimientos_oferta
    ADD CONSTRAINT mantenimientos_oferta_nombre_key UNIQUE (nombre);


--
-- Name: mantenimientos_oferta mantenimientos_oferta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimientos_oferta
    ADD CONSTRAINT mantenimientos_oferta_pkey PRIMARY KEY (id);


--
-- Name: marcas marcas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas
    ADD CONSTRAINT marcas_nombre_key UNIQUE (nombre);


--
-- Name: marcas marcas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas
    ADD CONSTRAINT marcas_pkey PRIMARY KEY (id);


--
-- Name: modalidades_entrega modalidades_entrega_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modalidades_entrega
    ADD CONSTRAINT modalidades_entrega_nombre_key UNIQUE (nombre);


--
-- Name: modalidades_entrega modalidades_entrega_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modalidades_entrega
    ADD CONSTRAINT modalidades_entrega_pkey PRIMARY KEY (id);


--
-- Name: motivos_perdida motivos_perdida_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivos_perdida
    ADD CONSTRAINT motivos_perdida_nombre_key UNIQUE (nombre);


--
-- Name: motivos_perdida motivos_perdida_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivos_perdida
    ADD CONSTRAINT motivos_perdida_pkey PRIMARY KEY (id);


--
-- Name: oferentes oferentes_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferentes
    ADD CONSTRAINT oferentes_nombre_key UNIQUE (nombre);


--
-- Name: oferentes oferentes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferentes
    ADD CONSTRAINT oferentes_pkey PRIMARY KEY (id);


--
-- Name: ofertas_productos ofertas_productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_productos
    ADD CONSTRAINT ofertas_productos_pkey PRIMARY KEY (id);


--
-- Name: organismos_jurisdiccion organismos_jurisdiccion_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismos_jurisdiccion
    ADD CONSTRAINT organismos_jurisdiccion_nombre_key UNIQUE (nombre);


--
-- Name: organismos_jurisdiccion organismos_jurisdiccion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismos_jurisdiccion
    ADD CONSTRAINT organismos_jurisdiccion_pkey PRIMARY KEY (id);


--
-- Name: portales_origen portales_origen_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portales_origen
    ADD CONSTRAINT portales_origen_nombre_key UNIQUE (nombre);


--
-- Name: portales_origen portales_origen_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portales_origen
    ADD CONSTRAINT portales_origen_pkey PRIMARY KEY (id);


--
-- Name: presupuestos presupuestos_numero_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_numero_key UNIQUE (numero);


--
-- Name: presupuestos presupuestos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_pkey PRIMARY KEY (id);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id);


--
-- Name: tipos_licitacion tipos_licitacion_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_licitacion
    ADD CONSTRAINT tipos_licitacion_nombre_key UNIQUE (nombre);


--
-- Name: tipos_licitacion tipos_licitacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_licitacion
    ADD CONSTRAINT tipos_licitacion_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- Name: idx_celty_monodroga; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_celty_monodroga ON public.celty USING btree (monodroga);


--
-- Name: idx_celty_numero_registro; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_celty_numero_registro ON public.celty USING btree (numero_registro);


--
-- Name: idx_licitacion_cliente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_licitacion_cliente ON public.licitaciones USING btree (cliente_id);


--
-- Name: idx_licitacion_numero; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_licitacion_numero ON public.licitaciones USING btree (numero_licitacion);


--
-- Name: idx_marcas_nombre; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_marcas_nombre ON public.marcas USING btree (nombre);


--
-- Name: idx_oferentes_nombre; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_oferentes_nombre ON public.oferentes USING btree (nombre);


--
-- Name: idx_producto_licitacion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_producto_licitacion ON public.productos USING btree (licitacion_id);


--
-- Name: idx_producto_resultado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_producto_resultado ON public.productos USING btree (resultado);


--
-- Name: alternativas_productos alternativas_productos_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alternativas_productos
    ADD CONSTRAINT alternativas_productos_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id) ON DELETE CASCADE;


--
-- Name: licitaciones licitaciones_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licitaciones
    ADD CONSTRAINT licitaciones_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(id);


--
-- Name: licitaciones licitaciones_tipo_licitacion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licitaciones
    ADD CONSTRAINT licitaciones_tipo_licitacion_id_fkey FOREIGN KEY (tipo_licitacion_id) REFERENCES public.tipos_licitacion(id);


--
-- Name: ofertas_productos ofertas_productos_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_productos
    ADD CONSTRAINT ofertas_productos_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id) ON DELETE CASCADE;


--
-- Name: presupuestos presupuestos_licitacion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presupuestos
    ADD CONSTRAINT presupuestos_licitacion_id_fkey FOREIGN KEY (licitacion_id) REFERENCES public.licitaciones(id);


--
-- Name: productos productos_licitacion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_licitacion_id_fkey FOREIGN KEY (licitacion_id) REFERENCES public.licitaciones(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 9cDKBdtw6ofwdqK4YMFl5yMM2iMIy66AtnzDFRuAHHgcul7g7qesrihM6LwUnsk

