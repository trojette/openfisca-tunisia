# -*- coding: utf-8 -*-


import datetime
import os
import pandas as pd
import pkg_resources


smig_1990_2010_path = os.path.join(
    pkg_resources.get_distribution('openfisca-tunisia').location,
    'openfisca_tunisia',
    'assets',
    'SMIG-40-48.xlsx',
    )

smig_all_path = os.path.join(
    pkg_resources.get_distribution('openfisca-tunisia').location,
    'openfisca_tunisia',
    'assets',
    'SMIGSMAG.xlsx',
    )


smig_1990_2010 = pd.read_excel(
    smig_1990_2010_path,
    header = 9,
    parse_cols = "B,C,G",
    names = ['smic_horaire', 'smic_mensuel', 'deb'],
    )

smig_40h = smig_1990_2010.loc[:25].copy()
smig_40h['deb'] = pd.to_datetime(smig_40h.deb, dayfirst = True)
smig_40h['fin'] = smig_40h.deb.shift(-1) + datetime.timedelta(days=-1)

smig_48h = smig_1990_2010.loc[37:].copy()
smig_48h.deb = pd.to_datetime(smig_48h.deb, dayfirst = True)
smig_48h['fin'] = smig_48h.deb.shift(-1) + datetime.timedelta(days=-1)
smig_48h.smic_horaire = (smig_48h.smic_horaire * 1000).astype(int)

smig_all = pd.read_excel(
    smig_all_path,
    parse_cols = "A:D",
    names = ['type', 'deb', 'fin', 'smic_horaire'],
    ).sort_values(['type', 'deb'])

smig = smig_all.query("type == 'SMIG'").reset_index(drop = True)

verif = (smig
    .merge(smig_48h, how = 'outer', on = 'deb')
    .query('smic_horaire_x != smic_horaire_y')
    )

header = """<CODE code="smig_horaire" description="SMIG horaire" format="float" type="monetary">
"""
footer = """</CODE>
"""
parts = ["""<VALUE deb="{}" fin="{}" valeur="{}" />
""".format(
    str(smig.deb.loc[i].date()),
    str(smig.fin.loc[i].date()),
    str(smig.horaire.loc[i] / 1000)
    ) for i in range(0, len(smig))
    ]
print "".join([header] + parts + [footer])


smag = smig_all.query("type == 'SMAG'").reset_index()
header = """<CODE code="smag_horaire" description="SMAG horaire" format="float" type="monetary">
"""
footer = """</CODE>
"""
parts = ["""<VALUE deb="{}" fin="{}" valeur="{}" />
""".format(
    str(smag.deb.loc[i].date()),
    str(smag.fin.loc[i].date()),
    str(smag.horaire.loc[i] / 1000)
    ) for i in range(0, len(smig))
    ]
print "".join([header] + parts + [footer])
