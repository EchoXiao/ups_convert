# ups_convert



# coding: utf-8

# In[1306]:

import pandas as pd 
import numpy as np

### read ups and sf_backup file
ups = pd.read_csv('ups.csv')
ups = ups[[20, 21, 11, 26, 30, 35, 43, 44, 33]]
ups.columns = ['id', 'sf_awb_no', 'pick_up_date', 'weight', 'first', 'second', 'third', 'forth', 'ups_price']

backup = pd.read_csv('epv_delivered_out.csv', encoding = 'utf-16')

ups_del_weight = ups[['id', 'sf_awb_no', 'pick_up_date', 'first', 'second', 'third', 'forth', 'ups_price']]

ups_weight = ups[['id', 'sf_awb_no', 'weight']].groupby('id').sum().reset_index()
ups = ups_del_weight.merge(ups_weight, how = 'left', on = 'id')



# In[1307]:

ups.head()


# In[1308]:

# ups.loc[ups.forth != [('003', '013', '014')], 'ups_price' ] = 0
ups.loc[ups.query("forth != ['003', '013', '014']").index, 'ups_price'] = 0



# In[1309]:

# ups['ups_price'][ups['forth']] 
# ups.ups_price.map({forth})
ups.head()


# In[1310]:

### read zone file

JFK = pd.read_excel("JFK.xlsx")
ORD = pd.read_excel("ORD.xlsx")
LAX = pd.read_excel("LAX.xlsx")

JFK['Gate_Way'] = 'JFK'
ORD['Gate_Way'] = 'ORD'
LAX['Gate_Way'] = 'LAX'
zone = pd.concat([JFK, ORD, LAX])


# In[1311]:

# zone[(zone['Gate_Way'] == 'LAX') & (zone['Ground'] == 6)]


# In[ ]:




# In[ ]:




# In[1312]:

#### read 'freight' file
one = pd.read_excel('1.xlsx')
two = pd.read_excel('2.xlsx')
three = pd.read_excel('3.xlsx')
thirteen = pd.read_excel('13.xlsx')


# In[1313]:

#### merged ups and backup
### come up with merged
onlynotnaups = ups[ups['sf_awb_no'].isin(ups['sf_awb_no'].dropna().astype(str))]
backup['main_sf_awb'] = backup['main_sf_awb'].astype(str)
backup['sf_awb_no'] = backup['sf_awb_no'].astype(str)

merged = onlynotnaups.merge(backup, how='left', on='sf_awb_no')


#### delete the columns where weight == 0
zero_weight = merged[merged['weight'] == 0]
del_weight = merged[merged['weight'] != 0]
zero_weight = zero_weight[['id', 'sf_awb_no', 'forth', 'ups_price']]
# merged.head()


# In[1314]:


# weight_sum = merged[['sf_awb_no', 'weight']].groupby(['sf_awb_no'], as_index = False).sum()
# pivot_table =merged.pivot_table('price', index = ['id', 'sf_awb_no'], columns = ['first', 'second', 'third', 'forth']).fillna(0)
# print(pd.merge(merged, weight_sum, how = 'left', on = 'sf_awb_no'))
# print(backup[backup['sf_awb_no'].astype(str).isin(onlynotnaups['sf_awb_no'])])
# print(ups['sf_awb_no'ups['sf_awb_no'].dropna().astype(str)))

# a = merged[['sf_awb_no', 'consignee_postal_code', 'sf_chargeable_weight']].dropna()

merged = del_weight

merged['dest_zip'] = merged['consignee_postal_code'] // 100

# merged['Ground'] = np.nan


# In[1315]:

merged.head()


# In[1316]:


#### zone reindex
#### merged = merged + zone
zone = zone.reset_index()
for x in zone.index:
	z = zone.loc[x]
	ground_filter = (z['Gate_Way'] == merged['gateway']) & (merged['dest_zip'] >= z['Start']) & (merged['dest_zip'] <= z['End']) 
	merged.loc[ground_filter, 'Ground'] = z['Ground']



# In[1317]:



# print(merged[['sf_awb_no', 'gateway', 'sf_actual_weight', 'Ground']])
# 2. map with type -- get the freight

# index_three = (merged[merged['forth'] == '003'])
# index_thirteen = (merged[merged['forth'] == '013'])
# index_two = (merged[merged['forth'] == '002'])

# uniqued = pd.concat([index_two, index_thirteen, index_three])

# for index in uniqued.index:

# print(uniqued.head())
# print(one.head())


# In[1318]:

merged.head()


# In[1319]:

# print(one.reset_index().T)

#### freight
one = pd.melt(one, id_vars = ['Lbs.'], value_vars=list(one.columns)[1:])
two = pd.melt(two, id_vars = ['Lbs.'], value_vars=list(two.columns)[1:])
three = pd.melt(three, id_vars = ['Lbs.'], value_vars=list(three.columns)[1:])
thirteen = pd.melt(thirteen, id_vars = ['Lbs.'], value_vars=list(thirteen.columns)[1:])


one.head()


# In[1320]:


one ['type'] = '1'
two['type'] = '2'
three['type'] = '3'
thirteen['type'] = '13'

one.head()
# thirteen


# In[1321]:

# one.loc[0]['Lbs.'],two.loc[0]['Lbs.'],three.loc[0]['Lbs.'],thirteen.loc[0]['Lbs.'], 


# In[1322]:

freight = pd.concat([one, two, three, thirteen], ignore_index=True)
# sf_data = merged[['id', 'sf_awb_no', 'sf_chargeable_weight', 'Ground', 'first', 'second' ,'third' , 'forth']]
freight.head()


# In[1323]:

freight_cp = freight.copy()
# sf_data_cp = sf_data.copy()
merged_cp = merged.copy()


# In[ ]:




# In[1324]:

freight = freight_cp.copy()
# sf_data = sf_data_cp.copy()
merged = merged_cp.copy()
#### merged = ups + backup - weightis0 + zone


# In[1325]:


freight['Lbs.'] = freight['Lbs.'].astype(str)
freight['variable'] = freight['variable'].astype(str)
# freight['type'] = freight['type'].astype(str)



merged = merged.dropna()
merged = merged[merged['Ground'].astype(str) != 'nan']
# print(merged['Ground'] != 'nan')
merged['sf_chargeable_weight'] = merged['sf_chargeable_weight'].astype(float).astype(int).astype(str)
merged['Ground'] = merged['Ground'].astype(float).astype(int).astype(str)
merged['forth'] = merged['forth'].astype(str)


print(freight['type'].iloc[1])


# In[1326]:

freight['type'] = freight['type'].astype(int)
freight['type'] = ["%03d" % n for n in freight['type']]
# print(type(freight['type'].iloc[1]))
print(freight.head())


# In[1327]:

merged.head()
# merged.columns
# = ups[ups['sf_awb_no'].isin(ups['sf_awb_no'].dropna().astype(str))]
# sf_data[[sf_data['sf_awb_no'].isin(sf_data['sf_awb_no'].dropna().astype(str))]]
# sf_data[['sf_chargeable_weight', 'Ground', 'forth']] = (sf_data[['sf_chargeable_weight', 'Ground', 'forth']].dropna().astype(int).astype(str))
# sf_freight[['sf_chargeable_weight', 'Ground', 'forth']] = (sf_freight[['sf_chargeable_weight', 'Ground', 'forth']].dropna().astype(int).astype(str))

# freight
# sf_data = sf_data.dropna().astype(int).astype(str)

# merged[['sf_chargeable_weight', 'Ground', 'forth']] = (merged[['sf_chargeable_weight', 'Ground', 'forth']].dropna().astype(int).astype(str))

# freight[['Lbs.', 'variable', 'type']].head()
# freight[freight['type'] == '13']


# In[1328]:

merged[['Ground', 'sf_chargeable_weight', 'forth']].head()


# In[1354]:

freight['variable'] = freight['variable'].astype(int)
freight.head()


# In[1355]:

print(type(freight['variable'].iloc[1]))
print(type(freight['Lbs.'].iloc[1]))
print(type(freight['value'].iloc[1]))
print(type(freight['type'].iloc[1]))

# print(type(freight['zone'].iloc[1]))



# In[1356]:

freight.columns


# In[1357]:

freight['zone'] = freight['variable'] % 10
freight['variable'] = freight['variable']
# freight['zone'] = freight['zone'].astype(str)

# merged['Ground'] = merged['Ground'].astype(float)
# merged[merged.dropna()]
freight.head()


# In[1369]:


freight['zone'] = freight['zone'].astype(str)
freight['variable'] = freight['variable'].astype(str)
freight['value'] = freight['value'].astype(str)


# In[1370]:




# merged[['sf_chargeable_weight', 'Ground', 'forth']]
print(type(freight.loc[1]['zone']))
print(type(freight.loc[1]['Lbs.']))
print(type(freight.loc[1]['variable']))
print(type(freight.loc[1]['value']))
print(type(freight.loc[1]['type']))

print(type(merged.loc[1]['Ground']))
print(type(merged.loc[1]['forth']))



# In[ ]:




# In[1371]:

merged[['sf_chargeable_weight', 'Ground', 'forth']].head()


# In[1372]:

freight.head()


# In[1373]:

print(type(freight.loc[1]['Lbs.']))
print(type(freight.loc[1]['variable']))
print(type(freight.loc[1]['type']))
print(type(freight.loc[1]['zone']))




print(type(merged.loc[1]['sf_chargeable_weight']))
print(type(merged.loc[1]['Ground']))
print(type(merged.loc[1]['forth']))


# In[1374]:


sf_freight = merged.merge(
	freight, 
	how = 'left', 
	left_on = ['sf_chargeable_weight', 'Ground', 'forth'], 
	right_on = ['Lbs.', 'zone', 'type'])


sf_freight[['value', 'id', 'variable', 'type', 'zone']].head()
# zero_weight


# In[1375]:

sf_freight = sf_freight.merge(
        zero_weight,
        how = 'left',
        on = ('id', 'sf_awb_no'))
# sf_freight['ups_freight_price'] = sf_freight['ups_price_x'] + sf_freight['ups_price_y']
# sf_freight[['id', 'value', 'type', 'zone', 'variable']]
sf_freight


# In[1376]:

# freight[['Lbs.', 'variable', 'type']].head()


# In[1377]:

# print(type(sf_data[['sf_chargeable_weight', 'Ground', 'forth']].loc[38]['sf_chargeable_weight']))
# print(type(sf_data[['sf_chargeable_weight', 'Ground', 'forth']].loc[38]['Ground']))
# print(type(sf_data[['sf_chargeable_weight', 'Ground', 'forth']].loc[38]['forth']))


# In[1378]:

print(type(freight.loc[1]['Lbs.']))
print(type(freight.loc[1]['variable']))
print(type(freight.loc[1]['type']))


# In[1379]:

# sf_freight['forth'] = sf_freight['forth_x'] + sf_freight['forth_y']
# sf_freight['variable']


# In[1383]:

pt = sf_freight.copy()
pt['value'] = pt['value'].fillna(0).astype(float)
pivot_table = pt.pivot_table('value', index = ['id','sf_awb_no', 'pick_up_date', 'weight', 'sf_actual_weight', 'sf_chargeable_weight', 'gateway', 'Ground'], columns = ['first', 'second', 'third', 'forth_x'], aggfunc=np.mean).fillna(0)
pivot_table


# In[1381]:

###### pivot_table
# freight[(freight['Lbs.'] == '113') & (freight['type'] == '3')]


# In[1235]:

# merged.head()


# In[1236]:

# sf_data[(sf_data['sf_chargeable_weight'] == '2')]


# In[1237]:

# merged.head()


# In[ ]:




# In[1109]:

# outcome =  pd.merge(merged, sf_freight, how = 'left', left_on = ('sf_chargeable_weight', 'Ground', 'forth'), right_on = ('Lbs.', 'variable', 'type') )


# In[1110]:

# outcome


# In[1111]:

# outcome = outcome[['id_x', 'sf_awb_no_x', 'pick_up_date', 'weight', 'first', 'second', 'third', 'forth_x', 'value', 'ups_price', 'sf_actual_weight', 'sf_chargeable_weight_x', 'gateway',  'Ground_x']]


# In[1112]:

# outcome


# In[1113]:

# pivot_table = outcome.pivot_table('value', index = ('id_x','sf_awb_no_x', 'pick_up_date', 'weight','ups_price', 'sf_actual_weight', 'sf_chargeable_weight_x', 'gateway', 'Ground_x'), columns = ['first', 'second', 'third', 'forth_x'], aggfunc = lambda x: x).fillna(0)


# In[ ]:




# In[1114]:




# In[1115]:

# df1.set_index(['index'] + unstack_cols).unstack(level=unstack_cols)






