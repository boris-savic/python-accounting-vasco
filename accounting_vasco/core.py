from lxml import etree

from accounting_vasco.builder import build_xml
from accounting_vasco.definitions import construct_vasco_json


class Transfer:
    def __init__(self):
        self.entries = None


class Tax:
    VAT_STANDARD = 'VAT_STANDARD'
    VAT_LOW = 'VAT_LOW'
    VAT_SPECIAL_LOW = 'VAT_SPECIAL_LOW'
    VAT_EXEMPT_HOME = 'VAT_EXEMPT_HOME'
    REVERSE_VAT_EU_GOODS = 'REVERSE_VAT_EU_GOODS'
    REVERSE_VAT_EU_SERVICE = 'REVERSE_VAT_EU_SERVICE'
    EXPORT_OTHER_MARKETS_GOODS = 'EXPORT_OTHER_MARKETS_GOODS'

    def __init__(self, vat_type, base, amount):
        self.vat_type = vat_type
        self.base = base
        self.amount = amount

    def get_vasco_vat_type(self):
        if self.vat_type == Tax.VAT_STANDARD:
            return 'ddv_visja_promet_znotraj_SLO'
        elif self.vat_type == Tax.VAT_LOW:
            return 'ddv_nizja_promet_znotraj_SLO'
        elif self.vat_type == Tax.VAT_SPECIAL_LOW:
            return 'ddv_posebna_nizja_promet_znotraj_SLO'
        elif self.vat_type == Tax.VAT_EXEMPT_HOME:
            return 'oproscen_promet_brez_pravice_do_odbitka'
        elif self.vat_type == Tax.REVERSE_VAT_EU_GOODS:
            return 'oproscen_promet_dobave_v_EU'
        elif self.vat_type == Tax.REVERSE_VAT_EU_SERVICE:
            return 'oproscen_promet_dobave_storitev_v_EU'
        elif self.vat_type == Tax.EXPORT_OTHER_MARKETS_GOODS:
            return 'oproscen_promet_izvoz_blaga'

        # Default value
        return 'ne_gre_v_knjigo'

class TaxData:
    def __init__(self, tax_date):
        self.tax_date = tax_date
        self.taxes = []

    def add_tax(self, vat_type, base, amount):
        self.taxes.append(Tax(vat_type=vat_type, base=base, amount=amount))


class Partner:
    def __init__(self, code, name, address, zip, tax_number, vat_id=None, country_iso=None):
        self.code = code
        self.name = name
        self.address = address
        self.zip = zip
        self.tax_number = tax_number
        self.vat_id = vat_id
        self.country_iso = country_iso


class Entry:
    def __init__(self,
                 symbol,
                 document_number,
                 date_document,
                 date_of_service,
                 date_of_entry,
                 document_description,
                 account_code,
                 cost_code=None,
                 cost_code2=None,
                 cost_code3=None,
                 cost_code4=None,
                 debit=None,
                 credit=None,
                 tax_data=None,
                 partner=None,
                 date_due=None,
                 veza=None):
        self.symbol = symbol
        self.document_number = document_number
        self.date_document = date_document
        self.date_of_service = date_of_service
        self.date_of_entry = date_of_entry
        self.document_description = document_description
        self.account_code = account_code
        self.cost_code = cost_code
        self.cost_code2 = cost_code2
        self.cost_code3 = cost_code3
        self.cost_code4 = cost_code4
        self.debit = debit
        self.credit = credit
        self.tax_data = tax_data   # Object TaxData
        self.partner = partner
        self.date_due = date_due
        self.veza = veza


class VASCOExport:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def render_xml(self):
        xml_content = build_xml(construct_vasco_json(self))

        return ("%s%s" % ('<?xml version="1.0" encoding="UTF-8"?>\n',
                          etree.tostring(xml_content,
                                         pretty_print=True,
                                         xml_declaration=False,
                                         ).decode('utf-8')))