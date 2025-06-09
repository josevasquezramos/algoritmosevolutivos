import pandas as pd
import plotly.express as px
from ipywidgets import interact, Checkbox

# Cargar datos
df = pd.read_csv('notas_1u.csv')
df.head()

# Estadísticas generales (no interactivas)
print("Estadísticas generales:")
general = df.describe()
display(general)

print("\nEstadísticas por tipo de examen:")
estadisticas = df.groupby('Tipo_Examen')['Nota'].describe()
display(estadisticas)

# Configuración
COLORES = {'A': '#1f77b4', 'B': '#ff7f0e', 'C': '#2ca02c'}
tipos_disponibles = sorted(df['Tipo_Examen'].unique().tolist())

# Gráficos estáticos para el general
print("\nDistribución general de notas:")
fig_general_hist = px.histogram(df, x='Nota', nbins=20, title='Distribución General de Notas')
fig_general_hist.update_layout(showlegend=False)
fig_general_hist.show()

print("\nDistribución por tipo de examen (general):")
fig_general_box = px.box(df, x='Tipo_Examen', y='Nota', color='Tipo_Examen', 
                         color_discrete_map=COLORES, title='Distribución por Tipo de Examen')
fig_general_box.show()

# Gráficos interactivos
# Crear controles
controles = {}
if 'A' in tipos_disponibles:
    controles['mostrar_A'] = Checkbox(value=True, description='Tipo A')
if 'B' in tipos_disponibles:
    controles['mostrar_B'] = Checkbox(value=True, description='Tipo B')
if 'C' in tipos_disponibles:
    controles['mostrar_C'] = Checkbox(value=True, description='Tipo C')

@interact(**controles)
def actualizar_graficos(mostrar_A=True, mostrar_B=True, mostrar_C=True):
    tipos_activos = []
    if 'A' in tipos_disponibles and mostrar_A:
        tipos_activos.append('A')
    if 'B' in tipos_disponibles and mostrar_B:
        tipos_activos.append('B')
    if 'C' in tipos_disponibles and mostrar_C:
        tipos_activos.append('C')
    
    if not tipos_activos:
        print("Selecciona al menos un tipo de examen")
        return
    
    # Filtrar datos
    df_filtrado = df[df['Tipo_Examen'].isin(tipos_activos)]
    
    # Histograma interactivo
    fig_hist = px.histogram(
        df_filtrado, 
        x='Nota', 
        color='Tipo_Examen',
        nbins=20,
        barmode='overlay',
        opacity=0.7,
        color_discrete_map=COLORES,
        title='Distribución de Notas por Tipo de Examen'
    )
    fig_hist.update_layout(bargap=0.1)
    fig_hist.show()
    
    # Gráfico de densidad
    fig_densidad = px.histogram(
        df_filtrado,
        x='Nota',
        color='Tipo_Examen',
        marginal='rug',
        hover_data=df_filtrado.columns,
        color_discrete_map=COLORES,
        title='Distribución de Densidad'
    )
    fig_densidad.update_traces(opacity=0.7)
    fig_densidad.show()
    
    # Boxplot interactivo
    fig_box = px.box(
        df_filtrado,
        x='Tipo_Examen',
        y='Nota',
        color='Tipo_Examen',
        color_discrete_map=COLORES,
        title='Distribución Detallada por Tipo'
    )
    fig_box.show()