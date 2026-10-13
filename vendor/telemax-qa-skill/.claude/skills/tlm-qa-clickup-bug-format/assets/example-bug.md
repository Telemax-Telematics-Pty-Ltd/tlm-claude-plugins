# Ví dụ một bug hoàn chỉnh

Dựng từ một dòng Defects đã review. Dùng làm mẫu về mức độ cụ thể cần đạt, không
phải để chép nguyên văn. Phần giữa hai vạch `---` là **nguyên văn** thân bug gửi lên
ClickUp — kể cả cách xuống dòng: tiêu đề mục nằm sát nội dung, chỉ một dòng trống giữa
hai mục, mỗi đoạn văn là một dòng (không ngắt dòng cứng).

---

## Ví dụ 1 — bug UI (2 scenario)

**Title**
`[Vehicle Detail] Missing error message when vehicle name is left empty`

**Summary**
Saving the Vehicle Detail form with an empty Vehicle Name closes the dialog without any validation message. The vehicle is stored with a blank name, so it shows as an empty row in the Vehicles list and fleet managers cannot identify it. Affects both editing an existing vehicle and creating a new one.

**Description**
The required-field check on Vehicle Name is missing on the client, and the API accepts an empty name, so nothing stops the save.

**Scenario 1 — Edit an existing vehicle**
URL: https://dashboard-stage.telemax.com.au/manage/vehicles-v3/20451
1. Log in to dashboard-stage as a Fleet Manager
2. Open the URL above
3. Clear the Vehicle Name field
4. Click Save
Actual: Dialog closes, no validation message shown. The list row for vehicle `20451` renders with an empty title. `PUT /vehicles/20451` returns 200.
Expected: Save is blocked and "Vehicle name is required." is displayed under the field. No request is sent.

**Scenario 2 — Create a new vehicle**
URL: https://dashboard-stage.telemax.com.au/manage/vehicles-v3/new
1. Log in to dashboard-stage as a Fleet Manager
2. Open the URL above
3. Fill every required field except Vehicle Name
4. Click Save
Actual: Vehicle is created with an empty name. `POST /vehicles` returns 201.
Expected: Save is blocked and "Vehicle name is required." is displayed under the field.

**Evidence**
- Scenario 1: `TC-B-004-FAIL.png` (attached)
- Scenario 2: `TC-B-005-FAIL.png` (attached)

**Field ClickUp**
- TC ID: `TC-B-004`, `TC-B-005` · Environment: dashboard-stage
- Priority: High (mapped from test case Priority = High)
- Status: Open
- Assignee: đề xuất từ commit đụng `VehicleFormValidator.cs` — **chờ duyệt**

---

## Ví dụ 2 — bug API (1 scenario)

**Title**
`[PUT /vehicles/{id}] Returns 500 with stack trace on malformed JSON body`

**Summary**
Sending a malformed JSON body to the vehicle update endpoint crashes the request with a 500 instead of returning a 400. The error response leaks the internal exception type and server file path, which exposes implementation details to any API client.

**Scenario 1 — Truncated JSON body**
URL: `PUT https://api-stage.telemax.com.au/vehicles/20451`
1. Authenticate against staging and obtain a valid token
2. Send the request above with body `{"name": ` (truncated JSON)
Actual: `500 Internal Server Error`. Body contains `Newtonsoft.Json.JsonReaderException` and the server path `/app/src/Telemax.Api/Controllers/VehiclesController.cs`.
Expected: `400 Bad Request` with the standard error envelope. No internal type name or file path in the response body.

**Field ClickUp**
- TC ID: `TC-API-007` · Environment: staging API
- Priority: High · Status: Open
