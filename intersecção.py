from qgis.core import QgsApplication, QgsProject, QgsVectorLayer
from qgis.analysis import QgsNativeAlgorithms
import processing

# Inicializar a aplicação QGIS (necessário apenas se você estiver rodando fora do QGIS)
# app = QgsApplication([], False)
# app.initQgis()

# Inicializar algoritmos nativos do QGIS
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Carregar camadas
supressao = QgsProject.instance().mapLayersByName('Área de supressão')[0]
preservacao = QgsProject.instance().mapLayersByName('Área de preservação permanente')[0]
reserva_legal = QgsProject.instance().mapLayersByName('Reserva legal')[0]

# Executar operação de dissolução na área de preservação
params_dissolucao_preservacao = {
    'INPUT': preservacao,
    'FIELD': None,  # Campo de dissolução (None para dissolver tudo)
    'OUTPUT': 'memory:'
}

result_dissolucao_preservacao = processing.run("native:dissolve", params_dissolucao_preservacao)
if result_dissolucao_preservacao and result_dissolucao_preservacao['OUTPUT']:
    layer_dissolucao = result_dissolucao_preservacao['OUTPUT']
    layer_dissolucao.setName("APP Dissolvida")
    QgsProject.instance().addMapLayer(layer_dissolucao)

    # Executar operação de interseção com a área de supressão
    params_interseccao = {
        'INPUT': supressao,
        'OVERLAY': layer_dissolucao,  # Utiliza a camada de preservação dissolvida como entrada
        'OUTPUT': 'memory:'
    }

    result_interseccao_sup_press_dissolvido = processing.run("native:intersection", params_interseccao)
    if result_interseccao_sup_press_dissolvido and result_interseccao_sup_press_dissolvido['OUTPUT']:
        layer_interseccao = result_interseccao_sup_press_dissolvido['OUTPUT']
        layer_interseccao.setName("Área de supressão APP")
        QgsProject.instance().addMapLayer(layer_interseccao)

        # Fazer a diferença com a área de supressão
        diferenca_sup_press_dissolvido = processing.run("native:difference", {
            'INPUT': supressao,
            'OVERLAY': layer_interseccao,
            'OUTPUT': 'memory:'
        })

        if diferenca_sup_press_dissolvido and 'OUTPUT' in diferenca_sup_press_dissolvido:
            layer_diferenca = diferenca_sup_press_dissolvido['OUTPUT']
            layer_diferenca.setName("Diferença da supressão com a app")
            QgsProject.instance().addMapLayer(layer_diferenca)

            # Executar operação de interseção com a reserva legal
            params_interseccao_rl = {
                'INPUT': reserva_legal,
                'OVERLAY': layer_diferenca,
                'OUTPUT': 'memory:'
            }

            result_interseccao_rl = processing.run("native:intersection", params_interseccao_rl)
            if result_interseccao_rl and 'OUTPUT' in result_interseccao_rl:
                layer_interseccao_rl = result_interseccao_rl['OUTPUT']
                layer_interseccao_rl.setName("Área de supressão em RL")
                QgsProject.instance().addMapLayer(layer_interseccao_rl)

                # Fazer a diferença com o shapefile resultante da diferença com a área de supressão
                diferenca_interseccao_sup_rl = processing.run("native:difference", {
                    'INPUT': layer_diferenca,
                    'OVERLAY': layer_interseccao_rl,
                    'OUTPUT': 'memory:'
                })

                if diferenca_interseccao_sup_rl and 'OUTPUT' in diferenca_interseccao_sup_rl:
                    layer_diferenca_final = diferenca_interseccao_sup_rl['OUTPUT']
                    layer_diferenca_final.setName("Área de supressão fora")
                    QgsProject.instance().addMapLayer(layer_diferenca_final)
                else:
                    print("Falha ao executar a operação de diferença com o shapefile resultante da diferença com a área de supressão.")
            else:
                print("Falha ao executar a operação de interseção com a reserva legal.")
        else:
            print("Falha ao executar a operação de diferença com a área de supressão.")
    else:
        print("Falha ao executar a operação de interseção com a área de supressão.")
else:
    print("Falha ao executar a operação de dissolução da área de preservação.")

# Finalizar a aplicação QGIS (necessário apenas se você estiver rodando fora do QGIS)
# app.exitQgis()
