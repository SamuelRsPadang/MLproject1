# Informasi cara menjalankan dashoard.

## Setup Environment 
Lokasi di dalam folder project `submission_data_python` dengan file `requirement.txt`

### PowerShell

```
python -m venv myenv

.\myenv\Scripts\activate.ps1

pip install -r requirements.txt
```

### Streamlit
Setelah setup install package dari `reqirements.txt` selesai. Dalam project folder, jalankan:
```
streamlit run dashboard/dashboard.py
```