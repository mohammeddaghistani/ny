import streamlit as st
import sys
import os
from pathlib import Path

# إضافة مسار الوحدات
sys.path.append(str(Path(__file__).parent / "modules"))

# استيراد وحداتك الحالية
from data_processor import DataProcessor
from models import ModelManager
import utils

# إعداد الصفحة
st.set_page_config(
    page_title="اسم تطبيقك الكامل",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# إدارة الجلسة
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.data = None
    st.session_state.model = None
    st.session_state.results = {}

# 🔧 الشريط الجانبي
with st.sidebar:
    st.image("assets/images/logo.png", width=150)
    st.title("لوحة التحكم")
    
    # قسم التحميل
    st.header("📁 تحميل البيانات")
    uploaded_file = st.file_uploader(
        "اختر ملف البيانات", 
        type=['csv', 'xlsx', 'json', 'txt']
    )
    
    # قسم الإعدادات
    st.header("⚙️ الإعدادات")
    mode = st.selectbox(
        "وضع التشغيل",
        ["تطوير", "إنتاج", "اختبار"]
    )
    
    # خيارات متقدمة
    with st.expander("خيارات متقدمة"):
        cache_enabled = st.checkbox("تفعيل التخزين المؤقت", True)
        debug_mode = st.checkbox("وضع التصحيح", False)
    
    st.divider()
    st.caption(f"الإصدار: 1.0.0 | الوضع: {mode}")

# 🎯 المنطقة الرئيسية
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 الرئيسية", 
    "📊 البيانات", 
    "🤖 النماذج", 
    "📈 النتائج"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("مرحباً بك في تطبيقك المتكامل 🎉")
        st.markdown("""
        ### مميزات التطبيق:
        - ✅ معالجة البيانات المتقدمة
        - ✅ نماذج الذكاء الاصطناعي
        - ✅ تصورات تفاعلية
        - ✅ إدارة كاملة
        """)
        
        # أزرار سريعة
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            if st.button("🚀 بدء التشغيل", use_container_width=True):
                st.session_state.initialized = True
                st.rerun()
        
        with col1_2:
            if st.button("🔄 إعادة تعيين", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        
        with col1_3:
            if st.button("📊 توليد تقرير", use_container_width=True):
                with st.spinner("جاري إنشاء التقرير..."):
                    report = utils.generate_report()
                    st.success("تم إنشاء التقرير!")
    
    with col2:
        st.info("**حالة النظام:**")
        st.metric("الذاكرة المستخدمة", "2.4 GB")
        st.metric("البيانات المحملة", 
                 "✓" if st.session_state.data else "✗")
        st.metric("النموذج جاهز", 
                 "✓" if st.session_state.model else "✗")

with tab2:
    st.header("إدارة البيانات")
    
    if uploaded_file:
        # معالجة الملف المرفوع
        processor = DataProcessor(uploaded_file)
        df = processor.load_data()
        
        st.session_state.data = df
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("معاينة البيانات")
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("إحصائيات")
            st.write(f"الصفوف: {df.shape[0]}")
            st.write(f"الأعمدة: {df.shape[1]}")
        
        with col2:
            st.subheader("تصور سريع")
            chart_type = st.selectbox(
                "نوع الرسم",
                ["خطي", "عمودي", "مبعثر", "توزيع"]
            )
            
            if st.button("إنشاء رسم بياني"):
                fig = processor.plot_data(chart_type)
                st.pyplot(fig)
    else:
        st.warning("⚠️ يرجى تحميل ملف بيانات أولاً")

with tab3:
    st.header("النماذج والتدريب")
    
    model_options = ["شبكة عصبية", "شجرة قرار", "SVM", "تجمع"]
    selected_model = st.selectbox("اختر النموذج", model_options)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # إعداد النموذج
        st.subheader("معلمات النموذج")
        
        with st.form("model_form"):
            epochs = st.slider("عدد الدورات", 1, 100, 10)
            learning_rate = st.slider("معدل التعلم", 0.001, 0.1, 0.01)
            batch_size = st.selectbox("حجم الدفعة", [16, 32, 64, 128])
            
            submitted = st.form_submit_button("🎯 تدريب النموذج")
            
            if submitted and st.session_state.data is not None:
                with st.spinner("جاري التدريب..."):
                    manager = ModelManager(selected_model)
                    model, history = manager.train(
                        st.session_state.data,
                        epochs=epochs,
                        lr=learning_rate,
                        batch_size=batch_size
                    )
                    st.session_state.model = model
                    st.session_state.results['history'] = history
                    st.success("تم التدريب بنجاح!")
    
    with col2:
        st.subheader("تقييم النموذج")
        if st.session_state.model:
            metrics = manager.evaluate()
            
            for name, value in metrics.items():
                st.metric(name, f"{value:.4f}")
            
            if 'history' in st.session_state.results:
                # رسم منحنى التعلم
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                history = st.session_state.results['history']
                ax.plot(history['loss'], label='Loss')
                ax.plot(history['val_loss'], label='Val Loss')
                ax.legend()
                st.pyplot(fig)

with tab4:
    st.header("النتائج والتقارير")
    
    if st.session_state.results:
        # عرض النتائج
        st.subheader("ملخص الأداء")
        
        # جدول النتائج
        results_df = utils.results_to_dataframe(st.session_state.results)
        st.dataframe(results_df, use_container_width=True)
        
        # تصدير النتائج
        col1, col2, col3 = st.columns(3)
        export_format = col1.selectbox(
            "صيغة التصدير",
            ["CSV", "Excel", "JSON", "PDF"]
        )
        
        if col2.button("💾 حفظ النتائج"):
            utils.export_results(
                st.session_state.results, 
                export_format.lower()
            )
            st.success(f"تم التصدير بصيغة {export_format}")
        
        if col3.button("📧 إرسال بالبريد"):
            email = st.text_input("البريد الإلكتروني")
            if email:
                utils.send_results_email(email, st.session_state.results)
                st.success("تم الإرسال!")
    else:
        st.info("لا توجد نتائج لعرضها. قم بتدريب نموذج أولاً.")

# 🎯 الأزرار السفلية
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    if st.button("❓ المساعدة", use_container_width=True):
        st.info("راجع الوثائق في docs/")

with footer_col2:
    if st.button("📖 السجلات", use_container_width=True):
        st.code(utils.get_logs(), language="text")

with footer_col3:
    if st.button("🚪 خروج", use_container_width=True):
        st.session_state.clear()
        st.stop()

# 🛠️ وظائف مساعدة
@st.cache_data
def load_config():
    import json
    with open("assets/config.json") as f:
        return json.load(f)

@st.cache_resource
def initialize_components():
    # تهيئة المكونات الثقيلة هنا
    return {
        "processor": DataProcessor(),
        "models": ModelManager()
    }
