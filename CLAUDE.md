# BookingLite - Handoff Document (Dành cho Claude)

Tài liệu này tổng hợp toàn bộ kiến trúc, tiến độ công việc, các kỹ thuật đã sử dụng và những lỗi cần tránh để Claude có thể tiếp nhận và lập trình tiếp tục một cách mượt mà nhất.

---

## 1. Kiến trúc & Công nghệ (Architecture & Tech Stack)
- **Dự án**: BookingLite (App Đặt bàn trực tuyến và Dashboard Quản lý nhà hàng - Demo tĩnh/SPA).
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla ES6). Không dùng Framework JS (React/Vue).
- **Styling**: TailwindCSS + DaisyUI (chạy qua CDN script cho mục đích prototype nhanh gọn).
- **Icons**: Lucide Icons (load qua thẻ `<script>`).
- **Routing**: Tự xây dựng SPA Router nội bộ trong file `merchant/spa.js`. Sử dụng `fetch` kết hợp `View Transitions API` để chuyển cảnh không chớp trang, siêu mượt.
- **Design System**: Chuẩn **Premium UI** (Glassmorphism, shadow mềm mại, border-radius lớn: 12-24px, chuyển động nút bấm/form nảy nhẹ dùng `cubic-bezier(0.34, 1.56, 0.64, 1)`).

---

## 2. Các Tính Năng Đã Hoàn Thiện
### Khách hàng (End-User)
- Giao diện chọn Chi nhánh dạng Card UI có hiệu ứng hover sang trọng.
- Khi chọn nhánh, truyền query param `?branch=2` để trang đặt bàn hiển thị đúng chi nhánh tương ứng.

### Quản trị nhà hàng (Merchant)
- **Trang Đăng ký (Onboarding)**:
  - Khai báo số lượng chi nhánh sử dụng thiết kế Pill Counter (Bộ đếm viên thuốc bo tròn) với nút tăng/giảm cao cấp, thay thế cho giao diện thô ráp.
  - Render Form động: Khi tăng số lượng chi nhánh, tự động đẻ ra các khối nhập liệu mới. Chi nhánh 2 điền mẫu sẵn, từ 3 trở đi để trống.
  - Block Spam: Nếu điền > 2 chi nhánh và bấm "Tạo quán", hệ thống bật Modal chặn (z-index 9999) thông báo "Giới hạn bản Demo".
- **Chuyển đổi Chi nhánh Đa luồng (Multi-branch Switcher)**:
  - Tích hợp Menu Dropdown (dùng thẻ `<details>` DaisyUI) trên Sidebar.
  - Khi bấm đổi qua "Trum Quán 2": URL đổi thành `?branch=2` không reload trang.
  - **Mô phỏng dữ liệu (Demo Data Engine)**: File `spa.js` chứa hàm `applyDemoBranchData()` sẽ tự động quét trang hiện tại và đắp dữ liệu của Chi nhánh 2 lên giao diện:
    - **Dashboard**: Tự động thay đổi 4 thẻ KPI (Booking, Khách, Hủy, Doanh thu 12.5M) và tự chế tên khách mới trong bảng.
    - **Báo cáo**: Thay số biểu đồ Donut (Tỉ lệ hoàn tất lên 88%), số lượng khách vượt trội.
    - **Khách hàng**: Tổng lượng khách nhảy lên 5.102, danh sách bàn đổi thành tên các Nghệ sĩ nổi tiếng.
    - **Lịch**: Cộng dồn thêm số người ở các booking.
    - **Cài đặt**: Đổi Tên quán, Sức chứa xuống 15 bàn, Địa chỉ qua Quận 1.
- **Cơ chế Router SPA (`spa.js`)**:
  - Chặn sự kiện click của các `a.navlink` và xử lý thông qua Fetch API.
  - Đóng gói logic morphing DOM và gọi lại các icon/scripts vào luồng chuyển View Transitions.

---

## 3. Các Lỗi Khó (Gotchas) Đã Sửa Trọng Điểm
1. **Lỗi cú pháp JS khi Regex Replace**: Khi sử dụng Python thao tác trên `spa.js`, từng có lỗi để thừa một dấu phẩy `(document.addEventListener('click', , (e) => ...)` gây sập hoàn toàn luồng SPA và dropdown không hoạt động. Cần cẩn thận khi đắp ghép string.
2. **Vấn đề Dropdown & z-index**: Dropdown của DaisyUI cần `z-[100]` và `origin-top` + animation để xổ xuống mượt mà. Đảm bảo nó luôn đè lên các `.card` ở dưới. Modal thì phải luôn > `z-[9999]`.
3. **Thẻ Script không tự chạy trong SPA**: Dùng `.innerHTML` đắp code tĩnh sẽ không làm thẻ `<script>` thực thi. File `spa.js` đã phải móc toàn bộ thẻ `<script>` ra, tạo element script mới dán đè vào để trình duyệt chạy code. Tuyệt đối không can thiệp phá vỡ flow này trong `spa.js`.
4. **Lucide Icons tàng hình**: Mỗi khi JS render thêm DOM (VD: đẻ form chi nhánh) hoặc SPA nhảy qua tab mới, hàm `lucide.createIcons()` phải được gọi lại nếu không mọi biểu tượng SVG sẽ biến mất.
5. **Tailwind CDN Limitation**: Do chạy qua script `<script src="https://cdn.tailwindcss.com"></script>`, đừng ghép tên class động dạng string template (vd: `bg-${color}-500`) vì trình phân tích của Tailwind CDN sẽ không nhận diện được.
6. **SPA làm rớt `?branch` khi điều hướng (ĐÃ SỬA)**: Trong `spa.js`, khi chuyển menu phải **mang `?branch` hiện tại vào URL đích** và gọi `history.pushState(URL mới)` **TRƯỚC** khi chạy `applyDemoBranchData()`. Nếu không: qua menu khác sẽ quay về Chi nhánh 1 (vì `location.pathname`/`search` còn của trang cũ → đắp dữ liệu sai trang/sai nhánh).
7. **Selector `applyDemoBranchData()` phải khớp markup thực tế (ĐÃ SỬA)**: Sau khi đại tu UI (table → list, đổi font, thêm branch dropdown), các selector cũ (`tbody tr`, `td .font-bold`, `h1.nextElementSibling`) không còn khớp ⇒ Chi nhánh 2 không đổi số liệu. Đã viết lại theo "mỏ neo" bền vững: KPI tra theo **nhãn** (`setStatByLabel`), tên khách đổi **2 chiều** (`renameBranch` + map xuôi/ngược nên qua/lại đều đúng), Sơ đồ bàn theo `.badge b`, Cài đặt theo thứ tự `main input.input-bordered`, Báo cáo theo `.radial-progress`. Khi sửa lại markup các trang merchant, **giữ nguyên các mỏ neo này** kẻo hỏng chuyển chi nhánh.

---

## 4. Hướng Làm Tiếp Theo Dành Cho Claude
- Mọi kiến trúc nền tảng và cơ chế truyền dữ liệu Demo qua query params `?branch=` đã được thiết lập cực kỳ trơn tru, không lỗi lầm.
- Claude có thể tiếp quản để:
  1. Phát triển **Sơ đồ bàn (Grid Layout)**.
  2. Bổ sung các trang chưa có (Thực đơn / Tra cứu đơn).
  3. Áp dụng phong cách **Premium UI/UX** vào các form popup, modal đặt bàn mới, hoặc tối ưu giao diện điện thoại (Responsive) nếu phát sinh thêm khối mới.
  4. Nếu cần Mock Data phức tạp hơn, cứ tiếp tục nhét logic vào hàm `applyDemoBranchData()` trong `merchant/spa.js`. Chú ý dùng `window.location.pathname` để check đúng trang.

---

## 5. Chuẩn giao diện & QA Mobile (đã rà toàn bộ)
- **Font**: `Inter` (400–800) đồng bộ mọi trang; hỗ trợ tiếng Việt tốt.
- **Icon**: Lucide pin bản `0.360.0` (jsDelivr) ở tất cả trang — ổn định, không tự cập nhật.
- **Viewport**: `width=device-width, initial-scale=1.0` mọi trang — **cho phép pinch-zoom** (đã bỏ `user-scalable=no` ở trang quán & chọn chi nhánh để đạt accessibility).
- **End-user**: khung "điện thoại" (`h-[100dvh] sm:h-[800px]`), header/CTA cố định, nội dung cuộn riêng. Mobile = full màn; desktop = thẻ bo góc căn giữa.
- **Merchant app**: DaisyUI `drawer lg:drawer-open` — sidebar cố định ở `lg`, thu thành drawer ở mobile; mọi trang có nút mở menu `<label for="nav" class="lg:hidden">`. Bảng dữ liệu bọc `overflow-x-auto`.
- **Brand**: cam `#F26522` + xanh iPOS `#0067B1`; nền aurora (trang khách) / lưới chấm (app).
- **Đã kiểm**: không có phần tử fixed-width gây tràn ngang; tab/bộ lọc dài cho cuộn ngang.
- **Lưu ý hiệu năng (prototype)**: Tailwind chạy qua `cdn.tailwindcss.com` (JIT runtime) + `style.css` + DaisyUI full + Inter + Lucide ⇒ chấp nhận được cho demo, nhưng có FOUC nhẹ lúc load. Khi lên production nên build Tailwind tĩnh (CLI/PostCSS) để bỏ runtime compile.
