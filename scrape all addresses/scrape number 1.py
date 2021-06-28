import os

os.chdir(os.getcwd()+"\scrape all addresses")

#save table as csv, 1-19, 20-100 for some reason has to be done separately
f = open("page1.txt", "r")
lines = f.readlines()
f.close()

page1_list = []
for line in lines:
    line = line.split('Balance:')

    rank_address = line[0]
    rank_address = rank_address.split(',"')
    rank_clean = rank_address[0]
    rank_clean = int(rank_clean)

    address_raw = rank_address[1]
    address_dot = address_raw.replace("..", "")
    address_clean = address_dot
    if("wallet" in address_dot):
        address_dot = address_dot.split("wallet")
        address_clean = address_dot[0]
    if("-of-" in address_clean):
        address_of = address_clean.split("-of-")
        address_of = address_of[0]
        address_clean = address_of[0:len(address_of)-2]

    balance_raw = line[1]
    balance_comma = balance_raw.split(" BTC")
    balance_comma = balance_comma[0]
    balance_clean = balance_comma.replace(",", "")

    page1_list.append([rank_clean, address_clean, balance_clean])

f = open('address_list_page1.txt', 'w')
for item in page1_list:
    f.write(str(item) + '\n')
f.close()
