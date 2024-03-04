from qgis.core import QgsProject, QgsField, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
from qgis.utils import iface

area_sup = QgsProject.instance().mapLayersByName('Área_de_supressão')[0]
pv = area_sup.dataProvider()

# Adicionar atributo 'areaha'
pv.addAttributes([QgsField('Área ha', QVariant.Double)])
area_sup.updateFields()

expressao1 = QgsExpression('round($area/10000, 4)')  # Use a função round() para definir a precisão
contexto = QgsExpressionContext()
contexto.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(area_sup))

# Forçar início da edição
area_sup.startEditing()

# com edição (area_sup):
for f in area_sup.getFeatures():
    contexto.setFeature(f)
    idx_areaha = f.fieldNameIndex('Área ha')
    if idx_areaha != -1:
        f['Área ha'] = expressao1.evaluate(contexto)
        print(f['Área ha'])  # Mensagem de depuração
        area_sup.updateFeature(f)

# Forçar finalização da edição
area_sup.commitChanges()

# Atualizar a interface gráfica do QGIS
iface.mapCanvas().refresh()


