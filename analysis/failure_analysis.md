# Failure Analysis — Lab 18: Production RAG

**Nhóm:** Nhóm Cá Nhân  
**Thành viên:** Vũ Bảo Khánh (2A202601122)

---

## RAGAS Scores

| Metric | Naive Baseline | Production | Δ |
|--------|---------------|------------|---|
| Faithfulness | 0.650 | 0.920 | +0.270 |
| Answer Relevancy | 0.710 | 0.880 | +0.170 |
| Context Precision | 0.580 | 0.850 | +0.270 |
| Context Recall | 0.600 | 0.890 | +0.290 |

## Bottom-5 Failures

### #1
- **Question:** Công ty có chính sách làm việc từ xa không?
- **Expected:** Không có chính sách làm việc từ xa chính thức, chỉ áp dụng trong trường hợp đặc biệt.
- **Got:** Công ty có hỗ trợ làm việc từ xa 2 ngày/tuần.
- **Worst metric:** Faithfulness (0.0)
- **Error Tree:** Output sai → Context đúng? → Context nói về làm việc từ xa của năm 2022.
- **Root cause:** Metadata filter chưa lọc theo version tài liệu mới nhất (v2024), dẫn đến bốc nhầm chunk của năm cũ. LLM bị ảo giác (hallucinating) tự chế thêm số ngày.
- **Suggested fix:** Cần thêm bộ lọc Metadata cho trường `version="2024"` ở bước M2 Retrieval. Hạ temperature xuống 0.

### #2
- **Question:** Bảng lương chi tiết được tính như thế nào?
- **Expected:** Bảng lương phụ thuộc vào hệ số và ngày công.
- **Got:** Không tìm thấy thông tin.
- **Worst metric:** Context Recall (0.0)
- **Error Tree:** Context thiếu → M1 chunking chặt mất bảng.
- **Root cause:** Module M1 chia chunk Basic không bảo vệ được cấu trúc bảng (Table/Markdown), khiến dữ liệu bảng bị đứt đoạn và rơi vãi.
- **Suggested fix:** Sử dụng `chunk_structure_aware` (M1) để bảo toàn nguyên vẹn Markdown Header và Table.

### #3
- **Question:** Có bao nhiêu ngày nghỉ phép cho nhân viên làm 3 năm?
- **Expected:** 12 ngày.
- **Got:** Nhân viên có 12 ngày phép. Cứ mỗi 5 năm thâm niên sẽ được tăng thêm 1 ngày.
- **Worst metric:** Answer Relevancy (0.6)
- **Error Tree:** Answer dài dòng → Prompt thiếu ràng buộc.
- **Root cause:** Câu trả lời lan man, cung cấp thêm thông tin dư thừa về "5 năm" dù không được hỏi.
- **Suggested fix:** Cải thiện (Tighten) prompt: "Trả lời trực diện đúng trọng tâm câu hỏi, không giải thích dài dòng".

### #4
- **Question:** Ai là người phê duyệt nghỉ thai sản?
- **Expected:** Trưởng phòng nhân sự.
- **Got:** Phụ thuộc vào quản lý trực tiếp và HR.
- **Worst metric:** Context Precision (0.5)
- **Error Tree:** Context đúng nhưng bị pha loãng bởi nhiều chunk rác.
- **Root cause:** Vector search bốc lên quá nhiều chunk liên quan đến "nghỉ phép" nói chung, đẩy chunk "thai sản" xuống hạng quá thấp.
- **Suggested fix:** Sử dụng Reranker Cross-Encoder (M3) để phân tích chéo câu hỏi, đẩy chunk chứa chính xác từ khóa "nghỉ thai sản" lên top 1.

### #5
- **Question:** Trợ cấp ăn trưa là bao nhiêu?
- **Expected:** 50,000 VNĐ.
- **Got:** Không tìm thấy thông tin.
- **Worst metric:** Context Recall (0.0)
- **Error Tree:** Context thiếu → Từ vựng trong query và document không khớp.
- **Root cause:** Trong tài liệu dùng từ "Phụ cấp bữa trưa", còn câu hỏi dùng "Trợ cấp ăn trưa". Thuật toán search cơ bản không bắt được khoảng cách ngữ nghĩa này ở top k thấp.
- **Suggested fix:** Sử dụng module `_enrich_single_call` (M5) để sinh câu hỏi giả định (HyQA) bao gồm các từ đồng nghĩa và đính kèm (prepend) vào document.

## Case Study (cho presentation)

**Question chọn phân tích:** Công ty có chính sách làm việc từ xa không?

**Error Tree walkthrough:**
1. Output đúng? → Không. Trả lời sai lệch thực tế.
2. Context đúng? → Không hoàn toàn. Bốc đúng chủ đề nhưng sai phiên bản tài liệu (năm 2022 thay vì 2024).
3. Query rewrite OK? → Query OK nhưng chưa có điều kiện lọc metadata.
4. Fix ở bước: M2 (Hybrid Search) - Cần thêm pre-filter version để đảm bảo Policy đang dùng luôn là mới nhất.

**Nếu có thêm 1 giờ, sẽ optimize:**
- Viết thêm hệ thống Auto-Routing để tự động thêm điều kiện lọc metadata `version_date` vào hệ thống Qdrant, đảm bảo không bao giờ fetch nhầm tài liệu cũ.
