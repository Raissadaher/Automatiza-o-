from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsFeature,
    QgsGeometry, edit,
)

# Obtém a instância do projeto
project = QgsProject.instance()

# Carrega a camada original de supressão
supressao_layers = project.mapLayersByName('Área de supressão')

# Verifica se a camada original foi carregada com sucesso
if supressao_layers:
    supressao = supressao_layers[0]
    crs = supressao.crs()

    # Cria a camada de centroides com base na camada de supressão
    centroides = QgsVectorLayer(
        'Point?crs=' + crs.authid() + '&field=Área ha:double&field=Tipo:string&field=Data:string&field=id:int',
        'Centroides temp', 'memory'
    )

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
            feature_id = source_feature.attribute("id")

            centroid_feature = QgsFeature()
            centroid_feature.setGeometry(centroid)
            centroid_feature.setAttributes([area, tipo, data, feature_id])
            centroides.addFeature(centroid_feature)

        centroides.commitChanges()

        # Exporta a camada de centroides para o formato Shapefile com fuso SIRGAS 2000
        crs_sirgas = QgsCoordinateReferenceSystem('EPSG:4674')
        path = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/9753 Fazenda Bateias - Gordura/teste/Centroides temp.shp"
        result = QgsVectorFileWriter.writeAsVectorFormat(centroides, path, "utf-8", crs_sirgas, "ESRI Shapefile")

        if result == QgsVectorFileWriter.NoError:
            print("Camada de centroides exportada com sucesso para o formato SIRGAS 2000.")
        else:
            print("Falha ao exportar a camada de centroides para o formato SIRGAS 2000. Código de erro:", result)

        # Carrega a camada de centroides
        centroides_sirgas = QgsVectorLayer(path, "Centroides SIRGAS 2000", "ogr")

        # Adiciona os campos "Lat" e "Long" à tabela de atributos com precisão de 4 casas decimais
        if centroides_sirgas:
            with edit(centroides_sirgas):
                centroides_sirgas.addAttribute(QgsField("Lat", QVariant.Double, len=10, prec=4))
                centroides_sirgas.addAttribute(QgsField("Long", QVariant.Double, len=10, prec=4))

            # Preenche os campos "Lat" e "Long" com os valores das coordenadas dos centroides
            with edit(centroides_sirgas):
                for feature in centroides_sirgas.getFeatures():
                    centroid = feature.geometry().centroid().asPoint()
                    lat = round(centroid.y(), 4)
                    long = round(centroid.x(), 4)
                    feature.setAttribute("Lat", lat)
                    feature.setAttribute("Long", long)
                    centroides_sirgas.updateFeature(feature)

            print(
                "Coordenadas de latitude e longitude adicionadas à tabela de atributos com precisão de 4 casas decimais.")
        else:
            print("Falha ao carregar a camada de centroides SIRGAS 2000.")

    else:
        print("Falha ao criar a camada de centroides.")
else:
    print("Falha ao carregar a camada original de supressão.")


# Caminho para o arquivo shapefile da camada "Centroides"
path_to_layer = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/9753 Fazenda Bateias - Gordura/teste/Centroides.shp"

# Nome da camada no QGIS
layer_name = "Centroides temp"

# Carrega a camada
centroides_layer = QgsVectorLayer(path_to_layer, layer_name, "ogr")

# Verifica se a camada foi carregada com sucesso
if not centroides_layer.isValid():
    print("Falha ao carregar a camada 'Centroides'.")
else:
    # Adiciona a camada ao projeto do QGIS
    QgsProject.instance().addMapLayer(centroides_layer)
    print("Camada 'Centroides' adicionada ao projeto do QGIS com sucesso.")
