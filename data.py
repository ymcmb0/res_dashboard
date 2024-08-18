import pandas as pd
import random

# Generate random project names
project_names = [
    "HBL", "UBL", "Bank Al Habib", "MCB", "Meezan Bank", "Allied Bank", "JS Bank",
    "Soneri Bank", "Faysal Bank", "Askari Bank", "Standard Chartered", "NBP", "Bank Islami",
    "Dubai Islamic Bank", "Silk Bank", "Summit Bank", "Samba Bank", "HabibMetro", "CitiBank", "HSBC"
]

# Generate random dates
date_range = pd.date_range(start="2024-01-01", end="2024-12-31")
start_dates = random.sample(list(date_range), 20)
end_dates = [start_date + pd.Timedelta(days=random.randint(5, 20)) for start_date in start_dates]

# Generate random resources
resources = ["Ahmad", "Ali", "Ramzan", "Daud", "Sara", "Waqas", "Hamza", "Bilal",
             "Usman", "Ayesha", "Kamran", "Faraz", "Saad", "Zain", "Nida", "Farhan",
             "Nadia", "Imran", "Asad", "Hira", "Hassan", "Fatima", "Junaid", "Anum",
             "Yasir", "Mona", "Asim", "Shaista", "Shahbaz", "Huma", "Arif", "Rehan"]

# Assign resources randomly to projects
random_resources = [random.sample(resources, 4) for _ in range(20)]

# Create the DataFrame
df = pd.DataFrame({
    "Project Name": project_names,
    "Start Date": start_dates,
    "End Date": end_dates,
    "Resources": [', '.join(res) for res in random_resources]
})

# Adjust date format for Excel compatibility
df["Start Date"] = df["Start Date"].dt.strftime('%m/%d/%Y')
df["End Date"] = df["End Date"].dt.strftime('%m/%d/%Y')
df["Start Date"]=pd.to_datetime(df["Start Date"])
df["End Date"]=pd.to_datetime(df["End Date"])
df.to_csv("output.csv")