SELECT 

	table_name ||
	case 
	     when table_name = 'cbfollowup' then '|data_dat |365 |500'
		 when table_name = 'cbitembordero' then '|emissao_dat |365 |500'
		 when table_name = 'cbbordero' then '|data_dat |365 |500'
		 when table_name like 'cb%' then '| | |100'
		 when table_name like 'geql%' then '| | |100'
	     else '| | |500'
	end  as conf

FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')

  and ( 
  		table_name like 'ge%' or
		table_name like 'fi%' or
		table_name like 'cb%'
	  )

  
ORDER BY table_schema, table_name desc;