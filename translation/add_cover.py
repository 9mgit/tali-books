import json

# Read existing chapters
with open('chapters_es.json') as f:
    chapters = json.load(f)

# Create wrapped format with cover
data = {
    "chapters": chapters,
    "cover": {
        "eyebrow": "Una historia en diez partes",
        "dedication": "Para toda madre que siguió adelante cuando no tenía nada.<br>Para todo niño nacido en un mundo que no estaba listo para ellos.<br>Para cualquiera que miró algo roto y pensó — podría arregloarlo.",
        "intro": "Este no es un libro santo. Los libros santos te dicen qué creer. Este libro te dice qué hacer. Te pedido que mires. De verdad mires. Más allá del anger. Más allá de la bandera. Hasta el lugar donde cada ser humano guarda su miedo.",
        "labels": {
            "chapters": "Capítulos",
            "words": "Palabras", 
            "parts": "Partes"
        },
        "questions": {
            "title": "Las cuatro preguntas",
            "0": "¿Cuál es el dolor real?",
            "1": "¿Quién no está siendo visto?",
            "2": "¿Qué puedo hacer ahora mismo, con lo que tengo?",
            "3": "¿Es esto algo que debo manejar solo, o necesito a alguien con más conocimiento?"
        },
        "begin": "Comenzar a Leer",
        "sidebar": {
            "search": "⌕ Buscar en el libro…",
            "chapters": "Capítulos",
            "words": "Palabras",
            "parts": "Partes"
        }
    }
}

# Save wrapped version
with open('chapters_es.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Done - Spanish cover added')