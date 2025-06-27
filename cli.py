import sys
import os
import shutil
import stat
import time
import gc
from core import ingest, qa
from core.vector import close_vectorstore

def print_banner():
    print("\n🧠 PDF QA con Gemini Flash 1.5 + HuggingFace")
    print("Comandos disponibles:")
    print("  upload <ruta_pdf>   -> Procesa el PDF y genera embeddings (reemplaza vectorstore)")
    print("  ask <pregunta>      -> Haz una pregunta sobre el PDF")
    print("  exit                -> Salir\n")

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def eliminar_vectorstore():
    if os.path.exists("vectorstore"):
        try:
            close_vectorstore()
            gc.collect()
            time.sleep(1.5)
            shutil.rmtree("vectorstore", onerror=remove_readonly)
            print("🗑️ Vectorstore anterior eliminada\n")
        except Exception as e:
            print(f"❌ Error al eliminar vectorstore: {e}")

def main():
    print_banner()
    while True:
        try:
            command = input("📘 > ").strip()

            if command.lower() in ["exit", "salir", "quit"]:
                print("👋 Hasta luego, Sensei del Código.")
                break

            elif command.startswith("upload "):
                path = command[7:].strip()
                if os.path.exists(path):
                    eliminar_vectorstore()
                    ingest.process_pdf(path)
                    print("✅ PDF procesado con éxito")
                else:
                    print("❌ Archivo no encontrado")

            elif command.startswith("ask "):
                if not os.path.exists("vectorstore"):
                    print("⚠️ No hay PDF cargado. Usa 'upload <archivo.pdf>' antes de preguntar.")
                    continue
                question = command[4:].strip()
                try:
                    answer = qa.ask_question(question)
                    print(f"\n🤖 Respuesta: {answer}\n")
                except Exception as e:
                    print(f"❌ Error al hacer la pregunta: {e}")

            else:
                print("⚠️ Comando no reconocido. Usa 'upload', 'ask' o 'exit'.")

        except KeyboardInterrupt:
            print("\n👋 Cerrado por teclado. Hasta la próxima, crack, ídolo, máquina, sensei, genio, mostro.")
            break

if __name__ == "__main__":
    main()
