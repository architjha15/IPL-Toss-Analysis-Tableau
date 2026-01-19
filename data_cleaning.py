import pandas as pd

df = pd.read_csv("./data/ipl.csv")

correct_team_name = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}

correct_cols = ["team1", "team2", "toss_winner", "winner"]

for col in correct_cols:
    df[col] = df[col].replace(correct_team_name)

df.loc[df["venue"] == "Sharjah Cricket Stadium", "city"] = "Sharjah"
df.loc[df["venue"] == "Dubai International Cricket Stadium", "city"] = "Dubai"

df1 = df.copy()
df1["Team"] = df["team1"]
df1["Opponent"] = df["team2"]

df2 = df.copy()
df2["Team"] = df["team2"]
df2["Opponent"] = df["team1"]

final_df = pd.concat([df1, df2], ignore_index=True)

final_df["is_winner"] = (final_df["Team"]==final_df["winner"]).astype(int)
final_df["is_toss_winner"] = (final_df["Team"]==final_df["toss_winner"]).astype(int)

final_df["team_role"] = "Chasing"

final_df.loc[
    (final_df["is_toss_winner"] == 1) &
    (final_df["toss_decision"] == "bat"),
    "team_role"
] = "Defending"

final_df.loc[
    (final_df["is_toss_winner"] == 0) &
    (final_df["toss_decision"] == "field"),
    "team_role"
] = "Defending"




final_df["season"] = pd.to_datetime(final_df["match_date"]).dt.year

final_df["toss_advantage"] = (
    (final_df["is_toss_winner"] == 1) &
    (final_df["is_winner"] == 1)
).astype(int)

final_df["high_pressure_match"] = (
    (final_df["result_margin"].fillna(999) < 20) &
    (final_df["is_winner"] == 1)
        
).astype(int)

final_df.to_csv("./data/ipl_cleaned_data.csv", index=False)

print("Data cleaned and successfully exported.")