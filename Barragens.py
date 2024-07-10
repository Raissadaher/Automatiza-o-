from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProcessingFeatureSourceDefinition,
    QgsField
)
from qgis import processing
from qgis.utils import iface

# Obter a camada "Barragens Cadastradas - Plano Estadual de Segurança de Barragens"
barragens_cadastradas = QgsProject.instance().mapLayersByName('Barragens Cadastradas - Plano Estadual de Segurança de Barragens')[0]

# Transformar para o CRS 31982
crs_31982 = QgsCoordinateReferenceSystem('EPSG:31982')
transform_context = QgsProject.instance().transformContext()
transform = QgsCoordinateTransform(barragens_cadastradas.crs(), crs_31982, transform_context)

# Criar uma nova camada temporária com CRS transformado
transformed_layer = QgsVectorLayer('Point?crs=EPSG:31982', 'TransformedBarragensCadastradas', 'memory')
transformed_layer_data = transformed_layer.dataProvider()

# Adicionar os campos da camada original à nova camada
transformed_layer_data.addAttributes(barragens_cadastradas.fields())
transformed_layer.updateFields()

# Transformar e adicionar as feições à nova camada
for feature in barragens_cadastradas.getFeatures():
    geom = feature.geometry()
    geom.transform(transform)
    new_feature = QgsFeature(feature)
    new_feature.setGeometry(geom)
    transformed_layer_data.addFeature(new_feature)

# Adicionar a camada transformada ao projeto
QgsProject.instance().addMapLayer(transformed_layer)

# Aplicar buffer de 50 metros
buffer_params = {
    'INPUT': transformed_layer,
    'DISTANCE': 50,
    'SEGMENTS': 10,
    'END_CAP_STYLE': 0,
    'JOIN_STYLE': 0,
    'MITER_LIMIT': 2,
    'DISSOLVE': False,
    'OUTPUT': 'memory:BufferedBarragensCadastradas'
}
buffered_barragens_cadastradas = processing.run("native:buffer", buffer_params)['OUTPUT']

# Adicionar a camada de buffer ao projeto para verificação
QgsProject.instance().addMapLayer(buffered_barragens_cadastradas)

# Obter a camada "Barragens Não Cadastradas"
barragens_nao_cadastradas = QgsProject.instance().mapLayersByName('Barragens Não Cadastradas')[0]

# Transformar a camada "Barragens Não Cadastradas" para o CRS 31982 (se necessário)
if barragens_nao_cadastradas.crs() != crs_31982:
    transform_nao_cadastradas = QgsCoordinateTransform(barragens_nao_cadastradas.crs(), crs_31982, transform_context)
    nao_cadastradas_transformed = QgsVectorLayer('Polygon?crs=EPSG:31982', 'TransformedBarragensNaoCadastradas', 'memory')
    nao_cadastradas_transformed_data = nao_cadastradas_transformed.dataProvider()

    # Adicionar os campos da camada original à nova camada
    nao_cadastradas_transformed_data.addAttributes(barragens_nao_cadastradas.fields())
    nao_cadastradas_transformed.updateFields()

    # Transformar e adicionar as feições à nova camada
    for feature in barragens_nao_cadastradas.getFeatures():
        geom = feature.geometry()
        geom.transform(transform_nao_cadastradas)
        new_feature = QgsFeature(feature)
        new_feature.setGeometry(geom)
        nao_cadastradas_transformed_data.addFeature(new_feature)

    # Adicionar a camada transformada ao projeto
    QgsProject.instance().addMapLayer(nao_cadastradas_transformed)
else:
    nao_cadastradas_transformed = barragens_nao_cadastradas

# Identificar as áreas não sobrepostas
difference_params = {
    'INPUT': QgsProcessingFeatureSourceDefinition(nao_cadastradas_transformed.id(), True),
    'OVERLAY': QgsProcessingFeatureSourceDefinition(buffered_barragens_cadastradas.id(), True),
    'OUTPUT': 'memory:DifferencedBarragens'
}
differenced_barragens = processing.run("native:difference", difference_params)['OUTPUT']

# Adicionar a camada de diferença ao projeto
QgsProject.instance().addMapLayer(differenced_barragens)

# Filtrar feições não sobrepostas
non_overlapping_features = []
for feature in differenced_barragens.getFeatures():
    non_overlapping_features.append(feature)

# Criar uma nova camada temporária para as feições não sobrepostas
non_overlapping_layer = QgsVectorLayer('Polygon?crs=EPSG:31982', 'NonOverlappingBarragens', 'memory')
non_overlapping_data = non_overlapping_layer.dataProvider()

# Adicionar os campos da camada original à nova camada
non_overlapping_data.addAttributes(differenced_barragens.fields())
non_overlapping_layer.updateFields()

# Adicionar as feições não sobrepostas à nova camada
for feature in non_overlapping_features:
    non_overlapping_data.addFeature(feature)

# Adicionar a camada de não sobreposição ao projeto
QgsProject.instance().addMapLayer(non_overlapping_layer)
