# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN MÔN HỌC IE313

## PHÂN TÍCH VÀ TRỰC QUAN HÓA GIÁ THUÊ AIRBNB TẠI BANGKOK VÀ CÁC YẾU TỐ LIÊN QUAN

- **Đơn vị đào tạo**: Trường Đại học Công nghệ Thông tin — ĐHQG TP.HCM (UIT)
- **Môn học**: `IE313.F32.LT.CNTT` — Phân tích và Trực quan dữ liệu
- **Giảng viên hướng dẫn**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: **Nhóm 10**
  - **Phạm Quốc Thắng** (MSSV: 25410304) — Trưởng nhóm, Trực quan hóa & Báo cáo
  - **Lê Minh Thiện** (MSSV: 25410313) — Tiền xử lý, Thống kê suy luận & Thẩm định mô hình
- **Tổng thời lượng dự kiến**: 15 phút (10 phút Slide tổng quan + 5 phút Demo Dashboard trực tiếp)

---

## PHẦN 1: KỊCH BẢN THUYẾT TRÌNH SLIDE (10 PHÚT)

### Slide 1: Bìa đề tài & Thành viên nhóm (0.5 phút)

- **Nội dung slide**: Tên đề tài, GVHD, thành viên, logo UIT.
- **Lời thoại**:
  > *"Kính thưa thầy Phạm Thế Sơn và toàn thể các bạn, em là Phạm Quốc Thắng, đại diện Nhóm 10 lớp IE313.F32.LT.CNTT. Hôm nay, nhóm em xin được báo cáo đề tài nghiên cứu: **'Phân tích và trực quan hóa giá thuê Airbnb tại Bangkok và các yếu tố liên quan'**.*
  >
  > *Đồ án được thực hiện bởi hai thành viên: em phụ trách phân tích trực quan hóa, báo cáo và sản phẩm dashboard; bạn Lê Minh Thiện phụ trách kiểm toán, tiền xử lý dữ liệu và kiểm định thống kê."*

### Slide 2: Đặt vấn đề & Mục tiêu nghiên cứu (1 phút)

- **Nội dung slide**: Bối cảnh thị trường du lịch Bangkok, 4 câu hỏi nghiên cứu (RQ1 – RQ4), mục tiêu bài toán.
- **Lời thoại**:
  > *"Bangkok là một trong những trung tâm du lịch hàng đầu thế giới với lượng cung lưu trú trên Airbnb vô cùng đa dạng. Mục tiêu cốt lõi của đồ án là trả lời 4 câu hỏi nghiên cứu trọng tâm:*
  > 1. *Đặc trưng phân bố của giá thuê theo đêm ra sao, mức độ lệch và ngoại lai như thế nào?*
  > 2. *Có sự chênh lệch có ý nghĩa thống kê về giá giữa 4 loại phòng hay không?*
  > 3. *Các đặc tính quy mô vật lý như sức chứa, số phòng ngủ, phòng tắm có mối tương quan tuyến tính mạnh với giá hay không?*
  > 4. *Giá thuê phân hóa như thế nào theo 50 quận hành chính tại thủ đô Bangkok?*
  >
  > *Từ đó, nhóm đánh giá tính khả thi trong việc xây dựng mô hình hồi quy tuyến tính dự báo giá thuê."*

### Slide 3: Nguồn gốc dữ liệu & Kiểm toán toàn vẹn (1 phút)

- **Nội dung slide**: Inside Airbnb Bangkok (snapshot 29/06/2026), SHA-256, quy trình kiểm toán 90 cột.
- **Lời thoại**:
  > *"Về nguồn dữ liệu, nhóm sử dụng snapshot chi tiết từ tổ chức Inside Airbnb phát hành ngày 29/06/2026 với giấy phép CC BY 4.0. File thô nén có kích thước 20.6 MB gồm 31.069 dòng và 90 cột.*
  >
  > *Nhóm tuân thủ nghiêm ngặt tính tái lập trong khoa học dữ liệu: tệp thô được bảo toàn bất biến qua mã băm SHA-256. Qua kiểm toán cấu trúc, dữ liệu có tính đơn nhất 100% (mỗi dòng là một listing duy nhất, không trùng lặp ID). Về tiền tệ, nhóm đã đối chiếu chéo giữa từ điển dữ liệu và trường giá chi tiết để xác nhận đơn vị tính là Thai Baht (THB) và báo giá theo đêm (price per night)."*

### Slide 4: Quy trình làm sạch & Xây dựng Baseline (1 phút)

- **Nội dung slide**: Loại bỏ 2.082 dòng khuyết giá, bảo toàn ngoại lai, baseline 28.987 dòng × 16 cột.
- **Lời thoại**:
  > *"Trong khâu tiền xử lý, nhóm áp dụng chính sách làm sạch có nguyên tắc:*
  > - *Chỉ loại bỏ 2.082 dòng thiếu giá hoặc giá không hợp lệ, không thực hiện điền khuyết (imputation) tùy tiện trên biến mục tiêu.*
  > - *Không cắt gọt các mức giá cực cao (> 1.5×IQR) nhằm bảo toàn tính tự nhiên của thị trường.*
  >
  > *Kết quả xuất ra tệp baseline sạch `bangkok_cleaned.csv` gồm **28.987 dòng và 16 cột** đạt mã băm SHA-256 được kiểm chứng tự động trong toàn bộ pipeline."*

### Slide 5: Phát hiện RQ1 — Phân bố giá lệch phải cực mạnh (1.5 phút)

- **Nội dung slide**: Biểu đồ Figure 1 (Histogram log10 + zoom), bảng chỉ số thống kê mô tả.
- **Lời thoại**:
  > *"Bước vào kết quả EDA, đối với RQ1 về phân bố giá thuê:*
  > - *Giá trung vị (Median) đạt **1.592 THB/đêm**, trong khi giá trung bình (Mean) lên tới **2.956 THB/đêm**.*
  > - *Hệ số bất đối xứng Skewness đạt mức rất cao là **+52,31** và Kurtosis lên tới hơn 3.000.*
  >
  > *Phân phối giá có đuôi dài lệch phải cực mạnh do sự xuất hiện của các biệt thự, penthouse sang trọng có giá niêm yết lên tới 1,3 triệu THB. Điều này khẳng định kết luận quan trọng: **Giá trung vị là thước đo đại diện xu hướng trung tâm chuẩn xác hơn nhiều so với giá trung bình** khi phân tích thị trường Airbnb Bangkok."*

### Slide 6: Phát hiện RQ2 — So sánh giá theo loại phòng & Kiểm định ANOVA (1.5 phút)

- **Nội dung slide**: Biểu đồ Figure 2 (Boxplot), kiểm định ANOVA F-test, Levene test, hiện tượng host clustering.
- **Lời thoại**:
  > *"Đối với câu hỏi RQ2, giá có sự phân tầng rõ nét giữa 4 loại phòng:*
  > - *Hotel room và Entire home/apt dẫn đầu với giá trung vị khoảng **1.700 – 2.000 THB/đêm**.*
  > - *Private room đạt **1.390 THB** và Shared room chỉ khoảng **431 THB**.*
  >
  > *Về mặt thống kê suy luận, kiểm định One-way ANOVA cho giá trị $F = 5,93$ với $p = 0,00049 < 0,001$. Tuy nhiên, điểm cốt lõi về phương pháp luận là nhóm đã thẩm định lại 3 giả định của ANOVA:*
  > 1. *Dữ liệu vi phạm nghiêm trọng tính chuẩn.*
  > 2. *Kiểm định Levene ($p = 0,0248 < 0,05$) bác bỏ giả định phương sai đồng nhất.*
  > 3. *Có 3.215 chủ nhà sở hữu nhiều listing làm vi phạm tính độc lập hoàn toàn.*
  >
  > *Do đó, nhóm kết luận kết quả ANOVA chỉ mang tính khám phá (exploratory), không đủ cơ sở suy diễn nhân quả và chủ động không chạy so sánh cặp (Post-hoc)."*

### Slide 7: Phát hiện RQ3 — Tương quan tuyến tính giữa quy mô và giá (1 phút)

- **Nội dung slide**: Biểu đồ Figure 3 (Scatter + OLS), bảng ma trận Pearson r và p-value.
- **Lời thoại**:
  > *"Tại câu hỏi RQ3, nhóm kiểm tra mối liên hệ tuyến tính giữa 4 biến quy mô vật lý với giá thuê:*
  > - *Sức chứa (`accommodates`): $r = +0,1067$*
  > - *Số phòng ngủ (`bedrooms`): $r = +0,0881$*
  > - *Số phòng tắm (`bathrooms`): $r = +0,0841$*
  > - *Số giường (`beds`): $r = +0,0688$*
  >
  > *Dù toàn bộ $p$-value đều nhỏ hơn 0,001 do cỡ mẫu lớn ($n \approx 28.000$), nhưng độ lớn của hệ số $r$ đều dưới 0,11. Điều này chứng minh rằng **tương quan tuyến tính giữa quy mô phòng và giá thuê là rất yếu**; quy mô không phải là yếu tố đơn lẻ quyết định giá."*

### Slide 8: Phát hiện RQ4 — Phân hóa địa lý theo quận hành chính (1 phút)

- **Nội dung slide**: Biểu đồ Figure 4A (Heatmap) và Figure 4B (Bar chart), Pivot Table 2D.
- **Lời thoại**:
  > *"Đối với RQ4 về yếu tố địa lý:*
  > - *Mật độ nguồn cung listing tập trung áp đảo tại các quận thương mại dọc trục giao thông Sukhumvit: Vadhana (hơn 4.100 listing), Huai Khwang và Khlong Toei (hơn 3.600 listing).*
  > - *Khi kiểm soát cùng phân khúc căn hộ nguyên căn (Entire home/apt), giá thuê phân hóa cực kỳ sâu sắc: các quận trung tâm du lịch/lịch sử ven sông như Samphanthawong hay Phra Nakhon có trung vị xấp xỉ **3.000 THB/đêm**, cao gấp hơn 4 lần so với các quận ngoại vi như Bang Phlat (chỉ **678 THB/đêm**)."*

### Slide 9: Thẩm định mô hình hồi quy & Liêm chính học thuật (1 phút)

- **Nội dung slide**: Train/Test 70/30, 4-Fold CV, quy tắc chọn biến $|r| \ge 0,30$, Baseline DummyRegressor.
- **Lời thoại**:
  > *"Tại Bước 7 về mô hình hóa, nhóm thiết lập thử nghiệm chia 70% Train ($n=20.290$) và 30% Test ($n=8.697$) với `random_state=42`, thực hiện chọn biến độc lập trong 4-Fold CV để chống rò rỉ dữ liệu.*
  >
  > *Nhóm đặt ngưỡng chọn lọc tiên nghiệm là $|r| \ge 0,30$ và $p < 0,05$. Kết quả: cả 4 folds đều ghi nhận **0 biến số nào đạt chuẩn**.*
  >
  > *Với tinh thần liêm chính học thuật, nhóm không gọt giũa dữ liệu để ép chạy mô hình tuyến tính, mà báo cáo mốc so sánh cơ sở DummyRegressor (dự đoán trung bình $2.976$ THB, $R^2 \approx -0,000014$) và phân tích rõ các yếu tố phi tuyến của dữ liệu thực tế."*

### Slide 10: Chuyển tiếp sang phần Demo Dashboard (0.5 phút)

- **Lời thoại**:
  > *"Để biến toàn bộ các phát hiện nghiên cứu trên thành một sản phẩm dữ liệu trực quan phục vụ người dùng cuối, nhóm đã phát triển ứng dụng Dashboard tương tác bằng Streamlit. Sau đây, em xin chuyển sang phần trình diễn trực tiếp Dashboard."*

---

## PHẦN 2: KỊCH BẢN DEMO DASHBOARD TƯƠNG TÁC (5 PHÚT)

*Ghi chú kỹ thuật: Khởi chạy lệnh `streamlit run app.py` trước buổi báo cáo và mở sẵn tab trình duyệt tại `http://localhost:8501`.*

### Phút 1: Giới thiệu giao diện & Hàng chỉ số KPI

- **Hành động thao tác**:
  - Mở toàn màn hình trình duyệt.
  - Rê chuột chỉ vào tiêu đề đồ án, thông tin Nhóm 10 và badge SHA-256 ở Sidebar.
  - Chỉ chuột vào hàng 4 thẻ KPI.
- **Lời thoại**:
  > *"[Chỉ chuột vào màn hình]*
  > *Thưa thầy, đây là giao diện chính của Dashboard Airbnb Bangkok do nhóm xây dựng.*
  >
  > *Ứng dụng được thiết kế theo kiến trúc 3 tầng chuẩn mực: toàn bộ giao diện chạy trên file `app.py`, nạp trực tiếp dữ liệu sạch và gọi các module trong `src/` qua cơ chế cache `@st.cache_data`.*
  >
  > *[Chỉ vào 4 thẻ KPI]*
  > *Ngay trên đầu trang là 4 thẻ KPI cốt lõi: người xem thấy ngay tổng quy mô 28.987 căn hộ, mức giá trung vị 1.592 THB so với mức giá trung bình 2.956 THB, độ lệch Skewness +52,3 và tỷ lệ chủ nhà Superhost đạt 38,1%. Bốn con số này sẽ tự động cập nhật theo thời gian thực mỗi khi ta thay đổi bộ lọc."*

### Phút 2: Demo tính năng lọc tương tác trên Sidebar

- **Hành động thao tác**:
  - Tại Sidebar, click bỏ chọn `Shared room` và `Hotel room`, chỉ giữ lại `Entire home/apt`.
  - Kéo thanh trượt ngân sách từ mức 10.000 THB xuống 5.000 THB.
  - Chỉ vào hàng KPI vừa cập nhật tức thì.
- **Lời thoại**:
  > *"[Thao tác kéo lọc]*
  > *Ở thanh Sidebar bên trái, người dùng có thể điều chỉnh theo nhu cầu thực tế. Ví dụ: em chỉ muốn tìm căn hộ nguyên căn (Entire home/apt) với ngân sách tối đa 5.000 THB/đêm.*
  >
  > *Ngay lập tức, hàng KPI tự động tính toán lại: số lượng listing hiển thị giảm xuống còn 17.653 căn (chiếm 60,9% toàn mẫu), giá trung vị phân khúc này là 1.600 THB. Điều này giúp người dùng dễ dàng khoanh vùng phân khúc thị trường mình mong muốn."*

### Phút 3: Demo Tab 1 (RQ1) & Tab 2 (RQ2)

- **Hành động thao tác**:
  - Bấm nút reset bộ lọc ở Sidebar về mặc định (hoặc tích chọn lại đầy đủ).
  - Chọn **Tab 1: 📊 RQ1: Phân Bố Giá** -> Chỉ vào biểu đồ log-scale và bảng phân vị.
  - Chuyển sang **Tab 2: 🏠 RQ2: Loại Phòng & ANOVA** -> Cuộn chuột chỉ vào hộp thoại ANOVA và Khung khuyến nghị phương pháp luận.
- **Lời thoại**:
  > *"[Chuyển sang Tab 1]*
  > *Tại Tab 1, Dashboard thể hiện trực quan phân bố giá thuê qua 2 panel: thang đo log bên trái cho thấy toàn dải giá trị, panel zoom bên phải làm nổi bật vùng giá phổ thông. Bảng thống kê bên cạnh liệt kê đầy đủ $Q_1$, Median, $Q_3$, IQR và số ngoại lai.*
  >
  > *[Chuyển sang Tab 2]*
  > *Sang Tab 2, biểu đồ Boxplot so sánh trực quan độ phân tán giữa 4 loại phòng. Đặc biệt, nhóm dành riêng một khung thông tin **'Khuyến nghị phương pháp luận'** màu xanh để giải thích rõ lý do tại sao ANOVA có $p < 0,001$ nhưng nhóm vẫn khuyến cáo người xem không suy diễn quan hệ nhân quả do vi phạm giả định phương sai và gom cụm chủ nhà."*

### Phút 4: Demo Tab 3 (RQ3) & Tab 4 (RQ4)

- **Hành động thao tác**:
  - Chọn **Tab 3: 📐 RQ3: Quy Mô & Tương Quan** -> Chỉ vào bảng hệ số Pearson $r$ và 4 đồ thị Scatter.
  - Chuyển sang **Tab 4: 🗺️ RQ4: Phân Hóa Địa Lý** -> Cuộn xem Heatmap và Bar Chart.
- **Lời thoại**:
  > *"[Chuyển sang Tab 3]*
  > *Ở Tab 3, Dashboard vẽ đồng thời 4 đồ thị phân tán kèm đường xu hướng OLS giữa giá và các biến quy mô, đi kèm bảng hệ số Pearson $r$ tương ứng. Người xem thấy ngay độ dốc của đường hồi quy rất thoai thoải, minh chứng trực quan cho việc tương quan tuyến tính rất yếu.*
  >
  > *[Chuyển sang Tab 4]*
  > *Tại Tab 4, Bản đồ nhiệt Heatmap hiển thị trung vị giá của 15 quận trọng điểm theo từng loại phòng. Biểu đồ cột bên dưới tách riêng phân khúc Entire home/apt giúp nhận diện ngay các quận có giá thuê đắt đỏ nhất Bangkok như Samphanthawong hay Phra Nakhon."*

### Phút 5: Demo Tab 5 (Khám phá dữ liệu) & Tổng kết bế mạc

- **Hành động thao tác**:
  - Chọn **Tab 5: 📋 Khám Phá Dữ Liệu**.
  - Bấm sắp xếp cột `price` giảm dần.
  - Rê chuột vào nút **"📥 Tải xuống dữ liệu đã lọc (CSV)"**.
- **Lời thoại**:
  > *"[Tại Tab 5]*
  > *Cuối cùng, Tab Khám phá dữ liệu cho phép người dùng tra cứu chi tiết từng listing cụ thể và hỗ trợ xuất dữ liệu đã lọc ra tệp CSV chỉ bằng một cú click chuột.*
  >
  > *Như vậy, đồ án của Nhóm 10 đã hoàn thành trọn vẹn từ khâu xử lý dữ liệu thô, kiểm định thống kê học thuật, đến một ứng dụng Dashboard tương tác hoàn chỉnh và tiện ích.*
  >
  > *Em xin kết thúc phần trình bày của nhóm tại đây. Cảm ơn thầy và các bạn đã theo dõi. Nhóm rất mong nhận được những câu hỏi và ý kiến đóng góp từ thầy!"*

---

## PHẦN 3: GỢI Ý TRẢ LỜI CÁC CÂU HỎI VẤN ĐÁP (Q&A) TỪ HỘI ĐỒNG

### Câu 1: "Tại sao nhóm không loại bỏ bớt ngoại lệ (outliers) để phân phối bớt lệch và tăng tương quan?"

- **Trả lời**:
  > *"Dạ thưa thầy, quy tắc $1,5 \times \text{IQR}$ là một công cụ thống kê mô tả nhằm nhận diện các điểm đáng ngờ (flagging) để kiểm tra, không phải là cơ sở pháp lý để xóa dữ liệu. Trong thị trường lưu trú thực tế tại Bangkok, các biệt thự sang trọng hay căn hộ penthouse cao cấp có giá niêm yết hàng chục triệu hoặc hàng trăm nghìn THB là hoàn toàn tồn tại. Nếu tự ý cắt bỏ các điểm này, chúng ta sẽ bóp méo bức tranh thực tế của thị trường. Thay vào đó, nhóm chọn cách tiếp cận bền vững là sử dụng các đại lượng thống kê vững (robust statistics) như Trung vị (Median) và Khoảng tứ phân vị (IQR) thay vì giá trị Trung bình (Mean)."*

### Câu 2: "Tại sao nhóm kết luận mô hình hồi quy tuyến tính không khả thi? Như vậy có làm đồ án bị thiếu phần mô hình hóa không?"

- **Trả lời**:
  > *"Dạ thưa thầy, đồ án không hề thiếu phần mô hình hóa mà đã thực hiện đầy đủ quy trình thẩm định mô hình (Feasibility Evaluation) chuẩn mực khoa học:*
  > 1. *Nhóm phân chia 70% Train / 30% Test độc lập có `random_state=42` và 4-Fold Cross Validation trên tập Train để chống rò rỉ dữ liệu hoàn toàn.*
  > 2. *Nhóm áp dụng tiêu chuẩn chọn biến tiên nghiệm $|r| \ge 0,30$ và $p < 0,05$. Kết quả thực tế cho thấy không biến số nào vượt qua ngưỡng này.*
  > 3. *Nhóm giữ vững tính liêm chính học thuật: không cố tình gọt giũa dữ liệu để ép mô hình chạy ra $R^2$ ảo. Thay vào đó, nhóm thiết lập mô hình mốc so sánh chuẩn (Baseline DummyRegressor).*
  > 4. *Đồng thời, toàn bộ pipeline huấn luyện hoàn chỉnh (gồm Imputer, Scaler, OneHotEncoder và tinh chỉnh siêu tham số Ridge) đã được nhóm xây dựng và kiểm thử thành công trên dữ liệu giả lập trong bộ 91 unit tests của nhóm."*

### Câu 3: "Việc có nhiều listing cùng một chủ nhà (host clustering) ảnh hưởng như thế nào đến các kết luận thống kê?"

- **Trả lời**:
  > *"Dạ thưa thầy, trong tập dữ liệu sạch có 3.215 chủ nhà quản lý nhiều hơn 1 chỗ ở, thậm chí có chủ nhà quản lý hàng trăm căn hộ. Về mặt xác suất thống kê, các căn hộ này cùng chịu sự chi phối bởi một chính sách giá và phong cách vận hành của chủ nhà, do đó vi phạm giả định quan sát độc lập (IID - Independent and Identically Distributed). Khi giả định độc lập bị vi phạm, các giá trị $p$-value tính toán ra thường bị phóng đại (nhỏ hơn so với thực tế). Nhận thức rõ điều này, nhóm luôn lưu ý mọi kết quả kiểm định $p$-value trong đồ án chỉ mang tính khám phá (exploratory), không suy diễn nhân quả tổng quát."*
