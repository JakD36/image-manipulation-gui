# Install Dependencies

```bash
pip install -r requirements.txt
```

# Create Standalone Application
from the project root directory.
```bash
pyinstaller src/main.py --onefile -w --name CreateSatImages  
```
Options:

-w prevents console opening when opening app (Form mac this pushes it to create an app bundle)

--onefile creates a single easy to distribute file

--name sets name of the application bundle