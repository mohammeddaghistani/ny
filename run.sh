#!/bin/bash

# سكربت تشغيل التطبيق

echo "🚀 تشغيل التطبيق المتكامل..."

# تثبيت المتطلبات
pip install -r requirements.txt

# إنشاء المجلدات المطلوبة
mkdir -p data/raw data/processed
mkdir -p models
mkdir -p logs

# تشغيل التطبيق
streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.maxUploadSize 500 \
    --theme.primaryColor "#FF4B4B"
