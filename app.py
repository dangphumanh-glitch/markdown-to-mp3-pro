import asyncio
import os
import tempfile
import edge_tts
import streamlit as st

st.set_page_config(page_title="Markdown → MP3 Pro", page_icon="🎧", layout="centered")

st.title("🎧 Markdown → MP3 Pro")
st.markdown("Chuyển đổi file Markdown sang MP3 chất lượng cao phục vụ làm Audiobook.")

# Chọn giọng đọc chuẩn
voice = st.selectbox(
    "Chọn giọng đọc (Voice):",
    [
        "en-US-AriaNeural (Nữ - Mượt mà, truyền cảm)",
        "en-US-ChristopherNeural (Nam - Trầm ấm, chuyên nghiệp)",
        "en-US-GuyNeural (Nam - Rõ ràng, tự nhiên)",
        "en-US-JennyNeural (Nữ - Tươi tắn, thân thiện)"
    ]
)
# Lấy mã giọng thực tế từ chuỗi lựa chọn
voice_code = voice.split(" ")[0]

st.markdown("---")
uploaded_file = st.file_uploader("Tải lên file Markdown (.md) của bạn:", type=["md", "txt"])

if uploaded_file is not None:
    markdown_content = uploaded_file.read().decode("utf-8")
    st.text_area("Xem trước nội dung:", markdown_content[:500] + "\n...", height=150)
    
    if st.button("🚀 Bắt đầu chuyển đổi sang MP3"):
        if not markdown_content.strip():
            st.warning("File trống hoặc không có nội dung!")
        else:
            with st.spinner("Đang tổng hợp giọng đọc và tạo file hoàn chỉnh..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        temp_audio_path = temp_audio.name

                    async def generate_speech():
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
                    
                    # Nghe thử trực tiếp file MP3 hoàn chỉnh ngay trên web
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
                    st.error(f"Đã xảy ra lỗi kết nối dịch vụ: {e}")
