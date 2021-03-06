# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


CAT = Enum(['rsna', 'rsa', 'rsaa', 'rtns', 'rtte', 're', 'rtfr', 'raic', 'cnrps_sal', 'cnrps_pen'])


# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type


class categorie_salarie(Variable):
    column = EnumCol(CAT, default = 0)
    entity_class = Individus


class inv(Variable):
    column = BoolCol
    label = u'invalide'
    entity_class = Individus


class activite(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Individus


class boursier(Variable):
    column = BoolCol()
    entity_class = Individus





# TODO Remove Me


class prestations_sociales(Variable):
    column = IntCol
    entity_class = Individus
