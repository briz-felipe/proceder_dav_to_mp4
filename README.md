# README - Conversor de Vídeos DAV para MP4

## 📌 Visão Geral

Este projeto fornece uma solução para conversão de vídeos no formato DAV para MP4 utilizando FFmpeg, com processamento assíncrono para melhor performance. O script também extrai metadados importantes e gera thumbnails dos vídeos.

## 🛠 Pré-requisitos

- Python 3.8 ou superior
- FFmpeg (será instalado automaticamente se não estiver presente)
- Sistema operacional: Windows, Linux ou macOS

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone git@github.com:briz-felipe/proceder_dav_to_mp4.git
cd proceder_dav_to_mp4
```

### 2. Crie e ative um ambiente virtual (recomendado)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🏗 Estrutura de Diretórios (Recomendada vs Personalizada)

### 🟢 Configuração Recomendada (Padrão)

Crie a seguinte estrutura de pastas na raiz do projeto (elas também serão criadas automaticamente na primeira execução):

```
video-converter/
├── input_videos/       # (Padrão) Coloque seus arquivos .dav aqui
├── output_videos/      # (Padrão) Arquivos MP4 convertidos serão salvos aqui
├── img/                # (Padrão) Thumbnails gerados automaticamente (opcional)
├── main.py             # Script principal
├── README.md           # Este arquivo
└── requirements.txt    # Dependências do projeto
```

### 🔵 Configuração Personalizada (Avançado)

Você pode usar caminhos absolutos em qualquer local do seu computador:

1. **Edite diretamente no código**:
   ```python
   if __name__ == "__main__":
       input_path = 'C:/caminho/absoluto/para/seus/videos'  # Modifique aqui
       output_path = 'D:/outro/caminho/para/saida'          # Modifique aqui
       # ...
   ```

## ▶️ Como Executar

### Conversão básica:

```bash
python main.py
```

## 🔄 Fluxo de Processamento

1. O script verifica se o FFmpeg está instalado e tenta instalá-lo se necessário
2. Varre o diretório de entrada em busca de arquivos .dav
3. Para cada vídeo:
   - Converte para MP4 (codec copy para máxima velocidade)
   - Gera um thumbnail (primeiro frame do vídeo)
   - Extrai metadados (duração, tamanho do arquivo)
   - Analisa o nome do arquivo para obter informações adicionais
4. Salva um relatório CSV com todos os metadados

## 🏷 Formato do Nome do Arquivo

O script espera arquivos no formato:

```
ORIGEM-CANAL-CAMERA-ANO-MES-DIA-HORA-MINUTO-SEGUNDO.dav
```

Exemplo: `COMPANY-01-CAM12-2023-05-15-14-30-00.dav`

Se seus arquivos usam um formato diferente, modifique a função `convert_dav_to_mp4` no script.

## 📊 Saída

Após a execução, você terá:

1. Arquivos MP4 convertidos em `output_videos/`
2. Thumbnails em JPG em `img/`
3. Um arquivo CSV `output_videos.csv` com os metadados:

| origem | chanel | camera | final_gravacao       | duration | file_size |
|--------|--------|--------|----------------------|----------|-----------|
| COMPANY| 01     | CAM12  | 2023-05-15 14:30:00  | 00:05:23 | 24.56 MB  |

## 🐛 Solução de Problemas

### FFmpeg não instalado automaticamente

Se o script não conseguir instalar o FFmpeg automaticamente:

**Windows:**
1. Instale via Chocolatey: `choco install ffmpeg` (como administrador)
2. Ou baixe manualmente: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Problemas com caminhos

- Certifique-se de que os caminhos não contenham caracteres especiais
- No Windows, use barras invertidas (`\`) ou raw strings (`r'caminho'`)

### Outros problemas

Execute com modo verbose para ver mais detalhes:

```bash
python converter.py 2> debug.log
```

Verifique o arquivo `debug.log` para mensagens de erro detalhadas.

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch com sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## ✉️ Contato
briz.felipe@gmail.com
