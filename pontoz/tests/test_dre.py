from decimal import Decimal

import pytest

from pontoz import view
from pontoz.models import MonthlyReport


@pytest.fixture(scope='module')
def complete_dre():
    return view.render('dre.html')


@pytest.fixture(scope='module')
def monthly_reports():
    months = 'jan fev mar abr mai jun jul ago set out nov dez'.split()
    sales = (f'{i}.00' for i in range(1, 13))
    pointz_sales = (f'{i}.00' for i in range(13, 25))
    costs = (f'1.{i}' for i in range(10, 22))
    return [
        MonthlyReport(month=month, year=17, sale=sale, pointz_sale=pointz_sale, base_coin_cost=cost)
        for month, sale, pointz_sale, cost in zip(months, sales, pointz_sales, costs)
    ]


EXPECTED_CONTENTS = [
    '<title>Posto Flex</title>',
    '<th>Valor da Moeda Base</th>', '<td>R$ 0,018</td>',
    '<th>jan-17</th>', '<th>fev-17</th>', '<th>mar-17</th>', '<th>abr-17</th>',
    '<th>mai-17</th>', '<th>jun-17</th>', '<th>jul-17</th>', '<th>ago-17</th>',
    '<th>set-17</th>', '<th>out-17</th>', '<th>nov-17</th>', '<th>dez-17</th>',
    '<th>Total Período</th>',
    '<td>Vendas</td>', '<td>Vendas com Pontoz</td>',
    '% Participação nas Vendas', '1300%', '700%', '500%', '400%', '340%', '300%', '271%', '250%', '233%', '220%',
    '209%', '200%', '285%',
    '(-) Emissão de Moeda Base',
    '<td>R$ 13,86</td>',
    'Investimento / Faturamento',

]

EXPECTED_CONTENTS.extend(f'<td>R$ {i},00</td>' for i in range(1, 25))  # Sales
EXPECTED_CONTENTS.extend(f'<td>R$ 1,{i}</td>' for i in range(10, 22))  # Pontoz Sales
EXPECTED_CONTENTS.extend(f'<td>{i}%</td>' for i in range(3, 9))  # Investimento / Faturamento


@pytest.mark.parametrize(
    'content',
    EXPECTED_CONTENTS

)
def complete_dre(content, complete_dre):
    assert content in complete_dre


@pytest.mark.parametrize(
    'expected_content',
    [
        '<title>Posto Flex</title>',
        '<h1>Posto Flex</h1>',
    ]

)
def test_dre_title(expected_content):
    assert expected_content in view.render('dre.html', title='Posto Flex')


@pytest.mark.parametrize('value', ['0.018', '1.22', '123.34'])
def test_dre_base_coin_value(value):
    dec = Decimal(value)
    assert value in view.render('dre.html', base_coin_value=dec)


@pytest.mark.parametrize(
    'header',
    [
        '<th>jan-17</th>', '<th>fev-17</th>', '<th>mar-17</th>', '<th>abr-17</th>',
        '<th>mai-17</th>', '<th>jun-17</th>', '<th>jul-17</th>', '<th>ago-17</th>',
        '<th>set-17</th>', '<th>out-17</th>', '<th>nov-17</th>', '<th>dez-17</th>',
    ]
)
def test_dre_monthly_report_headers(header, monthly_reports):
    assert header in view.render('dre.html', monthly_reports=monthly_reports)


@pytest.mark.parametrize('expected_sale', [f'<td>R$ {i}.00</td>' for i in range(1, 13)])
def test_dre_monthly_report_sales(expected_sale, monthly_reports):
    assert expected_sale in view.render('dre.html', monthly_reports=monthly_reports)


@pytest.mark.parametrize('expected_pointz_sale', [f'<td>R$ {i}.00</td>' for i in range(13, 25)])
def test_dre_monthly_report_pointz_sales(expected_pointz_sale, monthly_reports):
    assert expected_pointz_sale in view.render('dre.html', monthly_reports=monthly_reports)


@pytest.mark.parametrize('expected_cost', [f'<td>R$ 1.{i}</td>' for i in range(10, 22)])
def test_dre_monthly_report_costs(expected_cost, monthly_reports):
    assert expected_cost in view.render('dre.html', monthly_reports=monthly_reports)
