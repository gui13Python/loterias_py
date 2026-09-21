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

### GitHub + Vercel (recomendado — é o que este projeto já está pronto pra usar)

**1. Subir pro GitHub**

```bash
cd gerador_flask
git init
git add .
git commit -m "primeira versão do gerador"
```

Crie um repositório vazio em github.com/new (sem README, sem .gitignore —
já temos um aqui), depois:

```bash
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
git branch -M main
git push -u origin main
```

**2. Importar na Vercel**

1. Entre em vercel.com com sua conta do GitHub.
2. Clique em "Add New… → Project" e selecione o repositório que você acabou
   de criar.
3. A Vercel detecta que é um app Flask automaticamente (por causa do
   `app.py` e do `requirements.txt`) — não precisa mexer em nada, é só
   clicar em "Deploy".
4. Em ~1 minuto ela te dá um link público, tipo
   `https://seu-projeto.vercel.app`. Esse é o link que qualquer pessoa
   abre no navegador do celular.

**3. Atualizações depois**

Qualquer novo `git push` pra branch `main` gera um novo deploy automático.

> O CSS fica na pasta `public/` (não em `static/`) porque é a convenção que
> a Vercel usa para servir arquivos estáticos — o app já está configurado
> pra isso, tanto local quanto lá.

### Alternativas (Render / Railway)

Também funcionam bem e leem o `Procfile` que já está no projeto:
1. Suba esta pasta pra um repositório no GitHub (mesmo passo acima).
2. Crie uma conta no Render.com ou Railway.app e aponte pro repositório.
3. O serviço lê o `requirements.txt` e o `Procfile` e publica um link
   público (algo como `https://seu-app.onrender.com`).

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
