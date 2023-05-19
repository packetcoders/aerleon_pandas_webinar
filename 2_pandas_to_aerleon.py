import pandas as pd

# Read the excel file
df = pd.read_excel('firewall_flows.xlsx')

firewalls = df['firewall'].drop_duplicates().unique().tolist()

for fw in firewalls:
   filter_names = df.query("firewall == @fw")["policy_name"].drop_duplicates().unique().tolist()
   for filter in filter_names:
        filter_input = df.query("firewall == @fw & policy_name == @filter")
        

