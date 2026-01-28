# 🛒 E-Commerce Product Crawler (GUI)

> A user-friendly, Python-based desktop tool to recursively scrape product data (Price, SKU, Stock) from online stores.

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://python.org)
[![GUI](https://img.shields.io/badge/Interface-Tkinter-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview

**E-Commerce Product Crawler** is a desktop application designed for non-technical users to extract structured data from e-commerce websites. Unlike CLI scripts, it features a visual **Graphical User Interface (GUI)** built with Tkinter.

It allows you to:
*   **Recursively Crawl**: Navigate pagination and category links up to a custom depth.
*   **Extract Fields**: Automatically captures Name, Price, Category, SKU, and Stock Status.
*   **Export Data**: Saves all scraped results directly to CSV.

## 🚀 Features
*   **Visual Control**: Start, Stop, and Monitor progress via a dedicated dashboard.
*   **Custom Selectors**: Configure CSS selectors to match any target website layout.
*   **Depth Control**: Set how many levels deep the crawler should go.
*   **Request Safety**: Configurable delays and timeouts to avoid getting blocked.

## 🛠 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/bahaeddinmselmi/ecommerce-product-crawler-gui.git
    cd ecommerce-product-crawler-gui
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🕹 Usage

1.  Run the application:
    ```bash
    python product-web-crawler.py
    ```

2.  **In the GUI window**:
    *   **Start URL**: Enter the shop page URL (e.g., `https://myshop.com/products`).
    *   **Max Depth**: Set how many clicks deep to follow links (default: 2).
    *   **Actions**: Click `Start Crawling`.

3.  **Output**:
    Data is saved to `output_products.csv` in the same directory.

## ⚙️ Configuration
You can tweak the default scraping logic in the source code or via the UI parameters.
*   `delay`: Seconds to wait between requests (politeness).
*   `selectors`: Dictionary of CSS selectors for data points.

## 📄 License
MIT
