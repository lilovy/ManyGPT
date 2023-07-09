import plotly.express as px
import plotly.io as pio
import io


def bar_chart(data: dict):
    fig = px.bar(x=list(data.keys()), y=list(data.values()))
    buffer = io.BytesIO()
    pio.write_image(fig, buffer, format="png")
    return buffer.getvalue()

print(bar_chart({"free": 3, "basic": 34, "advanced": 1}))