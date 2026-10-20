# ĐỒ ÁN MÔN HỌC IE313: PHÂN TÍCH VÀ TRỰC QUAN DỮ LIỆU
## HƯỚNG DẪN CÀI ĐẶT, THỰC THI VÀ TÁI LẬP KẾT QUẢ (RUNBOOK & DOCUMENTATION)

- **Trường**: Trường Đại học Công nghệ Thông tin - ĐHQG TP.HCM (UIT / VNU-HCM)
- **Lớp**: `IE313.F32.LT.CNTT` (Hệ Liên thông Đại học - Ngành Công nghệ Thông tin)
- **Giảng viên hướng dẫn**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: **Nhóm 10** (2 thành viên)
  - **Phạm Quốc Thắng** (MSSV: 25410304) — Trưởng nhóm, Phân tích & Trực quan hóa, Báo cáo & Slide
  - **Lê Minh Thiện** (MSSV: 25410313) — Tiền xử lý dữ liệu, Kiểm định thống kê, Thẩm định mô hình hồi quy

---

## Tên Đề Tài

> **PHÂN TÍCH VÀ TRỰC QUAN HÓA GIÁ THUÊ AIRBNB TẠI BANGKOK VÀ CÁC YẾU TỐ LIÊN QUAN**  
> *(Exploratory Data Analysis and Visualization of Bangkok Airbnb Rental Prices and Associated Factors)*

---

## 1. Cấu Trúc Thư Mục Dự Án

Toàn bộ mã nguồn, dữ liệu, kiểm thử và báo cáo được tổ chức độc lập và chuẩn mực:

```text
HK3-IE313.F32.LT.CNTT.PhanTichVaTrucQuanDuLieu/
├── README.md                  # Tài liệu hướng dẫn cài đặt và chạy dự án (file này)
├── app.py                     # Dashboard tương tác Streamlit (trình diễn web 5 Tab)
├── pyproject.toml             # Cấu hình ruff, pytest và kiểm thử độ bao phủ code (coverage)
├── requirements.txt           # Thư viện phân tích cốt lõi (pandas, numpy, scipy, matplotlib, seaborn, scikit-learn)
├── requirements-dev.txt       # Thư viện kiểm thử và chất lượng mã nguồn (pytest, pytest-cov, ruff)
├── requirements-lock.txt      # Phiên bản đóng băng (locked) đảm bảo tính tái lập 100%
├── .gitignore                 # Cấu hình loại trừ cache, virtualenv và checkpoints
│
├── data/                      # Quản lý dữ liệu nghiên cứu
│   ├── raw/                   # Dữ liệu gốc Inside Airbnb (bangkok_listings_2026-06-29.csv.gz, bất biến)
│   ├── processed/             # Dữ liệu baseline sạch sau tiền xử lý (bangkok_cleaned.csv: 28.987 × 16)
│   ├── source_manifest.json   # Siêu dữ liệu xuất xứ, thời điểm thu thập và mã băm SHA-256
│   └── inside_airbnb_data_dictionary_v4.3.csv # Từ điển dữ liệu Inside Airbnb v4.3
│
├── src/                       # Mã nguồn module hóa (phục vụ tái sử dụng và pipeline)
│   ├── __init__.py
│   ├── data_loader.py         # Kiểm tra SHA-256, parse giá nghiêm ngặt, nạp dữ liệu an toàn
│   ├── data_audit.py          # Kiểm toán cấu trúc, kiểu dữ liệu, khuyết và ngoại lệ
│   ├── wrangling.py           # Tiền xử lý, lọc khuyết giá, bảo toàn dữ liệu thô
│   ├── eda_stats.py           # Thống kê mô tả (RQ1), ANOVA (RQ2), Pearson r-p (RQ3), Pivot (RQ4)
│   ├── visualization.py       # Xuất 5 biểu đồ PNG chuẩn 300 DPI theo Matplotlib OO API
│   ├── modeling.py            # Chia train/test chống rò rỉ, chọn biến trong fold, đánh giá mốc cơ sở
│   ├── eda_report.py          # Tự động tổng hợp kết quả thống kê thành văn bản nhận xét
│   └── audit_markdown.py      # Sinh báo cáo kiểm toán Markdown tự động
│
├── notebooks/                 # 4 Jupyter Notebooks thực thi tuần tự theo bài học
│   ├── 01_data_audit_and_cleaning.ipynb    # Bước 1–4: Kiểm toán & Tiền xử lý dữ liệu (Bài 01, 02)
│   ├── 02_eda_and_statistical_tests.ipynb  # Bước 5: Thống kê mô tả & Kiểm định ANOVA, Pearson (Bài 05)
│   ├── 03_visualization_figures.ipynb      # Bước 6: Trực quan hóa dữ liệu chuẩn 300 DPI (Bài 03, 04)
│   └── 04_regression_modeling.ipynb        # Bước 7: Phân chia tập, chọn biến & Mốc hồi quy (Bài 06, 07)
│
├── tests/                     # 91 unit & integration tests (độ bao phủ > 89%)
│   ├── test_data_audit.py                  # Kiểm thử parser giá, kiểm toán cấu trúc, SHA-256
│   ├── test_wrangling.py                   # Kiểm thử logic làm sạch, loại dòng khuyết giá
│   ├── test_eda_stats.py                   # Kiểm thử công thức thống kê, ANOVA, Pearson, Pivot
│   ├── test_visualization.py               # Kiểm thử hàm vẽ biểu đồ và catalog ảnh
│   ├── test_modeling.py                    # Kiểm thử chia tập, chống rò rỉ và chọn biến
│   ├── test_modeling_review.py             # Kiểm thử hồi quy bổ trợ và thẩm định khả thi
│   ├── test_eda_review_regressions.py      # Kiểm thử hồi quy kiểm định thống kê
│   └── test_audit_followup.py              # Kiểm thử xử lý ngoại lệ tệp và manifest
│
└── reports/                   # Toàn bộ sản phẩm đầu ra đã nghiệm thu
    ├── eda_findings.md                     # Báo cáo tổng hợp phát hiện thống kê EDA tự động sinh
    ├── Nhom10_Bao_cao.docx                 # Báo cáo Word chính thức (chuẩn template UIT)
    ├── Nhom10_Bao_cao.pdf                  # Báo cáo PDF 11 trang (8 trang thân + bìa, TLTK, phụ lục)
    ├── Nhom10_Slides.pptx                  # Slide trình bày 12 trang (đầy đủ ghi chú Presenter Notes)
    ├── Nhom10_Slides.pdf                   # Slide định dạng PDF xem trước/dự phòng
    ├── Nhom10_Kich_ban_thuyet_trinh.md      # Kịch bản thuyết trình 10 phút slide + 5 phút demo
    ├── Nhom10_Huong_dan_nop.md             # Hướng dẫn quy cách nộp bài và đối chiếu tệp
    ├── figures/                            # 5 hình biểu đồ PNG 300 DPI, sơ đồ luồng và catalog JSON/CSV
    ├── stats/                              # 12 tệp kết quả thống kê mô tả, ANOVA, Pearson CSV/JSON
    ├── cleaning/                           # Nhật ký làm sạch và danh sách dòng bị loại trừ
    ├── audit/                              # Kết quả kiểm toán cấu trúc dữ liệu thô
    └── modeling/                           # Phân chia tập split_assignments.csv, feature_selection.json
```

---

## 2. Hướng Dẫn Cài Đặt Môi Trường

Dự án yêu cầu **Python 3.10+** (đã kiểm thử và chạy ổn định nhất trên **Python 3.12.3** trên nền tảng Linux / WSL2).

### Bước 2.1. Khởi tạo môi trường ảo (Virtual Environment)

Mở terminal tại thư mục gốc của dự án:

```bash
cd /var/www/lienthongdaihoc/HK3-IE313.F32.LT.CNTT.PhanTichVaTrucQuanDuLieu

# Tạo môi trường ảo .venv chuẩn của Python
python3 -m venv .venv

# Kích hoạt môi trường ảo
source .venv/bin/activate
```

> **Mẹo**: Luôn đảm bảo dòng đầu của terminal có tiền tố `(.venv)` trước khi chạy các lệnh tiếp theo.

### Bước 2.2. Cài đặt các gói phụ thuộc

Cài đặt bằng tệp `requirements-lock.txt` để đảm bảo 100% phiên bản gói trùng khớp với môi trường đã kiểm chứng:

```bash
# Cập nhật pip
pip install --upgrade pip

# Cài đặt gói thư viện đã khóa phiên bản (khuyên dùng)
pip install -r requirements-lock.txt

# (Hoặc) Cài đặt từ requirements tiêu chuẩn:
# pip install -r requirements.txt -r requirements-dev.txt
```

---

## 3. Chạy Kiểm Thử Tự Động (Unit & Integration Tests)

Dự án có **91 bài test** tự động bao phủ toàn bộ pipeline xử lý, kiểm định thống kê và phòng chống rò rỉ dữ liệu.

```bash
# Đảm bảo môi trường ảo đã kích hoạt
source .venv/bin/activate

# Chạy toàn bộ 91 bài test
pytest

# Chạy kiểm thử có đo lường độ bao phủ mã nguồn (code coverage)
pytest --cov=src tests/

# Kiểm tra chất lượng mã nguồn với Ruff linter
ruff check .
```

*Kết quả mong đợi*: Toàn bộ `91 passed`, thời gian chạy ~20 giây, độ bao phủ mã nguồn thư mục `src/` đạt xấp xỉ **89%**.

---

## 4. Chạy Pipeline Xử Lý Từ Dòng Lệnh (CLI Pipeline)

Bạn có thể chạy độc lập từng bước hoặc toàn bộ quy trình khoa học dữ liệu từ dòng lệnh:

### Bước 4.1. Kiểm toán dữ liệu thô (Data Audit)
```bash
python -m src.data_audit \
  --input data/raw/bangkok_listings_2026-06-29.csv.gz \
  --output-dir reports/audit \
  --manifest data/source_manifest.json \
  --data-dictionary data/inside_airbnb_data_dictionary_v4.3.csv \
  --generate-markdown reports/audit/DATA_AUDIT.md
```
*Kết quả*: Xác thực mã băm SHA-256 của tệp thô, xuất bảng kiểm toán kiểu dữ liệu, tỷ lệ khuyết tại `reports/audit/`.

### Bước 4.2. Tiền xử lý & Làm sạch dữ liệu (Data Wrangling)
```bash
python -m src.wrangling \
  --input data/raw/bangkok_listings_2026-06-29.csv.gz \
  --manifest data/source_manifest.json \
  --output-dir data/processed \
  --report-dir reports/cleaning
```
*Kết quả*: Tạo tệp baseline sạch `data/processed/bangkok_cleaned.csv` gồm **28.987 dòng × 16 cột**, loại bỏ 2.082 dòng thiếu giá, xuất nhật ký chi tiết vào `reports/cleaning/`.

### Bước 4.3. Thống kê mô tả & Kiểm định EDA (EDA Statistics)
```bash
python -m src.eda_stats \
  --input data/processed/bangkok_cleaned.csv \
  --output-dir reports/stats \
  --expected-sha256 961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7

# Tự động cập nhật nhận xét EDA
python -m src.eda_report
```
*Kết quả*: Xuất 12 tệp JSON/CSV chứa thống kê mô tả phân phối giá (RQ1), kiểm định ANOVA và Levene theo loại phòng (RQ2), ma trận tương quan Pearson theo quy mô (RQ3), bảng tổng hợp khu vực (RQ4).

### Bước 4.4. Trực quan hóa dữ liệu (Visualization)
```bash
python -m src.visualization \
  --input data/processed/bangkok_cleaned.csv \
  --output-dir reports/figures
```
*Kết quả*: Xuất 5 tệp biểu đồ độ phân giải cao 300 DPI vào `reports/figures/`:
- `fig1_price_distribution.png`: Histogram phân phối giá toàn miền (trục log10) và vùng $\le 10.000$ THB.
- `fig2_price_by_room_type.png`: Boxplot so sánh giá giữa 4 loại phòng.
- `fig3_price_vs_size_scatter.png`: Scatter plot kèm đường hồi quy OLS giữa giá và các biến quy mô phòng.
- `fig4_price_by_neighbourhood_heatmap.png`: Heatmap trung vị giá theo 15 quận đông listing nhất.
- `fig4_price_top_neighbourhoods_bar.png`: Biểu đồ cột so sánh giá căn hộ nguyên căn tại các quận trọng điểm.

### Bước 4.5. Phân chia tập & Thẩm định mô hình hồi quy (Modeling & Feasibility)
```bash
python -m src.modeling \
  --input data/processed/bangkok_cleaned.csv \
  --output-dir reports/modeling \
  --expected-sha256 961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7
```
*Kết quả*: Phân chia 70% Train ($n=20.290$) / 30% Test ($n=8.697$) với `random_state=42`, thực hiện chọn biến độc lập trong 4-Fold CV, đánh giá mốc dự đoán trung bình DummyRegressor ($R^2 \approx -0.000014$) và lưu vết tại `reports/modeling/`.

---

## 5. Chạy Trực Tiếp Bằng Jupyter Notebook

Dự án cung cấp 4 notebook có cấu trúc chặt chẽ, đã được thực thi sẵn cell outputs:

```bash
# Kích hoạt môi trường ảo
source .venv/bin/activate

# Khởi chạy JupyterLab trên cổng 8888 (không tự mở trình duyệt)
jupyter lab --no-browser --port=8888 --ip=0.0.0.0

# Hoặc khởi chạy Jupyter Classic Notebook
jupyter notebook --no-browser --port=8888 --ip=0.0.0.0
```

Truy cập đường link hiển thị trên terminal (dạng `http://127.0.0.1:8888/lab?token=...`) trên trình duyệt web và chạy tuần tự các notebook trong thư mục `notebooks/`:
1. `01_data_audit_and_cleaning.ipynb`: Nạp dữ liệu thô, xác thực SHA-256, kiểm toán khuyết và xuất file sạch.
2. `02_eda_and_statistical_tests.ipynb`: Tính thống kê phân phối giá, kiểm định ANOVA loại phòng, tương quan Pearson.
3. `03_visualization_figures.ipynb`: Vẽ và lưu 5 hình biểu đồ khoa học đạt chuẩn 300 DPI.
4. `04_regression_modeling.ipynb`: Chia tập Train/Test, chọn lọc biến per-fold và đánh giá mốc so sánh cơ sở.

### Bước 5.2. Khởi chạy Dashboard tương tác (Streamlit Web App)

Đồ án cung cấp ứng dụng web Dashboard tương tác phục vụ trình diễn và demo (5 phút) trước hội đồng:

```bash
# Kích hoạt môi trường ảo
source .venv/bin/activate

# Khởi chạy ứng dụng Streamlit Dashboard
streamlit run app.py
```

Ứng dụng sẽ tự động mở trên trình duyệt tại `http://localhost:8501`:
- **Sidebar bộ lọc:** Tùy chọn lọc linh hoạt theo loại phòng, quận hành chính, khoảng ngân sách và tùy chọn hiển thị ngoại lai cao cấp.
- **Hàng KPI thời gian thực:** Cập nhật ngay lập tức Tổng số listing, Giá trung vị, Giá trung bình và Tỷ lệ chủ nhà Superhost.
- **5 Tab nghiên cứu chuyên sâu:**
  1. *RQ1: Phân bố giá*: Histogram thang log10 + linear zoom và bảng thống kê mô tả.
  2. *RQ2: Loại phòng & ANOVA*: Boxplot so sánh giá và kết quả kiểm định $F$, $p$-value kèm khuyến nghị Levene.
  3. *RQ3: Quy mô & Tương quan*: Ma trận Pearson $r$, $p$-value và Scatter plot kèm đường hồi quy OLS.
  4. *RQ4: Phân hóa địa lý*: Heatmap theo 15 quận đông listing nhất, biểu đồ cột và bảng Pivot Table 2D.
  5. *Khám phá dữ liệu*: Bảng dữ liệu tương tác, sắp xếp theo giá và nút xuất dữ liệu đã lọc sang CSV.

---

## 6. Tóm Tắt Phát Hiện Nghiên Cứu (Research Findings)

| Câu hỏi nghiên cứu (RQ) | Phương pháp & Biến số | Kết quả định lượng chính | Ý nghĩa thực tiễn & Học thuật |
| :--- | :--- | :--- | :--- |
| **RQ1: Phân bố giá thuê** | Thống kê mô tả, IQR, Histogram trục log | Trung vị: **1.500 THB/đêm**, Trung bình: **2.977 THB/đêm**. Skewness = **40,71**, Ngoại lệ: **7,23%** ($> 4.195$ THB). | Phân phối giá lệch phải cực mạnh; trung vị là thước đo xu hướng trung tâm đại diện hơn trung bình. |
| **RQ2: Chênh lệch theo loại phòng** | Groupby, Boxplot, ANOVA một chiều ($F$), Levene test | Entire home/apt: trung vị **1.800 THB**; Hotel room: **1.542 THB**; Private room: **1.148 THB**; Shared room: **500 THB**. | Chênh lệch giá có ý nghĩa thống kê; kiểm định Levene ($p < 0,001$) bác bỏ giả định phương sai đồng nhất. |
| **RQ3: Tương quan với quy mô chỗ ở** | Hệ số Pearson ($r$) và $p$-value, Scatter plot | `accommodates`: $r = 0,103$; `bedrooms`: $r = 0,088$; `bathrooms`: $r = 0,088$; `beds`: $r = 0,069$ (đều $p < 0,001$). | Tương quan tuyến tính rất yếu ($r < 0,12$), chưa đạt ngưỡng chọn biến ($|r| \ge 0,30$). |
| **RQ4: Biến thiên theo khu vực địa lý** | Pivot table, Heatmap, Top 15 quận đông listing | Khlong Toei (**4.821** listing, trung vị 1.700 THB); Watthana (**4.580** listing, trung vị 1.800 THB). | Mật độ listing tập trung cao tại trục thương mại Sukhumvit; biến động giá lớn giữa quận trung tâm và ngoại vi. |
| **Hồi quy & Khả thi** | 70/30 Split, 4-Fold CV, DummyRegressor benchmark | Không có biến số đạt tiêu chuẩn chọn lọc ($|r| \ge 0,30$ & $p < 0,05$). Test MSE: **3,15 × 10⁸ THB²**, $R^2 \approx -0,000014$. | Minh bạch khoa học: Dữ liệu không đủ cơ sở hồi quy tuyến tính tin cậy; không cố tình cắt gọt số liệu để ép mô hình. |

---

## 7. Danh Mục Sản Phẩm Đồ Án Nghiệm Thu

| Tên tài liệu / Sản phẩm | Định dạng | Vị trí lưu trữ | Tình trạng |
| :--- | :---: | :--- | :---: |
| **Báo cáo chính thức (Word)** | `.docx` | [reports/Nhom10_Bao_cao.docx](reports/Nhom10_Bao_cao.docx) | Đã hoàn thiện |
| **Báo cáo chính thức (PDF)** | `.pdf` | [reports/Nhom10_Bao_cao.pdf](reports/Nhom10_Bao_cao.pdf) | 11 trang (8 trang thân) |
| **Slide thuyết trình (PowerPoint)**| `.pptx`| [reports/Nhom10_Slides.pptx](reports/Nhom10_Slides.pptx) | 12 slide có Presenter Notes |
| **Slide xem trước (PDF)** | `.pdf` | [reports/Nhom10_Slides.pdf](reports/Nhom10_Slides.pdf) | Đã hoàn thiện |
| **Kịch bản thuyết trình chi tiết** | `.md`   | [reports/Nhom10_Kich_ban_thuyet_trinh.md](reports/Nhom10_Kich_ban_thuyet_trinh.md) | 10p slide + 5p demo |
| **Hướng dẫn nộp và đối chiếu** | `.md`   | [reports/Nhom10_Huong_dan_nop.md](reports/Nhom10_Huong_dan_nop.md) | Đã sẵn sàng |
| **Bộ 5 hình biểu đồ 300 DPI** | `.png`  | [reports/figures/](reports/figures/) | Đạt chuẩn xuất bản |
| **Dữ liệu gốc bất biến** | `.csv.gz` | [data/raw/bangkok_listings_2026-06-29.csv.gz](data/raw/bangkok_listings_2026-06-29.csv.gz) | 20.6 MB (khớp SHA-256) |
| **Dữ liệu sạch baseline** | `.csv` | [data/processed/bangkok_cleaned.csv](data/processed/bangkok_cleaned.csv) | 28.987 dòng × 16 cột |
| **Dashboard tương tác (Streamlit)** | `.py` | [app.py](app.py) | Đã hoàn thiện |

---

## 8. Hướng Dẫn Đóng Gói Nén (ZIP) Để Nộp Bài

Khi nén mã nguồn nộp cho giảng viên, **tuyệt đối không nén thư mục `.venv`** (vì rất nặng ~580 MB và phụ thuộc đường dẫn máy). Hãy dùng lệnh sau tại thư mục gốc để tạo tệp ZIP sạch sẽ (~25 MB):

```bash
cd /var/www/lienthongdaihoc/HK3-IE313.F32.LT.CNTT.PhanTichVaTrucQuanDuLieu

# Đóng gói toàn bộ code và dữ liệu sạch, loại bỏ .venv và cache
zip -r Nhom10_SourceCode_IE313.zip . \
  -x "*/.venv/*" \
  -x "*/.git/*" \
  -x "*/.pytest_cache/*" \
  -x "*/.ruff_cache/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x ".coverage"
```

Tệp `Nhom10_SourceCode_IE313.zip` tạo ra sẽ có dung lượng ~25 MB, hoàn toàn đáp ứng ngưỡng tải lên của hệ thống Courses / Moodle UIT (< 50 MB).

