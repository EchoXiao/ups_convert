import pandas as pd
import numpy as np



### read ups, sf_backup, zone, freight

# ups
ups = pd.read_csv('ups.csv')
ups = ups[[20, 21, 11, 26, 28, 30, 35, 43, 44, 48, 52, 33]]
ups.columns = ['id', 'sf_awb_no', 'pick_up_date', 'ups_actual_weight', 'ups_chargeable_weight', 'first', 'second', 'third', 'forth',  'ups_final_price', 'ups_price', 'variable']
ups = ups.fillna(0)

ups_weight = ups[['id', 'sf_awb_no', 'ups_actual_weight', 'ups_chargeable_weight']]
ups_weight = ups_weight[(ups_weight['ups_actual_weight'] != 0) & ups_weight['ups_chargeable_weight'] != 0]

ups = ups[['id', 'sf_awb_no', 'pick_up_date', 'first', 'second', 'third', 'forth',  'ups_final_price', 'ups_price', 'variable']]
ups = ups.merge(ups_weight, how = 'left', on = ('id', 'sf_awb_no'))

# sf_backup

backup = pd.read_csv('epv_delivered_out.csv', encoding = 'utf-16')
backup['dest_zip'] = backup['consignee_postal_code'] // 100


# zone


JFK = pd.read_excel("JFK.xlsx")
ORD = pd.read_excel("ORD.xlsx")
LAX = pd.read_excel("LAX.xlsx")

JFK['Gate_Way'] = 'JFK'
ORD['Gate_Way'] = 'ORD'
LAX['Gate_Way'] = 'LAX'

zone = pd.concat([JFK, ORD, LAX])

# zone.head(10)



# freight

one = pd.read_excel('1.xlsx')
two = pd.read_excel('2.xlsx')
three = pd.read_excel('3.xlsx')
thirteen = pd.read_excel('13.xlsx')


one = pd.melt(one, id_vars = ['Lbs.'], value_vars=list(one.columns)[1:])
two = pd.melt(two, id_vars = ['Lbs.'], value_vars=list(two.columns)[1:])
three = pd.melt(three, id_vars = ['Lbs.'], value_vars=list(three.columns)[1:])
thirteen = pd.melt(thirteen, id_vars = ['Lbs.'], value_vars=list(thirteen.columns)[1:])


one['type'] = '1'
two['type'] = '2'
three['type'] = '3'
thirteen['type'] = '13'


freight = pd.concat([one, two, three, thirteen], ignore_index=True)
freight['type'] = freight['type'].astype(int)
freight['type'] = ["%03d" % n for n in freight['type']]
freight['zone'] = freight['variable'] % 10





######## ups + backup + zone + freight

# ups + backup = ups_backup

onlynotnaups = ups[ups['sf_awb_no'].isin(ups['sf_awb_no'].dropna().astype(str))]
backup['main_sf_awb'] = backup['main_sf_awb'].astype(str)
backup['sf_awb_no'] = backup['sf_awb_no'].astype(str)

ups_backup = onlynotnaups.merge(backup, how='left', on='sf_awb_no')
ups_backup = ups_backup.fillna(0)
ups_backup['dest_zip'] = ups_backup['dest_zip'].astype(int)


ups_backup['gateway'] = ups_backup['gateway'].astype(str)
zone['Gate_Way'] = zone['Gate_Way'].astype(str)



# ups_backup + zone = ups_backup

zone.reset_index(drop=True, inplace=True)
for x in zone.index:
    z = zone.iloc[x]
#     index = list(filter(lambda i: all([z['Gate_Way'] == str(ups_backup.iloc[i]['gateway']),
#                           (ups_backup.iloc[i]['dest_zip'] >= z['Start']), 
#                           (ups_backup.iloc[i]['dest_zip'] <= z['End'])]),ups_backup.index))
    flt =(z['Gate_Way'] == ups_backup['gateway']) & (ups_backup['dest_zip'] >= z['Start']) & (ups_backup['dest_zip'] <= z['End']) 
    
    ups_backup.loc[flt, 'Ground'] = z['Ground']
#     if len(index) != 0:
#         print(index)

##### ups_bakcup + freight = ups_backup

sf_freight = ups_backup.merge(
    freight, 
    how = 'left', 
    left_on = ['sf_chargeable_weight', 'variable'], 
    right_on = ['Lbs.', 'variable'])



# pivot_table = sf_freight.pivot_table('ups_price', index = ('id', 'sf_awb_no', 'pick_up_date', 'ups_total_price', 'ups_actual_weight', 'sf_actual_weight', 'ups_chargeable_weight', 'sf_chargeable_weight', 'value'), columns = ['first', 'second', 'third', 'forth']).fillna(0)
pivot_table = sf_freight.pivot_table('ups_price', index = ('id', 'sf_awb_no', 'pick_up_date', 'ups_actual_weight','ups_chargeable_weight', 'sf_actual_weight', 'sf_chargeable_weight','value'), columns = ['first', 'second', 'third', 'forth']).fillna(0)




pivot_table
