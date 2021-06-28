#scrapes all 100 pages of btc rich list, lists url of top 10,000 richest BTC holders
#https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html

import requests
import lxml.html as lh
import pandas as pd
from datetime import date

def url_to_df(url):
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)

    #Store the contents of the website under doc    
    doc = lh.fromstring(page.content)

    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')

    #Check the length of the first 12 rows
    [len(T) for T in tr_elements[:12]]
    tr_elements = doc.xpath('//tr')

    #Create empty list
    col=[]
    i=0

    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
        #If row is not of size 10, the //tr data is not from our table 
        if len(T)!=10:
            break
        
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1

    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    return df

def clean_df(df):
    raw_list = df.values.tolist()
    clean_list = []

    # 0 rank
    # 1 address
    # 2 balance
    for line in raw_list:
        #initialize
        rank_raw = line[0]
        address_raw = line[1]
        balance_raw = line[2]

        #rank processing
        rank_clean = int(rank_raw)

        #address processing
        address_dot = address_raw.replace("..", "")
        address_clean = address_dot
        if("wallet" in address_dot):
            address_dot = address_dot.split("wallet")
            address_clean = address_dot[0]
        if("-of-" in address_dot):
            address_of = address_dot.split("-of-")
            address_of = address_of[0]
            address_clean = address_of[0:len(address_of)-2]

        #balance processing
        balance_split = balance_raw.split(" BTC")
        balance_clean = balance_split[0].replace(",", "")

        clean_line = [rank_clean, address_clean, balance_clean]
        clean_list.append(clean_line)
    
    return(clean_list)

baseurl = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-'
url1 = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses'
endurl = '.html'
url_list = []
i = 2

#generating list of urls to scrape
while i <= 100:
    url = baseurl + str(i) + endurl
    i = i + 1
    url_list.append(url)

#scraping url to df
counter = 2
df_list = []
df1 = url_to_df(url1)
df_list.append(df1)
print('scraping page 2-9')
for url in url_list:
    if(counter%10 == 0):
        print('scraping page ' + str(counter) + ' to ' + str(counter + 9))
    df = url_to_df(url)
    df_list.append(df)
    counter = counter + 1

print('converting raw dataframes')
#cleaning df, writing cleaned data to list
clean_df_list = []
for df in df_list:
    temp = clean_df(df)
    clean_df_list.append(temp)

print('writing cleaned data to file')
#writing cleaned data to file
today = date.today()
f = open("address_list_" + str(today) + ".txt", "w")

for clean_df in clean_df_list:
    for df in clean_df:
        f.write(str(df) + '\n')

f.close()