-- =================================================
-- Gerado em : 2026-02-25T17:43:47.258912
-- Origem    : 10.80.91.30 / 10.50.13.22_eleva
-- Destino   : localhost / 10.50.13.22_eleva_teste
-- Registros : 235
-- =================================================

BEGIN;

-- gedepartamento: 5 registro(s)
COPY public.gedepartamento (id_gedepartamento_int, codigo_str, nome_str, id_geusuario_int, tstamp) FROM stdin;
7	7	ADMINISTRATIVO	1195	2006-08-25T15:29:03-03:00
3	3	BACK OFFICE	1195	2006-08-25T15:27:56-03:00
1	1	OPERAÇÃO COBRANÇA	1195	2006-08-25T15:27:28-03:00
4	4	GERÊNCIA	1195	2006-08-25T15:28:07-03:00
8	8	OUVIDORIA	1195	2006-08-25T15:29:35-03:00
\.

-- getipousuario: 1 registro(s)
COPY public.getipousuario (id_getipousuario_int, codigo_str, descricao_str) FROM stdin;
4	A	Admnistrativo
\.

-- geusuario: 28 registro(s)
COPY public.geusuario (id_geusuario_int, codigo_str, nomecompleto_str, ativo_str, nomelogin_str, senha_str, usuarioadm_str, id_geempresa_int, id_gefilial_int, automatico_str, usuario_int, tstamp, qtde_fup_int, usuario_externo_str, recebe_email_str, observacao_str, email_str, sit_contrato_str, admissao_dat, funcao_str, data_nasc_dat, controla_ramal_str, escolaridade_str, id_gedepartamento_int, agenda_str, fila_automatica_str, cpf_str, sincronizangs_str, apenas_cb002_new2_str, discagem_manual_str, id_getipousuario_int, codigo_rh_str, codigo_externo_str, id_geatuacao01_int, id_geatuacao02_int, id_geatuacao03_int, id_geclassificacaocontao_int, anotacao_txt, tstamp_ultimo_logou_npcob, normalizado_bi_str, controla_softphone_str, login_alpheratz_str, id_sysfuncionario_int, id_sysusuario_int, genero_int, situacao_ci_int, loginbanco_str, senhabanco_str, campanha_obrigatoria_str, situacao_ci_1_int, supervisor_experiencia_bit, tstamp_mdm_inclusao, tstamp_mdm_alteracao, funcao_old_str, consultordigital_str) FROM stdin;
1195	2001	ADMINISTRADOR PLANAE	1	planae	'3!5qs*L	S	1	1	N	1195	2017-01-10T16:19:12-02:00	\N	N	N	XYZ	N	ASCJNBWYXPDEFRGI	\N		2002-10-01	N		7	N	N	05903864848	S	N	S	4	0		\N	\N	\N	\N	\N	\N	\N	N		10	11	2	5	\N	\N	N	\N	\N	\N	2022-03-07T07:49:33		N
1045	1033	Gabriella Ramos Graisfimberg	0	ggrais	P1:d:v	S	1	1	N	1124	2007-01-17T09:11:59-02:00	\N	N	N			IASCJNBWYXPDEFRGI	2001-01-09		1979-09-03	N	SUPERIOR INCOMPLETO	3	\N	\N	\N	\N	\N	\N	\N	1605	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
2409	3122	Paulo Caputo Grossi	0	pgrossi	1e|AvTa	S	1	1	N	1124	2015-11-16T16:15:22-02:00	\N	N	N			ASCJNBWYXPDEFRGI	2003-07-08		1979-02-20	N	SUPERIOR INCOMPLETO	3	N	N	\N	N	N	N	4	0000005		\N	\N	\N	\N	\N	\N	\N	N		\N	\N	1	5	\N	\N	\N	\N	\N	\N	\N	\N	N
2	2	Administrador Planae Fiat	0	fiat	1jk@sDgC	S	1	1	N	3014	2006-08-09T15:39:33-03:00	\N	N	N			DASD	\N		\N	N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1219	1218	Marcelo Dias da Silva	0	msdias	._	S	1	1	N	3014	2006-09-06T10:48:20-03:00	\N	N	S	XYZ	msdias@paschoalotto.com.br	FASJBDF	2001-02-07	GESTOR	1975-03-04	N	SUPERIOR COMPLETO	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1984	2715	Daniela Dias Gomide	0	dgomide	"jk@lT)w9H	S	1	1	N	3177	2006-11-29T09:03:38-02:00	\N	N	N			DASCJDASCJD	2004-06-02	Coordenador	1982-02-14	N	SUPERIOR INCOMPLETO	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1014	1026	Giovana Bueno Ciaca	0	gciaca	'_w;oJY	S	1	1	N	3177	2008-01-16T11:55:21-02:00	999	N	S	XYZ	gciaca@paschoalotto.com.br	ASCJNBWYXPDEFRGIKH	2001-03-16	Coordenadora	1980-11-04	N	SUPERIOR INCOMPLETO	1	N	N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1156	1166	Flavia Cacciolari	0	fcacciolari	/n	S	1	1	N	1115	2009-11-06T11:28:52-02:00	\N	N	S		fcacciolari@paschoalotto.com.br	ASCJNBWYXPDEFRGIKH	2002-03-01		1979-10-16	N	SUPERIOR COMPLETO	1	N	N	\N	N	N	N	4	40950	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1366	2103	Administrador Planae Itaú	0	itau	1jk@sDgC	S	1	1	N	3014	2006-08-09T15:40:30-03:00	20	N	N	XYZ		DASD	\N		\N	N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
236	1007	Cleber D. do Nascimento	0	cdnascimento	7gn3	S	1	1	N	1163	2005-03-29T14:31:45-03:00	\N	N	N			ASFJ	\N	\N	\N	N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1047	1049	Nilton Cezar Ribeiro	0	nribeiro	/ps4hJjP	S	1	1	N	1126	2005-09-27T09:29:36-03:00	\N	N	N	XYZ		ASFJJ	2001-03-16	\N	1970-05-14	N	SUPERIOR COMPLETO	4	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
3177	3883	Javer Pereira	0	jpereira2	)boEnq(x	S	1	1	N	3177	2008-03-19T16:58:50-03:00	\N	N	N			ASCJNBWYXPDEFRGIKH	2006-04-24	Ass. Back Office	1983-04-25	N	SUPERIOR COMPLETO	3	S	N	\N	N	N	N	\N	42991	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1055	1065	Luiz Gustavo Nascimento	0	lnascimento	-lkEfJeFv)9	S	1	1	N	3177	2007-05-24T11:41:53-03:00	\N	N	N	XYZ		IASCJNBWYXPDEFRGI	2001-03-12	Gestor	1980-11-27	N	SUPERIOR COMPLETO	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
221	3	Administrador Planae Confiança	0	confianca	1jk@sDgC	S	1	1	N	1195	2005-09-16T08:51:24-03:00	\N	N	N			ASD	\N	\N	\N	N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1	9999	LUIZ APARECIDO ORNELAS	1	automatico	1jk	S	1	1	S	3014	2006-08-09T15:36:42-03:00	\N	N	N	XYZ		JASJF	2008-09-26	AUTONOMO	1977-01-01	N	\N	\N	\N	\N		\N	\N	\N	\N	010759	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	2022-03-07T07:49:33	AUTONOMO	N
2806	3514	OUVIDORIA	0	ouvidoria	Y5;c:q)x	S	1	1	N	3354	2007-08-31T14:47:21-03:00	\N	N	N	XYZ		IASCJNBWYXPDEFRGI	\N		\N	N		8	N	N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N
1124	1134	CARLOS EDUARDO SIMOES	1	csimoes	/cx:xNYp9	S	2	1	N	1124	2016-10-28T12:00:04-02:00	\N	N	N			ASCJNBWYXPDEFRGI	2001-12-03	TREINAMENTO	1978-03-01	N	ENSINO SUPERIOR COMPLETO	3	N	N	21509454870	S	N	N	4	001621		\N	\N	\N	\N	\N	2014-04-23T15:18:37.928141	S	N		1615	1588	2	5	\N	\N	N	\N	\N	\N	2021-04-07T12:12:50	TREINAMENTO	N
8310	6802	LORENA GONCALVES	1	lgoncalves	-ey@fBdWm(	S	1	33	N	8310	2023-08-16T09:17:23-03:00	\N	N	N			ASCJNBWYXPDEFRGIKH	2017-09-04	ANALISTA DE BACK OFFICE I	1992-11-13	N	ENSINO MEDIO COMPLETO	3	N	N	42406875865	S	N	N	4	082802		\N	\N	\N	\N	\N	\N	\N	N		27121	20735	1	5	\N	\N	N	\N	0	2023-06-10T13:02:58	2023-08-16T09:17:22	\N	N
8351	6843	DANIEL CANALE	1	dcanale	%ak@dM]	S	1	33	\N	\N	2024-04-01T15:24:07.552188-03:00	\N	\N	\N	\N	\N	ASD	2021-01-20	ASSISTENTE DE BACK OFFICE	2001-02-05	\N	ENSINO MEDIO COMPLETO	1	\N	\N	48910278862	S	\N	\N	4	121747    	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	57002	50920	\N	\N	\N	\N	\N	\N	\N	2024-04-01T15:24:08	2024-04-15T12:10:28	\N	N
8340	6832	ALESSANDRA GALHARDI GINEZ AGOSTINHO	1	aggagostinho	Q.;f	S	1	33	N	8367	2024-10-30T14:18:40-03:00	\N	N	N			ASCJNBWYXPDEFRGIKH	2021-01-18	ASSISTENTE DE BACK OFFICE	1974-08-14	N	ENSINO MEDIO COMPLETO	3	N	N	28605355867	S	N	N	4	121604		\N	\N	\N	\N		\N	\N	N		38132	31907	1	5	\N	\N	N	\N	0	2023-12-20T12:11:44	2024-11-13T16:51:33	\N	N
8164	6656	DIEGO BARBOSA BRAZ CORTEZ RODRIGUES	1	dbbcrodrigues	#_m=rG^Jky8d;	S	1	33	\N	\N	2022-09-02T11:13:09.831570-03:00	\N	\N	\N	\N	\N	ASD	2015-03-23	ANALISTA DE BACK OFFICE II	1986-11-03	\N	ENSINO SUPERIOR COMPLETO	1	\N	\N	34743574846	S	\N	\N	4	068730	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	21914	15185	\N	\N	\N	\N	\N	\N	\N	2022-09-02T11:13:10	2023-02-02T12:07:54	\N	N
6676	5203	PAULO ALEXANDRE DA COSTA	1	pcosta	Q5:i;pYMm	S	1	1	N	1115	2009-12-28T12:58:45-02:00	\N	N	N			ASCJBPDR	2006-08-07	TREINAMENTO	1980-08-17	N	ENSINO MEDIO TECNICO COMPLETO	3	N	N	30158841824	N	N	N	4	001538	\N	\N	\N	\N	\N	\N	2014-04-23T15:18:39.483319	S	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	2021-04-07T12:12:50	TREINAMENTO	N
8114	6605	NATASHA YORRANA BERSA	0	nybersa	/wl7uTY	S	1	1	N	8101	2021-12-08T13:10:56-03:00	\N	N	N			ASD	2021-04-15	ANALISTA SUPORTE DE ARQUIVO I	1996-03-02	N	ENSINO MEDIO COMPLETO	1	N	N	45205567830	S	N	N	4	124604		\N	\N	\N	\N	\N	\N	\N	N		27391	21011	1	5	\N	\N	N	\N	0	2021-12-08T13:09:17	2025-02-12T03:47:25	ANALISTA SUPORTE DE ARQUIVO I	N
8101	6592	LEONARDO SIMAO	0	lsimao	-qs?dP	S	1	1	N	1124	2021-08-27T12:19:33-03:00	\N	N	N			ASD	2008-02-11	ANALISTA SUPORTE DE ARQUIVO I	1978-05-15	N	ENSINO SUPERIOR INCOMPLETO	1	N	N	27401053802	S	N	N	4	003693		\N	\N	\N	\N	\N	\N	\N	N		604	577	2	5	\N	\N	N	\N	0	2021-08-27T12:16:52	2025-02-12T03:30:24	ANALISTA SUPORTE DE ARQUIVO I	N
7993	6485	GUILHERME COVOLO CALCADA	1	gcovolo	(ayHrMg	S	1	1	N	7993	2022-12-03T08:53:15-03:00	\N	N	N			ASD	2016-12-05	ANALISTA DE AÇÕES OPERACIONAIS III	1984-02-17	N	ENSINO MEDIO TECNICO COMPLETO	3	N	N	32388700841	N	N	N	4	079815		\N	\N	\N	\N	\N	\N	\N	N		6233	19427	2	5	\N	\N	N	\N	0	\N	2022-12-03T08:54:50	ANALISTA DE M.I.S II	N
8016	6507	JENNIFER FIORAVANTE GONCALVES	1	jfgoncalves	+dqAqDYM~y=	S	1	1	N	8016	2020-01-30T10:46:25-03:00	\N	N	N			ASD	2017-03-15	ANALISTA DE AÇÕES OPERACIONAIS III	1989-06-15	N	ENSINO SUPERIOR COMPLETO	1	N	N	37359101816	N	N	N	4	080152		\N	\N	\N	\N	\N	\N	\N	N		11074	6993	1	5	\N	\N	N	\N	0	\N	2022-03-07T07:49:33	ANALISTA DE AÇÕES OPERACIONAIS III	N
7997	6488	GABRIEL MATHEUS ESPANHOLO TRAGANTE	0	gmetragante	Y7=g7t	S	1	1	N	7997	2019-08-26T16:42:13-03:00	\N	N	N			ASD	2010-07-05	TREINAMENTO	1993-03-22	N	ENSINO MEDIO INCOMPLETO	1	N	N	41970486880	S	N	N	4	023063		\N	\N	\N	\N	\N	\N	\N	N		2318	2290	2	5	\N	\N	N	\N	\N	\N	2025-02-12T01:10:34	TREINAMENTO	N
8404	6893	Vinicius de Oliveira Ribeiro	1	voribeiro	7m|;eFaSw	S	1	1	N	8318	2025-06-23T10:50:37-03:00	\N	N	N			ASD	2024-10-23	ANALISTA DE INFRAESTRUTUR	1998-04-26	N	ENSINO MÉDIO COMPLETO	1	N	N	43528672846	S	N	N	4	216539		\N	\N	\N	\N	\N	\N	\N	N		65286	59256	2	5	\N	\N	N	\N	0	2025-06-23T10:50:03	2025-06-23T10:51:49	\N	N
\.

-- gefilial: 41 registro(s)
COPY public.gefilial (id_gefilial_int, codigo_str, nome_str, ativo_str, id_geempresa_int, endereco1_str, endereco2_str, cep_str, id_gecidade_int, contato_str, telefone_str, fax_str, email_str, cgc_str, inscricao_str, versao_sistema_str, path_atualizacao_str, id_geusuario_int, timestamp, ddd_fax_str, ddd_str, sigla_filial_str, versao_sistema_compativel_str, limite_atualizacao_tim, ip_str, usuario_str, senha_str, horario_str, bairro_str, observacao_geral_txt, gerente_str, id_gefilial_npjur_int, codigo_ngs_str) FROM stdin;
1	1	Bauru	1	1	Rua Prof. Durval Guedes de Azevedo 2-144	Jd. Infante Dom Henrique	17012633	4791	2222	21088000	21067937	faleconosco@npaschoalotto.com.br	48031918003069	isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-26T17:00:50.593162-03:00	14	14	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15					\N	1
109	100	São José do Rio Preto	1	1	Coronel Spinola de Castro, nº 3360	Sala 21 Ed. Firenze	15015500	5282	Gustavo Ferreira Cassandre	31228383		gcassandre@gruponp.com.br	04578876002033	Isento	..		1195	2012-03-27T09:35:14.253150-03:00		017	\N	\N	\N	\N	\N	\N		Centro		Gustavo	\N	77
108	32	Palmas	1	1	Av. JK, QD 104 Norte	Conj. 01- Lote 121- 2º andar - Salas 7/9	77006014	5458	Glaucia Sposito	32132239	32163301	galves@gruponp.com.br	04578876000170	Isento	..		1195	2012-03-20T14:59:44.167919-03:00	63	63	\N	\N	\N	\N	\N	\N	08:00 as 18:00 (Seg. a Sexta)	Centro		Glaucia Sposito	\N	76
107	30	São José dos Campos	1	1	Av. Dr. João Guilhermino, 429	Sala 16 - Saint James	12210131	5283	André Luiz da Silva	33080368	33080368	andresilva@gruponp.com.br	04578874000170	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:10:56.945121-03:00	0012	0012	\N	\N	\N	\N	\N	\N	08:00 as 18:00	Centro		André	\N	67
43	41	IMPERATRIZ	0	1				2							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-07-19T16:44:27.416037-03:00			\N	\N	\N	\N	\N	\N					\N	66
42	40	CARUARU	0	1				2							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-07-19T16:39:18.660654-03:00			\N	\N	\N	\N	\N	\N					\N	65
41	39	BARREIRA	0	1				2							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-07-19T16:32:02.634735-03:00			\N	\N	\N	\N	\N	\N					\N	64
40	38	PORTO VELHO	0	1				2							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-07-19T16:14:39.037998-03:00			\N	\N	\N	\N	\N	\N					\N	63
39	37	ARACAJU	0	1				2							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-07-19T15:47:17.428028-03:00			\N	\N	\N	\N	\N	\N					\N	62
38	107	Três Lagoas	1	1				2266							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-03-30T15:49:49.284549-03:00			\N	\N	\N	\N	\N	\N					\N	57
37	106	Sinop	1	1				2381							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-03-30T15:42:25.846708-03:00			\N	\N	\N	\N	\N	\N					\N	56
36	105	Rondonópolis	1	1				2367							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-03-30T15:46:53.412303-03:00			\N	\N	\N	\N	\N	\N					\N	55
35	104	Dourados	1	1				2222							1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-03-30T15:28:51.186961-03:00			\N	\N	\N	\N	\N	\N					\N	54
34	27	Cascavel	1	1	Avenida Brasil, nº. 6282	Edifício Central Park, Sala 52	85816290	3234	6021					Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-01-28T07:27:44.563109-02:00			\N	\N	\N	\N	\N	\N		Centro			\N	47
33	25	Marília	1	1	Rua Maranhão, n.º 75 - Sala 14		17500010	5052		33032222					1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:58:11.288151-03:00		14	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	27
32	26	Jaguariuna	0	1	RUA; ALFREDO ENGLER, Nº 243	1º ANDAR	13880000	5006	Luiz Henrique Ramos	38674564		lhramos@gruponp.com.br		ISENTO	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-01-28T07:19:19.884150-02:00		19	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		CENTRO			\N	26
31	24.	Recife	1	1	Rua Ribeiro de Brito, nº 830	Salas 1203 e 1204 - Centro Empresarial	51021310	2892	Alexandre de Campos Salles	21197805		asalles@gruponp.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:02:21.317209-03:00		81	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Boa Viagem			\N	25
30	101	Bauru - Fiat Centralizada	1	1	Rua Luiz Aleixo 7-17	Jardim Brasil	17013590	4791		21067997	21067990	faleconosco@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2006-10-17T08:03:27-03:00	14	14	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15	\N	\N	\N	\N	\N	24
29	23	Campinas	1	1	Rua José Paulino, 1248 -	2 Andar - Edificio Goiás	13013001	4832		35788282			48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:47:34.189184-03:00		19	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	23
28	22	Porto Alegre	1	1	Av Borges de Medeiros, 659	Sala 702 - Edifício Thadeu Nedeff	90020023	4192	Alessandra Sanches Pacheco	21023750	21023750	apacheco@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:00:49.796814-03:00	51	51	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	22
27	21	Feira de Santana	0	1				331		75626026			48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2007-01-18T14:50:48-02:00			\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15	\N	\N	\N	\N	\N	21
26	20	São José do Rio Preto	1	1	Avenida João Batista Parra, 673	Sala 1302 A - Enseada Tower	15015500	5282	Raquel	31228383	32222851	rpessanha@npaschoalotto.com.br	48031918003069	Isento	3	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-26T08:30:32.572429-03:00		17	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Enseada do Suá			\N	20
25	19	Rio de Janeiro	1	1	Rua do Ouvidor, 161 - Sala 605/606/607	6º Andar - Ed. Paço do Ouvidor	20040030	3631	Tânia	32144350	32144350	trodrigues@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-05-08T08:34:35.579998-03:00	021	021	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	19
24	18	Belo Horizonte	1	1	Rua Santa Catarina, 1.354	Sala 601 - 6º Andar - Edifício Juiz Adau	30170081	1403	Plauto	21287650	32614183	ppompeu@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:44:23.686243-03:00	031	31	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Bairro de Lourdes			\N	18
23	17	Bauru - 7 de Setembro	0	1				4791	Waldecir	14310451		wrafael@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2007-01-04T12:55:00-02:00			\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15	\N	\N	\N	\N	\N	17
22	16	Sorocaba	1	1	Av. Antônio C. Comitre 525 Sl 66,67,68	Jd. Campolim-Ed. Crystal Plaza	18047620	5307	WALLACE BORRERE	21035450	21035450	WBORRERE@GRUPONP.COM.BR	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:12:55.802051-03:00	015	015	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Campolim			\N	16
21	15	Ribeirão Preto	1	1	Av. Presidente Vargas - nº 2001	Sl 175, 176 - 17º Andar- Sta Angela	14020260	5213	Nelson Palomino	21017300	21017308	npalomino@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2010-01-20T17:22:43.812511-02:00	0016	16	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15					\N	15
20	14	São Paulo	1	1	Avenida Paulista, 1337	12° Andar. Cj. 122.	01311000	5288	Silvana G. da C. Patrão Lazar	21248200	21248201	spatrao@gruponp.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:12:03.408817-03:00	11	11	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Cerqueira César			\N	14
19	13	Cuiabá	1	1	AV HISTORIADOR RUBENS DE MENDONÇA 157	Sala 301- 3º Andar - Conj. Mestre Inácio	78050000	2302	Gilberto	21218350	36244435	gborges@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:51:35.559501-03:00	065	065	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Baú			\N	13
18	12	Salvador	1	1	Av. Tancredo Neves - n.º 1186 sala -1201	Edif. Catabas Center	41820020	535	ANDERSON FELINTO	21068400	21068417	afelinto@gruponp.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:04:56.699969-03:00	71	71	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Pituba			\N	12
17	11	Goiânia	1	1	Rua 9 c Rua 8 - nº 558 - Q. F34 LOTE 45	1º andar - EDIF SAMLL TOWER -SETOR OESTE	74120010	971	Edith Rebouças Mendonça	40059900	40059900	emendonca@gruponp.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2011-01-12T17:42:47.874295-02:00	062	62	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15					\N	11
16	10	Vitória	1	1	Avenida João Batista Parra, 673	Sala 1302 A - Enseada Tower	29052123	878	Raquel	21256850	33252177	rpessanha@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:14:53.919683-03:00	027	27	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Enseada do Suá			\N	10
15	9	Uberlândia	1	1	Av. Floriano Peixoto, 615	Sala 909 - 9º Andar	38400102	2162	Ana Paula	21017400	21017409	abernardo@npaschoalotto.com.br	48031918003069	isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:13:49.380994-03:00	034	034	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	9
14	8	Brasília	1	1	SRTVS QD 701 BLOCO O - SALAS 790,791,792	793 E - CENTRO MULTIEMPRESARIAL	70340903	801	Fabiano	21078000	21078000	fborges1@gruponp.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:46:17.779761-03:00	61	61	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15					\N	8
13	5	Campo Grande	1	1	Rua 13 de Maio, 2500	Salas 1107 e 1108 - 11º Andar	79002923	2210	Janete	21068000	21068000	jbonacina@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:49:12.401869-03:00	067	67	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	7
12	7	Londrina	1	1	Av. Higienópolis, 210 - Sala 09 - Térreo	CENTRO	86020080	3357	Fabiana Castro	21039350	33440666	fcastro@npaschoalotto.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:56:59.687456-03:00	043	43	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	6
11	6	Blumenau	1	1	Rua XV de Novembro - nº 759	Salas 805, 806, 807 e 808 - 8º andar	89010001	4392	Marcos Rodrigues	3226985			48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2007-01-04T12:54:11-02:00		47	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15	\N	\N	\N	\N	\N	5
10	4	Curitiba	1	1	Av. Marechal Floriano Deodoro, 502	Sala 1101 - 11º andar - Centro	80010010	3259	Meire Tarrufi	21063800	21063800	mtarrufi@npaschoalotto.com.br	48031918003069	isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:52:28.777367-03:00	41	41	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	4
4	24	Recife	1	1	Rua Ribeiro de Brito, nº 830	Salas 1203 e 1204 - Centro Empresarial	51021310	2892	Alexandre de Campos Salles	21197805		asalles@gruponp.com.br	48031918003069	Isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T15:02:21.317209-03:00		81	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Boa Viagem			\N	25
3	3	Florianópolis	1	1	Rua Jerônimo Coelho, 383	Sala 1207 - 12º Andar - Ático Linhares	88015100	4443	Hélio Alonso	21075900	32230152	halonso@npaschoalotto.com.br	48031918003069	isenta	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:53:50.809423-03:00	048	048	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Centro			\N	3
2	2	Fortaleza	1	1	AV. SANTOS DUMONT Nº 2122 - 11º ANDAR	SALAS 1101/1103 ED. MANHATTAN CENTER	60150161	675	Daiani Jorge	40068200	40068215	djorge@gruponp.com.br	48031918003069	isento	1.00.863	\\\\10.20.10.254\\npcobupdate\\atualizacoes\\setupnpcob_atualizacao.exe	1195	2012-03-20T14:55:31.250038-03:00	85	85	\N	\N	\N	10.20.10.22	npcob	#HPr0dNW15		Aldeota			\N	2
\.

-- geempresa: 2 registro(s)
COPY public.geempresa (id_geempresa_int, codigo_str, nome_str, ativo_str, endereco1_str, endereco2_str, cep_str, id_gecidade_int, contato_str, telefone_str, fax_str, email_str, cgc_str, inscricao_str, id_geusuario_int, timestamp, mci_empresa_int, centralizadora_int) FROM stdin;
1	1      	Paschoalotto Serviços Financeiros	1	R. Prof. Durval Guedes de Azevedo 02-144	Trade Center	17012633	4791		1421088000	1421088000		05500934000106	                    	1045	2009-10-15T14:52:35-03:00	\N	\N
2	2      	Paschoalotto Serviços Financeiros	1	R. Prof. Durval Guedes de Azevedo 2-144	Trade Center	17012633	4791		1421088000	1421088000		05500934000106	                    	1045	2009-10-15T14:52:51-03:00	930707208	1903
\.

-- geuf: 16 registro(s)
COPY public.geuf (id_geuf_int, uf_str, nome_str, prazo_forum_int, id_geusuario_int, tstamp, cep_inicial_str, regiao_str) FROM stdin;
26	SP	SAO PAULO	20	2	2003-06-17T14:06:47-03:00	10000000	Sudeste
27	TO	TOCANTINS	\N	\N	\N	77000000	Norte
1	AC	ACRE	\N	\N	\N	69900000	Norte
12	MS	MATO GROSSO DO SUL	25	2	2003-06-17T13:28:28-03:00	79000000	Centro Oeste
13	MT	MATO GROSSO	30	2	2003-06-17T13:29:02-03:00	78000000	Centro Oeste
18	PR	PARANA	30	2	2003-06-17T13:28:23-03:00	80000000	Sul
16	PE	PERNANBUCO	\N	\N	\N	50000000	Nordeste
23	RS	RIO GRANDE DO SUL	30	2	2003-06-17T11:34:37-03:00	90000000	Sul
5	BA	BAHIA	25	2	2003-06-17T13:29:06-03:00	40000000	Nordeste
19	RJ	RIO DE JANEIRO	30	2	2003-06-17T13:28:40-03:00	20000000	Sudeste
11	MG	MINAS GERAIS	30	2	2003-06-17T13:28:34-03:00	30000000	Sudeste
9	GO	GOIAS	30	2	2003-06-17T13:28:56-03:00	99900000	Centro Oeste
8	ES	ESPIRITO SANTO	30	2	2003-06-17T13:28:46-03:00	29000000	Sudeste
7	DF	DISTRITO FEDERAL	30	2	2003-06-17T13:28:52-03:00	00000000	Centro Oeste
24	SC	SANTA CATARINA	30	2	2003-06-17T13:28:16-03:00	88000000	Sul
6	CE	CEARA	30	2	2003-06-17T13:29:10-03:00	60000000	Nordeste
\.

-- gecidade: 33 registro(s)
COPY public.gecidade (id_gecidade_int, codigo_str, nome_str, uf_str, ibge_int, id_geusuario_int, tstamp, codigo_santander_str, id_geuf_int, id_gemunic_npjur_int, codigo_ngs_str) FROM stdin;
4791	4791	BAURU	SP	6003	2409	2006-11-10T10:46:34-02:00	\N	26	\N	4788
5282	5282	SAO JOSE DO RIO PRETO	SP	49805	\N	\N	\N	26	\N	5279
5458	5458	PALMAS	TO	21000	\N	\N	\N	27	\N	5455
5283	5283	SAO JOSE DOS CAMPOS	SP	49904	\N	\N	\N	26	\N	5280
2	2	ASSIS BRASIL	AC	54	\N	\N	\N	1	\N	1
2266	2266	TRES LAGOAS	MS	8305	\N	\N	\N	12	\N	2264
2381	2381	SINOP	MT	7909	\N	\N	\N	13	\N	2379
2367	2367	RONDONOPOLIS	MT	7602	\N	\N	\N	13	\N	2365
2222	2222	DOURADOS	MS	3702	\N	\N	\N	12	\N	2220
3234	3234	CASCAVEL	PR	4808	\N	\N	\N	18	\N	3232
5052	5052	MARILIA	SP	29005	\N	\N	\N	26	\N	5049
5006	5006	JAGUARIUNA	SP	24709	\N	\N	\N	26	\N	5003
2892	2892	RECIFE	PE	11606	\N	\N	\N	16	\N	2890
4832	4832	CAMPINAS	SP	9502	\N	\N	\N	26	\N	4829
4192	4192	PORTO ALEGRE	RS	14902	\N	\N	\N	23	\N	4190
331	331	FEIRA DE SANTANA	BA	10800	\N	\N	\N	5	\N	329
3631	3631	RIO DE JANEIRO	RJ	4557	\N	\N	\N	19	\N	3629
1403	1403	BELO HORIZONTE	MG	6200	\N	\N	\N	11	\N	1401
5307	5307	SOROCABA	SP	52205	\N	\N	\N	26	\N	5304
5213	5213	RIBEIRAO PRETO	SP	43402	\N	\N	\N	26	\N	5210
5288	5288	SAO PAULO	SP	50308	\N	\N	\N	26	\N	5285
2302	2302	CUIABA	MT	3403	\N	\N	\N	13	\N	2300
535	535	SALVADOR	BA	27408	\N	\N	\N	5	\N	533
971	971	GOIANIA	GO	8707	\N	\N	\N	9	\N	969
878	878	VITORIA	ES	5309	\N	\N	\N	8	\N	876
2162	2162	UBERLANDIA	MG	70206	\N	\N	\N	11	\N	2160
801	801	BRASILIA	DF	108	\N	\N	\N	7	\N	799
2210	2210	CAMPO GRANDE	MS	2704	\N	\N	\N	12	\N	2208
3357	3357	LONDRINA	PR	13700	\N	\N	\N	18	\N	3355
4392	4392	BLUMENAU	SC	2404	\N	\N	\N	24	\N	4390
3259	3259	CURITIBA	PR	6902	\N	\N	\N	18	\N	3257
4443	4443	FLORIANOPOLIS	SC	5407	\N	\N	\N	24	\N	4441
675	675	FORTALEZA	CE	4400	\N	\N	\N	6	\N	673
\.

-- cbsituacaocontrato: 18 registro(s)
COPY public.cbsituacaocontrato (id_cbsituacaocontrato_int, codigo_str, descricao_str, acao_str, com_senha_str, senha_str, id_geusuario_int, tstamp) FROM stdin;
21	H	Acordo Aprovado e Efetivado	2	0		1195	2007-04-26T11:44:38-03:00
20	K	Protestado	0	0		1219	2007-03-28T15:26:07-03:00
18	I	PROCESSO DE REFIN	2	0		1984	2005-10-20T17:46:12-02:00
17	G	Cheque Compensação	3	0		1014	2004-12-17T11:09:12-02:00
16	R	Saldo Remanescente	4	0		1156	2004-10-15T09:39:09-03:00
15	F	Pré Jurídico	0	0		1156	2004-06-25T15:48:24-03:00
14	E	NE- Não encontrado	1	1	&	1366	2004-08-26T10:08:47-03:00
13	D	Decurso de Prazo	4	0		2	2003-06-27T15:33:35-03:00
12	P	Pendente do Banco	2	0		236	2003-04-09T09:17:37-03:00
10	X	Baixar contrato conf. instrução Banco	1	0	9	1047	2003-03-21T16:39:07-03:00
9	Y	Contrato Cancelado (não cobrar)	2	0		3177	2009-01-13T15:30:58-02:00
8	W	Baixar contrato que está no Jurídico	1	0		2	2002-12-03T13:31:08-02:00
6	B	Baixado	1	0		1195	2005-09-16T08:48:07-03:00
5	N	Stand by do banco	3	0		1055	2004-03-16T14:02:09-03:00
4	J	Jurídico	4	0	+	221	2003-01-20T13:07:42-02:00
3	C	Ação Contrária	0	0		2	2002-12-03T13:30:32-02:00
2	S	Stand by	3	0		1	2002-09-08T09:27:36-03:00
1	A	Aberto	0	0		2806	2006-01-27T10:46:35-02:00
\.

-- gecliente: 1 registro(s)
COPY public.gecliente (id_gecliente_int, codigo_str, nome_str, abrev_str, ativo_str, endereco1_str, endereco2_str, cep_str, id_gecidade_int, contato_str, telefone_str, fax_str, email_str, cgc_str, inscricao_str, logo_txt, tabela_filha_str, id_geusuario_int, timestamp, chave_filacobranca_str, id_geempresa_int, cod_centro_custo, dsc_centro_custo, ngs_str, id_carteira_npcob_basao_int) FROM stdin;
386	386	GRUPO SALTA	SALTA	1	\N	\N	\N	4791	\N	\N	\N	\N	\N	\N	LogoClientesBanco_Planae.jpg	cbcontratoeleva	1195	2019-08-07T00:00:00-03:00	contrato_str	1	\N	\N	\N	\N
\.

-- cbsitcontato: 80 registro(s)
COPY public.cbsitcontato (id_cbsitcontato_int, id_gecliente_int, codigo_int, descricao_str, dias_cobranca_int, exclui_contrato_str, tp_acao_str, gera_retorno, proxima_chamada_tim, id_geusuario_int, positivo_str, tstamp, ativo_str, fup_banco_str, primordial_str, envia_email_str, codigo_banco_str, tipo_contato_str, limite_stdby_int, id_gemotivonajuizamento_int, id_geaplicacao_int, preenchimento_obrigatorio_str, boleto_str, ouvidoria_str, fup_filacobranca_str, provisionamento_str, liberacao_str, id_geqlresponsavel_int, id_geqlsituacao_int, contatou_cliente_str, doc_anexo_str, id_getipodocumento_int, historico_padrao_str, id_gegrupotipodocumento_int, id_geprocesso_int, id_gegrupoprocesso_int, documento_fisico_str, tempo_ideal_int, margem_tolerancia_int, monitor_ativo_str, id_cbsituacaocontrato_int, protesto_str, standby_automatico_str, email_automatico_str, escolhe_usuario_agendamento_str, recebimento_str, visualizacao_externa_str, id_geitemprocesso_int, descricao_npcob_web_str, abre_tela_depois_salvar_str, painel_npjur_str, id_cbvalortipodespesa_int, agendamento_str, agendamento_por_str, agendamento_dias_int, agendamento_agenda_str, agendamento_unico_str, situacao_parcela_int, telefone_str, situacao_cobranca_str, painel_jur_npjur_str, mov_processo_str, doc_str, assunto_email_auto_txt, lancamento_unico_str, lancamento_depende_str, id_gemotivoinadimplencia_int, atualiza_data_contato_manual_str, apenas_aberto_str, solic_aju_str, class_at_str, at_str, id_sysatdinamico_int, painel_custas_npjur_str, data_envio_date, atualiza_data_ultimo_contato_str, painel_purgacao_str, contato_alo_str, atendida_bit, produtiva_bit, cpc_bit, data_evento_bit, id_jutipocontrole, lanca_movimento_npjur_str, tipo_protocolo_npjur_bit, classificacao_str, painel_classificacao_str, qtde_ocorrencia_follow_int, horas_blacklist_int, tp_acio_str, terceiro_bit) FROM stdin;
14089	386	66	INIBIR CONTRATO	0	N	F	0	\N	1124	P	2023-10-23T13:33:45.664932-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	INIBIR CONTRATO	\N	\N	\N	N	0	0	N	6	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14088	386	38	SOL ERRO DIVERGENTE	0	N	F	1	\N	8310	P	2023-08-23T17:48:27.434387-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	\N	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14087	386	29	LINK SOLICITADO	0	N	F	1	\N	8310	P	2023-08-23T15:53:49.925430-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	LINK PARA PAGAMENTO NO CARTÃO DE CRÉDITO SOLICITADO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14084	386	28	LINK NÃO ENV	0	N	F	1	\N	8310	P	2023-09-14T17:22:46.413997-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	\N	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14083	386	27	LINK ENVIADO	0	N	F	1	\N	8310	P	2023-09-14T17:22:38.198940-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	LINK DE PAGAMENTO NO CARTÃO DE CRÉDITO ENVIADO.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14082	386	24	SOLIC LINK	0	N	F	1	\N	8310	P	2023-11-07T08:46:00.128267-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	SOLICITAR LINK PARA PAGAMENTO NO CARTÃO DE CREDITO.\r\nVALOR TOTAL:                                       \r\nQUANTIDADE PARCELAS:                                               \r\nVENCIMENTO:	\N	16	1003	N	0	0	N	\N	N	N	N	N	N	N	92		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14081	386	37	RET DE CONSULTA	0	N	F	1	\N	8351	P	2024-04-22T16:37:29.211463-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	SEGUE DÉBITOS EM ABERTO:	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14080	386	36	CONSULTA SIST	0	N	F	1	\N	8310	P	2023-10-17T10:11:40.690979-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	\N	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14079	386	174	BOLETO NÃO SOLICITADO	0	N	F	1	\N	8310	P	2023-08-16T13:38:51.613409-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	MOTIVO:	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14078	386	173	BKO - BOLETO SOLICITADO	0	N	F	1	\N	8340	P	2024-04-01T17:15:42.876771-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	BOLETO SOLICITADO - VALOR: 000,00 - COLIGADA: 00 - VENC: 00/00/0000.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14077	386	172	SOLICITAR BOLETO	0	N	F	1	\N	8310	P	2024-01-23T11:34:51.789522-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	#SOLICITAR BOLETO:\r\n(  ) ERRO  (  ) PROPOSTA\r\nDATA DE VENCIMENTO:\r\nVALOR TOTAL DO ACORDO: R$ \r\n#Á VISTA ( )               PARCELADO ( ) QUANTIDADE DE PARCELAS:\r\n#DATA E VALOR DAS PARCELAS NEGOCIADAS:      \r\n#TIPO DE ENVIO:	\N	16	1003	N	0	0	N	\N	N	N	N	N	N	N	88		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	1	1	0	0	\N	N	\N		N	\N	\N	T	1
14076	386	35	PARCELAS DIVERGENTES	0	N	F	1	\N	8310	P	2023-08-16T15:27:35.773863-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	POR GENTILEZA NEGOCIAR AS SEGUINTES PARCELAS:	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14075	386	34	PARCELA INDEVIDA	0	N	F	1	\N	8310	P	2023-08-16T13:30:15.680066-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	PARCELAS DO CÁLCULO SÃO INDEVIDAS	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14074	386	171	BKO - BOLETO NÃO ENVIADO	0	N	F	1	\N	8310	P	2023-08-23T09:46:45.177943-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	BOLETO NÃO ENCAMINHADO. MOTIVO:	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14073	386	170	BKO - BOLETO ENVIADO	0	N	F	1	\N	8310	P	2023-08-16T15:26:33.655927-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	BKO - BOLETO ENVIADO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14072	386	165	BKO - BOLETO DE PROPOSTA ENCAMINHADO	0	N	F	1	\N	8164	P	2022-12-21T09:11:31.561925-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	BOLETO DE PROPOSTA ENCAMINHADO PARA RF	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14071	386	164	BKO - BOLETO DE PROPOSTA SOLICITADO	0	N	F	1	\N	8310	P	2023-08-24T16:30:52.979495-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	BOLETO DE PROPOSTA SOLICITADO.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14070	386	163	BKO - PROPOSTA DIVERGENTE	0	N	F	1	\N	8310	P	2023-08-22T17:26:36.901387-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	PROPOSTA DIVERGENTE. MOTIVO:	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14069	386	162	BKO - PROPOSTA RECUSADA	0	N	F	1	\N	8164	P	2022-12-21T09:05:52.668668-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	PROPOSTA RECUSADA - VALOR SUGERIDO PELO PARCEIRO: R$	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14068	386	161	BKO - PROPOSTA APROVADA	0	N	F	1	\N	8164	P	2022-12-21T09:04:59.615278-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	PROPOSTA APROVADA	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14067	386	160	BKO - PROPOSTA ENCAMINHADA	0	N	F	1	\N	8310	P	2023-08-22T17:25:28.589370-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	PROPOSTA ENCAMINHADA A SALTA	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14066	386	33	ERRO GERAR BOLETO	0	N	F	1	\N	8310	P	2023-10-11T09:41:21.045658-03:00	S	N	N	N		D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	DATA DE VENCIMENTO:\r\nDATA E VALOR DAS PARCELAS NEGOCIADAS:\r\nVALOR TOTAL:\r\n( ) À VISTA ( ) PARCELADO - QUANTIDADE DE PARCELAS:\r\n	\N	16	1003	N	0	0	N	\N	N	N	N	N	N	N	87		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	88	N	\N	N	S	EM NEGOCIACAO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14065	386	1572	Acordo Whats Parcelado	\N	\N	\N	\N	\N	6676	\N	2022-08-18T17:23:55.734677-03:00	S	\N	\N	\N	\N	D	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	N	\N	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	1
14064	386	1571	Acordo Whats A Vista	\N	\N	\N	\N	\N	6676	\N	2022-08-18T17:23:55.734677-03:00	S	\N	\N	\N	\N	D	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	N	\N	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	1
14063	386	23	PROPOSTA EM ANÁLISE	\N	\N	\N	\N	\N	8114	\N	2022-05-23T11:59:40.688066-03:00	S	\N	\N	\N	\N	D	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	RF está aguardando o retorno da proposta.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	S	\N	\N	S	PROPOSTA	\N	\N	\N	N	\N	\N	1	0	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14062	386	15	PROPOSTA	\N	N		1	\N	8310	P	2023-10-11T09:38:43.405574-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	#PROPOSTA SOLICITADA PARA SALTA:\r\n(  ) À VISTA  (  ) PARCELADO\r\n\r\n#Cód. Coligada:\r\n#Data e valor das parcelas negociadas:  \r\n#Valor original com juros e com multa: \r\n#Valor sem juros e sem multa: \r\n#Valor oferecido ao RF: \r\n#Valor de contraproposta:\r\n#Ano do Débito:\r\n	\N	16	1003	N	\N	\N	N	\N	N	N	N	N	N	N	93		0	N	\N	N	\N	\N	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	S	PROPOSTA	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14061	386	22	RF NÃO RECEBEU BOLETO	\N	\N	\N	\N	\N	8114	\N	2022-01-24T16:42:05.917496-03:00	S	\N	\N	\N	\N	D	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	RF não recebeu o boleto negociado dia   /  /	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	S	\N	\N	S	DIRECIONADO EVENTO BANCO	\N	\N	\N	N	\N	\N	1	0	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14060	386	21	RF NÃO RECEBEU BOLETO	\N	N		0	\N	1124	P	2022-01-19T12:13:29.432873-03:00	S	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	RF não recebeu o boleto negociado dia   /  /	\N	\N	\N	N	\N	\N	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	\N	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	DIRECIONADO EVENTO BANCO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14059	386	1019	RECP - COM PREVISÃO DE PAGAMENTO	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, CLIENTE COM PREVISÃO DE PAGAMENTO PARA DIA	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	EM NEGOCIACAO	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14058	386	1054	RECP - EM NEGOCIAÇÃO	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, CLIENTE EM NEGOCIAÇÃO ALEGA QUE	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	EM NEGOCIACAO	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14057	386	1018	RECP - NÃO CONFIRMA DADOS	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, NÃO CONFIRMA DADOS	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	NÃO CONFIRMA DADOS	\N	\N	\N	N	\N	\N	1	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14056	386	1020	RECP - CLIENTE FALECIDO	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, CLIENTE FALECIDO	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	CLIENTE FALECIDO	\N	\N	\N	N	\N	\N	1	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14055	386	1001	RECP - DESCONHECE CLIENTE	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, DESCONHECE CLIENTE	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	DESCONHECE CLIENTE	\N	\N	\N	N	\N	\N	1	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14054	386	1007	RECP - SUSPEITA DE FRAUDE	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, ALEGA SUSPEITA DE FRAUDE	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	SUSPEITA DE FRAUDE	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14053	386	1014	RECP - QUEDA DE LIGAÇÃO CLIENTE	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, QUEDA DE LIGAÇÃO CLIENTE	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	QUEDA DE LIGACAO	\N	\N	\N	N	\N	\N	1	0	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14052	386	1006	RECP - FINANCIOU PARA TERCEIRO	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, FINANCIOU PARA TERCEIRO	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	FINANCIAMENTO COM TERCEIRO	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14051	386	1009	RECP - CLIENTE COM AÇÃO CONTRA O PARCEIRO	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, CLIENTE COM AÇÃO CONTRA O PARCEIRO	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	CLIENTE COM ACAO ADVERSA	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14050	386	1010	RECP - CL IDENT-PREV POS.	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, PREV POSITIVO	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	PREVENTIVO POSITIVO	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14049	386	1011	RECP - CL IDENT-PREV NEG.	\N	\N	\N	\N	\N	8114	\N	2021-12-23T13:26:38.826459-03:00	S	\N	\N	\N	386	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ENTROU EM CONTATO ATRAVÉS DO RECEPTIVO, PREV NEGATIVO	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	N	\N	\N	S	PREVENTIVO NEGATIVO	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14048	386	1025	RECP - ACORDO PARCELADO	0	N	F	0	\N	1124	P	2021-12-22T18:49:14.093404-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	ACORDO FORMALIZADO COM (   )  NO VALOR DE  (  )   R$       . ENVIO SERÁ VIA (  )	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	S	ACORDO	\N	N	N	N	N	N	1	1	1	0	\N	N	\N		N	\N	\N	T	0
14036	386	25	ACORDO PARCELADO	\N	\N	\N	\N	\N	8114	\N	2021-12-21T14:23:53.165781-03:00	S	\N	\N	\N	386	D	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	ACORDO FORMALIZADO COM (   )  NO VALOR DE  (  )   R$       . ENVIO SERÁ VIA (  )	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	S	\N	\N	S	ACORDO	\N	\N	\N	N	\N	\N	1	1	1	0	\N	\N	\N	\N	\N	\N	\N	\N	0
14035	386	26	RECEPT - ACORDO PARCELADO	\N	N		0	\N	1124	P	2021-12-22T18:45:49.980836-03:00	N	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	ACORDO FORMALIZADO COM (   )  NO VALOR DE  (  )   R$       . ENVIO SERÁ VIA (  )	\N	\N	\N	N	\N	\N	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	\N	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	ACORDO	\N	N	N	N	N	N	1	1	1	0	\N	N	\N		N	\N	\N	T	0
14030	386	32	Contrato suspenso 30	0	N	F	0	\N	8101	P	2021-12-22T13:10:08.026467-03:00	N	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	Contrato suspenso por 30 dias por solicitação do parceiro.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	CLIENTE COM ACAO	\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14029	386	31	Contrato suspenso 15	0	N	F	0	\N	8101	P	2021-12-22T13:09:56.018812-03:00	N	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	Contrato suspenso por 15 dias por solicitação do parceiro.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	CLIENTE COM ACAO	\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14028	386	30	Contrato Suspenso 7	0	N	F	0	\N	8101	P	2021-12-22T13:09:43.480150-03:00	N	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	Contrato suspenso por 7 dias por solicitação do parceiro	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	CLIENTE COM ACAO	\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14027	386	777777	TRATAMENTO DE BASE NEGATIVO	0	N	F	0	\N	7993	P	2020-02-12T12:21:19.602048-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	TRATAMENTO DE BASE NEGATIVO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N	TRATAMENTO DE BASE NEGATIVO	0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14026	386	666666	TRATAMENTO DE BASE POSITIVO	0	N	F	0	\N	7993	P	2020-02-12T12:20:40.545523-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	TRATAMENTO DE BASE POSITIVO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N	TRATAMENTO DE BASE POSITIVO	0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14025	386	14	QUEDA DE LIGAÇÃO CLIENTE	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	QUEDA DE LIGAÇÃO CLIENTE	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	QUEDA DE LIGACAO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14024	386	141414	Carta de Cobrança  - SMS	0	N	F	1	\N	8016	P	2020-01-30T10:56:14.367283-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	Carta de Cobrança  - SMS	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14023	386	5000	ENCAMINHADO TORPEDO SMS NESTA DATA	0	N	F	1	\N	8016	P	2020-01-30T10:56:09.312148-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	ENCAMINHADO TORPEDO SMS NESTA DATA	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N	ENCAMINHADO TORPEDO SMS NESTA DATA	0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	N	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14022	386	153	E-MAIL ENVIADO	0	N	F	0	\N	7997	P	2020-01-29T16:56:29.279479-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	Detalhamento da dívida e condições de pagamento enviados ao cliente via e-mail	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14021	386	54	EM NEGOCIAÇÃO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	EM CONTATO COM CLIENTE O MESMO INFORMA QUE ESTÁ EM NEGOCIAÇÃO, ONDE ALEGA QUE	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	EM NEGOCIACAO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14020	386	222	ATENÇÃO SUPERVISOR	0	N	F	0	\N	8310	P	2023-08-16T15:56:40.558074-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	\N	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	S	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14019	386	333	ATENÇÃO GERENTE	0	N	F	0	\N	7997	P	2020-01-22T13:21:13.489805-03:00	S	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	\N	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N		\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14018	386	157	PROPOSTA POR E-MAIL	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CLIENTE DESEJA RECEBER PROPOSTA DE ACORDO POR E-MAIL.  QUAL TIPO DE PROPOSTA (  ) A VISTA R$          (  ) PARCELADO EM   X DE R$             DATA DE PAGAMENTO:	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	EM NEGOCIACAO	\N	N	N	N	N	N	0	0	1	0	\N	N	\N		N	\N	\N	T	0
14017	386	1122	REENVIO BOLETO	0	N	F	1	\N	8114	P	2021-12-21T14:23:53.165781-03:00	S	N	N	N	386	D	0	\N	549	0	N	N	N	N	N	\N	\N	S	N	\N	REENVIO BOLETO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	N	REENVIO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14016	386	45	SOLICITOU RETORNO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	SOLICITOU RETORNO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	SEM NEGOCIACAO	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	0
14015	386	7	SUSPEITA DE FRAUDE	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	SUSPEITA DE FRAUDE	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	SUSPEITA DE FRAUDE	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14014	386	1005	RECP - SEM CONDIÇÕES	0	N	F	0	\N	8114	P	2021-12-21T14:23:53.165781-03:00	S	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CLIENTE ENTROU EM CONTATO PELO RECEPTIVO E ALEGA ESTAR SEM CONDIÇÕES DEVIDO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	SEM CONDICOES	\N	N	N	N	N	N	1	1	1	0	\N	N	\N		N	\N	\N	T	0
14013	386	1012	RECP - QUEDA DE LIGAÇÃO	0	N	F	0	\N	8114	P	2021-12-21T14:23:53.165781-03:00	S	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CLIENTE ENTROU EM CONTATO PELO RECEPTIVO E LIGAÇÃO CAIU DURANTE ATENCIMENTO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	QUEDA DE LIGACAO	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	0
14012	386	1002	RECP - BOLETO À VISTA	0	N	F	0	\N	1124	P	2021-12-22T18:40:39.428315-03:00	S	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	ACORDO FORMALIZADO COM (   )  NO VALOR DE  (  )   R$       . ENVIO SERÁ VIA (  )	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	ACORDO	\N	N	N	N	N	N	1	1	1	0	\N	N	\N		N	\N	\N	T	0
14011	386	1003	RECP - ALEGA PAGAMENTO	0	N	F	0	\N	8114	P	2021-12-21T14:23:53.165781-03:00	S	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CLIENTE ENTROU EM CONTATO PELO RECEPTIVO E ALEGA PAGAMENTO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	ALEGA PAGAMENTO	\N	N	N	N	N	N	1	1	1	0	\N	N	\N		N	\N	\N	T	0
14010	386	4	RECADO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	RECADO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	RECADO	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	1
14009	386	18	NÃO CONFIRMA DADOS	0	N	F	0	\N	8404	P	2025-06-23T10:52:48.012890-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	NÃO CONFIRMA DADOS	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	NAO CONFIRMA DADOS	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14008	386	16	NÃO ATENDE	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	NÃO ATENDE	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	SEM ATENDIMENTO PREVIEW	\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14007	386	17	NÃO ANOTOU RECADO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	NÃO ANOTOU RECADO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	NAO ANOTOU RECADO	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	1
14006	386	8	MUDO RECADOCXP.	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	MUDO RECADOCXP.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	MUDO	\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
14005	386	6	FINANCIOU PARA TERCEIRO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	FINANCIOU PARA TERCEIRO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	FINANCIAMENTO COM TERCEIRO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14004	386	1	DESCONHECE CLIENTE	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	DESCONHECE CLIENTE	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	DESCONHECE CLIENTE	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	0
14003	386	19	COM PREVISÃO DE PAGAMENTO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	COM PREVISÃO DE PAGAMENTO PARA DIA	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	EM NEGOCIACAO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14002	386	20	CLIENTE FALECIDO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CLIENTE FALECIDO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	CLIENTE FALECIDO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14001	386	9	CLIENTE COM AÇÃO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CLIENTE COM AÇÃO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	CLIENTE COM ACAO ADVERSA	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
14000	386	12	QUEDA LIGAÇAO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	387	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	QUEDA LIGAÇAO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	QUEDA DE LIGACAO	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	1
13999	386	5	SEM CONDIÇOES	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	SEM CONDIÇOES	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	SEM CONDICOES	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
13998	386	13	CL IDENT-QUEDA LIG.\r\n	0	N	F	0	\N	8101	P	2021-12-22T13:09:02.215408-03:00	N	N	N	N		G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	\N	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	QUEDA DE LIGACAO CLIENTE	\N	N	N	N	N	N	0	0	0	0	\N	N	\N		N	\N	\N	T	0
13997	386	10	CL IDENT-PREV POS.	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CL IDENT-PREV POS.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	PREVENTIVO POSITIVO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
13996	386	11	CL IDENT-PREV NEG.	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	CL IDENT-PREV NEG.	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	PREVENTIVO NEGATIVO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
13995	386	2	BOLETO À VISTA	9999	N	S	0	\N	8114	P	2021-12-21T14:23:53.165781-03:00	S	N	N	N	386	D	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	ACORDO FORMALIZADO COM (   )  NO VALOR DE  (  )   R$       . ENVIO SERÁ VIA (  )	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	ACORDO	\N	N	N	N	N	N	1	1	1	0	\N	N	\N		N	\N	\N	T	0
13994	386	3	ALEGA PAGAMENTO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	ALEGA PAGAMENTO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	ALEGA PAGAMENTO	\N	N	N	N	N	N	1	0	1	0	\N	N	\N		N	\N	\N	T	0
13993	386	444	AGENDAMENTO	0	N	F	0	\N	8114	P	2021-12-13T12:41:39.440764-03:00	S	N	N	N	386	G	0	\N	\N	0	N	N	N	N	N	\N	\N	N	N	\N	AGENDAMENTO	\N	\N	\N	N	0	0	N	\N	N	N	N	N	N	N	\N		0	N	\N	N	\N	0	N	N	\N	N	\N	N	N	\N	\N	\N	\N	\N	S	\N	N	S	AGENDAMENTO	\N	N	N	N	N	N	1	0	0	0	\N	N	\N		N	\N	\N	T	0
\.

-- gegrupoprocesso: 2 registro(s)
COPY public.gegrupoprocesso (id_gegrupoprocesso_int, codigo_str, nome_str, administrador_str, id_gegrupoprocessoadm_int, id_geusuario_int, tstamp, ativo_str) FROM stdin;
1002	386	Bko Salta	S	1002	8310	2023-08-10T10:12:04-03:00	N
1003	387	Bko Salta	N	1002	8310	2023-08-10T10:16:50-03:00	S
\.

-- geprocesso: 1 registro(s)
COPY public.geprocesso (id_geprocesso_int, id_gegrupoprocesso_int, codigo_str, descricao_str, id_geusuario_int, tstamp, permite_varios_str, admalteraprazo_str, id_geraretroativo_str, sql_campos_txt, sql_tabelas_txt, sql_where_txt) FROM stdin;
16	1002	387	Bko Salta	8310	2023-08-10T10:15:15.822172-03:00	N	S	N	\N	\N	\N
\.

-- geaplicacao: 2 registro(s)
COPY public.geaplicacao (id_geaplicacao_int, codigo_str, nome_str, siglamodulo_str, tipo_str, id_geusuario_int, timestamp, visualiza_agendador_str, novo_modelo_bit, id_cbmodlayout_int, versao_minima_str) FROM stdin;
495	CB002_NEW2	Atendimento Manual - Homologação	Cb	F	1195	2006-11-03T17:17:54-03:00	N	\N	\N	\N
549	CB173	Reenvio de Boleto (Novo)	CB	F	1195	2008-02-15T14:19:23-02:00	N	\N	\N	\N
\.

-- geitemprocesso: 4 registro(s)
COPY public.geitemprocesso (id_geitemprocesso_int, id_geprocesso_int, sequencia_int, descricao_str, prazo_int, procedimentos_txt, id_geaplicacao_int, carrega_str, finalizado_str, id_gegrupoprocesso_int, id_geusuario_int, tstamp) FROM stdin;
92	16	5	PARC EM CARTÃO	0		495	S	N	\N	8310	2023-08-22T17:57:20-03:00
88	16	2	SOLIC BOLETO	0		495	S	N	\N	8310	2023-09-27T11:26:56-03:00
87	16	1	ERRO FOLLOW	0		495	S	N	\N	8310	2023-08-23T17:49:09-03:00
93	16	6	PROP CADASTRO	0		495	S	N	\N	8310	2023-08-22T17:29:19-03:00
\.

-- gemotivoinadimplencia: 1 registro(s)
COPY public.gemotivoinadimplencia (id_gemotivoinadimplencia_int, codigo_str, descricao_str, id_geusuario_int, tstamp, id_geaplicacao_int, codigo_banco_str, ativo_str, descricao_banco_str, tempo_str, codigo_sem_interesse_str) FROM stdin;
88	1	Perda de Emprego	1195	2019-11-21T09:49:17-03:00	\N	106	S	DESEMPREGO	\N	
\.

COMMIT;
