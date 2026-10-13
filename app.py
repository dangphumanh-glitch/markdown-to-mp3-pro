import asyncio
import os
import tempfile
import edge_tts
import streamlit as st

st.set_page_config(page_title="Markdown → MP3 Pro", page_icon="🎧", layout="centered")

st.title("🎧 Markdown → MP3 Pro")
st.markdown("Chuyển đổi file Markdown sang MP3 chất lượng cao phục vụ làm Audiobook.")

voice = st.selectbox(
    "Chọn giọng đọc (Voice):",
    ["en-US-AriaNeural", "en-US-ChristopherNeural", "en-US-GuyNeural", "en-US-JennyNeural"],
    index=0
)

uploaded_file = st.file_uploader("Tải lên file Markdown (.md) của bạn:", type=["md", "txt"])

if uploaded_file is not None:
    markdown_content = uploaded_file.read().decode("utf-8")
    st.text_area("Xem trước nội dung:", markdown_content[:500] + "\n...", height=150)
    
    if st.button("🚀 Bắt đầu chuyển đổi sang MP3"):
        if not markdown_content.strip():
            st.warning("File trống hoặc không có nội dung!")
        else:
            with st.spinner("Đang kết nối tổng hợp giọng đọc..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        temp_audio_path = temp_audio.name

                    async def generate_speech():
                        # Thêm cơ chế thử lại nếu bị nghẽn mạng tạm thời
                        for attempt in range(3):
                            try:
                                communicate = edge_tts.Communicate(markdown_content, voice)
                                await communicate.save(temp_audio_path)
                                return
                            except Exception as err:
                                if attempt == 2:
                                    raise err
                                await asyncio.sleep(2)

                    asyncio.run(generate_speech())

                    st.success("🎉 Chuyển đổi thành công!")
                    
                    with open(temp_audio_path, "rb") as f:
                        st.download_button(
                            label="📥 Tải xuống file MP3",
                            data=f,
                            file_name=uploaded_file.name.replace(".md", ".mp3"),
                            mime="audio/mp3"
                        )

                    os.unlink(temp_audio_path)
                    
                except Exception as e:
                    st.error(f"Lỗi kết nối dịch vụ giọng đọc (403/Blocked). Vui lòng thử lại sau ít phút: {e}")
