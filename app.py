from flask import Flask, render_template, request, redirect, render_template_string, session
from waitress import serve
from urllib.parse import quote
from database import criar_tabela, salvar_cliente, listar_clientes

app = Flask(__name__)

app.secret_key = "2.s,87s2Salmo091."

USUARIO_ADMIN = "Fabio cruz"
SENHA_ADMIN = "Salmo091#@"

criar_tabela()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/regularizacao")
def regularizacao():
    return render_template("regularizacao.html")


@app.route("/laudos")
def laudos():
    return render_template("laudos.html")


@app.route("/projetos")
def projetos():
    return render_template("projetos.html")


@app.route("/consultoria")
def consultoria():
    return render_template("consultoria.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/orcamento", methods=["POST"])
def orcamento():
    nome = request.form.get("nome")
    whatsapp = request.form.get("whatsapp")
    email = request.form.get("email")
    cidade = request.form.get("cidade")
    servico = request.form.get("servico")
    mensagem = request.form.get("mensagem")

    salvar_cliente(nome, whatsapp, email, cidade, servico, mensagem)

    texto = f"""
Olá, sou {nome}.

WhatsApp: {whatsapp}
E-mail: {email}
Cidade/Bairro: {cidade}
Serviço desejado: {servico}

Descrição:
{mensagem}
"""

    numero_nexus = "5511948822408"
    texto_formatado = quote(texto)

    return redirect(f"https://wa.me/{numero_nexus}?text={texto_formatado}")


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""

    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == USUARIO_ADMIN and senha == SENHA_ADMIN:
            session["admin_logado"] = True
            return redirect("/admin")
        else:
            erro = "Usuário ou senha incorretos."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Login Admin - Nexus Edificações</title>
        <style>
            body{
                background:#0f172a;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }

            .login-box{
                background:#1e293b;
                padding:40px;
                border-radius:18px;
                width:100%;
                max-width:400px;
                box-shadow:0 10px 30px rgba(0,0,0,0.4);
            }

            h1{
                color:#fbbf24;
                margin-bottom:25px;
                text-align:center;
            }

            input{
                width:100%;
                padding:15px;
                margin-bottom:15px;
                border:none;
                border-radius:10px;
                font-size:16px;
            }

            button{
                width:100%;
                padding:15px;
                border:none;
                border-radius:10px;
                background:#fbbf24;
                color:#111827;
                font-size:18px;
                font-weight:bold;
                cursor:pointer;
            }

            .erro{
                color:#f87171;
                text-align:center;
                margin-bottom:15px;
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>Nexus Admin</h1>

            {% if erro %}
                <p class="erro">{{ erro }}</p>
            {% endif %}

            <form method="POST">
                <input type="text" name="usuario" placeholder="Usuário" required>
                <input type="password" name="senha" placeholder="Senha" required>
                <button type="submit">Entrar</button>
            </form>
        </div>
    </body>
    </html>
    """, erro=erro)


@app.route("/admin")
def admin():
    if not session.get("admin_logado"):
        return redirect("/login")

    clientes = listar_clientes()

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Painel Nexus Edificações</title>
        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                color:white;
                padding:30px;
            }

            .topo{
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:30px;
            }

            h1{
                color:#fbbf24;
            }

            a.sair{
                background:#ef4444;
                color:white;
                padding:10px 18px;
                border-radius:8px;
                text-decoration:none;
                font-weight:bold;
            }

            table{
                width:100%;
                border-collapse:collapse;
                background:#1e293b;
            }

            th, td{
                padding:12px;
                border:1px solid #334155;
                text-align:left;
                vertical-align:top;
            }

            th{
                background:#172554;
                color:#fbbf24;
            }

            tr:nth-child(even){
                background:#111827;
            }

            a{
                color:#25d366;
                font-weight:bold;
            }
        </style>
    </head>
    <body>

        <div class="topo">
            <h1>Painel de Clientes — Nexus Edificações</h1>
            <a class="sair" href="/logout">Sair</a>
        </div>

        <table>
            <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>WhatsApp</th>
                <th>E-mail</th>
                <th>Cidade</th>
                <th>Serviço</th>
                <th>Mensagem</th>
                <th>Data</th>
            </tr>

            {% for cliente in clientes %}
            <tr>
                <td>{{ cliente[0] }}</td>
                <td>{{ cliente[1] }}</td>
                <td>
                    <a href="https://wa.me/{{ cliente[2] }}" target="_blank">
                        {{ cliente[2] }}
                    </a>
                </td>
                <td>{{ cliente[3] }}</td>
                <td>{{ cliente[4] }}</td>
                <td>{{ cliente[5] }}</td>
                <td>{{ cliente[6] }}</td>
                <td>{{ cliente[7] }}</td>
            </tr>
            {% endfor %}
        </table>

    </body>
    </html>
    """, clientes=clientes)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

from flask import send_from_directory

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')
if __name__ == "__main__":
    print("Servidor Nexus Edificações iniciado...")
    serve(app, host="0.0.0.0", port=5000)