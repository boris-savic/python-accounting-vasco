import textwrap

from iso3166 import countries


def construct_vasco_json(vasco_export):
    data = {
        '_name': 'Prenos'
    }

    for i, entry in enumerate(vasco_export.entries):
        data[f'entry_{i}'] = build_entry_json(entry)

    return data


def build_entry_json(entry):
    data = {
        '_name': 'Knjizba',
        '_sorting': ['Simbol', 'Dokument', 'Datum_knjizenja', 'Obracunsko_obdobje', 'Datum_dokumenta', 'Opis_dokumenta',
                     'Konto', 'Partner', 'Rok_placila', 'Sm', 'Sm2', 'Sm3', 'Sm4', 'Debet', 'Kredit', 'Ir', 'Veza'],
        'symbol': {
            '_name': 'Simbol',
            '_value': str(entry.symbol)
        },
        'document_name': {
            '_name': 'Dokument',
            '_value': entry.document_number
        },
        'date_of_entry': {
            '_name': 'Datum_knjizenja',
            '_value': entry.date_of_entry.isoformat()
        },
        'accounting_period': {
            '_name': 'Obracunsko_obdobje',
            'month': {
                '_name': 'Mesec',
                '_value': str(entry.date_of_service.month)
            },
            'year': {
                '_name': 'Leto',
                '_value': str(entry.date_of_service.year)
            }
        },
        'date_document': {
            '_name': 'Datum_dokumenta',
            '_value': entry.date_document.isoformat()
        },
        'document_description': {
            '_name': 'Opis_dokumenta',
            '_value': entry.document_description or 'n/a'
        },
        'account': {
            '_name': 'Konto',
            '_value': str(entry.account_code)
        }
    }

    if entry.date_due:
        data['date_due'] = {
            '_name': 'Rok_placila',
            '_value': entry.date_due.isoformat()
        }

    if entry.veza:
        data['veza'] = {
            '_name': 'Veza',
            '_value': entry.veza
        }

    if entry.credit:
        data['credit'] = {
            '_name': 'Kredit',
            '_value': str(entry.credit)
        }
    else:
        data['debit'] = {
            '_name': 'Debet',
            '_value': str(entry.debit)
        }

    if entry.cost_code:
        data['cost_code'] = {
            '_name': 'Sm',
            'code': {
                '_name': 'Sifra',
                '_value': str(entry.cost_code)
            }
        }

    if entry.cost_code2:
        data['cost_code2'] = {
            '_name': 'Sm2',
            'code': {
                '_name': 'Sifra',
                '_value': str(entry.cost_code2)
            }
        }

    if entry.cost_code3:
        data['cost_code'] = {
            '_name': 'Sm3',
            'code': {
                '_name': 'Sifra',
                '_value': str(entry.cost_code3)
            }
        }

    if entry.cost_code4:
        data['cost_code4'] = {
            '_name': 'Sm4',
            'code': {
                '_name': 'Sifra',
                '_value': str(entry.cost_code4)
            }
        }

    # Append IR object if needed
    if entry.tax_data:
        data['tax_data'] = {
            '_name': 'Ir',
            'vat_date': {
                '_name': 'Datum_za_ddv',
                '_value': entry.tax_data.tax_date.isoformat()
            },
        }

        for i, tax in enumerate(entry.tax_data.taxes):
            data['tax_data'][f'vat_{i}'] = {
                '_name': 'Ddv',
                'tax_type': {
                    '_name': 'Vrsta_ddv',
                    '_value': tax.get_vasco_vat_type()
                },
                'base': {
                    '_name': 'Osnova',
                    '_value': str(tax.base)
                },
                'amount': {
                    '_name': 'Znesek',
                    '_value': str(tax.amount)
                }
            }

    if entry.partner:
        data['partner'] = {
            '_name': 'Partner',
            '_sorting': ['Sifra', 'Naziv1', 'Naziv2', 'Naslov', 'Posta', 'Drzava',
                         'Identifikacijska_stevilka', 'Davcna_stevilka'],
            'code': {
                '_name': 'Sifra',
                '_value': str(entry.partner.code)
            },
            'address': {
                '_name': 'Naslov',
                '_value': entry.partner.address[:40]
            },
            'zip': {
                '_name': 'Posta',
                '_value': str(entry.partner.zip)
            },
            'tax_number': {
                '_name': 'Davcna_stevilka',
                '_value': str(entry.partner.tax_number)
            }
        }

        if entry.partner.vat_id:
            data['partner']['vat_id'] = {
                '_name': 'Identifikacijska_stevilka',
                '_value': entry.partner.vat_id
            }

        if entry.partner.country_iso:
            data['partner']['country'] = {
                '_name': 'Drzava',
                '_value': countries.get(entry.partner.country_iso).numeric
            }

        name_split = textwrap.wrap(entry.partner.name, 40, break_long_words=True)

        for i, bn_part in enumerate(name_split):
            i = i + 1  # Start from 1
            data['partner'][f"name_part_{i}"] = {
                '_name': f"Naziv{i}",
                '_value': bn_part
            }

            if i == 2:
                break  # Stop at max length

    return data
