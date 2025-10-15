import pandas as pd

try:
    with open("clausulas_farmaceuticos.csv", "r", encoding="utf-8") as f:
        # Pule as 283 primeiras linhas
        for _ in range(283):
            next(f)
        
        # Leia e imprima a linha 284
        line_284 = next(f)
        print(f"Conteúdo da Linha 284 no seu CSV:\n>>> {line_284} <<<")

except FileNotFoundError:
    print("Erro: O arquivo 'clausulas_farmaceuticos.csv' não foi encontrado. Certifique-se de que ele está no mesmo diretório do script Python.")
except StopIteration:
    print("Erro: O arquivo não tem 284 linhas.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")

