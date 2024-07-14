#!/usr/bin/env python
# coding: utf-8

# <h2 align="center">AtliQ Hotels Data Analysis Project<h2>

# In[1]:


import pandas as pd


# ***
# ### ==> 1. Data Import and Data Exploration
# ***

# ### Datasets
# We have 5 csv file 
# 
#    - dim_date.csv  
#    - dim_hotels.csv
#    - dim_rooms.csv
#    - fact_aggregated_bookings
#    - fact_bookings.csv

# **Read bookings data in a datagrame**

# In[246]:


df_bookings = pd.read_csv('datasets/fact_bookings.csv')


# **Explore bookings data**

# In[247]:


df_bookings.head()


# In[248]:


df_bookings.shape


# In[249]:


df_bookings.room_category.unique()


# In[250]:


df_bookings.booking_platform.unique()


# In[251]:


df_bookings.booking_platform.value_counts()


# In[252]:


df_bookings.booking_platform.value_counts().plot(kind="bar")


# In[253]:


df_bookings.describe()


# **Read rest of the files**

# In[254]:


df_date = pd.read_csv('datasets/dim_date.csv')
df_hotels = pd.read_csv('datasets/dim_hotels.csv')
df_rooms = pd.read_csv('datasets/dim_rooms.csv')
df_agg_bookings = pd.read_csv('datasets/fact_aggregated_bookings.csv')


# In[255]:


df_hotels.shape


# In[256]:


df_hotels.head(3)


# In[257]:


df_hotels.category.value_counts()


# In[258]:


df_hotels.city.value_counts().plot(kind="bar")


# ***
# **Exercise: Explore aggregate bookings**
# ***

# In[259]:


df_agg_bookings.head(3)


# **Exercise-1. Find out unique property ids in aggregate bookings dataset**

# In[1]:


# write your code here


# **Exercise-2. Find out total bookings per property_id**

# In[2]:


# write your code here


# **Exercise-3. Find out days on which bookings are greater than capacity**

# In[3]:


# write your code here


# **Exercise-4. Find out properties that have highest capacity**

# In[4]:


# write your code here


# ***
# ### ==> 2. Data Cleaning
# ***

# In[265]:


df_bookings.describe()


# **(1) Clean invalid guests**

# In[266]:


df_bookings[df_bookings.no_guests<=0]


# As you can see above, number of guests having less than zero value represents data error. We can ignore these records.

# In[267]:


df_bookings = df_bookings[df_bookings.no_guests>0]


# In[268]:


df_bookings.shape


# **(2) Outlier removal in revenue generated**

# In[269]:


df_bookings.revenue_generated.min(), df_bookings.revenue_generated.max()


# In[270]:


df_bookings.revenue_generated.mean(), df_bookings.revenue_generated.median()


# In[271]:


avg, std = df_bookings.revenue_generated.mean(), df_bookings.revenue_generated.std()


# In[272]:


higher_limit = avg + 3*std
higher_limit


# In[273]:


lower_limit = avg - 3*std
lower_limit


# In[274]:


df_bookings[df_bookings.revenue_generated<=0]


# In[275]:


df_bookings[df_bookings.revenue_generated>higher_limit]


# In[276]:


df_bookings = df_bookings[df_bookings.revenue_generated<=higher_limit]
df_bookings.shape


# In[277]:


df_bookings.revenue_realized.describe()


# In[278]:


higher_limit = df_bookings.revenue_realized.mean() + 3*df_bookings.revenue_realized.std()
higher_limit


# In[279]:


df_bookings[df_bookings.revenue_realized>higher_limit]


# One observation we can have in above dataframe is that all rooms are RT4 which means presidential suit. Now since RT4 is a luxurious room it is likely their rent will be higher. To make a fair analysis, we need to do data analysis only on RT4 room types

# In[280]:


df_bookings[df_bookings.room_category=="RT4"].revenue_realized.describe()


# In[281]:


# mean + 3*standard deviation
23439+3*9048


# Here higher limit comes to be 50583 and in our dataframe above we can see that max value for revenue realized is 45220. Hence we can conclude that there is no outlier and we don't need to do any data cleaning on this particular column

# In[282]:


df_bookings[df_bookings.booking_id=="May012216558RT213"]


# In[283]:


df_bookings.isnull().sum()


# Total values in our dataframe is 134576. Out of that 77899 rows has null rating. Since there are many rows with null rating, we should not filter these values. Also we should not replace this rating with a median or mean rating etc 

# In[ ]:





# **Exercise-1. In aggregate bookings find columns that have null values. Fill these null values with whatever you think is the appropriate subtitute (possible ways is to use mean or median)**

# In[5]:


# write your code here


# **Exercise-2. In aggregate bookings find out records that have successful_bookings value greater than capacity. Filter those records**

# In[6]:


# write your code here


# ***
# ### ==> 3. Data Transformation
# ***

# **Create occupancy percentage column**

# In[292]:


df_agg_bookings.head(3)


# In[293]:


df_agg_bookings['occ_pct'] = df_agg_bookings.apply(lambda row: row['successful_bookings']/row['capacity'], axis=1)


# You can use following approach to get rid of SettingWithCopyWarning

# In[294]:


new_col = df_agg_bookings.apply(lambda row: row['successful_bookings']/row['capacity'], axis=1)
df_agg_bookings = df_agg_bookings.assign(occ_pct=new_col.values)
df_agg_bookings.head(3)


# Convert it to a percentage value

# In[295]:


df_agg_bookings['occ_pct'] = df_agg_bookings['occ_pct'].apply(lambda x: round(x*100, 2))
df_agg_bookings.head(3)


# In[299]:


df_bookings.head()


# In[297]:


df_agg_bookings.info()


# There are various types of data transformations that you may have to perform based on the need. Few examples of data transformations are,
# 
# 1. Creating new columns
# 1. Normalization
# 1. Merging data
# 1. Aggregation

# ***
# ### ==> 4. Insights Generation
# ***

# **1. What is an average occupancy rate in each of the room categories?**

# In[300]:


df_agg_bookings.head(3)


# In[301]:


df_agg_bookings.groupby("room_category")["occ_pct"].mean()


# I don't understand RT1, RT2 etc. Print room categories such as Standard, Premium, Elite etc along with average occupancy percentage

# In[304]:


df = pd.merge(df_agg_bookings, df_rooms, left_on="room_category", right_on="room_id")
df.head(4)


# In[306]:


df.drop("room_id",axis=1, inplace=True)
df.head(4)


# In[308]:


df.groupby("room_class")["occ_pct"].mean()


# In[309]:


df[df.room_class=="Standard"].occ_pct.mean()


# **2. Print average occupancy rate per city**

# In[310]:


df_hotels.head(3)


# In[311]:


df = pd.merge(df, df_hotels, on="property_id")
df.head(3)


# In[312]:


df.groupby("city")["occ_pct"].mean()


# **3. When was the occupancy better? Weekday or Weekend?**

# In[314]:


df_date.head(3)


# In[316]:


df = pd.merge(df, df_date, left_on="check_in_date", right_on="date")
df.head(3)


# In[321]:


df.groupby("day_type")["occ_pct"].mean().round(2)


# **4: In the month of June, what is the occupancy for different cities**

# In[323]:


df_june_22 = df[df["mmm yy"]=="Jun 22"]
df_june_22.head(4)


# In[324]:


df_june_22.groupby('city')['occ_pct'].mean().round(2).sort_values(ascending=False)


# In[327]:


df_june_22.groupby('city')['occ_pct'].mean().round(2).sort_values(ascending=False).plot(kind="bar")


# **5: We got new data for the month of august. Append that to existing data**

# In[329]:


df_august = pd.read_csv("datasets/new_data_august.csv")
df_august.head(3)


# In[334]:


df_august.columns


# In[332]:


df.columns


# In[337]:


df_august.shape


# In[338]:


df.shape


# In[336]:


latest_df = pd.concat([df, df_august], ignore_index = True, axis = 0)
latest_df.tail(10)


# In[339]:


latest_df.shape


# Check this post for codebasics resume project challange winner entry: https://www.linkedin.com/posts/ashishbabaria_codebasicsresumeprojectchallenge-data-powerbi-activity-6977940034414886914-dmoJ?utm_source=share&utm_medium=member_desktop

# **6. Print revenue realized per city**

# In[341]:


df_bookings.head()


# In[345]:


df_hotels.head(3)


# In[360]:


df_bookings_all = pd.merge(df_bookings, df_hotels, on="property_id")
df_bookings_all.head(3)


# In[361]:


df_bookings_all.groupby("city")["revenue_realized"].sum()


# **7. Print month by month revenue**

# In[356]:


df_date.head(3)


# In[357]:


df_date["mmm yy"].unique()


# In[363]:


df_bookings_all.head(3)


# In[364]:


df_date.info()


# In[365]:


df_date["date"] = pd.to_datetime(df_date["date"])
df_date.head(3)


# In[366]:


df_bookings_all.info()


# In[367]:


df_bookings_all["check_in_date"] = pd.to_datetime(df_bookings_all["check_in_date"])
df_bookings_all.head(4)


# In[368]:


df_bookings_all = pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date")
df_bookings_all.head(3)


# In[375]:


df_bookings_all.groupby("mmm yy")["revenue_realized"].sum()

