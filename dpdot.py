from datetime import datetime
import pandas as pd
import streamlit as st

# إعدادات صفحة التطبيق العصري
st.set_page_config(
    page_title="مُرتوي - تطبيق مريض السكري الذكي", page_icon="🩺", layout="centered"
)

# عنوان وتصميم الواجهة
st.markdown(
    """
    <div style='text-align: center; padding: 10px;'>
        <h1 style='color: #1E3A8A;'>🩺 تطبيق مريض السكري الذكي</h1>
        <p style='color: #64748B; font-size: 16px;'>منظومة متكاملة لمتابعة مستويات السكر وتذكيرات الأدوية والأنسولين.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# تهيئة القوائم المؤقتة في الجلسة
if "sugar_records" not in st.session_state:
  st.session_state.sugar_records = []
if "med_records" not in st.session_state:
  st.session_state.med_records = []

# استخدام التبويبات العصرية لتنظيم التطبيق
tab1, tab2 = st.tabs(["🩸 متابعة السكر اليومي", "⏰ تذكير الأدوية والجرعات"])

with tab1:
  st.subheader("تسجيل قراءات السكر في الدم")
  col1, col2 = st.columns(2)

  with col1:
    sugar_val = st.number_input(
        "مستوى السكر (mg/dL)", min_value=30, max_value=600, value=120, step=1
    )

  with col2:
    meal_status = st.selectbox(
        "حالة القياس",
        ["صائم (Fasting)", "بعد الوجبة (Postprandial)", "عشوائي (Random)"],
    )

  if st.button("حفظ قراءة السكر", use_container_width=True, type="primary"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # التقييم والتنبيه الفوري
    if sugar_val < 70:
      note = "منخفض ⚠️"
    elif sugar_val > 180:
      note = "مرتفع 🚨"
    else:
      note = "طبيعي ✅"

    st.session_state.sugar_records.insert(
        0,
        {
            "الوقت": now,
            "القراءة (mg/dL)": sugar_val,
            "الحالة": meal_status,
            "التقييم": note,
        },
    )
    st.success("تم حفظ قراءة السكر بنجاح!")

  if st.session_state.sugar_records:
    st.markdown("---")
    st.subheader("📊 سجل القراءات السابقة")
    df_sugar = pd.DataFrame(st.session_state.sugar_records)
    st.dataframe(df_sugar, use_container_width=True)

    # منحنى بياني متطور لتطور السكر
    st.line_chart(
        df_sugar.set_index("الوقت")["القراءة (mg/dL)"], use_container_width=True
    )

with tab2:
  st.subheader("إدارة مواعيد الأدوية والأنسولين")
  med_name = st.text_input(
      "اسم الدواء أو الأنسولين", placeholder="مثال: لانتوس، أكتبريد..."
  )
  med_time = st.text_input("وقت الجرعة والتذكير", placeholder="مثال: 08:00 صباحاً")

  if st.button("إضافة تذكير الدواء", use_container_width=True, type="primary"):
    if med_name and med_time:
      st.session_state.med_records.insert(
          0,
          {"الدواء": med_name, "موعد الجرعة": med_time, "الحالة": "مفعل ✅"},
      )
      st.success(f"تم إضافة تذكير الدواء ({med_name}) بنجاح!")
    else:
      st.error("الرجاء إدخال اسم الدواء ووقت الجرعة تماماً!")

  if st.session_state.med_records:
    st.markdown("---")
    st.subheader("💊 قائمة الأدوية المجدولة")
    df_med = pd.DataFrame(st.session_state.med_records)
    st.dataframe(df_med, use_container_width=True)