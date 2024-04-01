from qgis._core import QgsMapLayer, QgsWkbTypes, QgsProject, QgsExpressionContext, QgsExpression, QgsExpressionContextUtils, QgsField
project = QgsProject.instance()

#Data
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('Data', QVariant.String, len=0))
supressao.commitChanges()

#Tipo
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('Tipo', QVariant.String, len=0))
supressao.commitChanges()

#Área ha
supressao = project.mapLayersByName('Área de supressão')[0]
if supressao is not None:
    supressao.startEditing()
    supressao.addAttribute(QgsField('Área ha', QVariant.String))
    supressao.commitChanges()
    for feature in supressao.getFeatures():
        area = feature.geometry().area() / 10000
        area_arredondado = round(area, 4)
        supressao.changeAttributeValue(feature.id(), supressao.fields().indexFromName('Área ha'), round(area, 4))
        supressao.commitChanges()
        print("ID da Feição: {}, Área: {}".format(feature_id, area))
        print("ÁreaArredondado: {}".format(area_arredondado))
    print("Área em hectares calculada e atribuída com sucesso.")
else:
    print("Camada 'Área de supressão' não encontrada.")

#Poli
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('Poli', QVariant.String, len=0))
supressao.commitChanges()
