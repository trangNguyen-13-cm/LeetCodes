# 🧠 LeetCode Solutions

Kho lưu trữ lời giải LeetCode của mình, kèm ghi chú về cách tiếp cận và độ phức tạp.

> **Username LeetCode:** [your-username](https://leetcode.com/u/your-username/)

> 🤖 Các phần có marker `<!-- ...:START/END -->` được **tự động sinh** bởi `scripts/update_readme.py`. Đừng sửa tay trong các khối đó.

---

## 📊 Tiến độ

<!-- PROGRESS:START -->
<!-- PROGRESS:END -->

*Cập nhật lần cuối: <!-- UPDATED:START -->DD/MM/YYYY<!-- UPDATED:END -->*

## 💻 Ngôn ngữ đã dùng

<!-- LANGUAGES:START -->
<!-- LANGUAGES:END -->

---

## 📁 Cấu trúc thư mục

Bài giải được đồng bộ bằng LeetSync:

```
.
├── README.md
├── scripts/update_readme.py
├── .github/workflows/update-readme.yml
├── 1-two-sum/
│   ├── two-sum.py         # lời giải do LeetSync đẩy lên
│   └── README.md          # đề bài do LeetSync tạo
├── 15-3sum/
│   ├── 3sum.py
│   └── 3sum.cpp           # thêm ngôn ngữ khác: tự được nhận diện
└── ...
```

Script nhận diện cả thư mục `1-two-sum` lẫn `0001-two-sum`, ở thư mục gốc hoặc trong `easy/`, `medium/`, `hard/`.

---

## 📝 Danh sách bài đã giải

<!-- PROBLEMS:START -->
<!-- PROBLEMS:END -->

> 🟢 Easy · 🟡 Medium · 🔴 Hard

---

## 🏷️ Phân loại theo chủ đề

<!-- TOPICS:START -->
<!-- TOPICS:END -->

---

## ➕ Cách thêm bài mới

1. Giải bài trên LeetCode và bấm **Submit**. Khi bài được Accepted, LeetSync tự đẩy lên GitHub.
2. GitHub Actions tự chạy `scripts/update_readme.py` và commit lại README này.
3. Trước khi giải bài tiếp, nhớ `git pull` nếu bạn đang làm việc trên máy.

Chạy thủ công trên máy: `python scripts/update_readme.py` (thêm `--offline` nếu không muốn gọi LeetCode API).

**Độ khó và chủ đề** được lấy từ `README.md` của bài do LeetSync tạo, hoặc từ LeetCode API và lưu cache trong `.leetcode_cache.json`. Muốn ghi đè hoặc bổ sung `Chủ đề`, `Time`, `Space`, thêm comment ở đầu file lời giải:

```python
"""
LeetCode #1 - Two Sum
Chủ đề: Array, Hash Table
Time: O(n)
Space: O(n)
"""
```

### Quy ước commit

| Prefix | Ý nghĩa |
|--------|---------|
| `feat:` | Thêm lời giải mới |
| `refactor:` | Tối ưu / viết lại lời giải cũ |
| `docs:` | Sửa README hoặc ghi chú |
| `fix:` | Sửa lời giải bị sai |

---

## 🔁 Danh sách cần ôn lại

- [ ] #0000 - Tên bài *(lý do: chưa tối ưu / quên ý tưởng)*

---

## 📚 Tài nguyên tham khảo

- [NeetCode Roadmap](https://neetcode.io/roadmap)
- [Blind 75](https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions)
- [LeetCode Patterns](https://seanprashad.com/leetcode-patterns/)
