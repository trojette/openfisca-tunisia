# -*- coding: utf-8 -*-


import json
import xml.etree.ElementTree

from openfisca_core import conv, legislations, legislationsxml
from openfisca_tunisia.tests import base


def check_legislation_xml_file(year):
    legislation_tree = xml.etree.ElementTree.parse(base.TaxBenefitSystem.legislation_xml_file_path)
    legislation_xml_json = conv.check(legislationsxml.xml_legislation_to_json)(legislation_tree.getroot(),
        state = conv.default_state)

    legislation_xml_json, errors = legislationsxml.validate_legislation_xml_json(legislation_xml_json,
        state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_xml_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_xml_json, ensure_ascii = False,
                indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_xml_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    _, legislation_json = legislationsxml.transform_node_xml_json_to_json(legislation_xml_json)

    legislation_json, errors = legislations.validate_legislation_json(legislation_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    # Create tax_benefit system only now, to be able to debug XML validation errors in above code.
    if base.tax_benefit_system.preprocess_legislation is not None:
        base.tax_benefit_system.preprocess_legislation(legislation_json)

    legislation_json = legislations.generate_dated_legislation_json(legislation_json, year)
    legislation_json, errors = legislations.validate_dated_legislation_json(legislation_json,
        state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)).encode(
                'utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))


def test_legislation_xml_file():
    for year in range(2006, 2011):
        yield check_legislation_xml_file, year


if __name__ == '__main__':
    test_legislation_xml_file()
    import nose
    nose.core.runmodule(argv = [__file__, '-v', 'legislations_tests:test_legislation_xml_file'])
