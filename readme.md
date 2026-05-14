# 🎮 Caro AI (Gomoku) - Project Documentation

Dự án **Game Caro (Gomoku)** tích hợp trí tuệ nhân tạo (AI) được xây dựng trên ngôn ngữ Python. Sản phẩm tập trung vào việc nghiên cứu và tối ưu hóa các thuật toán tìm kiếm trên không gian trạng thái, mang lại trải nghiệm thi đấu thông minh và mượt mà.

---

## 🌟 Tính năng nổi bật

* **Chế độ chơi đa dạng:** Hỗ trợ chơi với máy (PvE) và chơi hai người (PvP).
* **Trí tuệ nhân tạo (AI) chuyên sâu:**
    * **Thuật toán Minimax:** Xây dựng cây trò chơi và duyệt các nước đi khả thi để tìm kết quả tối ưu.
    * **Cắt tỉa Alpha-Beta:** Kỹ thuật tối ưu hóa giúp loại bỏ các nhánh cây không ảnh hưởng đến kết quả, cho phép AI duyệt sâu hơn (Depth 5+) mà không tốn nhiều tài nguyên.
    * **Zobrist Hashing:** Mã hóa trạng thái bàn cờ để lưu trữ vào **Transposition Table**, tránh tính toán lặp lại các thế cờ đã gặp.
    * **Heuristic Scoring:** Hệ thống chấm điểm dựa trên các mẫu cờ (Pattern Matching) để AI đưa ra quyết định tấn công/phòng thủ linh hoạt.
* **Giao diện đồ họa (GUI):** Xây dựng bằng thư viện **Pygame**, hình ảnh trực quan, có menu lựa chọn và thông báo kết quả sinh động.

---

## 🚀 Hướng dẫn cài đặt và Khởi chạy

### 1. Yêu cầu hệ thống
* Python 3.8 trở lên.
* Thư viện Pygame.

### 2. Cài đặt môi trường
Mở Terminal (hoặc Command Prompt) và thực hiện các lệnh sau:

```bash
# Clone repository về máy
git clone [https://github.com/Oceanius/24022304_LeDoTungDuong_CaroAI.git](https://github.com/Oceanius/24022304_LeDoTungDuong_CaroAI.git)
cd 24022304_LeDoTungDuong_CaroAI

# Cài đặt thư viện cần thiết
pip install pygame
### 3. Khởi động trò chơi
Chạy file play.py hoặc mở Terminal gõ: python play.py
