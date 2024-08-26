from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED
from rich.columns import Columns

# Inicializar la consola
console = Console()

# Activos fijos iniciales
activos = {
    "salario_base": 1788.25,
    "plus_convenio": 125.34,
    "mejora_absorbible": 904.18,  # Valor actualizado
    "seguro_medico_familiares_1": 63.29,
    "seguro_medico_familiares_2": 63.29,
    "horas_noturnas_guardias": 624.20,  # Valor inicial (será actualizado)
    "pp_gratificacoes": 318.94,
    "home_allowance": 30.00,
    "gastos_comida_transporte": 156.08,  # Valor inicial (será actualizado)
    "descuento_del_mes": 0.00  # Valor inicial ahora es cero
}

# Nuevo diccionario para deducciones
deducciones = {}

# Solicitar el valor de las horas nocturnas y de fin de semana al usuario
horas_noturnas_guardias_input = float(input("Introduce el valor de las horas de finales de semana y nocturnas: "))
activos["horas_noturnas_guardias"] = horas_noturnas_guardias_input

# Solicitar el valor de los gastos de comida y transporte del mes
gastos_comida_transporte_input = float(input("Gastos de comida y transporte del mes: "))
activos["gastos_comida_transporte"] = gastos_comida_transporte_input

# Actualizar el valor de mejora_absorbible
activos["mejora_absorbible"] -= gastos_comida_transporte_input

# Calcular el valor_prod_especie
valor_prod_especie = (
    activos["seguro_medico_familiares_1"] +
    activos["seguro_medico_familiares_2"] +
    gastos_comida_transporte_input
)

# Agregar valor_prod_especie al diccionario de deducciones
deducciones["valor_prod_especie"] = valor_prod_especie

# Solicitar el valor del descuento del mes
descuento_del_mes_input = float(input("Descuento del mes (puede ser positivo o negativo, digite cero si no hay): "))
activos["descuento_del_mes"] = descuento_del_mes_input

# Sumar todos los activos para obtener el total
total_activos = sum(activos.values())

# Tasas a aplicar (actualizadas con los porcentajes correctos)
tasas = {
    "contingencias_comunes": 0.0470,  # 4.70%
    "equidad_intergeneracional": 0.0012,  # 0.12%
    "desempleo": 0.0155,  # 1.55%
    "formacion_profesional": 0.0010  # 0.10%
}

# Calcular los valores de las tasas
valores_tasas = {nombre: total_activos * tasa for nombre, tasa in tasas.items()}
total_aportaciones = sum(valores_tasas.values())

# Agregar el total de tasas al diccionario de deducciones como total_aportaciones
deducciones["total_aportaciones"] = total_aportaciones

# Solicitar el porcentaje del IRPF al usuario
porcentaje_irpf = float(input("Porcentaje del IRPF del mes (como porcentaje, por ejemplo 15 para 15%): "))

# Calcular el valor del IRPF
base_irpf = total_activos - valor_prod_especie
valor_irpf = base_irpf * (porcentaje_irpf / 100)

# Agregar el valor del IRPF al diccionario de deducciones
deducciones["valor_irpf"] = valor_irpf

# Imprimir dos líneas en blanco
console.print("\n")
console.print("\n")

# Crear las tablas
table_activos = Table(title=Text("Detalles de la suma de activos", style="bold green"), box=ROUNDED)
table_activos.add_column("Campo", style="bold")
table_activos.add_column("Valor (€)", style="bold")
for key, value in activos.items():
    table_activos.add_row(key, f"{value:.2f}")

table_tasas = Table(title=Text("Tasas aplicadas:", style="bold red"), box=ROUNDED)
table_tasas.add_column("Tasa / Deducción", style="bold")
table_tasas.add_column("Valor (€)", style="bold")
for nombre, valor in valores_tasas.items():
    table_tasas.add_row(nombre, f"{valor:.2f}")
table_tasas.add_row("Total de aportaciones", f"{deducciones['total_aportaciones']:.2f}")
table_tasas.add_row("Valor de producción en especie (deducciones)", f"{deducciones['valor_prod_especie']:.2f}")
table_tasas.add_row("Valor del IRPF", f"{deducciones['valor_irpf']:.2f}")

# Imprimir las tablas una al lado de la otra
console.print(Columns([table_activos, table_tasas]))

# Imprimir la base para el cálculo del IRPF
console.print(f"\nBase para el cálculo del IRPF: €{base_irpf:.2f}")

# Imprimir el total de deducciones
total_deducciones = deducciones["valor_prod_especie"] + deducciones["total_aportaciones"] + deducciones["valor_irpf"]
console.print(f"\nTotal de deducciones: €{total_deducciones:.2f}")

# Calcular y mostrar el salario del mes
salario_del_mes = total_activos - total_deducciones
console.print(f"\n{Text('El salario del mes es de:', style='bold green')} €{salario_del_mes:.2f}")
