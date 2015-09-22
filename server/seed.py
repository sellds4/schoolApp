import psycopg2
conn = psycopg2.connect("host='localhost' port='5432' dbname='school' user='postgres' password='postgres'")
cur = conn.cursor()
f = open(r'./data/school_data_noheader_08262015.csv', 'r')
cur.copy_from(f, 'schools', null="", columns=('name', 'address', 'city', 'state_abbrv', 'state', 'region', 'latitude', 'longitude',\
    'website', 'mascot', 'is_public', 'is_private', 'is_hbcu', 'is_tribal', 'is_religious', 'religious_affiliation',\
    'urbanization', 'urbanization_degree', 'enrollment', 'enrollment_range', 'in_state_tuition', 'out_state_tuition',\
    'percent_admit', 'percent_admit_men', 'percent_admit_women', 'graduate_enrollment', 'undergrad_enrollment',\
    'percent_amerindian_aknative', 'percent_asian_nativehi_pacislander', 'percent_asian', 'percent_nativehi_pacislander',\
    'percent_aficanamer', 'percent_hispanic_latino', 'percent_white', 'percent_women', 'percent_amerindian_aknative_undergrad',\
    'percent_asian_nativehi_pacislander_undergrad', 'percent_asian_undergrad', 'percent_nativehi_pacislander_undergrad',\
    'percent_aficanamer_undergrad', 'percent_hispanic_latino_undergrad', 'percent_white_undergrad', 'percent_women_undergrad',\
    'percent_amerindian_aknative_grad', 'percent_asian_nativehi_pacislander_grad', 'percent_asian_grad',\
    'percent_nativehi_pacislander_grad', 'percent_aficanamer_grad', 'percent_hispanic_latino_grad', 'percent_white_grad',\
    'percent_women_grad', 'act_75th_percentile', 'act_25th_percentile', 'sat_writing_75th_percentile',\
    'sat_writing_25th_percentile', 'sat_math_75th_percentile', 'sat_math_25th_percentile', 'sat_cr_75th_percentile',\
    'sat_cr_25th_percentile', 'ipeds_id'
))
f.close()
conn.commit()
conn.close()
