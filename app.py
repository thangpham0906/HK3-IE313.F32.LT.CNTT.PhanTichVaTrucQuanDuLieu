"""Dashboard tương tác trực quan hóa và phân tích dữ liệu Airbnb Bangkok.

Đồ án môn học IE313: Phân tích và Trực quan Dữ liệu (UIT - VNU-HCM) - Nhóm 10.
Thực hiện:
- Phạm Quốc Thắng (MSSV: 25410304) — Trưởng nhóm, Phân tích & Trực quan hóa
- Lê Minh Thiện (MSSV: 25410313) — Tiền xử lý, Thống kê suy luận & Thẩm định mô hình

Ứng dụng tái sử dụng 100% các module tính toán và hàm trực quan trong thư mục src/.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Đảm bảo thư mục gốc dự án có trong sys.path để import an toàn từ src/
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from src.data_loader import compute_sha256  # noqa: E402
from src.eda_stats import (  # noqa: E402
    EXPECTED_BASELINE_SHA256,
    compute_anova_test,
    compute_neighbourhood_pivot,
    compute_pairwise_correlations,
    compute_price_distribution_stats,
    compute_room_type_stats,
)
from src.visualization import (  # noqa: E402
    plot_neighbourhood_analysis,
    plot_price_distribution,
    plot_room_type_comparison,
    plot_size_correlation,
)


@st.cache_data
def load_baseline_data() -> pd.DataFrame:
    """Nạp dữ liệu sạch baseline và xác thực tính toàn vẹn qua mã SHA-256."""
    data_path = PROJECT_ROOT / "data/processed/bangkok_cleaned.csv"
    if not data_path.is_file():
        st.error(f"Không tìm thấy tệp dữ liệu baseline: {data_path}")
        st.stop()

    actual_hash = compute_sha256(data_path)
    df = pd.read_csv(data_path)
    df.attrs["sha256"] = actual_hash
    df.attrs["is_valid"] = actual_hash.lower() == EXPECTED_BASELINE_SHA256.lower()
    return df


def apply_filters(
    df: pd.DataFrame,
    selected_room_types: list[str],
    selected_districts: list[str],
    price_range: tuple[int, int],
    include_outliers: bool,
) -> pd.DataFrame:
    """Lọc dữ liệu dựa trên các tùy chọn của người dùng trên Sidebar."""
    filtered = df.copy()

    # 1. Lọc theo loại phòng (room_type)
    if selected_room_types:
        filtered = filtered[filtered["room_type"].isin(selected_room_types)]
    else:
        return filtered.iloc[0:0]

    # 2. Lọc theo quận hành chính (neighbourhood_cleansed)
    if selected_districts:
        filtered = filtered[filtered["neighbourhood_cleansed"].isin(selected_districts)]
    else:
        return filtered.iloc[0:0]

    # 3. Lọc theo khoảng giá (price)
    min_price, max_price = price_range
    filtered = filtered[filtered["price"] >= min_price]
    if not include_outliers:
        filtered = filtered[filtered["price"] <= max_price]

    return filtered


def main() -> None:
    st.set_page_config(
        page_title="Bangkok Airbnb Analytics - Nhóm 10",
        page_icon="🏙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Nạp dữ liệu cơ sở
    df_raw = load_baseline_data()

    # Tiêu đề & Thông tin đồ án
    st.title("🏙️ Phân Tích & Trực Quan Hóa Giá Thuê Airbnb Tại Bangkok")
    st.caption(
        "**Đồ án môn học IE313 — Phân tích và Trực quan dữ liệu** | "
        "Trường Đại học Công nghệ Thông tin (UIT - ĐHQG TP.HCM) | **Nhóm 10**"
    )

    # ========================== SIDEBAR BỘ LỌC ==========================
    with st.sidebar:
        st.header("🔍 Bộ Lọc Dữ Liệu")

        # 1. Lọc loại phòng
        all_rooms = sorted(df_raw["room_type"].dropna().unique().tolist())
        selected_rooms = st.multiselect(
            "Loại phòng (Room Type):",
            options=all_rooms,
            default=all_rooms,
            help="Chọn một hoặc nhiều loại chỗ ở để phân tích.",
        )

        # 2. Lọc quận
        all_districts = sorted(df_raw["neighbourhood_cleansed"].dropna().unique().tolist())
        top_10_districts = (
            df_raw["neighbourhood_cleansed"].value_counts().head(10).index.tolist()
        )
        quick_select = st.checkbox("Chỉ chọn nhanh Top 10 quận đông listing nhất", value=False)
        default_districts = top_10_districts if quick_select else all_districts

        selected_districts = st.multiselect(
            "Quận hành chính (Neighbourhood):",
            options=all_districts,
            default=default_districts,
            help="Lọc theo các quận/huyện tại thủ đô Bangkok.",
        )

        # 3. Lọc khoảng giá
        st.subheader("Ngân sách (THB/đêm)")
        price_min_val = int(df_raw["price"].min())
        price_slider = st.slider(
            "Khoảng giá thông dụng:",
            min_value=0,
            max_value=20000,
            value=(price_min_val, 10000),
            step=200,
            help="Kéo để giới hạn khoảng giá phân tích.",
        )

        include_outliers = st.checkbox(
            "Bao gồm căn hộ cao cấp / ngoại lai (> 20.000 THB)",
            value=False,
            help="Tích chọn để không giới hạn trần giá cao, bao gồm cả các biệt thự sang trọng.",
        )

        st.divider()
        st.markdown("**🛡️ Toàn vẹn dữ liệu**")
        status_icon = "✅" if df_raw.attrs.get("is_valid") else "⚠️"
        st.caption(f"{status_icon} **Mã SHA-256:** `{df_raw.attrs.get('sha256')[:16]}...`")
        st.caption(f"📊 **Quy mô baseline:** {len(df_raw):,} listing sạch")

    # Áp dụng bộ lọc
    df = apply_filters(df_raw, selected_rooms, selected_districts, price_slider, include_outliers)

    if df.empty:
        st.warning("⚠️ Không có listing nào thỏa mãn điều kiện lọc. Vui lòng mở rộng bộ lọc ở Sidebar!")
        return

    # ========================== KPI METRICS ROW ==========================
    stats_price = compute_price_distribution_stats(df["price"])
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            label="Tổng số Listing",
            value=f"{len(df):,}",
            delta=f"{(len(df) / len(df_raw)):.1%} tổng mẫu",
        )
    with kpi2:
        st.metric(
            label="Giá Trung Vị (Median)",
            value=f"{stats_price['median']:,.0f} THB",
            help="Thước đo đại diện xu hướng trung tâm, ít bị ảnh hưởng bởi giá cực đoan.",
        )
    with kpi3:
        st.metric(
            label="Giá Trung Bình (Mean)",
            value=f"{stats_price['mean']:,.0f} THB",
            delta=f"Skew: +{stats_price['skewness']:.1f}" if stats_price["skewness"] else None,
            delta_color="off",
            help="Giá trị trung bình bị kéo lệch bởi các căn hộ giá cực cao.",
        )
    with kpi4:
        superhost_pct = (df["host_is_superhost"] == "t").mean() * 100
        st.metric(
            label="Tỷ lệ Superhost",
            value=f"{superhost_pct:.1f}%",
            help="Tỷ lệ chủ nhà đạt danh hiệu Superhost uy tín.",
        )

    st.divider()

    # ========================== TABS NỘI DUNG NGHIÊN CỨU ==========================
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 RQ1: Phân Bố Giá",
            "🏠 RQ2: Loại Phòng & ANOVA",
            "📐 RQ3: Quy Mô & Tương Quan",
            "🗺️ RQ4: Phân Hóa Địa Lý",
            "📋 Khám Phá Dữ Liệu",
        ]
    )

    # ---------------- TAB 1: RQ1 PHÂN BỐ GIÁ ----------------
    with tab1:
        st.subheader("Phân Phối Giá Thuê Airbnb Bangkok (RQ1)")
        st.markdown(
            "Trực quan hóa phân phối toàn miền trên thang đo $\\log_{10}$ kết hợp vùng giá trung tâm "
            "nhằm quan sát hiện tượng đuôi dài lệch phải cực mạnh."
        )

        col_plot, col_stats = st.columns([2, 1])
        with col_plot:
            fig1, _ = plot_price_distribution(df["price"])
            st.pyplot(fig1)
            plt.close(fig1)

        with col_stats:
            st.markdown("##### 📌 Thống kê mô tả chi tiết")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"Chỉ số": "Cỡ mẫu (n)", "Giá trị": f"{stats_price['n']:,}"},
                        {"Chỉ số": "Tối thiểu (Min)", "Giá trị": f"{stats_price['min']:,.2f} THB"},
                        {"Chỉ số": "Phân vị 25% (Q1)", "Giá trị": f"{stats_price['q1']:,.2f} THB"},
                        {"Chỉ số": "Trung vị (Median)", "Giá trị": f"{stats_price['median']:,.2f} THB"},
                        {"Chỉ số": "Phân vị 75% (Q3)", "Giá trị": f"{stats_price['q3']:,.2f} THB"},
                        {"Chỉ số": "Khoảng tứ phân vị (IQR)", "Giá trị": f"{stats_price['iqr']:,.2f} THB"},
                        {"Chỉ số": "Độ lệch chuẩn (Std)", "Giá trị": f"{stats_price['std']:,.2f} THB"},
                        {"Chỉ số": "Hệ số bất đối xứng (Skewness)", "Giá trị": f"{stats_price['skewness']}"},
                        {"Chỉ số": "Ngoại lệ theo 1.5×IQR", "Giá trị": f"{stats_price['outliers_count']:,} ({stats_price['outliers_pct']}%)"},
                    ]
                ),
                hide_index=True,
                width="stretch",
            )

    # ---------------- TAB 2: RQ2 LOẠI PHÒNG & ANOVA ----------------
    with tab2:
        st.subheader("So Sánh Giá Giữa Các Loại Phòng & Kiểm Định ANOVA (RQ2)")
        col_r_plot, col_r_info = st.columns([2, 1])

        with col_r_plot:
            fig2, _ = plot_room_type_comparison(df)
            st.pyplot(fig2)
            plt.close(fig2)

        with col_r_info:
            st.markdown("##### 🧪 Kết quả kiểm định thống kê")
            anova_res = compute_anova_test(df)
            f_val = anova_res["omnibus_test"]["f_statistic"]
            p_val = anova_res["omnibus_test"]["p_value"]

            st.metric("ANOVA F-statistic", f"{f_val:.4f}" if f_val else "N/A")
            st.metric("p-value", f"{p_val:.4e}" if p_val else "N/A")

            st.info(
                f"**Khuyến nghị phương pháp luận:**\n\n"
                f"{anova_res['condition_checks']['scientific_recommendation']}"
            )

        st.markdown("##### 📋 Thống kê chi tiết từng loại phòng")
        rq2_data = compute_room_type_stats(df)
        df_room = pd.DataFrame.from_dict(rq2_data["by_room_type"], orient="index")
        st.dataframe(
            df_room[["n", "group_n_pct", "q1", "median", "q3", "mean", "std", "skewness"]].rename(
                columns={
                    "n": "Số mẫu",
                    "group_n_pct": "Tỷ trọng (%)",
                    "q1": "Q1 (THB)",
                    "median": "Trung vị (THB)",
                    "q3": "Q3 (THB)",
                    "mean": "Trung bình (THB)",
                    "std": "Độ lệch chuẩn",
                    "skewness": "Skewness",
                }
            ),
            width="stretch",
        )

    # ---------------- TAB 3: RQ3 QUY MÔ & TƯƠNG QUAN ----------------
    with tab3:
        st.subheader("Tương Quan Tuyến Tính Giữa Quy Mô Chỗ Ở Và Giá (RQ3)")
        st.markdown(
            "Đánh giá hệ số tương quan Pearson ($r$) giữa 4 biến quy mô vật lý và giá thuê."
        )

        col_s_plot, col_s_table = st.columns([2, 1])
        with col_s_plot:
            fig3, _ = plot_size_correlation(df, sample_display_n=min(3000, len(df)))
            st.pyplot(fig3)
            plt.close(fig3)

        with col_s_table:
            st.markdown("##### 📐 Ma trận hệ số Pearson")
            corr_df = compute_pairwise_correlations(df)
            st.dataframe(
                corr_df[["feature", "pearson_r", "p_value", "strength", "n_valid"]],
                hide_index=True,
                width="stretch",
            )
            st.caption(
                "💡 **Nhận xét:** Hệ số $r < 0,11$ cho thấy tương quan tuyến tính rất yếu. "
                "Quy mô phòng không phải là biến số quyết định duy nhất tới giá."
            )

    # ---------------- TAB 4: RQ4 PHÂN HÓA ĐỊA LÝ ----------------
    with tab4:
        st.subheader("Phân Hóa Giá Thuê Theo Địa Lý & Bảng Chéo 2D (RQ4)")
        fig4a, fig4b = plot_neighbourhood_analysis(df)

        st.markdown("##### 🗺️ Bản đồ nhiệt (Heatmap) Trung Vị Giá: Top Quận × Loại Phòng")
        st.pyplot(fig4a)
        plt.close(fig4a)

        st.markdown("##### 📊 So Sánh Giá Căn Hộ Nguyên Căn (Entire home/apt) Giữa Các Quận")
        st.pyplot(fig4b)
        plt.close(fig4b)

        st.markdown("##### 📑 Bảng chéo 2D (Pivot Table): Trung Vị Giá theo Quận × Loại Phòng")
        p_med, _, _, _ = compute_neighbourhood_pivot(df)
        st.dataframe(p_med, width="stretch")

    # ---------------- TAB 5: KHÁM PHÁ DỮ LIỆU ----------------
    with tab5:
        st.subheader("Tra Cứu & Trích Xuất Dữ Liệu Đã Lọc")
        st.markdown(f"Hiển thị danh sách **{len(df):,}** listing thỏa mãn bộ lọc hiện hành.")

        display_cols = [
            "id",
            "neighbourhood_cleansed",
            "room_type",
            "property_type",
            "price",
            "accommodates",
            "bedrooms",
            "bathrooms",
            "beds",
            "minimum_nights",
            "number_of_reviews",
            "review_scores_rating",
            "host_is_superhost",
        ]
        valid_cols = list(dict.fromkeys([c for c in display_cols if c in df.columns]))

        st.dataframe(
            df[valid_cols].sort_values("price", ascending=False),
            width="stretch",
            height=400,
        )

        csv_data = df[valid_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Tải xuống dữ liệu đã lọc (CSV)",
            data=csv_data,
            file_name="bangkok_airbnb_filtered.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
