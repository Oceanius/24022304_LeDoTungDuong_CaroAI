# 🎮 Caro AI (Gomoku) - Cơ sở Trí tuệ nhân tạo

Dự án đồ án **Game Caro (Gomoku)** tích hợp trí tuệ nhân tạo (AI) sử dụng các thuật toán tối ưu hóa tìm kiếm.
## 🌟 Tính năng nổi bật
* **Chế độ chơi:** Hỗ trợ chơi với máy (PvE) và chơi hai người (PvP).
* **Trí tuệ nhân tạo (AI) mạnh mẽ:**
    * **Thuật toán Minimax:** Xây dựng cây trò chơi và duyệt các nước đi khả thi. AI đóng vai trò người chơi MAX (tối đa hóa lợi ích) và giả định đối thủ là người chơi MIN (tối thiểu hóa lợi ích của máy).
    * **Cắt tỉa Alpha-Beta (Alpha-Beta Pruning):** Kỹ thuật bổ trợ cực kỳ quan trọng giúp loại bỏ các nhánh không cần thiết trong cây tìm kiếm. Khi phát hiện một nước đi chắc chắn tệ hơn nước đi đã tìm thấy trước đó, AI sẽ ngừng duyệt nhánh đó, giúp tăng tốc độ xử lý gấp nhiều lần.
    * **Zobrist Hashing & Transposition Table:** Mã hóa trạng thái bàn cờ để tránh tính toán lại những thế cờ đã gặp, giúp AI xử lý mượt mà ngay cả ở độ sâu lớn.
    * **Heuristic Scoring:** Hệ thống chấm điểm thế cờ dựa trên các mẫu (patterns) phổ biến (ví dụ: chuỗi 4 quân hở đầu, chuỗi 3 quân bị chặn...).

## 🧠 Phân tích thuật toán AI
AI trong dự án được triển khai tập trung tại `source/AI.py` với các kỹ thuật chính:
1. **Minimax & Alpha-Beta:** Lõi xử lý quyết định nước đi. AI sẽ duyệt đến độ sâu 5 (hoặc tùy chỉnh) để tìm ra nước đi có điểm số cao nhất.
2. **Hàm đánh giá (Evaluation):** Nằm trong `source/utils.py`, sử dụng một `patternDict` để chấm điểm các chuỗi quân cờ trên các hàng ngang, dọc và hai đường chéo.
3. **Phạm vi tìm kiếm (Bound Search):** Để tối ưu, AI chỉ tính toán trong các ô trống xung quanh quân cờ đã đặt (trong bán kính nhất định) thay vì toàn bộ bàn cờ 15x15.

## 📂 Cấu trúc thư mục
```text
📦 24022304_LeDoTungDuong_CaroAI
 ┣ 📂 assets           # Chứa tài nguyên hình ảnh (board, black/white piece)
 ┣ 📂 gui              # Quản lý giao diện người dùng
 ┃ ┣ 📜 button.py      # Lớp xử lý nút bấm
 ┃ ┗ 📜 interface.py   # Xử lý render đồ họa Pygame
 ┣ 📂 source           # Logic xử lý chính
 ┃ ┣ 📜 AI.py          # Triển khai thuật toán Minimax và Alpha-Beta
 ┃ ┣ 📜 gomoku.py      # Điều khiển luồng trận đấu
 ┃ ┗ 📜 utils.py       # Hàm tính điểm Heuristic và Zobrist Table
 ┣ 📜 play.py          # File chạy chính của trò chơi
 ┗ 📜 README.md        # Tài liệu hướng dẫn
