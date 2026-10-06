import streamlit as st
import pandas as pd
from datetime import date
import base64
import html

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Facturador - Almeida Surtilácteos",
    page_icon="🧀",
    layout="wide"
)

# =========================================================
# COLORES CORPORATIVOS
# =========================================================

AZUL = "#07345B"
AZUL_CLARO = "#0B4778"
DORADO = "#D99A00"
DORADO_CLARO = "#F2B51D"
GRIS = "#F4F6F8"
GRIS_TEXTO = "#5F6B76"
BLANCO = "#FFFFFF"

# =========================================================
# INFORMACIÓN DE LA EMPRESA
# =========================================================

LOGO_PATH = "logo.png"

company_info = {
    "name": "ALMEIDA SURTILÁCTEOS",
    "subtitle": "DISTRIBUCIÓN DE PRODUCTOS LÁCTEOS",
    "nit": "10800437147",
    "address": "Carrera 6 # 12-03",
    "city": "Ipiales, Nariño, Colombia",
    "phone": "317 225 9214",
    "email": "sebasalmeida98@gmail.com"
}


# =========================================================
# FUNCIONES
# =========================================================

def get_base64_image(path):
    try:
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except:
        return None


def money(value):
    return f"${value:,.0f}".replace(",", ".")


def clean(value):
    if pd.isna(value):
        return ""
    return html.escape(str(value))


logo_base64 = get_base64_image(LOGO_PATH)


# =========================================================
# CSS STREAMLIT
# =========================================================

st.markdown(
    f"""
    <style>

    .main {{
        background-color: #ffffff;
    }}

    .company-header {{
        background: linear-gradient(135deg, {AZUL}, {AZUL_CLARO});
        padding: 25px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
    }}

    .company-title {{
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 3px;
    }}

    .company-subtitle {{
        font-size: 15px;
        color: #f5c451;
        font-weight: 600;
    }}

    .section-title {{
        color: {AZUL};
        font-size: 21px;
        font-weight: 800;
        border-left: 5px solid {DORADO};
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }}

    .invoice-card {{
        background: white;
        border: 1px solid #dddddd;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }}

    .total-box {{
        background: {AZUL};
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: right;
    }}

    .total-label {{
        font-size: 14px;
        opacity: 0.8;
    }}

    .total-value {{
        font-size: 28px;
        font-weight: bold;
        color: #F5C451;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ENCABEZADO DEL SISTEMA
# =========================================================

col_logo, col_company = st.columns([1, 4])

with col_logo:
    if logo_base64:
        st.image(LOGO_PATH, width=220)
    else:
        st.warning("No se encontró logo.png")

with col_company:
    st.markdown(
        f"""
        <div style="padding-top:20px;">
            <div style="
                font-size:32px;
                font-weight:800;
                color:{AZUL};
            ">
                {company_info["name"]}
            </div>

            <div style="
                font-size:16px;
                color:{DORADO};
                font-weight:700;
            ">
                {company_info["subtitle"]}
            </div>

            <div style="
                margin-top:10px;
                color:{GRIS_TEXTO};
                font-size:14px;
            ">
                NIT: {company_info["nit"]} &nbsp; | &nbsp;
                {company_info["address"]} &nbsp; | &nbsp;
                {company_info["city"]}
            </div>

            <div style="
                color:{GRIS_TEXTO};
                font-size:14px;
            ">
                Tel: {company_info["phone"]} &nbsp; | &nbsp;
                {company_info["email"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")


# =========================================================
# DATOS DE LA FACTURA
# =========================================================

st.markdown(
    f'<div class="section-title">📄 Datos de la factura</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    invoice_number = st.text_input(
        "Número de factura",
        value="FV-0001"
    )

with col2:
    invoice_date = st.date_input(
        "Fecha de factura",
        value=date.today()
    )

with col3:
    due_date = st.date_input(
        "Fecha de vencimiento",
        value=date.today()
    )


col1, col2 = st.columns(2)

with col1:
    payment_method = st.selectbox(
        "Forma de pago",
        [
            "Contado",
            "Crédito",
            "Transferencia bancaria",
            "Efectivo",
            "Nequi",
            "Daviplata",
            "Otro"
        ]
    )

with col2:
    currency = st.selectbox(
        "Moneda",
        ["COP - Pesos Colombianos"],
        index=0
    )


# =========================================================
# DATOS DEL CLIENTE
# =========================================================

st.markdown(
    f'<div class="section-title">👤 Datos del cliente</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input(
        "Nombre / Razón social",
        value=""
    )

    client_document = st.text_input(
        "NIT / Cédula",
        value=""
    )

    client_address = st.text_input(
        "Dirección",
        value=""
    )

with col2:

    client_city = st.text_input(
        "Ciudad / Municipio",
        value=""
    )

    client_phone = st.text_input(
        "Teléfono",
        value=""
    )

    client_email = st.text_input(
        "Correo electrónico",
        value=""
    )


# =========================================================
# PRODUCTOS
# =========================================================

st.markdown(
    f'<div class="section-title">🧀 Productos / Servicios</div>',
    unsafe_allow_html=True
)


if "items_df" not in st.session_state:

    st.session_state["items_df"] = pd.DataFrame({
        "Descripción": [
            "Producto lácteo"
        ],
        "Cantidad": [
            1
        ],
        "Precio unitario": [
            0
        ]
    })


items_df = st.data_editor(
    st.session_state["items_df"],
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Descripción": st.column_config.TextColumn(
            "Descripción",
            width="large"
        ),
        "Cantidad": st.column_config.NumberColumn(
            "Cantidad",
            min_value=0,
            step=1
        ),
        "Precio unitario": st.column_config.NumberColumn(
            "Precio unitario",
            min_value=0,
            step=100
        )
    },
    hide_index=True
)


# =========================================================
# CÁLCULOS
# =========================================================

items_df["Cantidad"] = pd.to_numeric(
    items_df["Cantidad"],
    errors="coerce"
).fillna(0)

items_df["Precio unitario"] = pd.to_numeric(
    items_df["Precio unitario"],
    errors="coerce"
).fillna(0)

items_df["Importe"] = (
    items_df["Cantidad"] *
    items_df["Precio unitario"]
)

subtotal = float(items_df["Importe"].sum())


col1, col2, col3 = st.columns(3)

with col1:

    discount_rate = st.number_input(
        "Descuento (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

with col2:

    iva_rate = st.number_input(
        "IVA (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

with col3:

    additional_charge = st.number_input(
        "Otros cargos",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


discount_amount = subtotal * discount_rate / 100

base_iva = subtotal - discount_amount

iva_amount = base_iva * iva_rate / 100

total = (
    subtotal
    - discount_amount
    + iva_amount
    + additional_charge
)


# =========================================================
# OBSERVACIONES
# =========================================================

notes = st.text_area(
    "Observaciones / Notas",
    placeholder="Ej: Gracias por su compra. Productos entregados en perfecto estado."
)


# =========================================================
# VISTA PREVIA
# =========================================================

st.markdown("---")

st.markdown(
    f'<div class="section-title">👁️ Vista previa</div>',
    unsafe_allow_html=True
)


# =========================================================
# CONSTRUIR FILAS HTML
# =========================================================

rows_html = ""

for _, row in items_df.iterrows():

    description = clean(row["Descripción"])
    quantity = float(row["Cantidad"])
    price = float(row["Precio unitario"])
    amount = float(row["Importe"])

    if description == "" and amount == 0:
        continue

    rows_html += f"""
    <tr>
        <td style="
            padding:12px;
            border-bottom:1px solid #e5e5e5;
        ">
            {description}
        </td>

        <td style="
            padding:12px;
            text-align:center;
            border-bottom:1px solid #e5e5e5;
        ">
            {quantity:g}
        </td>

        <td style="
            padding:12px;
            text-align:right;
            border-bottom:1px solid #e5e5e5;
        ">
            {money(price)}
        </td>

        <td style="
            padding:12px;
            text-align:right;
            border-bottom:1px solid #e5e5e5;
            font-weight:600;
        ">
            {money(amount)}
        </td>
    </tr>
    """


# =========================================================
# LOGO HTML
# =========================================================

if logo_base64:

    logo_html = f"""
    <img
        src="data:image/png;base64,{logo_base64}"
        style="
            width:250px;
            max-height:150px;
            object-fit:contain;
        "
    >
    """

else:

    logo_html = f"""
    <div style="
        font-size:28px;
        font-weight:bold;
        color:{AZUL};
    ">
        ALMEIDA SURTILÁCTEOS
    </div>
    """


# =========================================================
# FACTURA HTML
# =========================================================

invoice_body = f"""

<div style="
    width:850px;
    margin:auto;
    background:white;
    padding:45px;
    font-family:Arial, Helvetica, sans-serif;
    color:#263238;
    border:1px solid #dddddd;
">

    <!-- ENCABEZADO -->

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:flex-start;
    ">

        <div>
            {logo_html}
        </div>

        <div style="
            text-align:right;
            min-width:260px;
        ">

            <div style="
                font-size:28px;
                font-weight:800;
                color:{AZUL};
            ">
                FACTURA DE VENTA
            </div>

            <div style="
                margin-top:8px;
                font-size:16px;
                font-weight:bold;
                color:{DORADO};
            ">
                No. {clean(invoice_number)}
            </div>

            <div style="
                margin-top:10px;
                font-size:13px;
                line-height:1.7;
            ">

                <b>Fecha:</b>
                {invoice_date.strftime("%d/%m/%Y")}
                <br>

                <b>Vencimiento:</b>
                {due_date.strftime("%d/%m/%Y")}
                <br>

                <b>Forma de pago:</b>
                {clean(payment_method)}

            </div>

        </div>

    </div>


    <!-- LINEA -->

    <div style="
        height:5px;
        background:{DORADO};
        margin:25px 0;
    "></div>


    <!-- EMPRESA / CLIENTE -->

    <div style="
        display:flex;
        justify-content:space-between;
        margin-bottom:25px;
    ">

        <div style="width:48%;">

            <div style="
                font-size:14px;
                font-weight:bold;
                color:{DORADO};
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                EMISOR
            </div>

            <div style="
                font-size:17px;
                font-weight:bold;
                color:{AZUL};
            ">
                {company_info["name"]}
            </div>

            <div style="
                font-size:13px;
                line-height:1.7;
                margin-top:5px;
            ">

                NIT: {company_info["nit"]}<br>
                {company_info["address"]}<br>
                {company_info["city"]}<br>
                Tel: {company_info["phone"]}<br>
                {company_info["email"]}

            </div>

        </div>


        <div style="
            width:48%;
            border-left:3px solid {DORADO};
            padding-left:20px;
        ">

            <div style="
                font-size:14px;
                font-weight:bold;
                color:{DORADO};
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                CLIENTE
            </div>

            <div style="
                font-size:17px;
                font-weight:bold;
                color:{AZUL};
            ">
                {clean(client_name) or "Cliente"}
            </div>

            <div style="
                font-size:13px;
                line-height:1.7;
                margin-top:5px;
            ">

                Documento: {clean(client_document)}<br>
                {clean(client_address)}<br>
                {clean(client_city)}<br>
                Tel: {clean(client_phone)}<br>
                {clean(client_email)}

            </div>

        </div>

    </div>


    <!-- TABLA -->

    <table style="
        width:100%;
        border-collapse:collapse;
        font-size:13px;
        margin-top:15px;
    ">

        <thead>

            <tr style="
                background:{AZUL};
                color:white;
            ">

                <th style="
                    padding:13px;
                    text-align:left;
                ">
                    DESCRIPCIÓN
                </th>

                <th style="
                    padding:13px;
                    text-align:center;
                ">
                    CANT.
                </th>

                <th style="
                    padding:13px;
                    text-align:right;
                ">
                    PRECIO UNITARIO
                </th>

                <th style="
                    padding:13px;
                    text-align:right;
                ">
                    IMPORTE
                </th>

            </tr>

        </thead>

        <tbody>

            {rows_html}

        </tbody>

    </table>


    <!-- TOTALES -->

    <div style="
        display:flex;
        justify-content:flex-end;
        margin-top:25px;
    ">

        <table style="
            border-collapse:collapse;
            width:330px;
            font-size:14px;
        ">

            <tr>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    Subtotal:
                </td>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    {money(subtotal)}
                </td>

            </tr>


            <tr>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    Descuento ({discount_rate:.1f}%):
                </td>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    - {money(discount_amount)}
                </td>

            </tr>


            <tr>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    IVA ({iva_rate:.1f}%):
                </td>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    {money(iva_amount)}
                </td>

            </tr>


            <tr>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    Otros cargos:
                </td>

                <td style="
                    padding:6px;
                    text-align:right;
                ">
                    {money(additional_charge)}
                </td>

            </tr>


            <tr style="
                background:{AZUL};
                color:white;
            ">

                <td style="
                    padding:13px;
                    text-align:right;
                    font-size:16px;
                    font-weight:bold;
                ">
                    TOTAL
                </td>

                <td style="
                    padding:13px;
                    text-align:right;
                    font-size:18px;
                    font-weight:bold;
                    color:#F5C451;
                ">
                    {money(total)}
                </td>

            </tr>

        </table>

    </div>


    <!-- OBSERVACIONES -->

    <div style="
        margin-top:35px;
        padding:15px;
        background:#f6f7f8;
        border-left:4px solid {DORADO};
    ">

        <div style="
            font-weight:bold;
            color:{AZUL};
            margin-bottom:5px;
        ">
            OBSERVACIONES
        </div>

        <div style="
            font-size:12px;
            color:#555;
        ">
            {clean(notes) if notes else "Sin observaciones."}
        </div>

    </div>


    <!-- PIE -->

    <div style="
        margin-top:35px;
        padding-top:15px;
        border-top:1px solid #dddddd;
        text-align:center;
        font-size:11px;
        color:#777;
    ">

        <strong style="color:{AZUL};">
            ALMEIDA SURTILÁCTEOS
        </strong>

        <br>

        Distribución de productos lácteos

        <br>

        Ipiales, Nariño, Colombia

        <br>

        Tel. {company_info["phone"]} |
        {company_info["email"]}

    </div>

</div>

"""


# =========================================================
# MOSTRAR FACTURA
# =========================================================

import streamlit.components.v1 as components

components.html(
    invoice_body,
    height=1100,
    scrolling=True
)


# =========================================================
# DESCARGAR HTML
# =========================================================

html_to_download = f"""
<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<title>
Factura {invoice_number} - Almeida Surtilácteos
</title>

<style>

body {{
    margin:0;
    background:#eeeeee;
}}

@media print {{

    body {{
        background:white;
    }}

    div {{
        page-break-inside:avoid;
    }}

}}

</style>

</head>

<body>

{invoice_body}

</body>

</html>
"""


st.download_button(
    label="⬇️ Descargar factura",
    data=html_to_download,
    file_name=f"factura_{invoice_number}.html",
    mime="text/html",
    use_container_width=True
)


st.info(
    "💡 Para obtener el PDF: descarga la factura, abre el archivo HTML "
    "en Chrome o Edge y presiona CTRL + P → Guardar como PDF."
)
