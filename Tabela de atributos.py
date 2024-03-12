from qgis._core import QgsMapLayer, QgsWkbTypes, QgsProject
project = QgsProject.instance()

#Data
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('data', QVariant.Int, len=0))
supressao.commitChanges()

#Tipo
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('tipo', QVariant.Int, len=0))
supressao.commitChanges()

#Área ha
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('area ha', QVariant.Int, len=0))
supressao.commitChanges()

#Poli
supressao: QgsMapLayer = project.mapLayersByName('Área de supressão')[0]
supressao.startEditing()
supressao.addAttribute(QgsField('poli', QVariant.Int, len=0))
supressao.commitChanges()

