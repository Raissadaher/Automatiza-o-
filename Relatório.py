import random
import math
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor
from qgis.gui import QgsMapCanvas
from qgis.core import *
from qgis.core import QgsProject, QgsCoordinateReferenceSystem
from qgis.utils import iface
from datetime import date
from qgis.core import QgsLayoutItemScaleBar, QgsProject, QgsLayoutItemMapOverview, QgsSimpleFillSymbolLayer, \
    QgsLineSymbol
from qgis.core import QgsProject, QgsLayoutItemMap, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes, QgsFillSymbol
from qgis.core import QgsSymbolLayer, QgsSymbolRenderContext, QgsGeometry, Qgis

# variaveis globais
project = QgsProject.instance()
manager = project.layoutManager()
layout = QgsPrintLayout(project)
page = QgsLayoutItemPage(layout)
page.setPageSize('A4', QgsLayoutItemPage.Orientation.Portrait)
layoutName = f"pagina_1_{random.randint(1, 500)}"
layout.initializeDefaults()
layout.setName(layoutName)
pageSize = QgsLayoutSize(210, 297, QgsUnitTypes.LayoutMillimeters)  # A4 size in portrait mode
layout.pageCollection().page(0).setPageSize(pageSize)
manager.addLayout(layout)

# Adicionando Poligono Maior
rectangle_maior = QgsLayoutItemShape(layout)
rectangle_maior.setShapeType(QgsLayoutItemShape.Rectangle)
rectangle_maior.setRect(0, 0, 0, 0)
layout.addLayoutItem(rectangle_maior)
rectangle_maior.attemptMove(QgsLayoutPoint(3, 2, QgsUnitTypes.LayoutMillimeters))
rectangle_maior.attemptResize(QgsLayoutSize(203.891, 290.855, QgsUnitTypes.LayoutMillimeters))
iface.openLayoutDesigner(layout)

# Isso adiciona rotulos ao mapa

layer = project.mapLayersByName('Área do imóvel')[0]
municipio = ""
nome = ""
cpf = ""
propriedade = ""
fonte_do_alerta = ""
id_alerta = ""
numero_car = ""
status_car = ""
area_imovel = ""
vegetação_nativa = ""
app_total = ""
rl_averbada = ""
rl_proposta = ""
area_supressao_fora = ""
area_supressao_rl = ""
area_supressao_app = ""
fitofisionomia  = ""
wkt = ""

if layer is not None:
    for feature in layer.getFeatures():
        municipio = feature['municipio']
        nome = feature['proprietar']
        cpf = feature['cpf_cnpj']
        propriedade = feature['nm_imovel']
        numero_car = feature['cod_imovel']
        area_imovel = feature['num_area']



dados = 'Municipio: ' + municipio + '\n' + 'Proprietário: ' + nome + '\n' + 'CPF/CNPJ: ' + cpf + '\n' + 'Propriedade: ' + propriedade + '\n' + 'Fonte do Alerta: MapBiomas' + '\n' + 'ID do Alerta:' + '\n'
title = QgsLayoutItemLabel(layout)
title.setText(dados)
title.setFont(QFont("Arial", 12))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptResize(QgsLayoutSize(203.891,34.305, QgsUnitTypes.LayoutMillimeters))
title.attemptMove(QgsLayoutPoint(3, 2, QgsUnitTypes.LayoutMillimeters))

#total_sum = layer.aggregate(QgsAggregateCalculator.Sum, "my_field_name")

layer = project.mapLayersByName('Área do imóvel')[0]
numero_car = ""
status_car = ""
area_imovel = ""
vegetação_nativa = ""
app_total = ""

wkt = ""

if layer is not None:
    for feature in layer.getFeatures():
        numero_car = feature['cod_imovel']
        area_imovel = feature['num_area']



dados = 'Municipio: ' + municipio + '\n' + 'Proprietário: ' + nome + '\n' + 'CPF/CNPJ: ' + cpf + '\n' + 'Propriedade: ' + propriedade + '\n' + 'Fonte do Alerta: MapBiomas' + '\n' + 'ID do Alerta:' + '\n'
title = QgsLayoutItemLabel(layout)
title.setText(dados)
title.setFont(QFont("Arial", 12))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptResize(QgsLayoutSize(203.891,34.305, QgsUnitTypes.LayoutMillimeters))
title.attemptMove(QgsLayoutPoint(3, 2, QgsUnitTypes.LayoutMillimeters))