from .GLOBAL_VARIABLES import HOME, cd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.markers import makeMarker
import os


class PDF:
    def crear_reporte_por_modelo(arquitectura, modelo, dataset, pesos, epocas, batch_size, accuracy, f1_score, loss, metrics_for_epoch):
        dataset = str(dataset)

        acc_epoch = []
        f1_epoch = []
        loss_epoch = []

        ''' Obtener los valores de Accuracy, F1 Score y Loss por época para usarlos más adelante
         en la grágica de cómo se comportó el modelo en cada época '''
        for i in metrics_for_epoch:
            acc_epoch.append(i['accuracy'])
            f1_epoch.append(i['f1'])
            #loss_epoch.append(i['loss'])

        # Accuracy y Loss por época
        # acc_epoch = [0.57, 0.85, 0.78, 0.89, 0.95, 0.98, 0.99, 0.99, 0.99, 0.99]
        # f1_epoch = [0.36, 0.96, 0.52, 0.64, 0.18, 0.42, 0.31, 0.97, 0.96, 0.81]
        loss_epoch = [0.12, 0.25, 0.58, 0.12, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01]

        # Función para obtener las coordenadas de (Epoca, Accuracy)
        def acc_coordinates(acc_epoch, epocas):
            acc_coord = []
            for i in range(epocas):
                acc_coord.append((i+1, acc_epoch[i]))
            return acc_coord
        
        # Función para obtener las coordenadas de (Epoca, F1 Score)
        def f1_coordinates(f1_epoch, epocas):
            f1_coord = []
            for i in range(epocas):
                f1_coord.append((i+1, f1_epoch[i]))
            return f1_coord

        # Función para obtener las coordenadas de (Epoca, Loss)
        def loss_coordinates(loss_epoch, epocas):
            loss_coord = []
            for i in range(epocas):
                loss_coord.append((i+1, loss_epoch[i]))
            return loss_coord

        # # # # # # # # # # #
        # Variables Colores #
        # # # # # # # # # # #

        # FUNCION PARA CONVERTIR RGB NORMAL A COLOR RGB DE REPORTLAB
        def colorRGB(r, g, b):
            return Color(r/255, g/255, b/255)

        color_verde_light = colorRGB(31, 191, 66)
        color_negro = colorRGB(0, 0, 0)
        color_amarillo_light = colorRGB(255, 237, 61)

        # # # # # # #  # # # #
        # Variables Espacios #
        # # # # # # #  # # # #

        ancho_pagina, alto_pagina = letter
        margen = 50
        espacio_entre_linea = 2
        espacio_entre_elementos = 5

        reportes_dir = os.path.join(HOME, 'reportesPDF', arquitectura)
        reporte_name = modelo+'_Reporte.pdf'
        os.makedirs(reportes_dir, exist_ok=True)
        cd(reportes_dir)

        pdf = canvas.Canvas(reporte_name, pagesize=letter)

        # Adicionar titulo al PDF
        pdf.setTitle("Reporte de entrenamiento")

        # # # # # # # # # #
        # MARCA SAFECROPS #
        # # # # # # # # # #

        # CALCULAR POSICION INICIAL
        posicionX_inicial = margen
        posicionY_inicial = alto_pagina - margen

        # DIBUJAR LOGO DE SAFECROPS
        width_img = 70
        height_img = 70

        tamaño_fuente = 24
        tipo_fuente = 'Helvetica-Bold'
        texto = 'SafeCrops'

        posicionX = posicionX_inicial
        posicionY = posicionY_inicial - tamaño_fuente - height_img

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.setFillColor(color_verde_light) # (color-relleno-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)
        ancho_texto = pdf.stringWidth(texto, tipo_fuente, tamaño_fuente)

        imagen = HOME + '/AppSafeCrops/static/img/logoSafeCrops.png'

        posicionX = margen - (width_img - ancho_texto)/2
        posicionY = alto_pagina - margen

        pdf.drawImage(imagen, posicionX, posicionY - width_img, width_img, height_img, mask='auto') # (posicionX, posicionY, width-imagen, height-imagen)

        # DIBUJAR TIPO REPORTE
        tamaño_fuente = 20
        tipo_fuente = 'Helvetica-Bold'
        texto = 'ENTRENAMIENTO'

        posicionX_datos = posicionX + ancho_texto + (espacio_entre_elementos * 23)
        posicionY_datos = posicionY_inicial - tamaño_fuente

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.setFillColor(color_negro) # (color-relleno-letra)
        pdf.drawString(posicionX_datos, posicionY_datos, texto) # (posicionX, posicionY, texto-dibujar)

        # DIBUJAR DATOS FECHA
        tamaño_fuente = 10
        tipo_fuente = 'Helvetica'
        texto = 'Fecha:'

        posicionX = posicionX_datos
        posicionY = posicionY_datos - tamaño_fuente - (espacio_entre_linea * 10)

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.setFillColor(color_negro) # (color-relleno-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)
        ancho_texto = pdf.stringWidth(texto, tipo_fuente, tamaño_fuente)

        tamaño_fuente = 10
        tipo_fuente = 'Helvetica-Bold'
        texto = str(datetime.today().strftime('%d/%b/%Y'))

        posicionX = posicionX + ancho_texto + espacio_entre_elementos
        posicionY = posicionY

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, fecha-dibujar(dd/Mes/aaaa))
        ancho_texto = pdf.stringWidth(texto, tipo_fuente, tamaño_fuente)

        # DIBUJAR DATOS HORA
        tamaño_fuente = 10
        tipo_fuente = 'Helvetica'
        texto = 'Hora:'

        posicionX = posicionX_datos
        posicionY = posicionY - tamaño_fuente - espacio_entre_linea

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)
        ancho_texto = pdf.stringWidth(texto, tipo_fuente, tamaño_fuente)

        tamaño_fuente = 10
        tipo_fuente = 'Helvetica-Bold'
        texto = str(datetime.today().strftime('%H:%M:%S'))

        posicionX = posicionX + ancho_texto + espacio_entre_elementos
        posicionY = posicionY

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, hora-dibujar(00:00:00))

        # DIBUJAR DATOS ARQUITECTURA
        tamaño_fuente = 10
        tipo_fuente = 'Helvetica'
        texto = 'Arquitectura:'

        posicionX = posicionX_datos
        posicionY = posicionY - tamaño_fuente - (espacio_entre_linea * 5)

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)
        ancho_texto = pdf.stringWidth(texto, tipo_fuente, tamaño_fuente)

        tamaño_fuente = 10
        tipo_fuente = 'Helvetica-Bold'
        texto = arquitectura.upper()

        posicionX = posicionX + ancho_texto + espacio_entre_elementos
        posicionY = posicionY

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)

        # DIBUJAR DATOS MODELO
        tamaño_fuente = 10
        tipo_fuente = 'Helvetica'
        texto = 'Modelo:'

        posicionX = posicionX_datos
        posicionY = posicionY - tamaño_fuente - espacio_entre_linea

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)
        ancho_texto = pdf.stringWidth(texto, tipo_fuente, tamaño_fuente)

        tamaño_fuente = 10
        tipo_fuente = 'Helvetica-Bold'
        texto = modelo.upper()

        posicionX = posicionX + ancho_texto + espacio_entre_elementos
        posicionY = posicionY

        pdf.setFont(tipo_fuente, tamaño_fuente) # (tipo-letra, tamaño-letra)
        pdf.drawString(posicionX, posicionY, texto) # (posicionX, posicionY, texto-dibujar)

        # DIBUJAR TABLA DE RESULTADOS
        dataset_lines = [dataset[i:i+20] for i in range(0, len(dataset), 20)] # Dividir el nombre del dataset en líneas más cortas

        pesos_lines = [pesos[i:i+20] for i in range(0, len(pesos), 20)] # Dividir el nombre de los pesos en líneas más cortas

        data = [
            ['Dataset', 'Pesos', 'Epocas', 'Batch Size', 'Accuracy', 'F1 Score', 'Loss'],
            ['\n'.join(dataset_lines), '\n'.join(pesos_lines), epocas, batch_size, accuracy, f1_score, loss],
        ] # Datos de la tabla

        style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey), # Color de fondo de la primera fila
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # Color de texto de la primera fila
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # Alinear horizontalmente al centro
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), # Tipo de letra de la primera fila
            ('TOPPADDING', (0, 0), (-1, 0), 6), # Espacio superior de la primera fila
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6), # Espacio inferior de la primera fila
            ('BACKGROUND', (0, 1), (-1, -1), color_amarillo_light), # Color de fondo del resto de filas
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
            # Agregar bordes internos
            ('GRID', (0, 0), (-1, -1), 1, colors.black), # Borde de la tabla (Exterior, Izquierda, Abajo, Derecha, Arriba, Color)
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black), # Borde interno de la tabla
        ] # Estilo de la tabla

        col_widths = [117.5, 117.5, 50, 60, 55, 55, 55] # Ancho de las columnas

        # Crear la tabla con datos y estilo
        table = Table(data, colWidths=col_widths) # Crear la tabla con los datos y el ancho de las columnas
        table.setStyle(TableStyle(style)) # Agregar el estilo a la tabla

        # Posicionar y agregar la tabla al PDF
        table_width, table_height = table.wrap(0, 0) # Obtener el ancho y alto de la tabla
        posicionX = margen # Posición en X
        posicionY = posicionY - table_height - (espacio_entre_linea * 30) # Posición en Y
        table.drawOn(pdf, posicionX, posicionY) # Dibujar la tabla en el PDF

        # DIBUJAR GRAFICA DE ACCURACY Y LOSS
        drawing_width = 450
        drawing_height = 325
        drawing = Drawing(drawing_width, drawing_height) # Crear un objeto Drawing(width, height)

        # Agregar fondo al Drawing
        background = Rect(0, 0, drawing_width, drawing_height, fill=True, fillColor=colors.white) # Crear un objeto Rect(x, y, width, height, fill, fillColor)
        drawing.add(background)


        # Agregar títulos a los ejes X e Y usando etiquetas (labels)
        x_title = Label()
        x_title.setText('Epochs')
        x_title.fillColor = colors.green
        x_title.fontSize = 12
        x_title.x = 200  # Posición X del título en el eje X
        x_title.y = 20   # Posición Y del título en el eje X
        x_title.textAnchor = 'middle'
        drawing.add(x_title)

        y_title = Label()
        y_title.setText('Accuracy / F1 Score / Loss')
        y_title.fillColor = colors.green
        y_title.fontSize = 12
        y_title.x = 15   # Posición X del título en el eje Y
        y_title.y = 160  # Posición Y del título en el eje Y
        y_title.angle = 90
        y_title.textAnchor = 'middle'
        drawing.add(y_title)

        data = [
            acc_coordinates(acc_epoch, epocas),
            f1_coordinates(f1_epoch, epocas),
            loss_coordinates(loss_epoch, epocas)
        ] # Crear una lista con los datos de las coordenadas

        lp = LinePlot() # Crear un objeto LinePlot
        lp.x = 50 # Posición en X
        lp.y = 50 # Posición en Y
        lp.fillColor = colors.white # Color de relleno
        lp.height = 225 # Alto
        lp.width = 300  # Ancho
        lp.data = data # Agregar los datos de las coordenadas
        lp.joinedLines = 1 # Unir las líneas
        lp.lines[0].symbol = makeMarker('FilledCircle') # Agregar marcador a la línea
        lp.lines[0].strokeColor = colors.blue # Color de la línea
        lp.lines[1].symbol = makeMarker('Circle') # Agregar marcador a la línea
        lp.lines[1].strokeColor = colors.gray # Color de la línea
        lp.lines[2].symbol = makeMarker('Circle')
        lp.lines[2].strokeColor = colors.red
        # lp.lineLabelFormat = '%2.2f' # Formato de los valores de las líneas
        lp.strokeColor = colors.black # Color de las líneas
        lp.xValueAxis.valueMin = 0 # Valor mínimo del eje X
        lp.xValueAxis.valueMax = epocas # Valor máximo del eje X

        # Calcular el paso para el eje X
        paso_eje_x = max(1, epocas // 10)  # Tomar al menos 1 y dividir entre 10 valores

        lp.xValueAxis.valueSteps = list(range(0, epocas + 1, paso_eje_x)) # Pasos del eje X
        lp.xValueAxis.labelTextFormat = '%2.0f' # Formato de los valores del eje X
        lp.yValueAxis.valueMin = 0 # Valor mínimo del eje Y
        lp.yValueAxis.valueMax = 1 # Valor máximo del eje Y
        lp.yValueAxis.valueSteps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] # Pasos del eje Y

        drawing.add(lp) # Agregar el objeto LinePlot al objeto Drawing

        # Crear una leyenda
        legend = Legend()
        legend.x = drawing_width - 135  # Posición en X de la leyenda
        legend.y = (drawing_height)/2 + 25  # Posición en Y de la leyenda
        legend.dx = 8   # Espaciado horizontal entre los elementos de la leyenda
        legend.dy = 8   # Espaciado vertical entre los elementos de la leyenda
        legend.fontName = 'Helvetica'  # Tipo de letra de la leyenda

        # Agregar elementos a la leyenda
        legend.colorNamePairs = [
            (lp.lines[0].strokeColor, ''), # Espacio para el color
            (lp.lines[1].strokeColor, ''), # Espacio para el color
            (lp.lines[2].strokeColor, ''), # Espacio para el color
            ('', 'Accuracy'), # Texto de Accuracy
            ('', 'F1 Score'), # Texto de F1 Score
            ('', 'Loss'), # Texto de Loss
            ('', ''), # Espacio para el texto
        ]
        drawing.add(legend)  # Agregar la leyenda al objeto Drawing

        posicionX = (ancho_pagina - drawing_width)/2 # Posición en X
        posicionY = posicionY - drawing_height - (espacio_entre_linea * 15) # Posición en Y

        drawing.drawOn(pdf, posicionX, posicionY) # Dibujar el objeto Drawing en el PDF

        pdf.showPage() # Crear una nueva página
        pdf.save() # Guardar el PDF

        return (reportes_dir + '/' + reporte_name)