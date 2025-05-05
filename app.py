from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'silvano'
app.config['MYSQL_PASSWORD'] = '023094'
app.config['MYSQL_DB'] = 'obj_estudo'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

@app.route('/')
def listar_notas():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, titulo, conteudo, data_criacao FROM notas ORDER BY data_criacao DESC")
            notas = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro ao executar a consulta: {err}")
            notas = []
        finally:
            cursor.close()
            conn.close()
        return render_template('listar_notas.html', notas=notas)
    return "Erro ao conectar ao banco de dados."
@app.route('/nota/<int:id>')
def exibir_nota(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, titulo, conteudo FROM notas WHERE id = %s", (id,))
            nota = cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Erro ao executar a consulta: {err}")
            nota = None
        finally:
            cursor.close()
            conn.close()
        if nota:
            return render_template('exibir_nota.html', nota=nota)
        return "Nota não encontrada."
    return "Erro ao conectar ao banco de dados."

@app.route('/criar', methods=['GET', 'POST'])
def criar_nota():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO notas (usuario_id, titulo, conteudo) VALUES (%s, %s, %s)"
                usuario_id = 1  # Substitua pela lógica real de obter o ID do usuário
                cursor.execute(query, (usuario_id, titulo, conteudo))
                conn.commit()
                return redirect(url_for('listar_notas'))
            except mysql.connector.Error as err:
                print(f"Erro ao inserir nota: {err}")
                # Adicione alguma forma de mostrar o erro ao usuário, se necessário
            finally:
                cursor.close()
                conn.close()
        return "Erro ao conectar ao banco de dados."
    return render_template('criar_nota.html')

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_nota(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "DELETE FROM notas WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao excluir nota: {err}")
            # Adicione alguma forma de mostrar o erro ao usuário, se necessário
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('listar_notas'))

@app.route('/editar/<int:id>', methods=['GET'])
def editar_nota(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, titulo, conteudo FROM notas WHERE id = %s", (id,))
            nota = cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Erro ao buscar nota para edição: {err}")
            nota = None
        finally:
            cursor.close()
            conn.close()
        if nota:
            return render_template('editar_nota.html', nota=nota)
        return "Nota não encontrada para edição."
    return "Erro ao conectar ao banco de dados."

@app.route('/editar/<int:id>', methods=['POST'])
def atualizar_nota(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = "UPDATE notas SET titulo = %s, conteudo = %s WHERE id = %s"
                cursor.execute(query, (titulo, conteudo, id))
                conn.commit()
                return redirect(url_for('exibir_nota', id=id))
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar nota: {err}")
                # Adicione alguma forma de mostrar o erro ao usuário, se necessário
            finally:
                cursor.close()
                conn.close()
        return "Erro ao conectar ao banco de dados."
    return "Método inválido para atualizar nota."

if __name__ == '__main__':
    app.run(debug=True)