import os
import tempfile
import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="Markdown → MP3 Pro", page_icon="🎧", layout="centered")

st.title("🎧 Markdown → MP3 Pro")
st.markdown("Chuyển đổi file Markdown sang MP3 ổn định qua Google Voice.")

# Chọn ngôn ngữ giọng đọc
lang_option = st.selectbox(
    "Chọn ngôn ngữ (Language):",
    ["English (en)", "Vietnamese (vi)"]
)
lang_code = "en" if "en" in lang_option else "vi"

st.markdown("---")
uploaded_file = st.file_uploader("Tải lên file Markdown (.md) của bạn:", type=["md", "txt"])

if uploaded_file is not None:
    markdown_content = uploaded_file.read().decode("utf-8")
    st.text_area("Xem trước nội dung:", markdown_content[:500] + "\n...", height=150)
    
    if st.button("🚀 Bắt đầu chuyển đổi sang MP3"):
        if not markdown_content.strip():
            st.warning("File trống hoặc không có nội dung!")
        else:
            with st.spinner("Đang tổng hợp giọng đọc từ Google..."):
                try:
                    # Tạo file MP3 bằng gTTS
                    tts = gTTS(text=markdown_content, lang=lang_code, slow=False)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        temp_audio_path = temp_audio.name
                    
                    tts.save(temp_audio_path)

                    st.success("🎉 Chuyển đổi thành công 100%!")
                    
                    # Trình phát audio nghe thử ngay trên web
                    st.audio(temp_audio_path, format="audio/mp3")

                    with open(temp_audio_path, "rb") as f:
                        st.download_button(
                            label="📥 Tải xuống file MP3",
                            data=f,
                            file_name=uploaded_file.name.replace(".md", ".mp3"),
                            mime="audio/mp3"
                        )

                    os.unlink(temp_audio_path)
                    
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {e}")
