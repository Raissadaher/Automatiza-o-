from qgis.core import QgsVectorLayer, QgsProject
from qgis.utils import iface

# Defina a URI do serviço WFS para a primeira camada
uri1 = "https://siga.meioambiente.go.gov.br/geoserver/geonode/barramentos_2018_1ha/ows?service=WFS&version=1.0.0&request=GetFeature&typename=geonode:barramentos_2018_1ha&srsname=EPSG:4674"

# Defina a URI do serviço WFS para a segunda camada
uri2 = "https://siga.meioambiente.go.gov.br/geoserver/geonode/vw_barragem_plano/ows?service=WFS&version=1.0.0&request=GetFeature&typename=geonode:vw_barragem_plano&srsname=EPSG:4674"

# Carregue a primeira camada WFS
vlayer1 = QgsVectorLayer(uri1, "Barragens 2018 (>1 ha)", "WFS")

# Verifique se a primeira camada foi carregada com sucesso
if not vlayer1.isValid():
    print("Primeira camada falhou ao carregar!")
else:
    print("Primeira camada carregada com sucesso!")
    # Zoom para a extensão da primeira camada
    iface.mapCanvas().setExtent(vlayer1.extent())
    iface.mapCanvas().refresh()
    # Verificar o número de feições carregadas na primeira camada
    count1 = vlayer1.featureCount()
    print(f"Number of features in first layer: {count1}")
    # Adicione a primeira camada ao projeto QGIS
    QgsProject.instance().addMapLayer(vlayer1)

# Carregue a segunda camada WFS
vlayer2 = QgsVectorLayer(uri2, "Barragens Cadastradas - Plano Estadual de Segurança de Barragens", "WFS")

# Verifique se a segunda camada foi carregada com sucesso
if not vlayer2.isValid():
    print("Segunda camada falhou ao carregar!")
else:
    print("Segunda camada carregada com sucesso!")
    # Zoom para a extensão da segunda camada
    iface.mapCanvas().setExtent(vlayer2.extent())
    iface.mapCanvas().refresh()
    # Verificar o número de feições carregadas na segunda camada
    count2 = vlayer2.featureCount()
    print(f"Number of features in second layer: {count2}")
    # Adicione a segunda camada ao projeto QGIS
    QgsProject.instance().addMapLayer(vlayer2)


