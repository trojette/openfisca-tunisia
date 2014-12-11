# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

# from openfisca_core.statshelpers import mark_weighted_percentiles

from .base import *


ALL = [x[1] for x in QUIMEN]


# def _typ_men(isol, af_nbenf):
#    '''
#    type de menage
#    'men'
#    TODO: prendre les enfants du ménages et non ceux de la famille
#    '''
#    _0_kid = af_nbenf == 0
#    _1_kid = af_nbenf == 1
#    _2_kid = af_nbenf == 2
#    _3_kid = af_nbenf >= 3
#
#    return (0*(isol & _0_kid) + # Célibataire
#            1*(not_(isol) & _0_kid) + # Couple sans enfants
#            2*(not_(isol) & _1_kid) + # Couple un enfant
#            3*(not_(isol) & _2_kid) + # Couple deux enfants
#            4*(not_(isol) & _3_kid) + # Couple trois enfants et plus
#            5*(isol & _1_kid) + # Famille monoparentale un enfant
#            6*(isol & _2_kid) + # Famille monoparentale deux enfants
#            7*(isol & _3_kid) ) # Famille monoparentale trois enfants et plus


@reference_formula
class revdisp_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Revenu disponible individuel"

    def function(self, rev_trav, pen, rev_cap, psoc, impo):
        '''
        Revenu disponible
        'ind'
        '''
        return rev_trav + pen + rev_cap + psoc + impo

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class revdisp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Revenu disponible du ménage"

    def function(self, revdisp_i):
        '''
        Revenu disponible - ménage
        'men'
        '''
        return self.sum_by_entity(revdisp_i)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class rev_trav(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_trav"

    def function(self, sali):
        '''Revenu du travail'''
        return sali  # + beap + bic + bnc  TODO

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# def _pen(rstnet, alr, alv, rto):
#    '''Pensions'''
#    return rstnet #+ alr + alv + rto TODO
#
# def _rstnet(pen):
#    '''Retraites nettes'''
#    return pen

@reference_formula
class rev_cap(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"rev_cap"

    def function(self, rfon):
        '''Revenus du patrimoine'''  # TODO
        return rfon

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# def _psoc(pfam):
#    '''Prestations sociales'''
#    return pfam
#
# def _pfam(af,s):
#    ''' Prestations familiales '''
#    return af


@reference_formula
class impo(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"impo"

    def function(self, irpp):
        '''Impôts directs'''
        return irpp

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


## def _decile(nivvie, wprm):
##     '''
##     Décile de niveau de vie
##     'men'
##     '''
##     labels = arange(1, 11)
##     method = 2
##     decile = mark_weighted_percentiles(nivvie, labels, wprm, method, return_quantiles = False)
##     return decile
