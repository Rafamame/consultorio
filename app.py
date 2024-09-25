from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="consultorio"
)

cursor = db.cursor()

# Página Inicial
@app.route('/')
def index():
    # Modificar a consulta para juntar a tabela de agendamentos, clientes e serviços
    sql = """
    SELECT a.id, c.nome AS cliente_nome, s.nome_servico AS servico_nome, a.data_horario 
    FROM agendamentos a
    JOIN clientes c ON a.cliente_id = c.id
    JOIN servicos s ON a.servico_id = s.id
    ORDER BY a.data_horario DESC
    """
    cursor.execute(sql)
    agendamentos = cursor.fetchall()
    
    return render_template('index.html', agendamentos=agendamentos)


# rota para agendar
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        servico_id = request.form['servico_id']
        data_horario = request.form['data_horario']
        
        sql = "INSERT INTO agendamentos (cliente_id, servico_id, data_horario) VALUES (%s, %s, %s)"
        val = (cliente_id, servico_id, data_horario)
        cursor.execute(sql, val)
        db.commit()

        return redirect('/')
    
    # Busca clientes e serviços do banco de dados
    cursor.execute("SELECT id, nome FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id, nome_servico FROM servicos")
    servicos = cursor.fetchall()

    return render_template('agendar.html', clientes=clientes, servicos=servicos)





# Rota para Cadastrar Cliente
@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        sql = "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)"
        val = (nome, telefone, email)
        cursor.execute(sql, val)
        db.commit()

        return redirect('/')
    
    return render_template('cadastrar_cliente.html')

# Rota para Cadastrar Serviço
@app.route('/cadastrar_servico', methods=['GET', 'POST'])
def cadastrar_servico():
    if request.method == 'POST':
        nome_servico = request.form['nome_servico']
        valor = request.form['valor']

        sql = "INSERT INTO servicos (nome_servico, valor) VALUES (%s, %s)"
        val = (nome_servico, valor)
        cursor.execute(sql, val)
        db.commit()

        return redirect('/')
    
    return render_template('cadastrar_servico.html')

# Rota para Listar Clientes
@app.route('/clientes')
def listar_clientes():
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('listar_clientes.html', clientes=clientes)

# Rota para Listar Serviços
@app.route('/servicos')
def listar_servicos():
    cursor.execute("SELECT * FROM servicos")
    servicos = cursor.fetchall()
    return render_template('listar_servicos.html', servicos=servicos)

if __name__ == '__main__':
    app.run(debug=True)
