from qgis.core import QgsProject, QgsVectorLayer, QgsFeature, QgsField, QgsGeometry
from qgis.PyQt.QtCore import QVariant
import processing

# Obter as camadas
layer_barragens_cadastradas = QgsProject.instance().mapLayersByName('Barragens Cadastradas - Plano Estadual de Segurança de Barragens')[0]
layer_barragens_2018 = QgsProject.instance().mapLayersByName('Barragens 2018  (>1 ha)')[0]

# Verificar se as camadas foram carregadas corretamente
if layer_barragens_cadastradas is None or layer_barragens_2018 is None:
    print("Uma ou ambas as camadas não foram encontradas.")
else:
    # Verificar se as camadas estão no mesmo CRS
    if layer_barragens_cadastradas.crs() != layer_barragens_2018.crs():
        print("As camadas estão em sistemas de coordenadas diferentes.")
        exit()

    # Criar buffer na camada de barragens cadastradas com tamanho ajustado
    buffer_distance = 0.00045  # Ajuste conforme necessário
    buffer_layer = QgsVectorLayer(f"Polygon?crs={layer_barragens_cadastradas.crs().authid()}", "Buffer", "memory")
    buffer_layer_data = buffer_layer.dataProvider()
    buffer_layer_data.addAttributes([QgsField("id", QVariant.Int)])
    buffer_layer.updateFields()
    
    features = layer_barragens_cadastradas.getFeatures()
    buffer_features = []
    for feature in features:
        buffered_geom = feature.geometry().buffer(buffer_distance, 5)
        if buffered_geom.isGeosValid():
            buffer_feature = QgsFeature()
            buffer_feature.setGeometry(buffered_geom)
            buffer_feature.setAttributes([feature.id()])
            buffer_features.append(buffer_feature)
    
    buffer_layer_data.addFeatures(buffer_features)
    QgsProject.instance().addMapLayer(buffer_layer)

    # Verificar se o buffer contém feições
    buffer_feature_count = buffer_layer.featureCount()
    print(f"Número de feições no buffer: {buffer_feature_count}")
    if buffer_feature_count == 0:
        print("O buffer está vazio. Verifique o processo de criação do buffer.")
        exit()
    
    # Seleção por localização com predicados ajustados
    try:
        params = {
            'INPUT': layer_barragens_2018,
            'PREDICATE': [0],  # Tocar e sobrepor
            'INTERSECT': buffer_layer,
            'METHOD': 0  # Selecionar novos
        }
        processing.run("qgis:selectbylocation", params)
        print("Seleção por localização realizada.")
    except Exception as e:
        print("Erro ao executar a seleção por localização:", e)
        exit()
    
    # Verificar se houve seleção de feições
    selected_count = layer_barragens_2018.selectedFeatureCount()
    print(f"Número de feições selecionadas: {selected_count}")
    
    # Inverter a seleção
    layer_barragens_2018.invertSelection()
    inverted_count = layer_barragens_2018.selectedFeatureCount()
    print(f"Número de feições selecionadas após inversão: {inverted_count}")
