import pandas as pd
from rich import print as rprint

#
# 1. Excel to Pandas
#

# Read the excel file/worksheets into pandas DataFrames
df_flows = pd.read_excel("firewall_flows.xlsx", sheet_name="flows")
df_networks = pd.read_excel("firewall_flows.xlsx", sheet_name="networks")
df_services = pd.read_excel("firewall_flows.xlsx", sheet_name="services")

#
# 2. Pandas to Aerleon
#


# Functions for working with DataFrame data
def get_firewalls(df):
    """Get list of firewalls"""
    return df["firewall"].drop_duplicates().unique().tolist()


def get_platform(df, fw):
    """Get platform for a firewall"""
    return df.query("firewall == @fw").platform.to_list()[0]


def get_filter_names(df, fw):
    """Get list of policy names for a firewall"""
    return df.query("firewall == @fw")["filter_name"].drop_duplicates().tolist()


def get_filter_terms(df, fw, filter):
    """Get filters for a firewall"""

    return df.query("firewall == @fw & filter_name == @filter")


def build_term(row):
    """Build term for a filter"""
    return {
        "name": row.description.lower().replace(" ", "-"),
        "source-address": row.src_ip,
        "destination-address": row.dst_ip,
        "destination-port": str(row.dst_port),
        "protocol": row.proto,
        "action": "accept",
    }


def build_aerlon_policy(df_flows):
    """
    Build Aerlon policy from firewall flows.
    Structure of Aerlon policy:
    [
     {
       "filename": "fw1-asa",
       "filters": [
         {
           "header": { "targets": { "ciscoasa": "acl-outside" }},
           "terms": [
             {
               "name": "client-to-web",
               "source-address": "ALL",
               "destination-address": "ALL",
               "destination-port": "HTTPS",
               "protocol": "tcp",
               "action": "accept"
             }
           ]
         },
         // More filters...
       ]
     },
     // More firewalls...
    ]
    """

    firewalls = get_firewalls(df_flows)

    fw_all_policy = []

    # Loop through firewalls
    for fw in firewalls:
        # Create a dictionary for each firewall
        fw_filters = {"filters": [], "filename": fw}

        # Get platform for a firewall
        platform = get_platform(df_flows, fw)

        # Get list of filter names for a firewall
        filter_names = get_filter_names(df_flows, fw)

        # Loop through filter names for firewall
        for filter_name in filter_names:
            # Create a dictionary for each filter
            filter_dict = {
                "header": {"targets": {platform: filter_name}},
                "terms": [],
            }

            # Get filter terms
            filter_terms = get_filter_terms(
                df_flows, fw, filter_name
            )  # Replaced filter with filter_name

            # Loop through and build filter terms
            for row in filter_terms.itertuples():
                # Build term for a filter
                filter_dict["terms"].append(
                    build_term(row)
                )
            # Add filter to firewall
            fw_filters["filters"].append(
                filter_dict
            )  

        # Add firewall to list of firewalls
        fw_all_policy.append(fw_filters)

    # Return policy containing all filters for all firewalls
    return fw_all_policy


def build_aerlon_def_network(df_networks):
    """Build Aerlon network definition from firewall networks."""
    networks = {"networks": {}}

    for net in df_networks.itertuples():
        networks["networks"][net.network] = {"values": [{"address": net.address}]}

    return networks


def build_aerlon_def_service(df_services):
    """Build Aerlon service definition from firewall services."""
    services = {"services": {}}

    for svc in df_services.itertuples():
        services["services"][svc.service] = [
            {"protocol": svc.protocol, "port": svc.port}
        ]

    return services


if __name__ == "__main__":
    # Build Aerlon policy
    aerlon_policy = build_aerlon_policy(df_flows)
    aerlon_def_network = build_aerlon_def_network(df_networks)
    aerlon_def_service = build_aerlon_def_service(df_services)

    # Print Aerlon policy
    rprint(aerlon_policy)
    rprint(aerlon_def_network)
    rprint(aerlon_def_service)
