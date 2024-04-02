from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsField, QgsCoordinateReferenceSystem, QgsProject
from qgis.core import QgsVectorFileWriter, edit

project = QgsProject.instance()

# Carrega a camada original
supressao = iface.addVectorLayer(
    "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/9753 Fazenda Bateias - Gordura/teste/Área de supressão.shp",
    "Área de supressão", "ogr")

# Verifica se a camada original foi carregada com sucesso
if supressao:
    # Define o CRS da camada de centroides como o mesmo da camada original
    crs = supressao.crs()
    centroides = QgsVectorLayer(
        'Point?crs=' + crs.authid() + '&field=Área ha:double&field=Tipo:string&field=Data:string&field=id:int',
        'Centroides temp', 'memory')

    # Verifica se a camada de centroides foi criada com sucesso
    if centroides:
        centroides.startEditing()

        # Adiciona os campos à camada de centroides
        centroides.addAttribute(QgsField('Área ha', QVariant.Double))
        centroides.addAttribute(QgsField('Tipo', QVariant.String))
        centroides.addAttribute(QgsField('Data', QVariant.String))

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
    crs = QgsCoordinateReferenceSystem('EPSG:4674')
    path = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/9753 Fazenda Bateias - Gordura/teste/Centroides temp.shp"
    result = QgsVectorFileWriter.writeAsVectorFormat(centroides, path, "utf-8", crs, "ESRI Shapefile")
    if result == QgsVectorFileWriter.NoError:
        print("Camada de centroides exportada com sucesso.")
    else:
        print("Falha ao exportar a camada de centroides. Código de erro:", result)
else:
    print("Camada de centroides não encontrada.")

# Carrega a camada de centroides
centroides = iface.addVectorLayer(path, "Centroides gerais", "ogr")

# Adiciona os campos "Lat" e "Long" à tabela de atributos
if centroides:
    with edit(centroides):
        centroides.addAttribute(QgsField("Lat", QVariant.Double))
        centroides.addAttribute(QgsField("Long", QVariant.Double))
    print("Campos 'Lat' e 'Long' adicionados à tabela de atributos.")

    # Atualiza a camada de centroides
    centroides.updateFields()

    # Preenche os campos "Lat" e "Long" com os valores das coordenadas dos centroides
# Preenche os campos "Lat" e "Long" com os valores das coordenadas dos centroides, com precisão de 4 casas decimais
with edit(centroides):
    for feature in centroides.getFeatures():
        centroid = feature.geometry().centroid().asPoint()
        lat = round(centroid.y(), 4)
        long = round(centroid.x(), 4)
        feature.setAttribute("Lat", lat)
        feature.setAttribute("Long", long)
        centroides.updateFeature(feature)
print("Coordenadas de latitude e longitude adicionadas à tabela de atributos com precisão de 4 casas decimais.")


