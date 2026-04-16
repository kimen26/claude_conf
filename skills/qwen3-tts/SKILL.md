# Skill : qwen3-tts

> Synthèse vocale locale et clonage de voix avec Qwen3 TTS sur Windows 11 (CPU)

## Quand utiliser ce skill

Active ce skill quand l'utilisateur veut :
- Générer de l'audio à partir de texte (TTS)
- Cloner une voix à partir d'un court enregistrement
- Lancer ou déboguer l'interface Qwen3 TTS locale
- Ajouter des fonctionnalités à l'interface (batch, export, nouvelles langues)

---

## Installation (déjà faite)

```
C:\Users\yann.ponaire\qwen3-tts\
├── venv\               ← Python venv isolé
├── run_tts.py          ← Interface Gradio
├── lancer_tts.bat      ← Double-clic pour lancer
└── hf_cache\           ← Modèle ~2.5GB téléchargé ici
```

**Package clé** : `qwen-tts` (pas `transformers` seul — `AutoModel` ne supporte pas `qwen3_tts`)

---

## Lancer l'interface

```powershell
# Option 1 : Double-clic sur
C:\Users\yann.ponaire\qwen3-tts\lancer_tts.bat

# Option 2 : Terminal
cd C:\Users\yann.ponaire\qwen3-tts
venv\Scripts\activate
python run_tts.py
```

→ Ouvre `http://localhost:7860`

---

## API du modèle (référence développeur)

```python
from qwen_tts import Qwen3TTSModel
import torch

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    device_map="cpu",
    dtype=torch.float32,
)

# Voix prédéfinie (9 disponibles)
# Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_Anna, Sohee
wavs, sr = model.generate_custom_voice(
    text="Bonjour le monde !",
    language="French",
    speaker="Ryan",
)

# Clonage de voix (ref_text = transcription OBLIGATOIRE)
wavs, sr = model.generate_voice_clone(
    text="Texte à synthétiser avec ta voix",
    language="French",
    ref_audio="chemin/vers/ta_voix.wav",   # 3 sec minimum
    ref_text="Ce que dit exactement l'audio de référence",
)

import soundfile as sf
sf.write("output.wav", wavs[0], sr)
```

---

## Contraintes matérielles

| Spec | Valeur |
|------|--------|
| CPU | AMD Ryzen 7 PRO 5875U |
| RAM | 32 GB |
| GPU | Intégré Radeon (pas de CUDA/ROCm actif) |
| Mode | CPU uniquement → float32 |
| Perf | ~2-8 sec pour 30 sec d'audio |

**Conséquences** :
- Pas de `bfloat16` (CPU ne le supporte pas bien)
- Pas de `flash_attention_2` (GPU requis)
- Pas de `device_map="cuda:0"`

---

## Netskope (proxy SSL)

Le bundle SSL pour pip et HuggingFace :
```
C:\Users\yann.ponaire\netskope-full-bundle.crt
```

Dans `run_tts.py`, ces variables sont définies au démarrage :
```python
os.environ["REQUESTS_CA_BUNDLE"] = r"C:\Users\yann.ponaire\netskope-full-bundle.crt"
os.environ["SSL_CERT_FILE"] = r"C:\Users\yann.ponaire\netskope-full-bundle.crt"
```

Pour pip dans ce venv : `C:\Users\yann.ponaire\AppData\Roaming\pip\pip.ini` contient `trusted-host`.

---

## Dépannage

| Erreur | Solution |
|--------|----------|
| `qwen3_tts not recognized` | Tu utilises `transformers.AutoModel` — utiliser `from qwen_tts import Qwen3TTSModel` |
| `SSL certificate verify failed` | Vérifier que `netskope-full-bundle.crt` existe et que `pip.ini` est configuré |
| Cache dans mauvais dossier | Vérifier que `HF_HOME` est défini AVANT les imports |
| Audio lent | Normal sur CPU — 30 sec d'audio = ~2-8 sec de génération |
| `ref_text obligatoire` | Pour cloner une voix, transcrire mot pour mot l'audio de référence |

---

## Évolutions possibles

- [ ] Batch processing (plusieurs textes en une fois)
- [ ] Export automatique vers dossier horodaté
- [ ] Intégration N8N (POST → audio WAV)
- [ ] ROCm pour accélérer avec la Radeon intégrée
