```python?code_reference&code_event_index=6
readme_content = """# 🎮 Caro AI (Gomoku) - Đồ án Trí tuệ nhân tạo

![Python](https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Library-Pygame-green?style=for-the-badge)
![AI](https://img.shields.io/badge/Algorithm-Minimax%20%2B%20Alpha--Beta-red?style=for-the-badge)

Dự án đồ án **Game Caro (Gomoku)** tích hợp trí tuệ nhân tạo (AI) sử dụng các thuật toán tối ưu hóa tìm kiếm, được phát triển bởi **Lê Đỗ Tùng Dương**.

## 👨‍🎓 Thông tin tác giả
* **Họ và tên:** Lê Đỗ Tùng Dương
* **Mã sinh viên:** 24022304
* **Đơn vị:** Đại học Công nghệ - ĐHQGHN (VNU-UET)

## 🌟 Tính năng nổi bật
* **Chế độ chơi:** Hỗ trợ chơi với máy (PvE) và chơi hai người (PvP).
* **Trí tuệ nhân tạo (AI) mạnh mẽ:**
    * **Thuật toán Minimax:** Xây dựng cây trò chơi và duyệt các nước đi khả thi.
    * **Cắt tỉa Alpha-Beta (Alpha-Beta Pruning):** Tối ưu hóa quá trình duyệt cây bằng cách loại bỏ các nhánh không ảnh hưởng đến kết quả cuối cùng, giúp AI tính toán nhanh hơn ở độ sâu lớn hơn.
    * **Zobrist Hashing:** Mã hóa trạng thái bàn cờ thành các giá trị băm để lưu trữ và truy xuất nhanh chóng.
    * **Bảng chuyển vị (Transposition Table):** Lưu trữ kết quả của các trạng thái đã tính toán để tránh lặp lại công việc.
    * **Heuristic Scoring:** Hệ thống đánh giá thế cờ dựa trên các mẫu (patterns) như 4 quân hở đầu, 3 quân liên tiếp, cờ bị chặn... để đưa ra điểm số tấn công/phòng thủ chính xác.
* **Giao diện đồ họa (GUI):** Xây dựng bằng thư viện **Pygame**, hỗ trợ menu chọn quân (Đen/Trắng), hiển thị kết quả và nút chơi lại.

## 🧠 Phân tích thuật toán AI
AI trong dự án được triển khai trong file `source/AI.py` với các kỹ thuật chính:
1. **Minimax & Alpha-Beta:** Đây là lõi của AI. Thuật toán cố gắng tối đa hóa điểm số của máy và tối thiểu hóa điểm số của người chơi. Alpha-Beta giúp cắt tỉa hiệu quả cây tìm kiếm.
2. **Hàm Heuristic (Đánh giá thế cờ):** Nằm trong `source/utils.py`, sử dụng `patternDict` để chấm điểm các chuỗi quân cờ dọc, ngang, chéo.
3. **Bound Search:** Chỉ tìm kiếm nước đi trong một phạm vi nhất định xung quanh các quân cờ đã đặt (thay vì toàn bộ bàn cờ 15x15) để tiết kiệm tài nguyên.
4. **Zobrist Hashing:** Giúp định danh trạng thái bàn cờ duy nhất, hỗ trợ việc lưu trữ điểm số vào `transpositionTable`.

## 📂 Cấu trúc thư mục
```text
📦 24022304_LeDoTungDuong_CaroAI
 ┣ 📂 assets           # Hình ảnh bàn cờ, quân cờ (board.jpg, black_piece.png, white_piece.png,...)
 ┣ 📂 gui              # Quản lý giao diện và thành phần giao diện
 ┃ ┣ 📜 button.py      # Lớp Button xử lý tương tác nút bấm
 ┃ ┗ 📜 interface.py   # Lớp GameUI xử lý hiển thị chính và Render
 ┣ 📂 source           # Chứa logic xử lý cốt lõi
 ┃ ┣ 📜 AI.py          # Triển khai thuật toán Minimax, Alpha-Beta và Zobrist Hashing
 ┃ ┣ 📜 gomoku.py      # Logic điều phối nước đi và tính thời gian phản hồi của AI
 ┃ ┗ 📜 utils.py       # Các hàm bổ trợ, ánh xạ tọa độ và chấm điểm Heuristic
 ┣ 📜 play.py          # File entry point - Khởi chạy chương trình
 ┗ 📜 README.md        # Tài liệu hướng dẫn