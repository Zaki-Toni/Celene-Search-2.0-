import sys
import os

# Configuración de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.domain_nlp.pipeline import NLPPipeline

def main():
    print("--- 🧠 Probando Pipeline de NLP (Español) ---")
    
    pipeline = NLPPipeline()
    
    # Pruebas con palabras clave
    test_queries = [
        "car",      # Debería dar: automobile, auto, machine...
        "dog",      # Debería dar: canine, pooch...
        "computer", # Debería dar: computing machine, data processor...
        "happy"     # Debería dar: felicitous, glad...
    ]
    
    for text in test_queries:
        print(f"\n🔎 Entrada: '{text}'")
        result = pipeline.process(text)
        
        print(f"   Original: {result.original_text}")
        print(f"   Términos ({len(result.expanded_terms)}): {result.expanded_terms}")
        print(f"   Query Booleana: {result.to_boolean_query()}")

if __name__ == "__main__":
    main()