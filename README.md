markdown
Copy code
# Py2exe Example

Dies ist ein einfaches Beispielprojekt, das zeigt, wie man `py2exe` verwendet, um Python-Skripte in ausführbare Windows-EXE-Dateien umzuwandeln.

## Voraussetzungen

- Python: Du musst Python auf deinem System installiert haben.
- pip: Du benötigst pip, um Python-Pakete zu installieren.

## Einschränkungen
Beachte, dass py2exe einige Einschränkungen hat und möglicherweise nicht mit allen Python-Bibliotheken oder -Funktionen kompatibel ist. Insbesondere Bibliotheken, die dynamisch geladene Module verwenden oder Python-Code zur Laufzeit generieren, können Schwierigkeiten bereiten.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen findest du in der LICENSE

## Installation als EXE

1. Lade dir die .exe Datei herunter
2. Führe sie aus

## Installation

1. Klone dieses Repository auf deinen Computer.

2. Navigiere zum Verzeichnis des Projekts in der Kommandozeile.

3. Installiere `py2exe` mithilfe von pip:

pip install py2exe


## Verwendung

1. Bearbeite die `main.py`-Datei, um deine Python-Skriptdatei(en) anzugeben, die in eine EXE-Datei umgewandelt werden sollen. 
2. Die ausführbare Datei und alle erforderlichen Dateien werden im dist-Verzeichnis erstellt.
3. Führe die erstellte EXE-Datei im dist-Verzeichnis aus, um dein Python-Programm zu starten.

```python
from distutils.core import setup
import py2exe

setup(console=['main.py'])
python setup.py py2exe

