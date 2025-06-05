import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from datetime import timedelta
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import time
import requests
from yfinance import download

# Configuración de la página
st.set_page_config(page_title="Análisis Financiero", layout="wide")

# -------- Sidebar --------
with st.sidebar:
    st.title("📊 Panel de Análisis")
    st.markdown("""
    <div style="background-color: #F4F6F7; padding: 20px; border-radius: 10px; font-size: 16px; color: #333; margin-top: 25px; line-height: 1.6;">
        Bienvenido al sistema de análisis financiero.<br>
        Ingrese un <b>ticker</b> perteneciente al índice <b>S&P 500</b> para comenzar el análisis.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    ticker_input = st.text_input("🔍 Ticker del S&P 500:", value="")

# -------- Encabezado principal --------
st.markdown("""
    <h1 style='text-align: center; color: #FFFFFF; font-family: Arial, sans-serif;'>
        Análisis Financiero Bursátil
    </h1>
    <p style='text-align: center; font-size: 20 px; color: #FFFFFF;'>
        Consulta profesional de información bursátil y datos históricos de mercado.
    </p>
""", unsafe_allow_html=True)

st.divider()

# -------- Funciones --------

def validar_ticker(ticker):
    try:
        data = download(ticker, period="1wk", progress=False)
        return not data.empty
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("🔴 Demasiadas solicitudes. Espera unos segundos.")
            time.sleep(10)  # Espera 10 segundos
            return validar_ticker(ticker)  # Reintentar
        return False
    except Exception:
        return False


def obtener_info_empresa(ticker):
    info = yf.Ticker(ticker).info
    nombre = info.get("longName", "Nombre no disponible")
    sector = info.get("sector", "Sector no disponible")
    descripcion = info.get("longBusinessSummary", "Descripción no disponible")
    return nombre, sector, descripcion

def calcular_cagr_1y(data):
    if data.empty or "Close" not in data.columns:
        return None
    fecha_final = data.index[-1]
    fecha_inicial = fecha_final - timedelta(days=365)
    data_filtrada = data[data.index >= fecha_inicial]
    if len(data_filtrada) < 2:
        return None

    precio_inicio = data_filtrada["Close"].iloc[0]
    precio_fin = data_filtrada["Close"].iloc[-1]

    if isinstance(precio_inicio, pd.Series):
        precio_inicio = precio_inicio.item()
    if isinstance(precio_fin, pd.Series):
        precio_fin = precio_fin.item()

    if pd.isna(precio_inicio) or pd.isna(precio_fin):
        return None

    cagr = (precio_fin / precio_inicio) ** (1 / 1) - 1
    return round(cagr * 100, 2)

def calcular_cagr_3y(data):
    if data.empty or "Close" not in data.columns:
        return None
    fecha_final = data.index[-1]
    fecha_inicial = fecha_final - timedelta(days=1095)
    data_filtrada = data[data.index >= fecha_inicial]
    if len(data_filtrada) < 2:
        return None

    precio_inicio = data_filtrada["Close"].iloc[0]
    precio_fin = data_filtrada["Close"].iloc[-1]

    if isinstance(precio_inicio, pd.Series):
        precio_inicio = precio_inicio.item()
    if isinstance(precio_fin, pd.Series):
        precio_fin = precio_fin.item()

    if pd.isna(precio_inicio) or pd.isna(precio_fin):
        return None

    cagr = (precio_fin / precio_inicio) ** (1 / 1) - 1
    return round(cagr * 100, 2)

def calcular_cagr_5y(data):
    if data.empty or "Close" not in data.columns:
        return None
    fecha_final = data.index[-1]
    fecha_inicial = fecha_final - timedelta(days=1825)
    data_filtrada = data[data.index >= fecha_inicial]
    if len(data_filtrada) < 2:
        return None

    precio_inicio = data_filtrada["Close"].iloc[0]
    precio_fin = data_filtrada["Close"].iloc[-1]

    if isinstance(precio_inicio, pd.Series):
        precio_inicio = precio_inicio.item()
    if isinstance(precio_fin, pd.Series):
        precio_fin = precio_fin.item()

    if pd.isna(precio_inicio) or pd.isna(precio_fin):
        return None

    cagr = (precio_fin / precio_inicio) ** (1 / 1) - 1
    return round(cagr * 100, 2)


# -------- Lógica principal --------
if ticker_input:
    ticker_input = ticker_input.upper()
    if validar_ticker(ticker_input):
        st.success(f"✅ Información encontrada para: **{ticker_input}**")
        
        st.divider()

        nombre, sector, descripcion = obtener_info_empresa(ticker_input)

        st.markdown(f"""
            <h2 style='text-align: center; color: #FFFFFF; font-family: Georgia, serif;'>Nombre: {nombre}</h2>
            <h3 style='text-align: center; color: #FFFFFF; font-family: Georgia, serif;'>🏭 Sector: {sector}</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style='background-color: #F4F6F7; padding: 25px; border-radius: 8px; margin: 30px auto; width: 85%;'>
                <p style='font-size: 16px; text-align: justify; color: #333; font-family: Georgia, serif; line-height: 1.6;'>
                    {descripcion}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
        st.divider()
        
            # Obtener precio actual y datos OHLC (últimos 2 días)
    data_actual = yf.download(ticker_input, period="2d", interval="1d")

    if not data_actual.empty and "Close" in data_actual.columns:
        # Usar valores individuales
        precio_actual = float(data_actual["Close"].iloc[-1])
        precio_anterior = float(data_actual["Close"].iloc[-2]) if len(data_actual) > 1 else precio_actual


        cambio_pct = float(((precio_actual - precio_anterior) / precio_anterior) * 100)

        color = "2ECC71" if cambio_pct >= 0 else "E74C3C"
        flecha = "🔼" if cambio_pct >= 0 else "🔽"

        open_ = float(data_actual["Open"].iloc[-1])
        high_ = float(data_actual["High"].iloc[-1])
        low_ = float(data_actual["Low"].iloc[-1])
        close_ = float(data_actual["Close"].iloc[-1])

        fecha = data_actual.index[-1].strftime('%Y-%m-%d')

        # Mostrar datos en formato bonito
        st.markdown(f"""
        <div style="background-color:#F8F9F9; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
            <h3 style="color:#333333;">📈 Precio actual de <span style="color:#0072B2;">{ticker_input}</span>:</h3>
            <div style="font-size: 26px; font-weight: bold; color: #{color};">
                {precio_actual:.2f} USD &nbsp; {flecha} {cambio_pct:.2f}%
            </div>
            <br>
            <div style="font-size: 16px; color: #555555;">
                <strong>OHLC (último cierre - {fecha}):</strong><br>
                🟢 <strong>Apertura:</strong> {open_:.2f} &nbsp;&nbsp; 🔺 <strong>Máximo:</strong> {high_:.2f} &nbsp;&nbsp;
                🔻 <strong>Mínimo:</strong> {low_:.2f} &nbsp;&nbsp; ⚪ <strong>Cierre:</strong> {close_:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)


        st.divider()
     

                # Selector de timeframe para grafica de precios
        st.subheader(f"📅 Selecciona el periodo de tiempo para: {ticker_input}")
        timeframes = {
            "1 Día": "1d",
            "5 Días": "5d",
            "1 Mes": "1mo",
            "3 Meses": "3mo",
            "6 Meses": "6mo",
            "1 Año": "1y",
            "2 Años": "2y",
            "5 Años": "5y",
            "Máximo disponible": "max"
        }
        periodo = st.selectbox("Periodo:", list(timeframes.keys()), index=7)  # default "5 Años"
        periodo_seleccionado = timeframes[periodo]

        # Mostrar gráfica si hay ticker
        if ticker_input:
            data = yf.Ticker(ticker_input).history(period=periodo_seleccionado, interval="1d", auto_adjust=True)

            if data.empty or "Close" not in data.columns:
                st.warning("⚠️ No se encontraron datos válidos para este ticker.")
            else:
                data.index = data.index.tz_localize(None)

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data["Close"],
                    mode="lines",
                    name="Precio de cierre",
                    line=dict(color="green", width=2)
                ))

                fig.update_layout(
                    title=f"Historial de Precio de Cierre: {ticker_input} ({periodo})",
                    xaxis_title="Fecha",
                    yaxis_title="Precio (USD)",
                    template="plotly_white",
                    height=500
                )

                st.plotly_chart(fig, use_container_width=True)

        
        st.divider()

        # -------- Rendimiento anualizado (CAGR) --------
        st.subheader("📈 Cálculo de Rendimientos Anualizados")

        precios_1y = yf.download(ticker_input, period="1y")
        rendimiento_anual = calcular_cagr_1y(precios_1y)
 
        if rendimiento_anual is not None:
            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Rendimiento anualizado (1 año) para {ticker_input}:</strong> 
                <span style="color: {'green' if rendimiento_anual >= 0 else 'red'};">
                    {'🔼' if rendimiento_anual >= 0 else '🔽'} {rendimiento_anual:.2f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

        precios_3y = yf.download(ticker_input, period="3y")
        rendimiento_anual = calcular_cagr_3y(precios_3y)
 
        if rendimiento_anual is not None:
            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Rendimiento anualizado (3 años) para {ticker_input}:</strong> 
                <span style="color: {'green' if rendimiento_anual >= 0 else 'red'};">
                    {'🔼' if rendimiento_anual >= 0 else '🔽'} {rendimiento_anual:.2f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

        precios_5y = yf.download(ticker_input, period="5y")
        rendimiento_anual = calcular_cagr_5y(precios_5y)
 
        if rendimiento_anual is not None:
            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Rendimiento anualizado (5 años) para {ticker_input}:</strong> 
                <span style="color: {'green' if rendimiento_anual >= 0 else 'red'};">
                    {'🔼' if rendimiento_anual >= 0 else '🔽'} {rendimiento_anual:.2f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: #F0F3F4; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> El rendimiento anualizado se calculó usando la fórmula del <em>Compound Annual Growth Rate (CAGR)</em>, 
                que representa el crecimiento promedio anual considerando interés compuesto.
            </div>
            """, unsafe_allow_html=True)

            st.divider()
        else:
            st.warning("No se pudo calcular el rendimiento anual. Puede que no haya suficientes datos disponibles.")
                     
        
         # -------- Gráfico comparativo de rendimientos (estético) --------
        st.subheader("📊 Comparación visual de rendimientos anualizados")

        # Crear listas de datos
        periodos = ["1 año", "3 años", "5 años"]
        rendimientos = []

        # Recalcular para asegurar consistencia
        rendimiento_1 = calcular_cagr_1y(precios_1y)
        rendimiento_3 = calcular_cagr_3y(precios_3y)
        rendimiento_5 = calcular_cagr_5y(precios_5y)

        for r in [rendimiento_1, rendimiento_3, rendimiento_5]:
            rendimientos.append(r if r is not None else 0)

        # Gráfico de barras horizontales
        fig_bar, ax = plt.subplots(figsize=(8, 2.5))
        colores = ["green" if r >= 0 else "red" for r in rendimientos]
        bars = ax.barh(periodos, rendimientos, color=colores, height=0.5)

        # Etiquetas
        for i, v in enumerate(rendimientos):
            ax.text(v + 0.5 if v >= 0 else v - 5, i, f"{v:.2f}%", va='center', fontsize=10, color='#333')

        ax.set_xlabel("Rendimiento (%)")
        ax.set_xlim(min(-10, min(rendimientos) - 5), max(10, max(rendimientos) + 5))
        ax.set_title(f"Rendimiento anualizado - {ticker_input}", fontsize=13)
        ax.axvline(0, color='gray', linewidth=0.8)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.3)

        st.pyplot(fig_bar)

        st.divider()

        # -------- Cálculo del riesgo (volatilidad anualizada) --------
       
        st.subheader("📉 Volatilidad anualizada (riesgo del activo)")
        
         # Calcular rendimientos diarios logarítmicos
        precios_1y["LogRet"] = np.log(precios_1y["Close"] / precios_1y["Close"].shift(1))
        rendimientos_diarios = precios_1y["LogRet"].dropna()

        if not rendimientos_diarios.empty:
            volatilidad_anual = np.std(rendimientos_diarios) * np.sqrt(252)
            volatilidad_pct = round(volatilidad_anual * 100, 2)

            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Volatilidad anualizada para {ticker_input}:</strong> 
                <span style="color:#0072B2;">{volatilidad_pct:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: #F4F6F7; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> Este valor representa la <em>volatilidad anual histórica</em> del activo, 
                medida por la desviación estándar de los rendimientos diarios logarítmicos. 
                Un valor más alto indica mayor incertidumbre o riesgo en el comportamiento del precio.
            </div>
            """, unsafe_allow_html=True)  

            st.divider()
            st.subheader(f"📉 Indicadores técnicos de {ticker_input}")

            # ==    = RSI ===

            # -------- Calcular RSI (14 días) correctamente --------
            window = 14
            delta = data["Close"].diff()

            gain = delta.where(delta > 0, 0.0)
            loss = -delta.where(delta < 0, 0.0)

            avg_gain = gain.rolling(window=window).mean()
            avg_loss = loss.rolling(window=window).mean()

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            data["RSI"] = rsi


            # -------- Gráfica de RSI en Plotly --------
            st.subheader(f"📊 RSI - Índice de Fuerza Relativa")

            # Asegurar datos válidos
            data_rsi = data.dropna(subset=["RSI"])

            if data_rsi.empty:
                st.warning("⚠️ No hay datos suficientes para calcular el RSI.")
            else:
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(
                    x=data_rsi.index,
                    y=data_rsi["RSI"],
                    mode="lines",
                    name="RSI",
                    line=dict(color="orange", width=2)
                ))

                # Líneas de sobrecompra y sobreventa
                fig_rsi.add_shape(type="line", x0=data_rsi.index.min(), x1=data_rsi.index.max(), y0=70, y1=70,
                                line=dict(color="red", width=1, dash="dash"))
                fig_rsi.add_shape(type="line", x0=data_rsi.index.min(), x1=data_rsi.index.max(), y0=30, y1=30,
                                line=dict(color="green", width=1, dash="dash"))

                fig_rsi.update_layout(
                    yaxis_title="RSI",
                    xaxis_title="Fecha",
                    title="RSI (14 días)",
                    height=400,
                    template="plotly_white",
                    showlegend=False
                )

                st.plotly_chart(fig_rsi, use_container_width=True)

            st.markdown("""
            <div style="background-color: #F4F6F7; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> El RSI es un oscilador que mide la velocidad y el cambio de los movimientos de precios recientes. 
                Su valor oscila entre 0 y 100 y ayuda a identificar condiciones de sobrecompra o sobreventa en el mercado
            </div>
            """, unsafe_allow_html=True) 

            # === MACD ===#
                        # -------- Calcular MACD --------
            ema_12 = data["Close"].ewm(span=12, adjust=False).mean()
            ema_26 = data["Close"].ewm(span=26, adjust=False).mean()

            macd = ema_12 - ema_26
            signal = macd.ewm(span=9, adjust=False).mean()

            data["MACD"] = macd
            data["Signal"] = signal

            st.divider()


            # -------- Gráfica del MACD en Plotly --------
            st.subheader(f"📉 MACD - Media Móvil de Convergencia/Divergencia de {ticker_input}")

            # Asegurar que haya datos válidos
            data_macd = data.dropna(subset=["MACD", "Signal"])

            if data_macd.empty:
                st.warning("⚠️ No hay datos suficientes para calcular el MACD.")
            else:
                fig_macd = go.Figure()

                fig_macd.add_trace(go.Scatter(
                    x=data_macd.index,
                    y=data_macd["MACD"],
                    mode="lines",
                    name="MACD",
                    line=dict(color="blue", width=2)
                ))

                fig_macd.add_trace(go.Scatter(
                    x=data_macd.index,
                    y=data_macd["Signal"],
                    mode="lines",
                    name="Señal",
                    line=dict(color="orange", width=1.5, dash="dot")
                ))

                fig_macd.update_layout(
                    yaxis_title="Valor",
                    xaxis_title="Fecha",
                    title="MACD",
                    height=400,
                    template="plotly_white"
                )

                st.plotly_chart(fig_macd, use_container_width=True)

            st.markdown("""
            <div style="background-color: #F4F6F7; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> El MACD es un indicador de seguimiento de tendencia que muestra la relación entre dos medias móviles exponenciales (EMA) de distinto periodo
            </div>
            """, unsafe_allow_html=True) 

        else:
          st.warning("No se pudo calcular la volatilidad. Datos insuficientes de precios diarios.")

        st.divider()


        st.markdown("<h2 style='color:#FFFFFF;'>💸 Valuación por múltiplos</h2>", unsafe_allow_html=True)

        # Inputs dinámicos de comparables
        st.markdown("<p style='color:#FFFFFF;'>Seleccione hasta 4 acciones comparables:</p>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            comp1 = st.text_input("Comparable 1", value="AAPL")
        with col2:
            comp2 = st.text_input("Comparable 2", value="MSFT")
        with col3:
            comp3 = st.text_input("Comparable 3", value="GOOGL")
        with col4:
            comp4 = st.text_input("Comparable 4", value="AMZN")

        comparables = [comp1, comp2, comp3, comp4]
        comparables = [c.upper().strip() for c in comparables if c.strip() != "" and c.upper() != ticker_input]

        # Extraer múltiplos del ticker principal
        info_objetivo = yf.Ticker(ticker_input).info
        try:
            pe = info_objetivo.get("trailingPE", None)
            pb = info_objetivo.get("priceToBook", None)
            ev_ebitda = info_objetivo.get("enterpriseToEbitda", None)
            ev_sales = info_objetivo.get("enterpriseToRevenue", None)

            df_val = pd.DataFrame([{
                "Ticker": ticker_input,
                "P/E": pe,
                "P/B": pb,
                "EV/EBITDA": ev_ebitda,
                "EV/Sales": ev_sales
            }])

            st.markdown(f"<h4 style='color:#FFFFFF;'>🔍 Múltiplos de {ticker_input}</h4>", unsafe_allow_html=True)

            # Comparables
            datos_comparables = []
            for comp in comparables:
                comp_info = yf.Ticker(comp).info
                datos_comparables.append({
                    "Ticker": comp,
                    "P/E": comp_info.get("trailingPE", None),
                    "P/B": comp_info.get("priceToBook", None),
                    "EV/EBITDA": comp_info.get("enterpriseToEbitda", None),
                    "EV/Sales": comp_info.get("enterpriseToRevenue", None)
                })

            df_comparables = pd.DataFrame(datos_comparables)
            df_comparados = pd.concat([df_val, df_comparables], ignore_index=True)

            styled_df = df_comparados.set_index("Ticker").round(2).style.background_gradient(cmap="Blues").format("{:.2f}")
            st.markdown("<p style='color:#FFFFFF;'>📊 Comparación de múltiplos:</p>", unsafe_allow_html=True)
            st.dataframe(df_comparados.set_index("Ticker").round(2), use_container_width=True)

            # Cálculo de promedios
            df_sector = df_comparables.dropna().select_dtypes(include=np.number)
            promedios = df_sector.mean()

            st.markdown("<p style='color:#FFFFFF;'>📈 Promedios de los comparables:</p>", unsafe_allow_html=True)
            st.dataframe(promedios.to_frame(name="Promedio").round(2).T)

            # Diagnóstico
            st.markdown("""
            <div style='font-size: 22px; color: #FFFFFF; font-weight: bold; margin-top: 20px;'>
                📌 Diagnóstico visual de valuación:         
            </div>
            """, unsafe_allow_html=True)

            for col in ["P/E", "P/B", "EV/EBITDA", "EV/Sales"]:
                val = df_val.iloc[0][col]
                if pd.notna(val) and col in promedios:
                 prom = promedios[col]
                estado = (
                    f"<span style='color: red; font-weight: bold;'>🔼 Sobrevaluada</span>"
                    if val > prom else
                    f"<span style='color: green; font-weight: bold;'>🔽 Subvaluada</span>"
                )

                st.markdown(f"""
                    <div style='font-size: 20px; color: #FFFFFF; margin-bottom: 10px;'>
                        <strong>{col}:</strong> {val:.2f} &nbsp;&nbsp; vs &nbsp;&nbsp; <strong>Promedio:</strong> {prom:.2f} → {estado}
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"No se pudo obtener información financiera. Error: {e}")

        st.markdown("""
        <div style="background-color: #F4F6F7; padding: 20px; border-radius: 10px; font-size: 16px; color: #333; margin-top: 25px; line-height: 1.6;">
            📘 <strong>¿Qué representa esta sección?</strong><br><br>
            Esta evaluación compara los <strong>múltiplos financieros</strong> de la empresa seleccionada con otras empresas del mismo sector o de referencia.<br><br>
            <ul>
                <li><strong>P/E (Precio / Ganancias):</strong> mide cuánto están dispuestos a pagar los inversionistas por cada dólar de ganancia.</li>
                <li><strong>P/B (Precio / Valor en Libros):</strong> compara el valor de mercado con el valor contable de los activos.</li>
                <li><strong>EV/EBITDA:</strong> mide el valor de la empresa frente a sus ganancias operativas. Útil para comparar compañías con estructuras de capital diferentes.</li>
                <li><strong>EV/Sales:</strong> compara el valor total de la empresa con sus ingresos. Útil para empresas con utilidades negativas.</li>
            </ul>
            <br>
            <strong>Interpretación:</strong> Si un múltiplo de la empresa es más alto que el promedio del sector, podría considerarse <span style="color:red;"><strong>sobrevaluada</strong></span>; si es más bajo, podría estar <span style="color:green;"><strong>subvaluada</strong></span>. Sin embargo, siempre debe analizarse junto a otros factores cualitativos y fundamentales.<br><br>
            💡 <em>Esta herramienta es útil como punto de partida para evaluar si una acción está cara o barata en comparación con sus competidores de la industria.</em>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.header("📊 Simulador de Portafolio: Rendimiento y Volatilidad")

        # Entrada de tickers
        tickers_input = st.text_input("Ingresa los tickers separados por coma (ej: AAPL, MSFT, TSLA, NVDA):", value="AAPL, MSFT, TSLA, NVDA")

        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip() != ""]

        st.divider()

        def calcular_cagr(data, años):
            if data.empty or "Close" not in data.columns:
                return None

            fecha_final = data.index[-1]
            fecha_inicial = fecha_final - timedelta(days=365 * años)

            data_filtrada = data.loc[data.index >= fecha_inicial]

            if data_filtrada["Close"].dropna().shape[0] < 2:
                return None

            # Asegurar que se accede al valor como escalar
            try:
                precio_inicio = float(data_filtrada["Close"].iloc[0])
                precio_fin = float(data_filtrada["Close"].iloc[-1])
            except:
                return None

            if precio_inicio == 0 or pd.isna(precio_inicio) or pd.isna(precio_fin):
                return None

            cagr = (precio_fin / precio_inicio) ** (1 / años) - 1
            return round(cagr * 100, 2)


        # Resultados
        rendimientos = []
        volatilidades = []

        for tkr in tickers:
            try:
                data = yf.download(tkr, period="5y", interval="1d", auto_adjust=True)
                data = data.dropna()

                cagr_1 = calcular_cagr(data, 1)
                cagr_3 = calcular_cagr(data, 3)
                cagr_5 = calcular_cagr(data, 5)

                # Volatilidad anualizada
                log_ret = np.log(data["Close"] / data["Close"].shift(1)).dropna()
                vol = np.std(log_ret) * np.sqrt(252)
                vol_pct = round(vol * 100, 2)

                rendimientos.append({
                    "Ticker": tkr,
                    "1 año(s)": f"{float(cagr_1):.2f}%" if cagr_1 is not None else "N/D",
                    "3 año(s)": f"{float(cagr_3):.2f}%" if cagr_3 is not None else "N/D",
                    "5 año(s)": f"{float(cagr_5):.2f}%" if cagr_5 is not None else "N/D"
                })

                volatilidades.append({
                    "Ticker": tkr,
                    "Volatilidad Anual": f"{float(vol_pct):.2f}%"
                })


            except Exception as e:
                st.warning(f"No se pudo obtener datos para {tkr}: {e}")

        # Mostrar resultados
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Rendimientos Anualizados")
            st.caption("Este cálculo se basa en el crecimiento compuesto del precio desde el inicio hasta el final de cada periodo. Se muestra el rendimiento anualizado para 1, 3 y 5 años (si hay datos suficientes).")
            st.dataframe(pd.DataFrame(rendimientos), use_container_width=True)

        with col2:
            st.subheader("📉 Volatilidad Anualizada")
            st.caption("La volatilidad anualizada representa el riesgo del activo, calculado como la desviación estándar de los rendimientos diarios multiplicada por la raíz cuadrada de 252 (días hábiles por año).")
            st.dataframe(pd.DataFrame(volatilidades), use_container_width=True)


        import plotly.express as px

        st.divider()
        st.header("🌐 Visualización de Frontera Eficiente")

        # Parámetros
        n_portfolios = 5000
        rf = 0.03  # tasa libre de riesgo fija

        # Descargar precios históricos de los tickers
        try:
            precios = yf.download(tickers, period="3y", interval="1d", auto_adjust=True)["Close"]
            precios = precios.dropna(axis=1)  # eliminar columnas con datos faltantes

            # Calcular rendimientos diarios y medias anuales
            daily_returns = precios.pct_change().dropna()
            mean_returns = daily_returns.mean() * 252
            cov_matrix = daily_returns.cov() * 252

            # Simulación de portafolios
            results = {
                "Rendimiento": [],
                "Volatilidad": [],
                "Sharpe Ratio": [],
                "Pesos": []
            }
        
            for _ in range(n_portfolios):
                pesos = np.random.random(len(mean_returns))
                pesos /= np.sum(pesos)

                rendimiento = np.dot(pesos, mean_returns)
                volatilidad = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))
                sharpe = (rendimiento - rf) / volatilidad

                results["Rendimiento"].append(rendimiento)
                results["Volatilidad"].append(volatilidad)
                results["Sharpe Ratio"].append(sharpe)
                results["Pesos"].append(pesos)

            df_portafolios = pd.DataFrame(results)
        except Exception as e:
             st.error(f"No se pudo construir la frontera eficiente. Error: {e}")
            # Identificar portafolios óptimos
        idx_sharpe = df_portafolios["Sharpe Ratio"].idxmax()
        idx_min_vol = df_portafolios["Volatilidad"].idxmin()
        idx_max_ret = df_portafolios["Rendimiento"].idxmax()

        pf_sharpe = df_portafolios.loc[idx_sharpe]
        pf_min_vol = df_portafolios.loc[idx_min_vol]
        pf_max_ret = df_portafolios.loc[idx_max_ret]

            # Código a agregar DESPUÉS de generar df_portafolios y ANTES de graficar:

            # Convertir pesos a diccionarios con los tickers
        n_assets = len(mean_returns)
        tickers_list = precios.columns.tolist()
        df_portafolios["Pesos"] = df_portafolios["Pesos"].apply(lambda w: dict(zip(tickers_list, w)))

            # Encontrar portafolios óptimos
        port_sharpe = df_portafolios.loc[df_portafolios["Sharpe Ratio"].idxmax()]
        port_min_vol = df_portafolios.loc[df_portafolios["Volatilidad"].idxmin()]
        port_max_ret = df_portafolios.loc[df_portafolios["Rendimiento"].idxmax()]

            # Mostrar comparativa
        st.header("🎯 Comparativa de Portafolios Óptimos")
        tabs = st.tabs(["Maxímo Sharpe Ratio", "Mínima Volatilidad", "Máximo Retorno"])

        for i, (nombre, portafolio) in enumerate(zip(
                ["Maxímo Sharpe Ratio", "Mínima Volatilidad", "Máximo Retorno"],
                [port_sharpe, port_min_vol, port_max_ret])):

                with tabs[i]:
                    st.subheader(f"{nombre}")

                    st.markdown(f"""
                    - **Rendimiento Esperado:** {portafolio['Rendimiento']*100:.2f}%
                    - **Volatilidad Esperada:** {portafolio['Volatilidad']*100:.2f}%
                    - **Sharpe Ratio:** {portafolio['Sharpe Ratio']:.2f}
                    """)

                    st.markdown("**Composición del Portafolio**")
                    pesos_dict = portafolio["Pesos"]
                    pesos_series = pd.Series(pesos_dict).sort_values(ascending=False)
                    pesos_df = pd.DataFrame({"Ticker": pesos_series.index, "Peso": (pesos_series * 100).round(2).astype(str) + "%"})
                    st.dataframe(pesos_df, use_container_width=True)

            # Gráfica
        fig = px.scatter(
                df_portafolios,
                x="Volatilidad",
                y="Rendimiento",
                color="Sharpe Ratio",
                color_continuous_scale="Turbo",
                title="Frontera Eficiente del Portafolio (Monte Carlo)",
                labels={"Volatilidad": "Volatilidad Esperada", "Rendimiento": "Rendimiento Esperado"},
                height=600
            )

        st.plotly_chart(fig, use_container_width=True)   


        st.divider()

    else:
         st.error("❌ Ticker inválido, por favor revise e intente de nuevo.")
    

st.caption("Profe pongame 100 :)")


st.divider()








