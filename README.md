# denkkraft
### README

---

#### **English**

### Project Overview

This project demonstrates a modular architecture for handling data fetching, analysis, and trust score calculation. It is designed to distribute responsibilities among three team members while maintaining seamless integration through a main program.

- **Modules:**
  1. `DataFetcher`: Fetches and preprocesses data.
  2. `DataAnalyzer`: Performs completeness and update frequency analysis.
  3. `TrustScoreCalculator`: Calculates and visualizes the trust score.

---

### Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aloha1357/denkkraft.git
   cd your-repository-name
   ```

2. **Install dependencies:**
   Ensure you have Python 3.8+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main program:**
   ```bash
   python main.py
   ```

---

### Usage Instructions

1. **DataFetcher:**
   - Initialize with a data source (path or URL).
   - Fetch data using the `fetch_data()` method, which returns a DataFrame and metadata.

   Example:
   ```python
   fetcher = DataFetcher("data.csv")
   df, metadata = fetcher.fetch_data()
   ```

2. **DataAnalyzer:**
   - Use `calculate_completeness_score()` to compute the completeness of the data.
   - Use `calculate_update_score()` to analyze metadata for update frequency.

   Example:
   ```python
   analyzer = DataAnalyzer()
   completeness_score = analyzer.calculate_completeness_score(df)
   update_score = analyzer.calculate_update_score(metadata)
   ```

3. **TrustScoreCalculator:**
   - Combine the scores using `calculate_trust_score()`.
   - Visualize the results with `visualize_scores()`.

   Example:
   ```python
   calculator = TrustScoreCalculator()
   trust_score = calculator.calculate_trust_score(completeness_score, update_score)
   calculator.visualize_scores(df, trust_score)
   ```

---

### Contribution

1. Fork the repository and create a new branch for your changes.
2. Test your changes thoroughly.
3. Submit a pull request for review.

---

#### **中文**

### 專案概述

本專案展示了一個模組化架構，負責處理資料抓取、分析以及信任分數計算。該設計將功能分工給三位成員，並通過主程式進行無縫整合。

- **模組:**
  1. `DataFetcher`: 負責抓取與預處理資料。
  2. `DataAnalyzer`: 進行資料完整性與更新頻率分析。
  3. `TrustScoreCalculator`: 計算並視覺化信任分數。

---

### 安裝與設置

1. **複製專案：**
   ```bash
   git clone https://github.com/aloha1357/denkkraft.git
   cd your-repository-name
   ```

2. **安裝依賴套件：**
   確保已安裝 Python 3.8+。
   ```bash
   pip install -r requirements.txt
   ```

3. **執行主程式：**
   ```bash
   python main.py
   ```

---

### 使用說明

1. **DataFetcher:**
   - 初始化時提供資料來源（檔案路徑或 URL）。
   - 使用 `fetch_data()` 方法抓取資料，返回 DataFrame 和元數據。

   範例：
   ```python
   fetcher = DataFetcher("data.csv")
   df, metadata = fetcher.fetch_data()
   ```

2. **DataAnalyzer:**
   - 使用 `calculate_completeness_score()` 計算資料完整性分數。
   - 使用 `calculate_update_score()` 分析元數據的更新頻率。

   範例：
   ```python
   analyzer = DataAnalyzer()
   completeness_score = analyzer.calculate_completeness_score(df)
   update_score = analyzer.calculate_update_score(metadata)
   ```

3. **TrustScoreCalculator:**
   - 使用 `calculate_trust_score()` 合併分數。
   - 使用 `visualize_scores()` 將結果視覺化。

   範例：
   ```python
   calculator = TrustScoreCalculator()
   trust_score = calculator.calculate_trust_score(completeness_score, update_score)
   calculator.visualize_scores(df, trust_score)
   ```

---

### 貢獻方式

1. Fork 此專案並為您的修改創建新分支。
2. 徹底測試您的修改。
3. 提交 Pull Request 進行審查。

