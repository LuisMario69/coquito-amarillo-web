import pandas as pd
import plotly.express as px
import plotly.io as pio

def generar_rueda_vida(datos):
    """
    Genera una visualización de la Rueda de la Vida
    
    :param datos: DataFrame con categorías y valores
    :return: Gráfico HTML de la Rueda de la Vida
    """
    fig = px.line_polar(
        datos, 
        r='valor', 
        theta='categoria', 
        line_close=True,
        title='Rueda de la Vida',
        range_r=[0, 10]
    )
    
    fig.update_traces(fill='toself')
    
    return pio.to_html(fig, full_html=False)