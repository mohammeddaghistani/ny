import os
import subprocess
from pathlib import Path

print("🔍 التحقق من هيكل المجلدات...")

current_dir = Path(__file__).parent
required = {
    "app.py": current_dir / "app.py",
    "modules/": current_dir / "modules",
    "modules/__init__.py": current_dir / "modules" / "__init__.py",
    "modules/data_processor.py": current_dir / "modules" / "data_processor.py",
    "modules/models.py": current_dir / "modules" / "models.py",
    "modules/utils.py": current_dir / "modules" / "utils.py"
}

for name, path in required.items():
    if path.exists():
        print(f"✅ {name}")
    else:
        print(f"❌ {name} - مفقود")

print("\n🚀 تشغيل التطبيق...")
os.system("streamlit run app.py")
