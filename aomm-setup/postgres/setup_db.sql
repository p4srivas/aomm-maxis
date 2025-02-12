create user aomm_data with encrypted password 'J6FJd85WgTa2Xptg';
GRANT CONNECT ON DATABASE aomm_data to aomm_data;
grant all privileges on database aomm_data to aomm_data;

create user aomm_data_ro with encrypted password 'J6FJd85WgTa2Xptg';
GRANT CONNECT ON DATABASE aomm_data to aomm_data_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO aomm_data_ro;