from qgis._core import QgsMapLayer, QgsWkbTypes, QgsProject

project = QgsProject.instance()

#Limite do imóvel
area_imovel :QgsMapLayer = project.mapLayersByName('Área do imóvel')[0]
print(area_imovel.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area do imovel.qml'))
if area_imovel.geometryType() == QgsWkbTypes.PolygonGeometry:
    area_imovel.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area do imovel.qml')
    area_imovel.triggerRepaint()

# Área de preservação permanente total
app :QgsMapLayer = project.mapLayersByName('Área de preservação permanente')[0]
print(app.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/APP Total.qml'))
if app.geometryType() == QgsWkbTypes.PolygonGeometry:
    app.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/APP Total.qml')
    app.triggerRepaint()

# Reserva Legal
rl :QgsMapLayer = project.mapLayersByName('Reserva legal')[0]
print(rl.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Reserva legal.qml'))
if rl.geometryType() == QgsWkbTypes.PolygonGeometry:
    rl.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Reserva legal.qml')
    rl.triggerRepaint()

#Área de supressão
area_supressao :QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
print(area_supressao.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de supressao.qml'))
if area_supressao.geometryType() == QgsWkbTypes.PolygonGeometry:
    area_supressao.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de supressao.qml')
    area_supressao.triggerRepaint()

#Área de supressão em APP
area_supressao_app :QgsMapLayer = project.mapLayersByName('Supressão APP')[0]
print(area_supressao_app.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de supressao.qml'))
if area_supressao_app.geometryType() == QgsWkbTypes.PolygonGeometry:
    area_supressao_app.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de supressao.qml')
    area_supressao_app.triggerRepaint()

#Área de supressão em RL
area_supressao_rl :QgsMapLayer = project.mapLayersByName('Supressão RL')[0]
print(area_supressao_rl.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de supressao.qml'))
if area_supressao_rl.geometryType() == QgsWkbTypes.PolygonGeometry:
    area_supressao_rl.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de supressao.qml')
    area_supressao_rl.triggerRepaint()


dano :QgsMapLayer = project.mapLayersByName('Dano')[0]
print(dano.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area danificada.qml'))
if dano.geometryType() == QgsWkbTypes.PolygonGeometry:
    dano.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area danificada.qml')
    dano.triggerRepaint()

area_uso_restrito :QgsMapLayer = project.mapLayersByName('Área de uso restrito')[0]
print(area_uso_restrito.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de uso restrito.qml'))
if area_uso_restrito.geometryType() == QgsWkbTypes.PolygonGeometry:
    area_uso_restrito.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area de uso restrito.qml')
    area_uso_restrito.triggerRepaint()

uc :QgsMapLayer = project.mapLayersByName('Unidade de conservação')[0]
print(uc.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Unidade de Conservacao.qml'))
if uc.geometryType() == QgsWkbTypes.PolygonGeometry:
    uc.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Unidade de Conservacao.qml')
    uc.triggerRepaint()

servidao :QgsMapLayer = project.mapLayersByName('Servidão administrativa')[0]
print(servidao.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Servidao administrativa.qml'))
if servidao.geometryType() == QgsWkbTypes.PolygonGeometry:
    servidao.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Servidao administrativa.qml')
    servidao.triggerRepaint()

area_licenciada :QgsMapLayer = project.mapLayersByName('Área licenciada')[0]
print(area_licenciada.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area licenciada.qml'))
if area_licenciada.geometryType() == QgsWkbTypes.PolygonGeometry:
    area_licenciada.loadNamedStyle('C:/Users/raissa.alves/Documents/Vetores/Estilos_QGIS/Area licenciada.qml')
    area_licenciada.triggerRepaint()


