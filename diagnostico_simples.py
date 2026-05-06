import os
import platform
import subprocess
from datetime import datetime

def main():
    print("="*50)
    print("CYBERCRIP - DIAGNÓSTICO RÁPIDO")
    print("="*50)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # 1. Sistema Operacional
    print("[ SISTEMA ]")
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Computador: {platform.node()}\n")
    
    # 2. Processador (via CMD)
    print("[ PROCESSADOR ]")
    try:
        cpu = subprocess.check_output(
            'wmic cpu get name', 
            shell=True, 
            encoding='utf-8'
        ).split('\n')[1].strip()
        print(f"CPU: {cpu}")
    except:
        print("CPU: Não detectado")
    print()
    
    # 3. Memória RAM (via CMD)
    print("[ MEMÓRIA RAM ]")
    try:
        ram_total = subprocess.check_output(
            'wmic memorychip get capacity', 
            shell=True, 
            encoding='utf-8'
        ).split('\n')[1:3]
        
        total_bytes = 0
        for linha in ram_total:
            if linha.strip().isdigit():
                total_bytes += int(linha.strip())
        
        ram_gb = round(total_bytes / (1024**3), 2)
        print(f"RAM Total: {ram_gb} GB")
    except:
        print("RAM Total: Não detectado")
    
    # RAM disponível
    try:
        ram_livre_bytes = subprocess.check_output(
            'wmic os get freephysicalmemory', 
            shell=True, 
            encoding='utf-8'
        ).split('\n')[1].strip()
        
        ram_livre_gb = round(int(ram_livre_bytes) / (1024**2), 2)  # Converter KB para GB
        print(f"RAM Disponível: {ram_livre_gb} GB")
    except:
        print("RAM Disponível: Não detectado")
    print()
    
    # 4. Disco
    print("[ DISCO ]")
    try:
        disco = subprocess.check_output(
            'wmic logicaldisk where DriveType=3 get DeviceID,Size,FreeSpace', 
            shell=True, 
            encoding='utf-8'
        ).split('\n')[1:4]
        
        for linha in disco:
            partes = linha.split()
            if len(partes) >= 3 and partes[0]:
                drive = partes[0]
                try:
                    total = int(partes[1]) / (1024**3)
                    livre = int(partes[2]) / (1024**3)
                    usado = ((int(partes[1]) - int(partes[2])) / (1024**3))
                    print(f"{drive} | Total: {total:.1f} GB | Livre: {livre:.1f} GB | Usado: {usado:.1f} GB")
                except:
                    continue
    except:
        print("Disco: Não detectado")
    print()
    
    # 5. Rede
    print("[ REDE ]")
    try:
        resultado = subprocess.run(
            ['ping', '-n', '1', '8.8.8.8'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        if resultado.returncode == 0:
            print("Internet: Conectado ✅")
        else:
            print("Internet: Sem conexão ❌")
    except:
        print("Internet: Falha no teste")
    print()
    
    # 6. Sugestões rápidas
    print("[ SUGESTÕES ]")
    if ram_gb < 8:
        print("- Considere aumentar a memória RAM (mínimo 8GB recomendado)")
    elif ram_gb < 16:
        print("- RAM ok, mas upgrade para 16GB melhoraria multitarefa")
    
    if ram_livre_gb < 2:
        print("- RAM disponível baixa. Feche programas pesados")
    
    print("\n" + "="*50)
    print("Relatório gerado pela CyberCrip Assistência Técnica")
    input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()