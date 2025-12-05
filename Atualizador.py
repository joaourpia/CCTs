import os
from git import Repo
from datetime import datetime

# --- CONFIGURAÇÕES ---
# Caminho da pasta onde está o seu projeto no computador
CAMINHO_PROJETO = r"C:\Python\CCTs" 
ARQUIVO_CSV = "CCTs_Extraidas.csv"

def atualizar_projeto():
    try:
        print(f"🔄 Iniciando atualização do projeto em: {CAMINHO_PROJETO}")
        
        # Inicializa o repositório
        repo = Repo(CAMINHO_PROJETO)
        
        # Verifica se há mudanças no git
        if not repo.is_dirty(untracked_files=True):
            print("✅ Nenhuma alteração encontrada. O arquivo CSV não foi modificado?")
            return

        # 1. Adicionar TODOS os arquivos modificados (app.py, csv, imagens, etc)
        print("📂 Adicionando todos os arquivos modificados...")
        repo.git.add(all=True)

        # 2. Criar o commit
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        mensagem = f"Atualização automática CCTs - {data_hoje}"
        repo.index.commit(mensagem)
        print(f"📝 Commit criado: {mensagem}")

        # 3. Enviar para o GitHub (Push)
        print("🚀 Enviando para o GitHub...")
        origin = repo.remote(name='origin')
        origin.push()
        
        print("\n✅ SUCESSO! O projeto foi atualizado.")
        print("⏳ O Streamlit Cloud deve processar a mudança em alguns minutos.")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("Dica: Verifique se suas credenciais do Git estão configuradas corretamente no Windows/Mac.")

if __name__ == "__main__":
    atualizar_projeto()
    input("\nPressione Enter para sair...")