#!/usr/bin/env python3
'''
Biblioteca de configuração do roteador wifi Intelbras IWR3000N

Esta biblioteca foi criada para configurar rapidamente lotes de roteadores
Intelbras IWR3000N. Pode funcionar com outros roteadores da fabricante.

1. Uso
A API do roteador trabalha com dados JSON, então para qualquer operação,
deve-se utilizar a função apiget para coletar os dados, modificá-los, e
enviar com a função apiset.
Para se obter todas as interfaces de API possíveis, pode-se utilizar a
função apibusca.

2. Exemplo
Alterar nome da rede wifi
>>> import IWR3000N
>>> conf = IWR3000N.Configurador('192.168.0.1')
>>> conf.login('admin', 'teste')
>>> code, j = conf.apiget('interface/wireless')
>>> j['ssid_ap'][0]['ssid'] = 'AP'
>>> conf.apiset('interface/wireless', j)
>>> (200, '{"op_mode":{"option_list":[0,1],"value":0},"ssid_ap":[{"enable_wps":0,"ssid":"AP","hidden_ssid":0,"enabled":1,"bandwidth":0,"channel":4,"channel_extension":0,"security":{"type":0,"crypto":{"type":0,"key_mode":1,"default_key":0,"key1":""}}}],"client_ssid":{"ssid":"","channel":4,"security":0,"cipher":0,"key":"","bssid":"","status":0},"lan_ip":"192.168.0.1"}')

Também e possível realizar ações sem enviar dados, como por exemplo,
reiniciar o dispositivo:
>>> import IWR3000N
>>> conf = IWR3000N.Configurador('192.168.0.1')
>>> conf.login('admin', 'teste')
>>> conf.apiget('system/reboot')

Para maior comodidade, foram adicionados também os valores padrões nas
variáveis do: host, usuário e senha, bastando apenas executar as funções.

3. Changelog
1.0 - 08/10/2018
* Primeira versão
'''

__version__ = '1.0'
__author__ = 'Victor Oliveira <victor.oliveira@gmx.com>'

import urllib.request as ur
import urllib.parse as up
import json
import re

HOST_PADRAO = '10.0.0.1'
USUARIO_PADRAO = 'admin'
SENHA_PADRAO = 'admin'

class Configurador:

    def __init__(self, host=HOST_PADRAO):
        '''Inicializa as variáveis base'''
        self._host = host
        self._urlbase = 'http://{}'.format(self._host)

    def _reqhelper(self, urlpart, data=None, method='POST'):
        '''Função para auxiliar nas requisições'''
        url = '{}{}'.format(self._urlbase, urlpart)
        if data:
            data = data.replace(' ', '')
            data = data.replace('\'', '\"')
            req = ur.Request(url, data.encode(), method=method)
            req = ur.urlopen(req)
        else:
            req = ur.urlopen(url)

        ret = req.read().decode()
        return req.code, ret

    def login(self, usuario=USUARIO_PADRAO, senha=SENHA_PADRAO):
        '''Realiza o login'''
        urlpart = '/v1/system/login'
        cred = '{{username:"{}",password:"{}"}}'.format(usuario, senha)
        self._reqhelper(urlpart, cred)

    def apibusca(self):
        '''Retorna todas as páginas que podem interagir com as API's'''
        urlpart = '/app.js'
        html = self._reqhelper(urlpart)
        pages_tmp = re.findall('\'/v1/.*\'', html[1])
        pages = list()
        for i in pages_tmp:
            i = i.strip('\'')
            i = i.strip('/v1/')
            pages.append(i)
        return sorted(list(set(pages)))

    def apiget(self, urlpart):
        '''Retorna código da requisição HTTP e JSON das configurações'''
        urlpart = '/v1/{}'.format(urlpart)
        code, ret = self._reqhelper(urlpart)
        if ret:
            j = json.loads(ret)
        else:
            j = ret
        return code, j

    def apiset(self, urlpart, jsondata):
        '''Configura uma página usando um arquivo JSON'''
        urlpart = '/v1/{}'.format(urlpart)
        j = json.dumps(jsondata, separators=(',', ':'))
        code, ret = self._reqhelper(urlpart, j, method='PUT')
        return code, ret
