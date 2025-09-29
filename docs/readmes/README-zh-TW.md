# Template-Driven Development Framework for AI-Augmented Coding

![banner](../../misc/banner.png)

## 概述

TempDD 是一個「模板驅動」的開發框架，透過可自訂的工作流程與智慧引導的模板互動，讓人與 AI 可以更有結構地協作。

隨著專案越來越複雜，AI 想要獨立完成任務變得困難，人機協作的重要性因此提升。開發者需要一種更有效的方式來與這些像黑盒般的 AI Agent 溝通。模板驅動的方法能提供清楚的結構，減輕使用者的思考負擔，並透過引導式流程確保人機協作的一致性。這個框架提供了一個基礎，讓使用者能依照自己的專案需求，客製化整個工作流程，並把複雜的過程化繁為簡，拆解成一系列「填寫模板」的任務。同時，它也結合了 Agent 機制來降低模板的複雜度，使 AI 能更有效率地協助使用者完成文件與開發相關工作。我們期望這個框架不只適用於各種軟體開發場景，也能延伸到非開發的情境。同時，也希望透過開源協作，匯聚全球知識並持續完善這個框架。

## 特性

- 📚 **透過分層文件逐步掌握AI** - 透過複雜的多層文件從AI使用者轉變為AI專家，放大您對AI行為的控制
- 📋 **可客製化的模板驅動工作流程** - 透過可客製化模板進行專案開發的結構化方法
- 💬 **可客製化的智慧引導模板互動** - 可客製化智慧體適應每個模板，提供互動式指導幫助使用者協作填寫模板
- 🤖 **跨AI工具整合** - 與Claude Code、Gemini CLI、Cursor和GitHub Copilot無縫整合
- 🌐 **多語言支援** - 使用者可以使用他們偏好的語言填寫模板

## 快速開始

### 1. 安裝

使用uv安裝`tempdd`：

```bash
uv tool install --force --from git+https://github.com/GitYCC/TempDD.git tempdd && exec $SHELL
```

### 2. 初始化專案

建立新的專案目錄並初始化TempDD：

```bash
mkdir demo
cd demo
tempdd init  # 您可以在初始化期間選擇內建工作流程和偏好的AI工具
```

### 3. 範例：使用Claude Code的預設工作流程

以下範例演示了如何使用Claude Code的預設工作流程。有關詳細的客製化選項和可用工作流程，請參考`tempdd help`。

進入Claude Code後，按順序執行以下指令：

```bash
# 取得說明並了解可用指令
/tempdd-go help

# 產生產品需求文件
/tempdd-go prd build

# 完成PRD後，建立架構設計
/tempdd-go arch build

# 完成架構設計文件後，進行研究
/tempdd-go research build

# 完成研究報告後，建構實施藍圖
/tempdd-go blueprint build

# 完成藍圖後，產生任務清單
/tempdd-go tasks build

# 完成任務清單後，執行任務以產生程式碼
/tempdd-go tasks run
```

從這個範例中，您可以看到開發過程從想法到實作透過多層文件進行。每個文件由AI在需要時向使用者詢問輸入來填寫，這減少了使用者填表的複雜性，同時增強了AI與人類之間的共識。值得注意的是，研究步驟涉及AI主動在線搜索資訊以提高其對實作的理解。我相信存在更好的工作流程，我們不應該期望一個工作流程滿足每個專案。因此，該框架設計為易於客製化。請參考["客製化您的工作流程"](#客製化您的工作流程)部分了解更多。

## 客製化您的工作流程

TempDD允許您建立適合特定開發需求的自訂工作流程。

按照以下步驟客製化您的工作流程：
1. **閱讀指南**：查看[./customized/](../../customized/)取得全面的工作流程建立說明
2. **建立您的工作流程**，遵循提供的結構和範例
3. **使用自訂工作流程初始化專案**：

```bash
tempdd init --workflow /path/to/your/custom/workflow_dir/
```

## 貢獻內建工作流程

我們鼓勵貢獻者幫助擴展TempDD的內建工作流程集合！透過貢獻新的工作流程，您可以幫助其他開發者從經過驗證的開發模式和專業領域工作流程中受益。

### 如何貢獻新的內建工作流程

1. **Fork此倉庫** - 建立您自己的fork進行工作
2. **新增您的工作流程檔案**：
   - 將新的設定檔案新增到`./tempdd/core/configs/`
   - 將對應的模板新增到`./tempdd/core/templates/`
3. **提交Pull Request** - 與社群分享您的工作流程

您的貢獻將幫助TempDD對不同領域和用例的開發者更有價值。無論是行動開發、資料科學、DevOps還是任何其他專業化工作流程，我們都歡迎您的專業知識！

## 跨AI工具整合

TempDD與多個AI開發工具無縫整合：

| AI工具 | 狀態 |
|---------|--------|
| **Claude Code** | ✅ 完全支援 |
| **Gemini CLI** | ✅ 完全支援 |
| **Cursor** | ✅ 完全支援 |
| **GitHub Copilot** | ✅ 完全支援 |

## 致謝

感謝以下倉庫的啟發：
- [github/spec-kit](https://github.com/github/spec-kit)
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)