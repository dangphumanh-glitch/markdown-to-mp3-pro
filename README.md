# Markdown → MP3 Pro

Phiên bản nâng cấp:
- Dán Markdown hoặc tải `.md`
- Tự làm sạch Markdown
- Tự chia văn bản dài thành các đoạn TTS
- Tự tách chương theo Heading # / ##
- Nhiều giọng Việt/Anh/Nhật/Trung
- Chỉnh tốc độ, cao độ, âm lượng
- Chỉnh khoảng nghỉ giữa đoạn
- Tạo MP3 từng chương
- Ghép toàn bộ thành một audiobook MP3
- MP3 192 kbps

## Cài đặt

Python 3.10+:

```bash
pip install -r requirements.txt
```

Ngoài ra cần FFmpeg để pydub đọc/ghép MP3:
- Windows: cài FFmpeg và thêm thư mục `bin` vào PATH.
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`

## Chạy

```bash
streamlit run app.py
```

Trình duyệt sẽ mở giao diện.
