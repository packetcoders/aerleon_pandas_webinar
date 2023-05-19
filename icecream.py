import pandas as pd
from rich import print as rprint
# Read the excel file

df_flows = pd.read_excel('firewall_flows.xlsx', sheet_name="flows")
df_networks = pd.read_excel('firewall_flows.xlsx', sheet_name="networks")
df_services = pd.read_excel('firewall_flows.xlsx', sheet_name="services")

##

firewalls = df_flows['firewall'].drop_duplicates().unique().tolist()

all_fw_filters = []

# firewall > filters > terms

for fw in firewalls:
    fw_filter_dict = {"filters": [],
                     "filename": fw}

    df_fw_filter_names = df_flows.query("firewall == @fw")["policy_name"].drop_duplicates().tolist()
    platform = df_flows.query("firewall == @fw").platform.to_list()[0]
    fw_filters = []
    for filter in df_fw_filter_names:
        df_fw_filters = df_flows.query("firewall == @fw & policy_name == @filter")

        filter_dict = {
            "header": {
                "targets": {
                    platform: filter
                }
            },
            "terms": []
        }

        for _, row in df_fw_filters.iterrows():
            filter_dict["terms"].append({
                "name": row['policy_name'],
                "source-address": row['src_ip'],
                "destination-address": row['dst_ip'],
                "destination-port": str(row['dst_port']),
                "protocol": row['proto'],
                "action": "accept"  # You can modify this based on your requirements
            })

        fw_filter_dict["filters"].append(filter_dict)

    #fw_filter_dict["filters"].append(filter_dict)
    all_fw_filters.append(fw_filter_dict)

rprint(all_fw_filters)

#########################################

networks = {"networks": {}}

for net in df_networks.itertuples():
    print(net)
    networks["networks"][net.network] = {"values": [{"address": net.address}]}


#########################################

services = {"services": {}}

for svc in df_services.itertuples():
    services["services"][svc.service] = [{"protocol": svc.protocol, "port": svc.port}]


#########################################



#########################################


print(networks)
print(services)

import re  # no qa

# Import the naming module and the api module from the aerleon library.
from aerleon.lib import naming  # isort:skip
from aerleon import api  # isort:skip

# Create an instance of the Naming class
definitions = naming.Naming()

# Use the ParseDefinitionsObject method to parse the "networks" object
definitions.ParseDefinitionsObject(networks, "networks")

# Use the ParseDefinitionsObject method to parse the "services" object
definitions.ParseDefinitionsObject(services, "services")

# Use the Generate method from the api module to generate configurations
# from the "cisco_asa_policy" object, passing in the definitions object
# as an argument
configs = api.Generate([all_fw_filters[0]], definitions=definitions)

# Render the the ASA configuration from the configs object
acl = configs["cisco_asa_policy.asa"]

# Remove additional blank lines from rendered ACLs
#acl = re.sub("\n\n\n", "\n", acl)

#if __name__ == "__main__":
    # Print the ACL
print(acl)  # no qa