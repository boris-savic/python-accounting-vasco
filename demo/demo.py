from datetime import datetime
from decimal import Decimal

from accounting_vasco.core import Entry, VASCOExport, TaxData, Tax, Partner

export = VASCOExport()


tax_data = TaxData(tax_date=datetime.now().date())
tax_data.add_tax(vat_type=Tax.VAT_STANDARD, base=Decimal(100), amount=Decimal(22))

partner = Partner(code='0001',
                  name='Very long partner name to be place here to check if splits name correctly',
                  address='Pot za Brdom 100',
                  zip='1000 Ljubljana',
                  country_iso='SI',
                  tax_number=21475032,
                  vat_id='SI21475032')

entry_1 = Entry(symbol=3,
                document_number='PE1-BL1-1',
                date_document=datetime.now().date(),
                date_of_service=datetime.now().date(),
                date_of_entry=datetime.now().date(),
                document_description='Daily total 1',
                account_code='7600',
                cost_code='1337',
                cost_code2=None,
                cost_code3=None,
                cost_code4=None,
                debit=None,
                credit=Decimal('19'),
                tax_data=tax_data,
                partner=partner)


export.add_entry(entry_1)

print(export.render_xml())

