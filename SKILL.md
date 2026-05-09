---
name: ontology
description: "Habilidad de consulta y gestión de ontologías para Hermes – cargar archivos RDF/OWL, ejecutar consultas SPARQL, razonamiento opcional, respaldo a Notion y Obsidian."
version: 0.2.0
author: Hermes (personalizado)
category: mlops
metadata:
  hermes:
    tags: [ontología, rdf, owl, sparql, grafo-de-conocimiento, notion, obsidian]
---
# Gestor de Ontologías Hermes

## Propósito
Cargar archivos RDF/Turtle, OWL, RDF/XML o JSON-LD en un grafo RDFLib, ejecutar consultas SPARQL, (opcionalmente) aplicar razonamiento OWL con Owlready2, y mantener respaldos duraderos en Notion y Obsidian.

## Cómo funciona
1. **Cargar** – `load.py` lee un archivo de ontología, opcionalmente aplica razonamiento, y almacena en caché el grafo como un pickle (`~/.hermes/ontology/cache/<name>.pkl`) para reutilización rápida.  
2. **Consultar** – `query.py` carga el grafo en caché (o carga sobre la marcha), ejecuta una consulta SPARQL proporcionada por el usuario, imprime una tabla formateada, y (si está habilitado) respalda la consulta **y** los resultados a:
   - Notion – una base de datos llamada **Consultas de Ontologías** (creada automáticamente en el primer uso).  
   - Obsidian – un archivo markdown diario bajo `~/obsidian/ontology/YYYY-MM-DD.md`.  
3. **Listar** – `list.py` muestra todas las ontologías en caché con tamaño y marca de tiempo de última modificación.  
4. **Limpiar** – `clear.py` elimina todos los archivos pickle en caché.  

## Instalación
La habilidad es pura Python; solo necesita la biblioteca estándar más los paquetes opcionales a continuación.

bash
Requisito principal – RDFLib
uv pip install rdflib

Opcional – para razonamiento OWL (habilitar en configuración)
uv pip install owlready2

## Configuración
Agregue el siguiente bloque a `~/.hermes/config.yaml` (ajuste como desee):

yaml
ontology:
  enabled: true
  default_format: turtle        # turtle, xml, json-ld, ntriples, etc.
  backup_to_notion: true       # establecer false para omitir respaldo a Notion
  backup_to_obsidian: true     # establecer false para omitir respaldo a Obsidian
  reasoner: false              # true si instaló owlready2 y quiere razonamiento
  cache_dir: ~/.hermes/ontology/cache
  backup_notion_db: Consultas de Ontologías   # Nombre de DB de Notion para resultados de consultas
  backup_obsidian_dir: ~/obsidian/ontology

## Uso
Puede invocar la habilidad directamente desde la CLI de Hermes o desde dentro de otra habilidad/script.

bash
Cargar una ontología (será almacenada en caché)
hermes run ontology_load --file myfile.ttl

Ejecutar una consulta SPARQL (usa la ontología en caché más reciente, o especificar --file)
hermes run ontology_query --query "
    PREFIX ex: <http://example.org/>
    SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10
" --backup

Listar ontologías cargadas
hermes run ontology_list

Limpiar la caché
hermes run ontology_clear

## Sesión de ejemplo
bash
$ hermes run ontology_load --file habits.ttl
Ontología 'habits.ttl' cargada en grafo con 20 triples.
Almacenada en caché en: /home/r3volve7/.hermes/ontology/cache/habits.pkl

$ hermes run ontology_query --query "
    PREFIX ex: <http://example.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?habit ?label WHERE {
      ?habit a ex:Habit ;
             rdfs:label ?label .
    }
" --backup
http://example.org/Exercise

• habit: http://example.org/Exercise

• label: Ejercicio Diario

http://example.org/Meditation

• habit: http://example.org/Meditation

• label: Meditación

http://example.org/Reading

• habit: http://example.org/Reading

• label: Lectura (1/5)
Los resultados de la consulta también se anexan a `~/obsidian/ontology/2026-05-09.md` y (si Notion está configurado) a una página de Notion en la base de datos **Consultas de Ontologías**.

## Extensión
- Agregar un script que inserte nuevos triples y persista el grafo (`add_triple.py`).  
- Exportar el grafo a GraphML o JSON-LD para visualización.  
- Conectar las consultas de ontología a HSIL para almacenar aprendizajes como triples RDF para razonamiento semántico.