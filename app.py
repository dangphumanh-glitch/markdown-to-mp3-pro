import asyncio
import os
import tempfile
import edge_tts
import streamlit as st

st.set_page_config(page_title="Markdown → MP3 Pro", page_icon="🎧", layout="centered")

st.title("🎧 Markdown → MP3 Pro")
st.markdown("Chuyển đổi file Markdown sang Audiobook với hệ thống giọng đọc AI đa dạng.")

# Phân loại chi tiết các tùy chọn giọng đọc theo Nam/Nữ và sắc thái
voice_options = {
    "🇺🇸 Nam Trầm Ấm / Chuyên nghiệp (Christopher - US)": "en-US-ChristopherNeural",
    "🇺🇸 Nam Tự Nhiên / Rõ ràng (Guy - US)": "en-US-GuyNeural",
    "🇺🇸 Nữ Truyền Cảm / Mượt mà (Aria - US)": "en-US-AriaNeural",
    "🇺🇸 Nữ Tươi Tắn / Thân thiện (Jenny - US)": "en-US-JennyNeural",
    "🇻🇳 Nam Tiếng Việt Trầm Ấm (NamMinh - VN)": "vi-VN-NamMinhNeural",
    "🇻🇳 Nữ Tiếng Việt Truyền Cảm (HoaiMy - VN)": "vi-VN-HoaiMyNeural"
}

selected_label = st.selectbox("Chọn phong cách giọng đọc:", list(voice_options.keys()))
voice_code = voice_options[selected_label]

st.markdown("---")
uploaded_file = st.file_uploader("Tải lên file Markdown (.md hoặc .txt) của bạn:", type=["md", "txt"])

if uploaded_file is not None:
    markdown_content = uploaded_file.read().decode("utf-8")
    st.text_area("Xem trước nội dung:", markdown_content[:500] + "\n...", height=150)
    
    if st.button("🚀 Bắt đầu chuyển đổi sang MP3"):
        if not markdown_content.strip():
            st.warning("File trống hoặc không có nội dung!")
        else:
            with st.spinner(f"Đang tổng hợp giọng đọc ({selected_label})..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        temp_audio_path = temp_audio.name

                    async def generate_speech():
                        # Cơ chế thử lại giúp kết nối ổn định, chống lỗi mạng
                        for attempt in range(3):
                            try:
                                communicate = edge_tts.Communicate(markdown_content, voice_code)
                                await communicate.save(temp_audio_path)
                                return
                            except Exception as err:
                                if attempt == 2:
                                    raise err
                                await asyncio.sleep(2)

                    asyncio.run(generate_speech())

                    st.success("🎉 Chuyển đổi thành công!")
                    
                    # Khung nghe thử trực tiếp ngay trên web
                    st.audio(temp_audio_path, format="audio/mp3")

                    with open(temp_audio_path, "rb") as f:
                        st.download_button(
                            label="📥 Tải xuống file MP3",
                            data=f,
                            file_name=uploaded_file.name.replace(".md", "_audio.mp3"),
                            mime="audio/mp3"
                        )

                    os.unlink(temp_audio_path)
                    
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi kết nối dịch vụ giọng đọc: {e}. Vui lòng bấm thử lại nút chuyển đổi.")
