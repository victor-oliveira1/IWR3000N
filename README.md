# IWR3000N
Biblioteca de configuração do roteador wifi Intelbras IWR3000N  

Esta biblioteca foi criada para configurar rapidamente lotes de roteadores  
Intelbras IWR3000N. Pode funcionar com outros roteadores da fabricante.  
  
## 1. Uso  
A API do roteador trabalha com dados JSON, então para qualquer operação,  
deve-se utilizar a função apiget para coletar os dados, modificá-los, e  
enviar com a função apiset.  
Para se obter todas as interfaces de API possíveis, pode-se utilizar a  
função apibusca.  

## 2. Exemplo
Alterar nome da rede wifi  
> \>\>\> import IWR3000N  
\>\>\> conf = IWR3000N.Configurador('192.168.0.1')  
\>\>\> conf.login('admin', 'teste')  
\>\>\> code, j = conf.apiget('interface/wireless')  
\>\>\> j['ssid_ap'][0]['ssid'] = 'AP'  
\>\>\> conf.apiset('interface/wireless', j)  
\>\>\> (200, '{"op_mode":{"option_list":[0,1],"value":0},"ssid_ap":[{"enable_wps":0,"ssid":"AP","hidden_ssid":0,"enabled":1,"bandwidth":0,"channel":4,"channel_extension":0,"security":{"type":0,"crypto":{"type":0,"key_mode":1,"default_key":0,"key1":""}}}],"client_ssid":{"ssid":"","channel":4,"security":0,"cipher":0,"key":"","bssid":"","status":0},"lan_ip":"192.168.0.1"}')  

Também e possível realizar ações sem enviar dados, como por exemplo,  
reiniciar o dispositivo:  
> \>\>\> import IWR3000N  
\>\>\> conf = IWR3000N.Configurador('192.168.0.1')  
\>\>\> conf.login('admin', 'teste')  
\>\>\> conf.apiget('system/reboot')  

Para maior comodidade, foram adicionados também os valores padrões nas
variáveis do: host, usuário e senha, bastando apenas executar as funções.

## 3. Changelog
1.0 - 08/10/2018  
* Primeira versão  

Victor Oliveira <victor.oliveira@gmx.com>
