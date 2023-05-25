1. Working with Pandas
```
from rich import print as rprint
import pandas as pd
df = pd.read_excel("firewall_flows.xlsx", sheet_name="flows")

rprint(df)

df.to_html()
print(df.to_html())

df.to_markdown()
print(df.to_markdown())

df.iloc[0]

df["firewall"]
df["firewall"].tolist()

df.query("firewall == 'fw1-asa'")
df.query("firewall == 'fw1-asa' & proto == 'tcp'")

df.query("firewall == 'fw1-asa' & proto == 'tcp'").size()

for row in df.itertuples():
    print(row.platform)
```

2. Excel to ACL
```

```