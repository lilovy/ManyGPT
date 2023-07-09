import plotly.express as px
import plotly.io as pio
import io


def bar_chart(data: dict):
    fig = px.bar(x=list(data.keys()), y=list(data.values()), labels=dict(x="Plan", y="Users", color="Total users"))
    buffer = io.BytesIO()
    pio.write_image(fig, buffer, format="png")
    return buffer.getvalue()
