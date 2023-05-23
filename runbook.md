1. Working with Pandas
```
df = pd.read_excel("firewall_flows.xlsx", sheet_name="flows")

print(df)

df.iloc[0]

df["firewall"]
df["firewall"].tolist()

df.query("firewall == 'fw1-asa'")
df.query("firewall == 'fw1-asa' & proto == 'tcp'")

for row in df.itertuples():
    print(row.platform)
```

2. Excel to ACL
```
TBC
```
