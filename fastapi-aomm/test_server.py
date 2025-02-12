#import requests

#print(requests.get("http://localhost:8000/").json())

#print(requests.get("http://localhost:8000/capabilities/1").json())

#print(requests.get("http://localhost:8000/tasks/5").json())

import pandas as pd

df = pd.DataFrame({
  "Value Stream Id": ["6.1", "6.2", "6.3", "6.1", "6.2", "6.3"],
  "comparison": ["user", "user", "user", "average", "average", "average"],
  "Score": [2, 1, 3, 1.4, 3.1, 2.5],
})


# Plotly Express

import plotly.express as px

fig = px.bar(df, x="Value Stream Id", y="Score", color="comparison", barmode="group")

# Increase the height of the graph
fig.update_layout(height=300, width=400)
fig.update_layout(yaxis_range=[0,5.0])
fig.show()
