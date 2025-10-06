Guía de instalación
1.- Activar el entorno vitual
    ".\env\Scripts\activate"
2.- Instalar las librerias requeridas
    "pip install -e."
3.- Ejecutar el comando
    "myflix recommend"


Guía de uso

El comando principal es ´myflix recommend´. De forma predeterminada recomienda basado en el mayor puntaje y con un
minimo de votos de 500k. 
Puedes usar las siguientes opciones para personalizar las recomendaciones:
-l, --limit : Limita el número de resultados, por defecto mostrará solo 5
-m, --min-rating : Define un valor minimo de rating aceptable. 0.0 por defecto
-g, --genres : Añade una lista separada por coma de generos que quieres sean mostrados en las recomendaciones
-e, --exclude : Añade una lista separada por coma de los generos que no quieres que sean mostrados en las recomendaciones
-v, --min-votes: Define un número minimo de votos validos
-r, --r : Permite definir un rango de calificaciones (como float) para filtrar los resultados
