import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown
import ipywidgets as widgets

df = pd.read_csv(r"C:\Users\ASUS\My_Learning\IEEE hackathon\insights.csv")

expected_cols = ['stars', 'forks', 'open_issues', 'total_loc', 
                 'avg_cyclomatic_complexity', 'max_cyclomatic_complexity', 
                 'total_contributors', 'top_contributor', 'top_contributions', 
                 'risk_score', 'risk_level']

for col in expected_cols:
    if col not in df.columns:
        if col == 'top_contributor':
            df[col] = 'N/A'
        elif col == 'top_contributions':
            df[col] = 0
        elif col == 'risk_level':
            df[col] = 'Medium'
        else:
            df[col] = 0

repo_dropdown = widgets.Dropdown(
    options=df['name'].tolist(),
    description='Select Repo:',
    layout=widgets.Layout(width='400px')
)

def display_repo_insights(repo_name):
    repo = df[df['name'] == repo_name].iloc[0]
    
    display(Markdown(f"##  Insights for Repository: *{repo_name}*"))
    
    display(Markdown(f"- *Stars:* {repo['stars']} → popularity"))
    display(Markdown(f"- *Forks:* {repo['forks']} → contribution potential"))
    display(Markdown(f"- *Open Issues:* {repo['open_issues']} → pending work"))
    display(Markdown(f"- *Total LOC:* {repo['total_loc']} → codebase size"))
    display(Markdown(f"- *Avg Cyclomatic Complexity:* {repo['avg_cyclomatic_complexity']} → maintainability"))
    display(Markdown(f"- *Max Cyclomatic Complexity:* {repo['max_cyclomatic_complexity']} → risky functions"))
    display(Markdown(f"- *Total Contributors:* {repo['total_contributors']} → collaboration level"))
    
    top_contrib = repo['top_contributor'] if repo['top_contributor'] != 'N/A' else "No data"
    top_commits = repo['top_contributions'] if repo['top_contributions'] != 0 else 0
    display(Markdown(f"- *Top Contributor:* {top_contrib} ({top_commits} commits) → reliance on a single contributor"))
    
    risk = repo['risk_level']
    if risk == "High":
        risk_text = " High risk: may require refactoring or attention"
    elif risk == "Medium":
        risk_text = " Medium risk: monitor regularly"
    else:
        risk_text = " Low risk: well-maintained"
    
    display(Markdown(f"- *Risk Level:* {risk} → {risk_text}"))

    plt.figure(figsize=(8,5))
    
    contrib_col = 'contributors' if 'contributors' in df.columns else 'total_contributors'
    
    sns.scatterplot(
        data=df,
        x=contrib_col,
        y='stars',
        size='forks',
        hue='risk_level',
        palette='Set1',
        legend='full',
        sizes=(50, 300)
    )
    plt.title("Stars vs Contributors (size=forks, color=risk)")
    plt.xlabel("Contributors")
    plt.ylabel("Stars")
    plt.legend(loc='upper left')
    plt.show()

out = widgets.Output()

def on_repo_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        out.clear_output()
        with out:
            display_repo_insights(change['new'])

repo_dropdown.observe(on_repo_change)
display(repo_dropdown, out)
