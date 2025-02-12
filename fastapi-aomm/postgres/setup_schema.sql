
--
-- TOC entry 000 (class AOMM Levels)
-- Name: aomm_levels; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.aomm_levels AS ENUM (
    'Initiating',
    'Emerging',
    'Performing',
    'Advancing',
    'Leading'
);


ALTER TYPE public.aomm_levels OWNER TO aomm_data;

--
-- TOC entry 001 (class Service)
-- Name: service; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.service AS ENUM (
    'Home Broadband',
    'Mobile Service',
    'Enterprise Solutions',
    'Home BB & Ent. Soln.',
    'All Services'
);


ALTER TYPE public.service OWNER TO aomm_data;

--
-- TOC entry 002 (class Operation)
-- Name: operation; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.operation AS ENUM (
    'OP_TM',
    'OP_NOC',
    'OP_NA',
    'OP_FO',
    'OP_IM',
    'OP_SO',
    'OP_CX',
    'OP_NO',
    'OP_AO',
    'OP_OT'
);

ALTER TYPE public.operation OWNER TO aomm_data;

--ALTER TYPE public.operation ADD VALUE 'OP_AO' AFTER 'OP_NP';
--ALTER TYPE public.operation ADD VALUE 'OP_OT' AFTER 'OP_AO';
--ALTER TYPE public.operation ADD VALUE 'default' BEFORE 'OP_TM';
--
-- TOC entry 003 (class Operation_Map)
-- Name: operation_map; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.operation_map (
    operation_id public.operation NOT NULL,
    operation_name character varying(255) NOT NULL
);

ALTER TABLE public.operation_map OWNER TO aomm_data;

--
-- TOC entry 0xx (class Operation_Map_PK)
-- Name: operation_map operation_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.operation_map
    ADD CONSTRAINT operation_map_pkey PRIMARY KEY (operation_id);

INSERT INTO public.operation_map (operation_id, operation_name) VALUES 
    ('OP_TM','Network Planning and Topology Management'),
    ('OP_NOC','Network Operations Center'),
    ('OP_NA','Service Operations Center'),
    ('OP_FO','Field Operations'),
    ('OP_IM','Inventory Management'),
    ('OP_SO','Products and Services'),
    ('OP_CX','Customer Experience'),
    ('OP_NO','Network Optimization'),
    ('OP_AO','Autonomous Operations'),
    ('OP_OT','Other Topics');

--delete from public.operation_map where operation_id = 'OP_NP';
--INSERT INTO public.operation_map (operation_id, operation_name) VALUES 
--    ('OP_AO','Autonomous Operations'),
--    ('OP_OT','Other Topics');
--
-- TOC entry 004 (class Operation_Sub_Group)
-- Name: operation_sub_group; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.operation_sub_group AS ENUM (
    'OP_CX_01',
    'OP_CX_02',
    'OP_CX_03',
    'OP_CX_04',
    'OP_FO_01',
    'OP_FO_02',
    'OP_IM_01',
    'OP_IM_02',
    'OP_TM_01',
    'OP_TM_02',
    'OP_TM_03',
    'OP_NA_01',
    'OP_NA_02',
    'OP_NA_03',
    'OP_NA_04',
    'OP_NOC_1',
    'OP_NOC_2',
    'OP_NOC_3',
	'OP_NOC_4',
	'OP_NOC_5',
	'OP_NOC_6',
	'OP_NOC_7',
	'OP_NOC_8',
    'OP_NO_01',
    'OP_NO_02',
    'OP_NO_03',
    'OP_NO_04',
    'OP_NO_05',
    'OP_NO_06',
    'OP_NO_07',    
    'OP_SO_01',
    'OP_SO_02',
    'OP_SO_03',
    'OP_SO_04',
    'OP_SO_05',
    'OP_SO_06',
    'OP_AO_01',
    'OP_AO_02',
    'OP_AO_03',
    'OP_OT_01',
    'OP_OT_02',
    'OP_OT_03'
);


ALTER TYPE public.operation_sub_group OWNER TO aomm_data;
--ALTER TYPE public.operation_sub_group ADD VALUE 'default' BEFORE 'OP_CX_01';

--
-- TOC entry 005 (class Operation_Sub_Group_Map)
-- Name: operation_sub_group_map; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.operation_sub_group_map (
    operation_sub_group_id public.operation_sub_group NOT NULL,
    operation_sub_group_name character varying(255) NOT NULL
);

ALTER TABLE public.operation_sub_group_map OWNER TO aomm_data;

--
-- TOC entry 0xx (class Operation_Sub_Group_Map_PK)
-- Name: operation_sub_group_map operation_sub_group_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.operation_sub_group_map
    ADD CONSTRAINT operation_sub_group_map_pkey PRIMARY KEY (operation_sub_group_id);


INSERT INTO operation_sub_group_map (operation_sub_group_id, operation_sub_group_name) VALUES 
    ('OP_CX_01','Customer Experience Management'),
    ('OP_CX_02','Customer Information Management'),
    ('OP_CX_03','Customer Order Management'),
    ('OP_CX_04','Customer Behavior Analysis'),
    ('OP_FO_01','Asset Management'),
    ('OP_FO_02','Work Order Management'),
    ('OP_IM_01','Inventory Management'),
    ('OP_IM_02','Supply Chain Fulfillment'),
    ('OP_TM_01','Network Planning'),
    ('OP_TM_02','Network Deployment'),
    ('OP_TM_03','Network Topology Management'),
    ('OP_NA_01','Service Analysis'),
    ('OP_NA_02','Service Management'),
    ('OP_NA_03','Service Problem Management'),
    ('OP_NA_04','Service Quality and Performance Management'),
    ('OP_NOC_1','RAN Network Performance Management'),
    ('OP_NOC_2','RAN Network Trouble Management'),
    ('OP_NOC_3','Core Network Performance Management'),
    ('OP_NOC_4','Core Network Trouble Management'),
    ('OP_NOC_5','IP Network Performance Management'),
    ('OP_NOC_6','IP and Backhaul Network Trouble Management'),
    ('OP_NOC_7','Network Usage Management'),
    ('OP_NOC_8','E2E Network Performance Management'),
    ('OP_NO_01','Network Capacity Management'),
    ('OP_NO_02','Network Optimization for RAN'),
    ('OP_NO_03','Network Optimization for Core'),
    ('OP_NO_04','Network Optimization for IP and Backhaul'),
    ('OP_NO_05','Network Optimization for QoE'),
    ('OP_NO_06','Network Traffic Management'),
    ('OP_NO_07','Anomaly Management'),
    ('OP_SO_01','Product and Service Configuration & Activation'),
    ('OP_SO_02','Product and Service Operational Analysis'),
    ('OP_SO_03','Product and Service Performance Management'),
    ('OP_SO_04','Product and Service Problem Management'),
    ('OP_SO_05','Security Management'),
    ('OP_SO_06','Service Offer Management'),
    ('OP_AO_01','Autonomous Operations Platform and People'),
    ('OP_AO_02','Autonomous Operations Culture'),
    ('OP_AO_03','Autonomous Operations Business Strategy'),
    ('OP_OT_01','B2B2X Partner Engagement'),
    ('OP_OT_02','Employee Engagement'),
    ('OP_OT_03','Engagement of Smart Things');    


--delete from public.operation_sub_group_map where operation_sub_group_id = 'OP_NP_01';
--INSERT INTO public.operation_sub_group_map (operation_sub_group_id, operation_sub_group_name) VALUES 
--    ('OP_AO_01','Autonomous Operations Platform and People'),
--    ('OP_AO_02','Autonomous Operations Culture'),
--    ('OP_AO_03','Autonomous Operations Business Strategy'),
--    ('OP_OT_01','B2B2X Partner Engagement'),
--    ('OP_OT_02','Employee Engagement'),
--    ('OP_OT_03','Engagement of Smart Things'); 


--
-- TOC entry 006 (class Technology)
-- Name: technology; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.technology AS ENUM (
    'Radio Access Network',
    'Core Network',
    'IP Core Network',
    'Optical Network',
    'Transmission and Microwave',
    'Fixed Network',
    'Data Center',
    'Field Operations',
    'Infrastructure Maintenance'
);


ALTER TYPE public.technology OWNER TO aomm_data;


--
-- TOC entry 007 (class Dimension)
-- Name: dimension; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.dimension AS ENUM (
    'Party',
    'Technology',
    'Culture',
    'Strategy',
    'Operations',
    'Data'
);


ALTER TYPE public.dimension OWNER TO aomm_data;



--
-- TOC entry 008 (class Sub_Dimension)
-- Name: sub_dimension; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.sub_dimension (
    id SERIAL,
    sub_dimension_id character varying(10) NOT NULL,
    sub_dimension_name character varying(255) NOT NULL,
    sub_dimension_definition text,
    sub_dimension_context text,
    dimension public.dimension NOT NULL
);


ALTER TABLE public.sub_dimension OWNER TO aomm_data;

--
-- TOC entry 0xx (class Sub_Dimension_PK)
-- Name: sub_dimension sub_dimension_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sub_dimension
    ADD CONSTRAINT sub_dimension_pkey PRIMARY KEY (sub_dimension_id);

--
-- TOC entry 009 (class Criteria)
-- Name: criteria; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.criteria (
    id SERIAL,
    criteria_id character varying(10) NOT NULL,
    criteria_scope text,
    criteria_description text,
    sub_dimension_id character varying(10) NOT NULL
);


ALTER TABLE public.criteria OWNER TO aomm_data;


--
-- TOC entry 0xx (class Criteria_PK)
-- Name: criteria criteria_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.criteria
    ADD CONSTRAINT criteria_pkey PRIMARY KEY (criteria_id);

--
-- TOC entry 0xx (class Criteria_FK)
-- Name: criteria_sub_dimension_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.criteria
    ADD CONSTRAINT criteria_sub_dimension_id_fkey FOREIGN KEY (sub_dimension_id) REFERENCES public.sub_dimension(sub_dimension_id);



--
-- TOC entry 010 (class Attribute)
-- Name: attribute; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.attribute (
    id SERIAL,
    attribute_id character varying(10) NOT NULL,
    criteria_id character varying(10) NOT NULL,
    attribute_id_level1 character varying(10) NOT NULL,
    attribute_level1 text NOT NULL,
    attribute_id_level2 character varying(10) NOT NULL,
    attribute_level2 text NOT NULL,
    attribute_id_level3 character varying(10) NOT NULL,
    attribute_level3 text NOT NULL,
    attribute_id_level4 character varying(10) NOT NULL,
    attribute_level4 text NOT NULL,
    attribute_id_level5 character varying(10) NOT NULL,
    attribute_level5 text NOT NULL
);


ALTER TABLE public.attribute OWNER TO aomm_data;


--
-- TOC entry 0xx (class Attribute_PK)
-- Name: attribute attribute_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.attribute
    ADD CONSTRAINT attribute_pkey PRIMARY KEY (attribute_id);

--
-- TOC entry 0xx (class Attribute_FK)
-- Name: attribute_criteria_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.attribute
    ADD CONSTRAINT attribute_criteria_id_fkey FOREIGN KEY (criteria_id) REFERENCES public.criteria(criteria_id);



--
-- TOC entry 011 (class Value_Stream)
-- Name: value_stream; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.value_stream (
    id SERIAL,
    value_stream_id character varying(10) NOT NULL,
    value_stream_name character varying(255) NOT NULL,
    operation public.operation NOT NULL,
    operation_sub_group public.operation_sub_group NOT NULL
);


ALTER TABLE public.value_stream OWNER TO aomm_data;


--
-- TOC entry 0xx (class Value_Stream_PK)
-- Name: value_stream value_stream_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.value_stream
    ADD CONSTRAINT value_stream_pkey PRIMARY KEY (value_stream_id);

--
-- TOC entry 012 (class Value_Stream_Technology relation)
-- Name: value_stream_technology_relation; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.value_stream_technology_relation (
    relation_id integer NOT NULL,
    value_stream_id character varying(10) NOT NULL,
    technology public.technology NOT NULL
);


ALTER TABLE public.value_stream_technology_relation OWNER TO aomm_data;

--
-- TOC entry 0xx (class Value_Stream_Technology_PK)
-- Name: value_stream_technology_relation value_stream_technology_relation_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.value_stream_technology_relation
    ADD CONSTRAINT value_stream_technology_relation_pkey PRIMARY KEY (relation_id);


--
-- TOC entry 0xx (class Value_Stream_Technology_FK)
-- Name: value_stream_technology_relation value_stream_technology_relation_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.value_stream_technology_relation
    ADD CONSTRAINT value_stream_technology_relation_value_stream_id_fkey FOREIGN KEY (value_stream_id) REFERENCES public.value_stream(value_stream_id);


--
-- TOC entry 013 (class Value_Stream_Service relation)
-- Name: value_stream_service_relation; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.value_stream_service_relation (
    relation_id integer NOT NULL,
    value_stream_id character varying(10) NOT NULL,
    service public.service NOT NULL
);


ALTER TABLE public.value_stream_service_relation OWNER TO aomm_data;

--
-- TOC entry 0xx (class Value_Stream_Service_PK)
-- Name: value_stream_service_relation value_stream_service_relation_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.value_stream_service_relation
    ADD CONSTRAINT value_stream_service_relation_pkey PRIMARY KEY (relation_id);


--
-- TOC entry 0xx (class Value_Stream_Service_FK)
-- Name: value_stream_service_relation value_stream_service_relation_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.value_stream_service_relation
    ADD CONSTRAINT value_stream_service_relation_value_stream_id_fkey FOREIGN KEY (value_stream_id) REFERENCES public.value_stream(value_stream_id);


--
-- TOC entry 014 (class Capability)
-- Name: capability; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.capability (
    id SERIAL,
    capability_id character varying(10) NOT NULL,
    capability_name character varying(255) NOT NULL,
    capability_definition text,
    weighting numeric(5,2),
    value_stream_id character varying(10) NOT NULL,
    sub_dimension_id character varying(10) NOT NULL
);

--ALTER TABLE capability ADD COLUMN weighting NUMERIC(5,2);
--UPDATE capability SET weighting = 20;

ALTER TABLE public.capability OWNER TO aomm_data;


--
-- TOC entry 0xx (class Capability_PK)
-- Name: capability capability_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.capability
    ADD CONSTRAINT capability_pkey PRIMARY KEY (capability_id);

--
-- TOC entry 0xx (class Capability_FK)
-- Name: capability capability_value_stream_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.capability
    ADD CONSTRAINT capability_value_stream_id_fkey FOREIGN KEY (value_stream_id) REFERENCES public.value_stream(value_stream_id);

--
-- TOC entry 0xx (class Capability_FK)
-- Name: capability capability_sub_dimension_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.capability
    ADD CONSTRAINT capability_sub_dimension_id_fkey FOREIGN KEY (sub_dimension_id) REFERENCES public.sub_dimension(sub_dimension_id);



--
-- TOC entry 015 (class Question)
-- Name: question; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.question (
    id SERIAL,
    question_id character varying(10) NOT NULL,
    question_description text NOT NULL,
    criteria_id character varying(10) NOT NULL
);

--ALTER TABLE question DROP COLUMN weighting;

ALTER TABLE public.question OWNER TO aomm_data;


--
-- TOC entry 0xx (class Question_PK)
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (question_id);

--
-- TOC entry 0xx (class Question_FK)
-- Name: question question_criteria_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_criteria_id_fkey FOREIGN KEY (criteria_id) REFERENCES public.criteria(criteria_id);


--
-- TOC entry 016 (class Capability_Question relation)
-- Name: capability_question_relation; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.capability_question_relation (
    capability_id character varying(10) NOT NULL,
    question_id character varying(10) NOT NULL
);


ALTER TABLE public.capability_question_relation OWNER TO aomm_data;

--
-- TOC entry 0xx (class Capability_Question_Relation_PK)
-- Name: capability_question_relation capability_question_relation_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.capability_question_relation
    ADD CONSTRAINT capability_question_relation_composite_pkey PRIMARY KEY (capability_id, question_id);

--
-- TOC entry 0xx (class Capability_Question_Relation_FK)
-- Name: capability_question_relation capability_question_relation_capability_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.capability_question_relation
    ADD CONSTRAINT capability_question_relation_capability_id_fkey FOREIGN KEY (capability_id) REFERENCES public.capability(capability_id);

--
-- TOC entry 0xx (class Capability_Question_Relation_FK)
-- Name: capability_question_relation capability_question_relation_question_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.capability_question_relation
    ADD CONSTRAINT capability_question_relation_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id);    

--
-- TOC entry 017 (class CLA)
-- Name: cla; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.cla (
    id SERIAL,
    cla_id character varying(10) NOT NULL,
    cla_level1_id character varying(10) NOT NULL,
    cla_level1_description text NOT NULL,
    cla_level2_id character varying(10) NOT NULL,
    cla_level2_description text NOT NULL,
    cla_level3_id character varying(10) NOT NULL,
    cla_level3_description text NOT NULL,
    cla_level4_id character varying(10) NOT NULL,
    cla_level4_description text NOT NULL,
    cla_level5_id character varying(10) NOT NULL,
    cla_level5_description text NOT NULL,
    question_id character varying(10) NOT NULL,
    criteria_id character varying(10) NOT NULL
);


ALTER TABLE public.cla OWNER TO aomm_data;


--
-- TOC entry 0xx (class CLA_PK)
-- Name: cla cla_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.cla
    ADD CONSTRAINT cla_pkey PRIMARY KEY (cla_id);

--
-- TOC entry 0xx (class CLA_FK)
-- Name: cla cla_question_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.cla
    ADD CONSTRAINT cla_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id);

--
-- TOC entry 0xx (class CLA_FK)
-- Name: cla cla_criteria_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.cla
    ADD CONSTRAINT cla_criteria_id_fkey FOREIGN KEY (criteria_id) REFERENCES public.criteria(criteria_id);


--
-- TOC entry 017 (class Role)
-- Name: role; Type: TYPE; Schema: public; Owner: aomm_data
--

CREATE TYPE public.role AS ENUM (
    'admin',
    'user',
    'audit',
    'report'
);


ALTER TYPE public.role OWNER TO aomm_data;

--
-- TOC entry 018 (class User)
-- Name: user; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.user (
    id SERIAL,
    user_id character varying(255) NOT NULL,
    fname character varying(255) NOT NULL,
    lname character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    role public.role,
    hashed_password character varying(255) NOT NULL,
    creation_time timestamp NOT NULL,
    last_login_time timestamp,
    is_active character varying(1) NOT NULL
);

--ALTER TABLE public.user ALTER COLUMN is_active TYPE varchar(1) USING is_active::varchar(1);

ALTER TABLE public.user OWNER TO aomm_data;


--
-- TOC entry 0xx (class User_PK)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.user
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);

INSERT INTO public.user (user_id, fname, lname, email, role, hashed_password, creation_time, last_login_time, is_active) VALUES 
('ADMIN@ADMIN.COM', 'Admin', 'Admin', 'ADMIN@ADMIN.COM', 'admin', '047c88291e9877788365c59346e6918d54529cdceb7daf1e5cd490493a8e2028', timestamp '2025-01-06 10:12:20', timestamp '2025-01-07 10:12:20', 't');

--
-- TOC entry 018 (class User_Operation_Map)
-- Name: user_operation_map; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.user_operation_map (
    relation_id SERIAL,
    user_id character varying(255) NOT NULL,
    operation_id public.operation NOT NULL
);

ALTER TABLE public.user_operation_map OWNER TO aomm_data;

--
-- TOC entry 0xx (class User_Operation_Map_PK)
-- Name: user_operation_map user_operation_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.user_operation_map
    ADD CONSTRAINT user_operation_map_pkey PRIMARY KEY (relation_id);

INSERT INTO public.user_operation_map (user_id, operation_id) VALUES 
('ADMIN@ADMIN.COM', 'OP_TM'),
('ADMIN@ADMIN.COM', 'OP_NOC'),
('ADMIN@ADMIN.COM', 'OP_NA'),
('ADMIN@ADMIN.COM', 'OP_FO'),
('ADMIN@ADMIN.COM', 'OP_IM'),
('ADMIN@ADMIN.COM', 'OP_SO'),
('ADMIN@ADMIN.COM', 'OP_CX'),
('ADMIN@ADMIN.COM', 'OP_NO'),
('ADMIN@ADMIN.COM', 'OP_AO'),
('ADMIN@ADMIN.COM', 'OP_OT');


--
-- TOC entry 019 (class Self_Assessment)
-- Name: self_assessment; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.self_assessment (
    id SERIAL,
    self_assessment_id UUID NOT NULL,
    creation_time timestamp NOT NULL,
    update_time timestamp,
    user_id character varying(255) NOT NULL,
    service public.service NOT NULL, 
    operation public.operation NOT NULL,
    operation_sub_group public.operation_sub_group NOT NULL,
    is_archived character varying(1) NOT NULL
);

ALTER TABLE public.self_assessment OWNER TO aomm_data;
--ALTER TABLE self_assessment ADD COLUMN is_archived VARCHAR(1);
--UPDATE self_assessment SET is_archived = 'f'
--ALTER TABLE self_assessment ALTER COLUMN is_archived SET NOT NULL;
--ALTER TABLE self_assessment ALTER COLUMN user_id TYPE VARCHAR(255);


--
-- TOC entry 0xx (class Self_Assessment_PK)
-- Name: self_assessment self_assessment_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.self_assessment
    ADD CONSTRAINT self_assessment_pkey PRIMARY KEY (self_assessment_id);


--
-- TOC entry 0xx (class Self_Assessment_FK)
-- Name: self_assessment self_assessment_user_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.self_assessment
    ADD CONSTRAINT self_assessment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user(user_id);


--
-- TOC entry 020 (class SA_Technology_Relation)
-- Name: sa_technology_relation; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.sa_technology_relation (
    relation_id SERIAL,
    self_assessment_id UUID NOT NULL,
    technology public.technology NOT NULL
);


ALTER TABLE public.sa_technology_relation OWNER TO aomm_data;


--
-- TOC entry 0xx (class SA_Technology_Relation_PK)
-- Name: sa_technology_relation sa_technology_relation_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_technology_relation
    ADD CONSTRAINT sa_technology_relation_pkey PRIMARY KEY (relation_id);

--
-- TOC entry 0xx (class SA_Technology_Relation_FK)
-- Name: sa_technology_relation sa_technology_relation_self_assessment_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_technology_relation
    ADD CONSTRAINT sa_technology_relation_self_assessment_id_fkey FOREIGN KEY (self_assessment_id) REFERENCES public.self_assessment(self_assessment_id);


--
-- TOC entry 021 (class SA_Question_Relation)
-- Name: sa_question_relation; Type: TABLE; Schema: public; Owner: aomm_data
--

CREATE TABLE public.sa_question_relation (
    relation_id SERIAL,
    self_assessment_id UUID NOT NULL,
    question_id character varying(10) NOT NULL,
    weighting numeric(5,2) NOT NULL,
    selected_cla_level_id character varying(10) NOT NULL,
    cla_level character varying(2) NOT NULL,
    capability_id character varying(10) NOT NULL,
    value_stream_id character varying(10) NOT NULL,
    criteria_id character varying(10) NOT NULL,
    sub_dimension_id character varying(10) NOT NULL,
    capability_score numeric(5,2) NOT NULL,
    is_archived character varying(1) NOT NULL
);


ALTER TABLE public.sa_question_relation OWNER TO aomm_data;

--ALTER TABLE sa_question_relation ALTER COLUMN is_archived TYPE varchar(5) USING is_archived::varchar(5);
--UPDATE sa_question_relation SET is_archived = 'f';
--ALTER TABLE sa_question_relation ALTER COLUMN is_archived TYPE varchar(1) USING is_archived::varchar(1);

--ALTER TABLE sa_question_relation ADD COLUMN capability_score NUMERIC(5,2);
--UPDATE sa_question_relation SET capability_score = 1.5
--ALTER TABLE sa_question_relation ALTER COLUMN capability_score SET NOT NULL;


--
-- TOC entry 0xx (class SA_Question_Relation_PK)
-- Name: sa_question_relation sa_question_relation_pkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_pkey PRIMARY KEY (relation_id);

--
-- TOC entry 0xx (class SA_Question_Relation_FK)
-- Name: sa_question_relation sa_question_relation_self_assessment_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_self_assessment_id_fkey FOREIGN KEY (self_assessment_id) REFERENCES public.self_assessment(self_assessment_id);

--
-- TOC entry 0xx (class SA_Question_Relation_FK)
-- Name: sa_question_relation sa_question_relation_question_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id);

--
-- TOC entry 0xx (class SA_Question_Relation_FK)
-- Name: sa_question_relation sa_question_relation_capability_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_capability_id_fkey FOREIGN KEY (capability_id) REFERENCES public.capability(capability_id);

--
-- TOC entry 0xx (class SA_Question_Relation_FK)
-- Name: sa_question_relation sa_question_relation_value_stream_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_value_stream_id_fkey FOREIGN KEY (value_stream_id) REFERENCES public.value_stream(value_stream_id);

--
-- TOC entry 0xx (class SA_Question_Relation_FK)
-- Name: sa_question_relation sa_question_relation_criteria_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_criteria_id_fkey FOREIGN KEY (criteria_id) REFERENCES public.criteria(criteria_id);

--
-- TOC entry 0xx (class SA_Question_Relation_FK)
-- Name: sa_question_relation sa_question_relation_sub_dimension_id_fkey; Type: CONSTRAINT; Schema: public; Owner: aomm_data
--

ALTER TABLE ONLY public.sa_question_relation
    ADD CONSTRAINT sa_question_relation_sub_dimension_id_fkey FOREIGN KEY (sub_dimension_id) REFERENCES public.sub_dimension(sub_dimension_id);

--DROP TABLE public.sa_question_relation;
--DROP TABLE public.sa_technology_relation;
--DROP TABLE public.self_assessment;
--DROP TABLE public.user_operation_map;
--DROP TABLE public.user;
--DROP TYPE public.role;
--DROP TABLE public.cla;
--DROP TABLE public.capability_question_relation;
--DROP TABLE public.question;
--DROP TABLE public.capability;
--DROP TABLE public.value_stream_service_relation;
--DROP TABLE public.value_stream_technology_relation;
--DROP TABLE public.value_stream;
--DROP TABLE public.attribute;
--DROP TABLE public.criteria;
--DROP TABLE public.sub_dimension;
--DROP TYPE public.dimension;
--DROP TYPE public.technology;
--DROP TABLE public.operation_sub_group_map;
--DROP TABLE public.operation_map;
--DROP TYPE public.operation_sub_group;
--DROP TYPE public.operation;
--DROP TYPE public.service;
--DROP TYPE public.aomm_levels;


select n.nspname as enum_schema,  
       t.typname as enum_name,  
       e.enumlabel as enum_value
from pg_type t 
   join pg_enum e on t.oid = e.enumtypid  
   join pg_catalog.pg_namespace n ON n.oid = t.typnamespace;