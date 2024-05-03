from qgis._core import QgsApplication
from qgis.core import QgsProject, QgsVectorLayer
from qgis.analysis import QgsNativeAlgorithms
import processing

# Inicializar algoritmos nativos do QGIS
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Carregar camadas
supressao = QgsProject.instance().mapLayersByName('Área de supressão')[0]
preservacao = QgsProject.instance().mapLayersByName('Área de preservação permanente')[0]
reserva_legal = QgsProject.instance().mapLayersByName('Reserva legal')[0]

# Definir caminho para o arquivo de saída da dissolução da área de preservação
saida_dissolucao_preservacao = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/4136/Dissolucao_preservacao.shp"

# Executar operação de dissolução na área de preservação
params_dissolucao_preservacao = {
    'INPUT': preservacao,
    'FIELD': None,  # Campo de dissolução (None para dissolver tudo)
    'OUTPUT': saida_dissolucao_preservacao
}

result_dissolucao_preservacao = processing.run("native:dissolve", params_dissolucao_preservacao)

# Verificar se a operação de dissolução da área de preservação foi bem-sucedida
if result_dissolucao_preservacao and result_dissolucao_preservacao['OUTPUT']:
    print("Operação de dissolução da área de preservação concluída com sucesso. O arquivo de saída foi salvo em:",
          saida_dissolucao_preservacao)

    # Definir caminho para o arquivo de saída da interseção com a área de supressão
    saida_interseccao_sup_press_dissolvido = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/4136/Interseccao_sup_pres_dissolvido.shp"

    # Executar operação de interseção com a área de supressão
    params_interseccao = {
        'INPUT': supressao,
        'OVERLAY': result_dissolucao_preservacao['OUTPUT'],  # Utiliza a camada de preservação dissolvida como entrada
        'OUTPUT': saida_interseccao_sup_press_dissolvido
    }

    result_interseccao_sup_press_dissolvido = processing.run("native:intersection", params_interseccao)

    # Verificar se a operação de interseção foi bem-sucedida
    if result_interseccao_sup_press_dissolvido and result_interseccao_sup_press_dissolvido['OUTPUT']:
        print("Operação de interseção com a área de supressão concluída com sucesso. O arquivo de saída foi salvo em:",
              saida_interseccao_sup_press_dissolvido)

# Fazer a diferença com a área de supressão
diferenca_sup_press_dissolvido = processing.run("native:difference", {'INPUT': supressao, 'OVERLAY':
    result_interseccao_sup_press_dissolvido['OUTPUT'], 'OUTPUT': 'memory:'})

if diferenca_sup_press_dissolvido and 'OUTPUT' in diferenca_sup_press_dissolvido:
    print("Operação de diferença com a área de supressão concluída com sucesso.")

    # Definir caminho para o arquivo de saída da interseção com a reserva legal
    saida_interseccao_reserva_legal = "C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/4136/Interseccao_diferenca_sup_rl.shp"

    # Executar operação de interseção com a reserva legal
    params_interseccao_rl = {
        'INPUT': reserva_legal,
        'OVERLAY': diferenca_sup_press_dissolvido['OUTPUT'],
        # Utiliza a camada resultante da diferença com a área de supressão como entrada
        'OUTPUT': saida_interseccao_reserva_legal
    }

    result_interseccao_rl = processing.run("native:intersection", params_interseccao_rl)

    # Verificar se a operação de interseção foi bem-sucedida
    if result_interseccao_rl and 'OUTPUT' in result_interseccao_rl:
        print("Operação de interseção com a reserva legal concluída com sucesso. O arquivo de saída foi salvo em:",
              saida_interseccao_reserva_legal)

        # Fazer a diferença com o shapefile resultante da diferença com a área de supressão
        diferenca_interseccao_sup_rl = processing.run("native:difference",
                                                      {'INPUT': diferenca_sup_press_dissolvido['OUTPUT'],
                                                       'OVERLAY': result_interseccao_rl['OUTPUT'],
                                                       'OUTPUT': 'C:/Users/raissa.alves/Desktop/GEGEO/Alertas/2024/4136/Diferenca_interseccao_sup_rl.shp'})

        if diferenca_interseccao_sup_rl and 'OUTPUT' in diferenca_interseccao_sup_rl:
            print(
                "Operação de diferença com o shapefile resultante da diferença com a área de supressão concluída com sucesso.")
        else:
            print(
                "Falha ao executar a operação de diferença com o shapefile resultante da diferença com a área de supressão.")
    else:
        print("Falha ao executar a operação de interseção com a reserva legal.")
else:
    print("Falha ao executar a operação de diferença com a área de supressão.")

