Caro AI 🎮

Đây là project game Caro (Gomoku) được viết bằng Python và thư viện Pygame.
Người chơi sẽ đấu với AI trên bàn cờ 15x15, trong đó AI sử dụng thuật toán Minimax kết hợp Alpha-Beta Pruning để tìm nước đi tối ưu.

Project được thực hiện với mục đích học tập và tìm hiểu về:

AI trong game
Thuật toán Minimax
Alpha-Beta Pruning
Zobrist Hashing
Xử lý giao diện bằng Pygame
Demo Gameplay
Người chơi chọn quân đen hoặc trắng
AI sẽ tự động tính toán nước đi
Game tự kiểm tra thắng/thua
Có thể chơi lại sau khi kết thúc
Công nghệ sử dụng
Python
Pygame
Thuật toán AI

AI trong project sử dụng:

Minimax Algorithm

Thuật toán Minimax giúp AI mô phỏng các nước đi trong tương lai để chọn ra nước đi tốt nhất.

Alpha-Beta Pruning

Kết hợp với Minimax để cắt tỉa các nhánh không cần thiết, giúp tăng tốc độ xử lý.

Heuristic Evaluation

Bàn cờ được đánh giá dựa trên các pattern như:

4 quân liên tiếp
Open 3
Broken 3
Open 2
...

Mỗi pattern sẽ có điểm số riêng để AI đánh giá thế cờ.

Zobrist Hashing

Dùng để lưu trạng thái bàn cờ trong Transposition Table nhằm giảm việc tính toán lại các trạng thái đã xét.

Cấu trúc project
24022304_LeDoTungDuong_CaroAI
│
├── assets/                # Hình ảnh giao diện và quân cờ
│   ├── black_piece.png
│   ├── white_piece.png
│   ├── board.jpg
│   └── ...
│
├── gui/                   # Giao diện game
│   ├── button.py
│   └── interface.py
│
├── source/
│   ├── AI.py              # Xử lý AI và thuật toán Minimax
│   ├── gomoku.py          # Logic lượt đi của AI
│   ├── utils.py           # Các hàm hỗ trợ
│   └── ...
│
├── play.py                # File chạy game chính
└── README.md
Cách chạy project
1. Clone repository
git clone https://github.com/Oceanius/24022304_LeDoTungDuong_CaroAI.git
2. Di chuyển vào thư mục project
cd 24022304_LeDoTungDuong_CaroAI
3. Cài thư viện cần thiết
pip install pygame
4. Chạy game
python play.py
Một vài đặc điểm của AI
AI ưu tiên các nước đi nguy hiểm
Có đánh giá threat level để sắp xếp candidate moves
Có sử dụng Transposition Table để tối ưu Minimax
Có incremental evaluation giúp giảm thời gian tính toán
Hạn chế
Khi tăng depth lớn thì AI tính toán vẫn khá chậm
Giao diện còn đơn giản
Chưa có nhiều mức độ khó
Chưa hỗ trợ chơi online
Hướng phát triển
Tối ưu tốc độ AI
Thêm nhiều độ khó
Thêm animation và âm thanh
Thêm PvP
Cải thiện giao diện
Tác giả
Lê Đỗ Tùng Dương
Student Project
Repository

24022304_LeDoTungDuong_CaroAI