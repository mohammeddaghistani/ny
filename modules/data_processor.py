import pandas as pd
import numpy as np
from typing import Union, Dict, Any
import streamlit as st

class DataProcessor:
    """معالج بيانات أساسي"""
    
    def __init__(self, file_path=None):
        self.data = None
        self.file_path = file_path
        
    def load_data(self, file_path=None):
        """تحميل البيانات من ملف"""
        if file_path:
            self.file_path = file_path
            
        try:
            # دعم صيغ متعددة
            if self.file_path.name.endswith('.csv'):
                self.data = pd.read_csv(self.file_path)
            elif self.file_path.name.endswith('.xlsx'):
                self.data = pd.read_excel(self.file_path)
            elif self.file_path.name.endswith('.json'):
                self.data = pd.read_json(self.file_path)
            else:
                st.error("صيغة الملف غير مدعومة")
                return None
                
            st.success(f"تم تحميل {len(self.data)} صف و {len(self.data.columns)} عمود")
            return self.data
            
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات: {str(e)}")
            return None
    
    def get_info(self):
        """الحصول على معلومات عن البيانات"""
        if self.data is None:
            return "لا توجد بيانات"
        
        info = {
            'الصفوف': len(self.data),
            'الأعمدة': len(self.data.columns),
            'القيم الناقصة': self.data.isnull().sum().sum(),
            'أنواع البيانات': self.data.dtypes.to_dict()
        }
        return info
    
    def clean_data(self):
        """تنظيف البيانات"""
        if self.data is None:
            return None
        
        # حذف الصفوف المكررة
        self.data.drop_duplicates(inplace=True)
        
        # معالجة القيم الناقصة
        for col in self.data.columns:
            if self.data[col].dtype in ['int64', 'float64']:
                self.data[col].fillna(self.data[col].median(), inplace=True)
            else:
                self.data[col].fillna(self.data[col].mode()[0], inplace=True)
        
        return self.data
    
    def plot_data(self, chart_type="عمودي"):
        """إنشاء رسوم بيانية"""
        import matplotlib.pyplot as plt
        
        if self.data is None or len(self.data) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            sample_col = numeric_cols[0]
            
            if chart_type == "عمودي":
                self.data[sample_col].value_counts().head(10).plot(kind='bar', ax=ax)
                ax.set_title(f"توزيع {sample_col}")
            elif chart_type == "خطي":
                self.data[sample_col].plot(kind='line', ax=ax)
                ax.set_title(f"اتجاه {sample_col}")
            elif chart_type == "مبعثر" and len(numeric_cols) > 1:
                self.data.plot(kind='scatter', x=numeric_cols[0], y=numeric_cols[1], ax=ax)
                ax.set_title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
            elif chart_type == "توزيع":
                self.data[sample_col].plot(kind='hist', ax=ax, bins=30)
                ax.set_title(f"توزيع {sample_col}")
        
        plt.tight_layout()
        return fig
