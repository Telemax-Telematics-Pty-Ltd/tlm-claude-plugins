---
name: tlm-qa-clickup-bug-format
description: >-
  Dùng khi cần tạo bug hoặc defect trên ClickUp cho test case Fail/Blocked, hoặc khi
  người dùng nói "tạo bug cho case này", "file bug lên ClickUp".
---

# tlm-qa-clickup-bug-format

Khuôn để mọi bug từ harness lên ClickUp đồng nhất, đủ thông tin cho dev fix ngay,
không phải hỏi lại. Skill là phần TĨNH (bug trông thế nào); agent lo phần ĐỘNG (tạo
bug qua MCP sau khi người dùng duyệt).

Chạy `bash .claude/scripts/qa-config.sh clickup` cho list/space đích, tag, priority map,
status ban đầu và rule assign. Giá trị nào còn `CHƯA ĐIỀN` là điều kiện chưa thoả:
DỪNG và hỏi người dùng, không đoán.

Ví dụ một bug hoàn chỉnh: [assets/example-bug.md](assets/example-bug.md).

## Nguồn dữ liệu bug

Bug được tạo từ **sheet "Defects & Follow-ups"** (sau khi người dùng review: sửa
Actual, đánh Fix Status). Dữ liệu lấy qua `write_defects.py --mode read`, đã kèm sẵn
steps/expected từ sheet Test Cases. KHÔNG tự bịa nội dung ngoài những gì có trong file.

**Dòng cần tạo bug = chưa có Bug ID VÀ chưa có Fix Status.** Người dùng từ chối một
bug bằng cách đặt **Fix Status = "Won't fix"**, KHÔNG phải bằng cách xoá dòng — xoá
dòng thì lần retest sau case vẫn Fail, vẫn chưa có Bug ID, nên nó quay lại.

**Đọc bản LOCAL.** Nếu người dùng review trên Google Drive, phải tải file về ghi đè
bản local trước khi chạy `--mode read`. Đọc bản local trong khi họ sửa bản Drive là
đọc file cũ.

## Đầu vào skill cần

| Cần | Nguồn | Thiếu thì |
|---|---|---|
| Actual Result cụ thể | cột Actual của sheet Defects (agent điền từ log, người dùng đã review) | Hỏi. **Không viết "nó lỗi" hay mô tả chung chung** |
| Steps + Expected | sheet Test Cases, qua `--mode read` | Hỏi. Không tự viết lại các bước |
| List/Space ClickUp đích | `qa-config.md` | **Hỏi. Không đoán list** — tạo bug nhầm list là rác cho người khác dọn |
| Duyệt danh sách bug + assignee | người dùng | Không tạo bug khi chưa được duyệt |
| Quyết định khi có bug trùng | người dùng | Nêu bug cũ ra và hỏi dùng ID cũ hay tạo mới |

## Ngôn ngữ

Bug viết bằng **tiếng Anh** — cùng ngôn ngữ với sheet "Test Cases" (EN), là nguồn
chân lý mà Steps/Expected được lấy ra. Ngoại lệ: message hệ thống trích nguyên văn
giữ đúng ngôn ngữ gốc trong ngoặc kép.

## Chống trùng — với ClickUp, không chỉ với file

Trước khi tạo, **search ClickUp** theo TC ID và theo tiêu đề gần đúng
(`ClickUp:clickup_search`). Đã có bug mở cho cùng triệu chứng → **không tạo mới**:
lấy Ticket ID cũ đưa vào bugmap writeback và báo người dùng.

File chỉ chống trùng trong phạm vi chính nó; nó không biết tester khác đã raise gì.
Bỏ bước này là đường nhanh nhất để dev nhận 3 bug giống hệt nhau.

## Nội dung bug — Summary trước, Details sau

Thân bug luôn theo đúng thứ tự này:

**1. Summary** — đoạn ngắn **~50 từ** (tối đa ~60), luôn ở đầu: cái gì sai, ở màn hình/
endpoint nào, ảnh hưởng ai. Người lướt ClickUp chỉ đọc đoạn này phải hiểu được bug. Cột
Description trong Defects trống thì tổng hợp từ Title + bối cảnh (KHÔNG chép nguyên Title).
Không mở đầu bằng tên class.

**2. Details** — phần chi tiết cho dev, gồm:

- **Description** — mô tả đầy đủ hơn Summary khi cần (bối cảnh, phạm vi ảnh hưởng). Bug
  là tài liệu cho **dev**, nên chi tiết kỹ thuật (status code, message lỗi) đặt ở Actual.
- **Scenarios** — Steps to reproduce **tách thành 1 hoặc nhiều scenario**, mỗi scenario
  là một đường tái hiện riêng (khác dữ liệu, khác role, khác điểm vào…). Một bug chỉ có
  một đường thì vẫn ghi `Scenario 1`. Mỗi scenario gồm, theo thứ tự:
  1. Tiêu đề scenario ngắn: `Scenario N — <khác biệt của đường này>`
  2. **URL**: đường dẫn **đầy đủ** tới màn hình/endpoint có bằng chứng, ví dụ
     `https://dashboard-stage.telemax.com.au/manage/vehicles-v3/20451` — ghép
     `BASE_URL` (`telemax-e2e/.env`) với path thật lúc test, kèm ID/query thật. **Không
     ghi path tương đối** (`/manage/vehicles-v3/…`) hay mô tả kiểu "trang vehicle".
     Bug API thì ghi method + URL đầy đủ. URL lấy từ log/trace của lần chạy (trang
     đang mở lúc case fail); log không có thì **hỏi**, không tự dựng ID.
  3. Các bước, đánh số — lấy từ **Test Steps** (cột G sheet Test Cases). Đủ để người
     khác làm theo ra đúng lỗi.
  4. `**Actual:** …` — hiện trạng thật của **scenario này**, lấy từ cột **Actual Result** của
     Defects (agent điền từ log, người dùng đã review). Cụ thể: message sai gì, status
     code nào, hành vi lệch ra sao — không viết chung chung "nó lỗi".
  5. `**Expected:** …` — kết quả đúng của **scenario này**, lấy từ **Expected Result** (cột
     I). Nếu là message, trích nguyên văn.

  Actual/Expected đặt **ngay sau từng scenario**, không gom chung một cục ở cuối bug.
- **Evidence** — mọi bằng chứng có đường dẫn đều ghi **URL đầy đủ** (trang lỗi, link
  ảnh/video đã upload, link run). File đính kèm (screenshot) vẫn đính qua
  `ClickUp:clickup_attach_task_file`, và nêu tên file để dev biết ảnh nào của scenario nào.
- **Field ClickUp** — TC ID, môi trường, priority, status, assignee (xem "Truy vết").

### Xuống dòng — không dòng trống thừa

Mỗi mục (Summary, Description, Scenario N, Evidence, Field ClickUp) là một khối:
**tiêu đề mục ở dòng riêng, nội dung bắt đầu ngay dòng kế tiếp** — không có dòng trống
giữa tiêu đề và nội dung. **Chỉ dùng đúng 2 ký tự xuống dòng (một dòng trống) để tách
hai mục**, không bao giờ nhiều hơn.

```
**Summary**
<nội dung>

**Scenario 1 — <...>**
URL: <url đầy đủ>
1. <bước>
**Actual:** <...>
**Expected:** <...>
```

`**Actual:**` và `**Expected:**` luôn **tô đậm**, nằm **đầu dòng, không thụt lề** — không
viết thành bullet (`- `) hay item đánh số, không lồng vào danh sách bước.

Trong một mục cũng không chèn dòng trống (giữa steps, `Actual:`, `Expected:`), và mỗi
đoạn văn viết trên **một dòng** — không ngắt dòng cứng giữa câu. "Details" chỉ là tên
nhóm các mục sau Summary, **không** in thành một dòng tiêu đề riêng (nó sẽ thành tiêu
đề không có nội dung ngay dưới).

## Tiêu đề bug

Ngắn, cụ thể, có ngữ cảnh: `[Màn hình/API] — <triệu chứng ngắn>`.
Ví dụ: `[Vehicle Detail] Missing error message when vehicle name is left empty`.
Tránh tiêu đề mơ hồ kiểu "Bug ở trang chi tiết".

## Truy vết & liên kết

- Ghi **TC ID** liên quan trong bug (để đối chiếu ngược file test case).
- Ghi **ticket gốc** (`TLM-XXXX`) để bug link ngược về yêu cầu. Ticket gốc không tồn
  tại (spec dán tay, khoá là `TMP-<slug>`) → ghi thẳng vào bug là chưa có ticket yêu
  cầu, đừng bỏ trống lặng lẽ: dev đọc bug sẽ không biết đối chiếu với cái gì.
- Nêu **môi trường** test.
- Đính screenshot/log nếu có (`ClickUp:clickup_attach_task_file`), không đính data
  nhạy cảm nguyên văn. Bug từ case UI thường đã có ảnh sẵn ở
  `.qa/TLM-XXXX/phase1/<TC-ID>-FAIL.png` (Phase 1) hoặc `telemax-e2e/test-results/`
  (chạy bằng code) — đính vào, đừng để dev phải tự dựng lại.

## Sau khi tạo bug

Bug tạo trên ClickUp sinh **Ticket ID dạng TLM-xxxx**. Ghi ID này trả lại file test
case:

```
bash .claude/scripts/qa-py.sh .claude/skills/tlm-qa-testcase-template/scripts/write_defects.py --file <out.xlsx> --mode writeback \
  --bugmap '{"TC-A-003": "TLM-9001"}'
bash .claude/scripts/qa-py.sh .claude/skills/tlm-qa-testcase-template/scripts/recalc.py <out.xlsx>
```

**Khoá theo TC ID, KHÔNG theo số dòng.** Giữa `--mode read` và `--mode writeback`,
chỉ cần người dùng chèn hoặc xoá một dòng trong Excel là mọi index dòng lệch đi và
Ticket ID sẽ gắn sang case khác — sai lặng lẽ, không có gì báo.

Script ghi vào cột "Bug ID/Ticket" của sheet Defects **và** cạnh Result của round
fail ở sheet Test Cases. Nhờ đó nhìn file biết ngay case nào đã có bug, và lần
retest `--mode read`/`fill` tự bỏ qua dòng đã có Ticket ID nên không tạo trùng.

## Ranh giới

- Skill chỉ định KHUÔN; KHÔNG tự tạo bug. `bug-proposer` dùng khuôn này để **đề
  xuất**; `bug-filer` mới tạo qua ClickUp MCP, và chỉ sau khi người dùng đã duyệt cả
  lô ở command.
- KHÔNG tạo bug cho dòng đã có Bug ID, đã có Fix Status, hoặc case `[MANUAL]`.
- KHÔNG đính data khách/nhạy cảm nguyên văn vào bug.

## Tự kiểm trước khi tạo bug

- [ ] Mở đầu bằng Summary ~50 từ, rồi mới đến Details
- [ ] Steps tách thành ≥1 scenario; mỗi scenario có URL đầy đủ + `**Actual:**` + `**Expected:**` (đậm, đầu dòng, không thụt lề)
- [ ] Mọi evidence có đường dẫn đều là URL đầy đủ (không path tương đối)
- [ ] Tiêu đề mục sát nội dung; chỉ một dòng trống giữa hai mục, không dòng trống nào khác
- [ ] Tiêu đề cụ thể, có ngữ cảnh màn hình/API
- [ ] Có TC ID + môi trường
- [ ] Actual cụ thể (message/status thật), không chung chung
- [ ] Assignee đã được người dùng duyệt (hoặc để trống, ghi "assign tay")
- [ ] Đã search ClickUp chống trùng trước khi tạo
- [ ] List/Space đích trong `qa-config.md` đã điền (không còn `CHƯA ĐIỀN`)
- [ ] Sau khi tạo: ghi Bug ID về file bằng bugmap khoá theo TC ID
- [ ] Đã chạy `recalc.py` sau writeback
