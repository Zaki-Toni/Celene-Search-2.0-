# Celene-Search-2.0
# 🔍 Motor de Búsqueda Semántica con Expansión de Consultas

> Un sistema de Recuperación de Información (IR) inteligente que utiliza **WordNet** para entender lo que buscas, no solo lo que escribes.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![NLP](https://img.shields.io/badge/NLP-NLTK-yellow)
![Search](https://img.shields.io/badge/Engine-Whoosh-orange)
![License](https://img.shields.io/badge/License-MIT-grey)

## 📖 Descripción

Este proyecto es una implementación de un **Motor de Búsqueda Semántico** diseñado bajo una arquitectura modular y escalable. 

A diferencia de los buscadores tradicionales que buscan coincidencias exactas de texto, este sistema implementa un **Pipeline de NLP** que analiza gramaticalmente la consulta del usuario, filtra palabras irrelevantes y expande los términos de búsqueda utilizando sinónimos de la base de datos léxica **WordNet**.

**Ejemplo:**
Si buscas: *"Coche veloz"*
El sistema busca internamente: *"Coche OR Auto OR Automóvil OR Carro AND Veloz OR Rápido OR Ligero..."*

## ✨ Características Principales

*   **Arquitectura SOLID:** Diseño desacoplado en capas (Presentación, Servicios, Dominio NLP, Infraestructura).
*   **Expansión de Consultas (Query Expansion):** Uso de `nltk.corpus.wordnet` para encontrar sinónimos contextuadas.
*   **Procesamiento Inteligente:**
    *   **POS Tagging:** Distingue si una palabra es sustantivo, verbo o adjetivo para buscar el sinónimo correcto.
    *   **Stop-word Removal:** Ignora palabras vacías ("el", "la", "de") para optimizar la expansión.
*   **Motor de Indexación:** Basado en **Whoosh**, con soporte para ranking BM25F.
*   **Interfaz Web:** Aplicación ligera en ???? para realizar búsquedas y ver resultados resaltados.

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura de capas estricta:

1.  **Capa de Presentación:** Interfaz Web (Flask).
2.  **Capa de Aplicación:** Servicios de Búsqueda e Indexación.
3.  **Capa de Dominio (NLP):** Lógica de expansión semántica.
4.  **Capa de Infraestructura:** Adaptadores para Whoosh y Sistema de Archivos.

## 📂 Estructura del Proyecto

```text
Celene-Search 2.0/
│
├── data/
│   └── documents/          # 📄 ¡Pon tus archivos ????? aquí!
│
├── src/
│   ├── core/               # Interfaces y contratos (IIndexReader, etc.)
│   ├── indexing/           # Lógica de carga y escritura en Whoosh
│   ├── nlp/                # Pipeline, Tokenizer, WordNet Expander
│   ├── web/                # ?????????
│   └── services/           # Orquestadores (SearchService)
│
├── index_storage/          # 🗄️ Índice generado automáticamente
├── app.py                  # Punto de entrada de la aplicación Web
├── indexer_script.py       # Script para ejecutar la indexación
└── requirements.txt        # Librerías necesarias
