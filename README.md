# 🧠 LeetCode Solutions

Kho lưu trữ lời giải LeetCode của mình, kèm ghi chú về cách tiếp cận và độ phức tạp.

> **Username LeetCode:** [TrangNgT](https://leetcode.com/u/kEtUgh1uWe/)

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

```
.
├── README.md
├── scripts/update_readme.py
├── .github/workflows/update-readme.yml
├── easy/
│   └── 0001-two-sum/
│       ├── solution.py
│       ├── solution.cpp      # thêm ngôn ngữ khác: chỉ cần thêm file
│       └── notes.md          # (tuỳ chọn)
├── medium/
└── hard/
```

**Quy ước:** thư mục `<số-4-chữ-số>-<slug-trên-leetcode>`, file lời giải `solution.<đuôi>`.

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

1. Tạo thư mục, ví dụ `easy/0001-two-sum/`, rồi thêm file `solution.py` (hoặc `.cpp`, `.java`, ...).
2. Ghi **comment đầu file** theo mẫu bên dưới để script đọc được thông tin.
3. Commit và push:

```bash
git add .
git commit -m "feat: add 0001 Two Sum (Easy)"
git push origin main
```

GitHub Actions sẽ tự chạy script và cập nhật README. Muốn cập nhật ngay trên máy:

```bash
python scripts/update_readme.py
```

### Mẫu comment đầu file

```python
"""
LeetCode #1 - Two Sum
Chủ đề: Array, Hash Table
Time: O(n)
Space: O(n)
"""
```

```cpp
/*
 * LeetCode #1 - Two Sum
 * Chủ đề: Array, Hash Table
 * Time: O(n)
 * Space: O(n)
 */
```

Với `//` hoặc `#` cũng được, miễn là có các dòng `LeetCode #<số> - <tên>`, `Chủ đề:`, `Time:`, `Space:` trong 40 dòng đầu.

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
