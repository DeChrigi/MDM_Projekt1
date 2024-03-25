import plotly.graph_objects as go
import plotly.io as pio
import DBHandler as dbh

def getCountByCategoryPlot():
    # Get Data from DBHandler
    df = dbh.getCountByCategoriesFilterByCountry('CH')
    # Format Data for Columnchart
    data = go.Bar(x=df["Category_Name"],
                  y=df["Count"])
    # Create figure
    fig = go.Figure(data=data)

    # Format the chart
    fig = updateBarLayout(fig)

    # Create insertion html
    plot_div = pio.to_html(fig, full_html=False)
    # return insertion html
    return plot_div

def getAvgByCategoriesPlot():
    # Get Data from DBHandler
    df = dbh.getAverageStatCountByCategoryFilterByCountry('CH')
    # Format Data for Columnchart
    data = go.Bar(x=df["Category_Name"],
                  y=df["Avg_Views"])
    # Create figure
    fig = go.Figure(data=data)

    # Format the chart
    fig = updateBarLayout(fig)

    # Create insertion html
    plot_div = pio.to_html(fig, full_html=False)
    # return insertion html
    return plot_div

def updateBarLayout(fig):
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(autosize=True
    )
    

    for trace in fig.data:
        trace.marker.color = '#3e4451'

    return fig