from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Configuración de la conexión a MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Chimichurri2002!",  # cambiá si usás otra
    "database": "books_demo"
}

@app.route("/libros/top", methods=["GET"])
def obtener_libros_top():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
            SELECT l.titulo, l.autor, AVG(v.puntuacion) as promedio
            FROM libros l
            JOIN valoraciones v ON l.isbn = v.isbn
            GROUP BY l.isbn
            ORDER BY promedio DESC
            LIMIT 5;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        libros = [
            {
                "titulo": fila[0],
                "autor": fila[1],
                "promedio": round(fila[2], 2)
            }
            for fila in resultados
        ]

        cursor.close()
        conn.close()

        return jsonify({"libros_mejor_puntuados": libros})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
