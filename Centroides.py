from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext,
    edit
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
    if centroides.isValid():
        centroides.startEditing()

        # Adiciona os campos à camada de centroides
        centroides.dataProvider().addAttributes([
            QgsField('Área ha', QVariant.Double),
            QgsField('Tipo', QVariant.String),
            QgsField('Data', QVariant.String),
            QgsField('id', QVariant.Int)
        ])
        centroides.updateFields()

        # Loop sobre todas as feições da camada original
        for source_feature in supressao.getFeatures():
            geometry = source_feature.geometry()
            centroid = geometry.centroid()
            area = source_feature['Área_ha']
            tipo = source_feature['Tipo']
            data = source_feature['Data']
            feature_id = source_feature['id']

            centroid_feature = QgsFeature(centroides.fields())
            centroid_feature.setGeometry(centroid)
            centroid_feature.setAttributes([area, tipo, data, feature_id])
            centroides.addFeature(centroid_feature)

        centroides.commitChanges()

        # Transforma a camada de centroides para o CRS SIRGAS 2000
        crs_sirgas = QgsCoordinateReferenceSystem('EPSG:4674')
        transform = QgsCoordinateTransform(crs, crs_sirgas, QgsProject.instance())
        centroides_sirgas = QgsVectorLayer(
            'Point?crs=' + crs_sirgas.authid() + '&field=Área ha:double&field=Tipo:string&field=Data:string&field=id:int&field=Lat:double&field=Long:double',
            'Centroides temp SIRGAS 2000', 'memory'
        )

        if centroides_sirgas.isValid():
            centroides_sirgas.startEditing()
            centroides_sirgas.dataProvider().addAttributes([
                QgsField('Lat', QVariant.Double, len=10, prec=4),
                QgsField('Long', QVariant.Double, len=10, prec=4)
            ])
            centroides_sirgas.updateFields()

            for feature in centroides.getFeatures():
                geometry = feature.geometry()
                geometry.transform(transform)
                centroid = geometry.centroid().asPoint()
                lat = round(centroid.y(), 4)
                long = round(centroid.x(), 4)
                attributes = feature.attributes()
                attributes.extend([lat, long])

                centroid_feature = QgsFeature(centroides_sirgas.fields())
                centroid_feature.setGeometry(geometry)
                centroid_feature.setAttributes(attributes)
                centroides_sirgas.addFeature(centroid_feature)

            centroides_sirgas.commitChanges()

            # Adiciona a camada transformada ao projeto
            QgsProject.instance().addMapLayer(centroides_sirgas)
            print("Camada 'Centroides temp SIRGAS 2000' adicionada ao projeto do QGIS com sucesso.")

        else:
            print("Falha ao criar a camada de centroides SIRGAS 2000.")

    else:
        print("Falha ao criar a camada de centroides.")
else:
    print("Falha ao carregar a camada original de supressão.")
