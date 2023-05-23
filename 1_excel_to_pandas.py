import pandas as pd
from rich import print as rprint

# Read the excel file/worksheets into pandas DataFrames
df_flows = pd.read_excel("firewall_flows.xlsx", sheet_name="flows")
df_networks = pd.read_excel("firewall_flows.xlsx", sheet_name="networks")
df_services = pd.read_excel("firewall_flows.xlsx", sheet_name="services")

# Print the DataFrames
rprint(df_flows)
rprint(df_networks)
rprint(df_services)
