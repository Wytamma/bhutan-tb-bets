import pandas as pd
import glob
import re
from pathlib import Path
import matplotlib.pyplot as plt
import argparse
import seaborn as sns

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)


parser = argparse.ArgumentParser(description="Process the output from a BETS analysis.")
parser.add_argument(
    "directory", type=Path, help="The output directory of the BETS analysis."
)

args = parser.parse_args()

directory = args.directory

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)


title = Path(directory).stem
ouput_path_plus_wildcards = str(directory) + '/*/*.out'
paths = [Path(path) for path in glob.glob(ouput_path_plus_wildcards)]
data = []
for path in paths:
    with open(path) as f:
        lines = f.readlines()
    lines = [l for l in lines if l.startswith('Marginal likelihood:')]
    line = lines[-1]
    ML = line.split(' ')[2]
    match = re.search(r'SD=\((.*?)\)', line).group(0)
    SD = match[4:-1]
    data.append({'Name':path.stem, 'ML': float(ML), 'SD':float(SD)})

df = pd.DataFrame(data).sort_values('Name')

df['Group'] = df['Name']
fig, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle(f'BETS for {title}')


# ax2 = sns.pointplot(
#     errorbar="sd",
#     ax=ax2,
#     data=df,
#     x="Group", 
#     y="ML", 
#     palette="dark"
# )

ax2.errorbar(
    data = df,
    x="Name", 
    y='ML', 
    yerr=df.SD,
    fmt='o', 
    ecolor='lightgray', 
    color='black'
)

df['logBF'] = df['ML'] - df['ML'].max()    
gdf = df.groupby('Group')[['ML', 'SD']].mean().reset_index()
gdf['logBF'] = gdf['ML'] - gdf['ML'].max()    
df = pd.merge(df, gdf[['Group', 'ML', 'logBF']], on='Group', how='inner', suffixes=('', '_group'))

ax3 = sns.barplot(
    ax=ax3,
    data=df,
    x="Group", y="logBF"
)
ax3.invert_yaxis()
plt.savefig(f'{directory}/BETS.png', bbox_inches='tight')
plt.savefig(f"{directory}/BETS.svg", bbox_inches="tight")
df.to_csv(f'{directory}/BETS.csv')

fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle(f'Individual for {title}')
ax1.errorbar(
    data = df,
    y='Name', 
    x='ML', 
    xerr='SD', 
    fmt='o', 
    ecolor='lightgray', 
    color='black'
)
ax2 = sns.barplot(
    ax=ax2,
    data=df,
    x="Group", y="SD",
)
plt.savefig(f'{directory}/BETS-individual.png', bbox_inches='tight')