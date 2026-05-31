from pathlib import Path

p = Path("app.py")
s = p.read_text(encoding="utf-8")

rotas = '''
@app.route("/blog/quanto-custa-regularizar-imovel")
def artigo_custo_regularizacao():
    return render_template("artigo_custo_regularizacao.html")


@app.route("/blog/o-que-e-habite-se")
def artigo_habite_se():
    return render_template("artigo_habite_se.html")


@app.route("/blog/diferenca-entre-art-e-rrt")
def artigo_art_rrt():
    return render_template("artigo_art_rrt.html")


@app.route("/blog/problemas-de-infiltracao")
def artigo_infiltracao():
    return render_template("artigo_infiltracao.html")


@app.route("/blog/trincas-e-rachaduras")
def artigo_trincas():
    return render_template("artigo_trincas.html")


@app.route("/blog/tecnico-em-edificacoes")
def artigo_tecnico_edificacoes():
    return render_template("artigo_tecnico_edificacoes.html")


@app.route("/blog/regularizacao-de-reformas")
def artigo_regularizacao_reformas():
    return render_template("artigo_regularizacao_reformas.html")


@app.route("/blog/laudo-de-vistoria")
def artigo_laudo_vistoria():
    return render_template("artigo_laudo_vistoria.html")


'''

if "/blog/quanto-custa-regularizar-imovel" not in s:
    s = s.replace('@app.route("/orcamento", methods=["POST"])', rotas + '@app.route("/orcamento", methods=["POST"])')

p.write_text(s, encoding="utf-8")
