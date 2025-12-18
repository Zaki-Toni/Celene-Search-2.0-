import sys
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.infrastructure.fs.loader import FileDocumentLoader
from src.infrastructure.search_engine.adapter import WhooshAdapter
from src.infrastructure.search_engine.writer import WhooshWriter
from src.infrastructure.search_engine.reader import WhooshReader
from src.domain_nlp.pipeline import NLPPipeline
from src.services.indexing_service import IndexingService
from src.services.search_service import SearchService

# Carpetas temporales para el test
TEST_DOCS_DIR = os.path.join(project_root, 'data', 'temp_test_docs')
TEST_INDEX_DIR = os.path.join(project_root, 'data', 'temp_test_index')

def setup_environment():
    """Crea carpetas y un archivo de prueba."""
    # 1. Limpiar entornos previos
    if os.path.exists(TEST_DOCS_DIR): shutil.rmtree(TEST_DOCS_DIR)
    if os.path.exists(TEST_INDEX_DIR): shutil.rmtree(TEST_INDEX_DIR)
    
    os.makedirs(TEST_DOCS_DIR)
    
    # 2. Crear un archivo simulado
    # Nota: Usamos la palabra 'automóvil' en el texto.
    # Luego buscaremos 'coche' para probar que el NLP conecta ambos.
    file_path = os.path.join(TEST_DOCS_DIR, "test_car.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("The red automobile is very fast on the highway.")
    
    print("✅ Entorno de pruebas creado.")

def test_indexing_service():
    print("\n--- 1. Probando IndexingService ---")
    
    # Instanciamos dependencias
    adapter = WhooshAdapter(TEST_INDEX_DIR)
    writer = WhooshWriter(adapter)
    loader = FileDocumentLoader(TEST_DOCS_DIR)
    
    # Instanciamos el servicio
    service = IndexingService(writer, loader)
    
    # Ejecutamos
    count = service.run_indexing()
    
    # Verificaciones
    if count == 1:
        print("✅ ÉXITO: El servicio indexó 1 documento.")
    else:
        print(f"❌ FALLO: Se esperaban 1 doc, se indexaron {count}.")

def test_search_service():
    print("\n--- 2. Probando SearchService (con NLP) ---")
    
    # Instanciamos dependencias
    adapter = WhooshAdapter(TEST_INDEX_DIR)
    reader = WhooshReader(adapter)
    nlp = NLPPipeline() # Esto cargará NLTK
    
    # Instanciamos el servicio
    service = SearchService(reader, nlp)
    
    # PRUEBA DE FUEGO:
    # El documento tiene "automóvil". Buscaremos "car".
    # Si el servicio funciona, el NLP expandirá "coche" -> "automóvil" y lo encontrará.
    query = "car"
    print(f"🔍 Buscando: '{query}' ...")
    
    results = service.execute_search(query)
    
    if len(results) > 0:
        print(f"✅ ÉXITO: Se encontró el documento '{results[0].title}'.")
        print(f"   Snippet: {results[0].snippet}")
    else:
        print("❌ FALLO: No se encontraron resultados. Falló la expansión semántica o la lectura.")

def cleanup():
    """Borra las carpetas temporales."""
    if os.path.exists(TEST_DOCS_DIR): shutil.rmtree(TEST_DOCS_DIR)
    if os.path.exists(TEST_INDEX_DIR): shutil.rmtree(TEST_INDEX_DIR)
    print("\n🧹 Limpieza completada.")

if __name__ == "__main__":
    try:
        setup_environment()
        test_indexing_service()
        test_search_service()
    finally:
        # Siempre limpiamos, aunque falle el test
        cleanup()