# Automating ACLs with Aerleon and Pandas
This repo contains the examples and scripts from the Packet Coders webinar:
> Automating ACLs with Aerleon and Pandas
## Setup
```
poetry install
```

## Repo Scripts

1. Import Excel worksheets to DataFrames.
```
python3 1_excel_to_pandas.py
```

2. Perform step 1 and convert to Aerleon def and policy formats.
```
python3 2_pandas_to_aerleon.py
```

3. Perform steps 1 and 2, plus render into firewall policy configs.
```
python3 3_aerleon_render.py
```


