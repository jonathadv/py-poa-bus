#!/usr/bin/env python3

t11_page = 'http://www.eptc.com.br/EPTC_Itinerarios/Cadastro.asp?Linha=101-11&Tipo=TH&Veiculo=1&Sentido=0&Logradouro=0'

import eptc_parser.eptc_html_parser as parser
result = parser.main(t11_page)

print (result)

