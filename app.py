import asyncio
import os
import tempfile
import edge_tts
from pydub import AudioSegment
import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Markdown → MP3 Pro (Spotify Quality)", page_icon="🎧", layout="centered")

st.title("🎧 Markdown → MP3 Pro (Chuẩn Spotify)")
st.markdown("Chuyển đổi file Markdown sang MP3 chất lượng cao (44.1 kHz, Bitrate chuẩn) dành riêng cho việc phát hành Audiobook.")

# Chọn giọng đọc tiếng Anh (hoặc thay đổi tùy ý)
voice = st.selectbox(
    "Chọn giọng đọc (Voice):",
    ["en-US-AriaNeural", "en-US-ChristopherNeural", "en-US-GuyNeural", "en-US-JennyNeural"],
    index=0
)

uploaded_file = st.file_uploader("Tải lên file Markdown (.md) của bạn:", type=["md", "txt"])

if uploaded_file is not None:
    # Đọc nội dung file Markdown
    markdown_content = uploaded_file.read().decode("utf-8")
    
    st.text_area("Xem trước nội dung:", markdown_content[:500] + "\n...", height=150)
    
    if st.button("🚀 Bắt đầu chuyển đổi sang MP3 chuẩn Spotify"):
        if not markdown_content.strip():
            st.warning("File trống hoặc không có nội dung!")
        else:
            with st.spinner("Đang tổng hợp giọng đọc và xử lý âm thanh chất lượng cao..."):
                try:
                    # Tạo file tạm cho audio gốc từ edge-tts
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        temp_audio_path = temp_audio.name

                    # Chạy edge-tts bất đồng bộ
                    async def generate_speech():
                        communicate = edge_tts.Communicate(markdown_content, voice)
                        await communicate.save(temp_audio_path)

                    asyncio.run(generate_speech())

                    # Sử dụng pydub + ffmpeg để chuẩn hóa âm thanh đạt chuẩn Spotify (44.1 kHz, chất lượng cao)
                    output_mp3_path = temp_audio_path.replace(".mp3", "_spotify.mp3")
                    
                    # Nạp file và ép chuẩn xuất âm thanh
                    sound = AudioSegment.from_file(temp_audio_path)
                    sound = sound.set_frame_rate(44100) # Ép chuẩn 44.1 kHz theo yêu cầu Spotify
                    sound.export(
                        output_mp3_path, 
                        format="mp3", 
                        bitrate="192k", # Đảm bảo bitrate cao, không bị rè hoặc giảm chất lượng
                        parameters=["-ar", "44100"]
                    )

                    st.success("🎉 Chuyển đổi thành công! File đã đạt chuẩn kỹ thuật để đưa lên Spotify.")
                    
                    # Cung cấp nút tải file MP3 chuẩn
                    with open(output_mp3_path, "rb") as f:
                        st.download_button(
                            label="📥 Tải xuống file MP3 (Chuẩn Spotify)",
                            data=f,
                            file_name=uploaded_file.name.replace(".md", "_spotify_ready.mp3"),
                            mime="audio/mp3"
                        )

                    # Dọn dẹp file tạm
                    os.unlink(temp_audio_path)
                    
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")