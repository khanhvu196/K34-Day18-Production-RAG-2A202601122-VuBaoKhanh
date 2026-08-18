# Individual Reflection — Lab 18

**Tên:** Vũ Bảo Khánh (Mã học viên: 2A202601122)  
**Module phụ trách:** Toàn bộ hệ thống (M1, M2, M3, M4, M5)

---

## 1. Đóng góp kỹ thuật

- **Module đã implement:** 
  - M1: Advanced Chunking (Semantic, Hierarchical, Structure-aware)
  - M2: Hybrid Search (Vietnamese Segmentation, BM25, Dense Qdrant, RRF)
  - M3: Reranking (Cross-encoder model)
  - M4: RAGAS Evaluation & Failure Analysis
  - M5: LLM Enrichment (Single-call tóm tắt, HyQA, Contextual)
- **Các hàm/class chính đã viết:** `chunk_semantic()`, `BM25Search.index()`, `DenseSearch.search()`, `reciprocal_rank_fusion()`, `CrossEncoderReranker.rerank()`, `_enrich_single_call()`, `failure_analysis()`.
- **Số tests pass:** Toàn bộ tests của M1-M5 đều đã pass xanh (100%).

## 2. Kiến thức học được

- **Khái niệm mới nhất:** Reciprocal Rank Fusion (RRF) để gộp kết quả tìm kiếm từ khoá (BM25) và ngữ nghĩa (Vector) hiệu quả mà không cần train mô hình gộp. Cơ chế Evaluation của RAGAS.
- **Điều bất ngờ nhất:** Chỉ bằng 1 thủ thuật nhỏ là tiêm thêm "1 câu mô tả ngữ cảnh tài liệu" (Contextual Prepend) vào đầu mỗi chunk lại giúp khả năng truy xuất tăng đáng kể.
- **Kết nối với bài giảng:** 
  - Bài giảng phần "Hybrid Search" và "LLM-as-a-judge" đã được minh hoạ cực kì rõ nét qua M2 và M4.
  - Vấn đề "Lost in the middle" và "Hallucination" được phát hiện rất nhạy nhờ RAGAS Metrics.

## 3. Khó khăn & Cách giải quyết

- **Khó khăn lớn nhất:** 
  1. Giới hạn Rate Limit 429 từ Gemini API Free Tier khi dùng để chấm điểm (RAGAS) và Enrichment.
  2. Lỗi Font Unicode và Windows `FileExistsError` khi xuất Report trong Terminal.
  3. Xung đột thư viện Reranker (`FlagReranker` hay bị lỗi với transformers mới).
- **Cách giải quyết:** 
  1. Viết cơ chế Fallback (try/except) và điền `0.0` để Pipeline không bị đứng hình.
  2. Cấu hình `$env:PYTHONIOENCODING="utf-8"` và thay thế `os.rename` bằng `os.replace`.
  3. Dùng thẳng `sentence_transformers.CrossEncoder` để vượt qua lỗi.
- **Thời gian debug:** Mất khoảng 1-2 tiếng để xử lý mượt mà toàn bộ lỗi xung quanh môi trường và API.

## 4. Nếu làm lại

- **Sẽ làm khác điều gì:** Sẽ tích hợp thêm cơ chế Backoff Delay (nghỉ 15 giây khi gặp lỗi 429) thay vì phó mặc cho Try/Except, giúp khai thác API miễn phí lấy điểm chính xác hơn.
- **Module nào muốn thử tiếp:** Muốn nghiên cứu sâu hơn về thuật toán Flashrank để tăng tốc độ Rerank trên CPU.

## 5. Tự đánh giá

| Tiêu chí | Tự chấm (1-5) |
|----------|---------------|
| Hiểu bài giảng | 5 |
| Code quality | 5 |
| Teamwork | 5 |
| Problem solving | 5 |
