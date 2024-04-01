from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsCoordinateReferenceSystem
from qgis.core import QgsProject, QgsGeometry, QgsVectorFileWriter

# Carrega a camada original
supressao = iface.addVectorLayer("C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/9753 Fazenda Bateias - Gordura/teste/Área de supressão.shp", "Área de supressão", "ogr")

# Verifica se a camada original foi carregada com sucesso
if supressao:
    # Define o CRS da camada de centroides como o mesmo da camada original
    crs = supressao.crs()
    centroides = QgsVectorLayer('Point?crs=' + crs.authid() + '&field=Área ha:double&field=Tipo:string&field=Data:string&field=id:int', 'Centroides gerais', 'memory')

    # Verifica se a camada de centroides foi criada com sucesso
    if centroides:
        centroides.startEditing()

        # Adiciona os campos à camada de centroides
        centroides.addAttribute(QgsField('Área ha', QVariant.Double))
        centroides.addAttribute(QgsField('Tipo', QVariant.String))
        centroides.addAttribute(QgsField('Data', QVariant.String))
        centroides.addAttribute(QgsField('id', QVariant.Int))

        # Loop sobre todas as feições da camada original
        for source_feature in supressao.getFeatures():
            geometry = source_feature.geometry()
            centroid = geometry.centroid()
            area = source_feature.attribute("Área ha")
            tipo = source_feature.attribute("Tipo")
            data = source_feature.attribute("Data")
            feature_id = source_feature.id()

            centroid_feature = QgsFeature()
            centroid_feature.setGeometry(centroid)
            centroid_feature.setAttributes([area, tipo, data, feature_id])
            centroides.addFeature(centroid_feature)

        centroides.commitChanges()

        # Adiciona a camada de centroides ao projeto
        QgsProject.instance().addMapLayer(centroides)
    else:
        print("Falha ao criar a camada de centroides.")
else:
    print("Falha ao carregar a camada original.")
    
# Exporta a camada
if centroides:
    crs = centroides.crs()
    path = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/9753 Fazenda Bateias - Gordura/teste/Centroides gerais.shp"
    result = QgsVectorFileWriter.writeAsVectorFormat(centroides, path, "utf-8", crs, "ESRI Shapefile")
    if result == QgsVectorFileWriter.NoError:
        print("Camada de centroides exportada com sucesso.")
    else:
        print("Falha ao exportar a camada de centroides. Código de erro:", result)
else:
    print("Camada de centroides não encontrada.")



