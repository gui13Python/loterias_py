# Aposta Certa — Gerador de Jogos (Flask)

App web em Python/Flask para gerar jogos de Lotofácil e Mega-Sena, com opção
de escolher dezenas manualmente (parcial ou totalmente) em ambos os jogos.

## Rodar localmente

```bash
pip install -r requirements.txt
python app.py
```

O terminal vai mostrar algo como `Running on http://0.0.0.0:5000`.

## Acessar pelo celular (mesma rede Wi-Fi)

1. Descubra o IP local do seu computador:
   - Windows: `ipconfig` (procure "Endereço IPv4")
   - Mac/Linux: `ifconfig` ou `ip a` (procure algo como `192.168.x.x`)
2. No celular, com o mesmo Wi-Fi do computador, abra o navegador e acesse:
   `http://SEU_IP_LOCAL:5000` (ex: `http://192.168.0.12:5000`)

Isso já resolve pra testar com você mesmo ou mostrar pra alguém na mesma rede.
Pra vender de verdade, o app precisa estar hospedado num servidor com endereço
público — os próximos passos.

## Colocar no ar pra qualquer pessoa acessar (deploy)

Opções simples e com plano gratuito pra começar:

- **Render.com** — conecta direto num repositório do GitHub, detecta o
  `Procfile` e sobe sozinho. Mais fácil pra manter no ar.
- **Railway.app** — parecido com o Render, também lê o `Procfile`.
- **PythonAnywhere** — bom pra quem quer algo bem simples sem lidar com
  `Procfile`/`gunicorn` (usa WSGI próprio).

Passo geral (Render/Railway):
1. Suba esta pasta pra um repositório no GitHub.
2. Crie uma conta no serviço escolhido e aponte pro repositório.
3. O serviço lê o `requirements.txt` e o `Procfile` e publica um link
   público (algo como `https://seu-app.onrender.com`) — esse é o link que
   funciona no navegador de qualquer smartphone.

## Estrutura do projeto

```
gerador_flask/
├── app.py              # lógica de geração + rotas Flask
├── templates/
│   └── index.html      # página (Jinja2)
├── static/
│   └── style.css        # visual
├── requirements.txt
├── Procfile
└── README.md
```

## Sobre a seleção manual

- Marque algumas dezenas: elas ficam fixas e o restante é sorteado
  respeitando os filtros estatísticos (pares/ímpares, primos, moldura, soma
  para a Lotofácil; pares/ímpares, soma e sequência para a Mega-Sena).
- Marque todas as dezenas do jogo (15 na Lotofácil, 6 na Mega-Sena): o app
  não sorteia nada, só mostra as estatísticas do jogo montado por você e
  avisa se ele bate com os filtros ou não.
