import asyncio
import os
import tempfile
import edge_tts
import streamlit as st

st.set_page_config(page_title="Markdown → MP3 Pro", page_icon="🎧", layout="centered")

st.title("🎧 Markdown → MP3 Pro")
st.markdown("Chuyển đổi file Markdown sang MP3 chất lượng cao phục vụ làm Audiobook.")

# Danh sách giọng đọc kèm câu mẫu để nghe thử
voice_options = {
    "Aria (Nữ - US, Mượt mà, truyền cảm)": "en-US-AriaNeural",
    "Christopher (Nam - US, Trầm ấm, chuyên nghiệp)": "en-US-ChristopherNeural",
    "Guy (Nam - US, Rõ ràng, tự nhiên)": "en-US-GuyNeural",
    "Jenny (Nữ - US, Tươi tắn, thân thiện)": "en-US-JennyNeural"
}

col1, col2 = st.columns([3, 1])
with col1:
    selected_voice_label = st.selectbox("Chọn giọng đọc (Voice):", list(voice_options.keys()))
    voice = voice_options[selected_voice_label]

with col2:
    st.write("")
    st.write("")
    preview_btn = st.button("🔊 Nghe thử giọng")

# Xử lý khi bấm nút nghe thử giọng mẫu
if preview_btn:
    with st.spinner("Đang tạo âm thanh mẫu..."):
        try:
            sample_text = "Hello! This is a sample preview of the selected voice for your audiobook."
            sample_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            
            async def generate_sample():
                communicate = edge_tts.Communicate(sample_text, voice)
                await communicate.save(sample_path)

            asyncio.run(generate_sample())
            st.audio(sample_path, format="audio/mp3", autoplay=True)
            # os.unlink(sample_path) # Giữ lại để phát trực tiếp trên UI
        except Exception as e:
            st.error(f"Không thể phát âm thanh mẫu: {e}")

st.markdown("---")
uploaded_file = st.file_uploader("Tải lên file Markdown (.md) của bạn:", type=["md", "txt"])

if uploaded_file is not None:
    markdown_content = uploaded_file.read().decode("utf-8")
    st.text_area("Xem trước nội dung:", markdown_content[:500] + "\n...", height=150)
    
    if st.button("🚀 Bắt đầu chuyển đổi sang MP3"):
        if not markdown_content.strip():
            st.warning("File trống hoặc không có nội dung!")
        else:
            with st.spinner("Đang tổng hợp giọng đọc và tạo file..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        temp_audio_path = temp_audio.name

                    async def generate_speech():
                        communicate = edge_tts.Communicate(markdown_content, voice)
                        await communicate.save(temp_audio_path)

                    asyncio.run(generate_speech())

                    st.success("🎉 Chuyển đổi thành công!")
                    
                    # Trình phát audio nghe thử file hoàn chỉnh
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
                    st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")
