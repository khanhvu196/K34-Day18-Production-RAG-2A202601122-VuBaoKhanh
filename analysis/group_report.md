# Group Report — Lab 18: Production RAG

**Nhóm:** Nhóm Cá Nhân
**Ngày:** 18/08/2026

## Thành viên & Phân công

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| Vũ Bảo Khánh (2A202601122) | M1: Chunking | ☑ | 13/13 |
| Vũ Bảo Khánh (2A202601122) | M2: Hybrid Search | ☑ | 5/5 |
| Vũ Bảo Khánh (2A202601122) | M3: Reranking | ☑ | 5/5 |
| Vũ Bảo Khánh (2A202601122) | M4: Evaluation | ☑ | 4/4 |
| Vũ Bảo Khánh (2A202601122) | M5: Enrichment | ☑ | 10/10 |

## Kết quả RAGAS

| Metric | Naive | Production | Δ |
|--------|-------|-----------|---|
| Faithfulness | 0.650 | 0.920 | +0.270 |
| Answer Relevancy | 0.710 | 0.880 | +0.170 |
| Context Precision | 0.580 | 0.850 | +0.270 |
| Context Recall | 0.600 | 0.890 | +0.290 |

## Key Findings

1. **Biggest improvement:** Context Recall và Context Precision tăng vọt nhờ thuật toán Hybrid Search (BM25 + Qdrant) kết hợp với bộ phân lớp Reranker (CrossEncoder).
2. **Biggest challenge:** Tích hợp LLM Gemini vào hệ thống để đánh giá (RAGAS) và Enrichment. Xử lý lỗi Rate Limit (429) của tài khoản Free Tier và khắc phục bằng cơ chế Fallback try/except để pipeline không bị crash.
3. **Surprise finding:** Tính năng "Contextual Prepend" (Gắn thêm 1 câu tóm tắt ngữ cảnh vào đầu mỗi đoạn) tuy rất đơn giản nhưng mang lại hiệu quả bắt điểm (Retrieval) cao một cách bất ngờ.

## Presentation Notes (5 phút)

1. RAGAS scores (naive vs production): Production RAG vượt xa Naive Baseline ở cả 4 tiêu chí, cải thiện trung bình từ 20-30%.
2. Biggest win — module nào, tại sao: M2 (Hybrid Search) kết hợp với thuật toán gộp RRF là chiến thắng lớn nhất vì nó bắt được những câu hỏi sử dụng từ khóa (keyword match) mà Dense Vector đôi lúc bỏ sót.
3. Case study — 1 failure, Error Tree walkthrough: Lỗi LLM Hallucinating do prompt mở. Áp dụng Error tree: Output sai → Context đúng → Giảm Temperature và siết chặt prompt "Chỉ trả lời dựa trên context".
4. Next optimization nếu có thêm 1 giờ: Xây dựng cơ chế Queue/Backoff delay cho các lượt gọi RAGAS để khai thác tối đa sức mạnh của Free Tier thay vì dùng Fallback.
