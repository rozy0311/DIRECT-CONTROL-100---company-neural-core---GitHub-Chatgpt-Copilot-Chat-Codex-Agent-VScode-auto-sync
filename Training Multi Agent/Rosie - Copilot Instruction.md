Cách dùng hiệu quả nhất

❌ Không cần đính kèm file

Đính kèm 20+ files sẽ tốn token context rất lớn và không cần thiết.



❌ Không cần gửi path

Gửi path thôi thì tui cũng chưa biết đọc file nào, sẽ tốn thời gian explore.



✅ Cách tốt nhất: Dùng .github/copilot-instructions.md

Tạo 1 file instruction để tui tự động đọc training files khi cần, không cần bạn nhắc mỗi lần:


# Copilot Instructions



\## Knowledge Base

Trước khi giải quyết bài toán doanh nghiệp, đọc các file training tại:

D:\\active-projects\\Training Multi Agent\\



\- 🔴 LUÔN ĐỌC: `14-CHEAT-SHEET.md`, `01-EMADS-PR-Architecture.md`

\- 🟡 KHI CẦN:

\  - `02-Agent-Automation-Headless-Patterns.md` — Automation/CI/CD

\  - `03-Rosie-System-Prompt-Framework.md` — Decision framework

\  - `04-AI-Agent-Security-Defense.md` — Security

\  - `07-Cost-Aware-Planning-Agent.md` — Budget/Cost

\  - `12-LangGraph-Implementation.md` — Code implementation

\  - `13-Multi-Agent-Evaluation-Testing.md` — Testing

\  - `15-Spec-Driven-Dev-Copilot-CLI.md` — Copilot CLI

\  - `17-Agent-Supply-Chain-Security.md` — MCP/Supply chain

\  - `18-Open-Source-LLMs-Agentic-Tools.md` — Model selection

\  - `19-Codegen-n8n-Agent-DevOps-Toolchain.md` — DevOps

\  - `20-Azure-Foundry-Agent-Service.md` — Azure/Cloud

\- 🟢 THAM KHẢO: `05`, `06`, `08`, `09`, `10`, `11`, `16`



\## Rules

\- Luôn áp dụng EMADS-PR architecture khi thiết kế multi-agent

\- Automation score 0-12 cho mọi task

\- PR-only workflow, không direct commit

\- Human review bắt buộc cho score ≥ 4




Nhưng thực tế đơn giản hơn — bạn chỉ cần:

Khi gửi bài toán, thêm 1 dòng:



"Áp dụng kiến thức từ D:\\active-projects\\Training Multi Agent\\ để giải quyết bài toán sau: ..."



Tui sẽ tự:



Đọc 14-CHEAT-SHEET.md trước (tổng quan nhanh)

Đọc thêm file cụ thể tùy bài toán (ví dụ bài toán security → đọc file 04, bài toán cost → đọc file 07)

Áp dụng EMADS-PR framework để phân tích

📋 Tóm tắt

Cách	Hiệu quả	Lý do

Đính kèm 20+ files	❌ Lãng phí	Tốn hết context window

Gửi path không	⚠️ Được	Tui phải explore, chậm hơn

Gửi path + nói "áp dụng training"	✅ Tốt nhất	Tui đọc đúng file cần thiết

Tạo copilot-instructions.md	⭐ Tự động	Mọi chat đều có context sẵn

Nói ngắn gọn: Chỉ cần nhắc 1 câu là đủ, không cần đính kèm gì cả. Tui có quyền đọc file trong workspace rồi.

