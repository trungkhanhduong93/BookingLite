# Booking Lite — Prototype HTML tĩnh

SAAS giúp Merchant (quán ăn/cà phê) nhận đơn đặt bàn từ end-user.
Tiêu chí cốt lõi: **Onboarding siêu nhanh**. Đây là **prototype tĩnh** để demo ý tưởng
(không backend, dữ liệu là dummy/mock).

**Tác giả:** trung.duong (Trum)

## Cấu trúc

> Kiến trúc nghiệp vụ chi tiết: xem **ARCHITECTURE.md** (BA design).

```
/index.html               # Trang chủ tổng — 2 lối vào (khách / chủ quán)
/end-user/                # Luồng KHÁCH (mobile-first, khung điện thoại)
  index.html              # Trang quán "Nhà hàng Trum Quán"
  thuc-don.html           # Thực đơn theo danh mục
  1-chon-gio.html         # Step 1: chọn ngày, giờ, số khách
  2-thong-tin.html        # Step 2: thông tin liên hệ / login
  3-xac-nhan.html         # Step 3: xác nhận thành công (xoá sessionStorage)
  tra-cuu.html            # Tra cứu & theo dõi/huỷ đơn (mã + SĐT)
/merchant/                # App QUẢN TRỊ (drawer sidebar, responsive)
  index.html              # Landing marketing + đăng nhập
  onboarding.html         # Nhập thông tin quán → nhận link đặt bàn
  dashboard.html          # Tổng quan: KPI + đơn hôm nay
  lich.html               # Lịch đặt bàn (timeline theo khung giờ)
  ban.html                # Sơ đồ bàn (floor map theo khu vực)
  khach-hang.html         # Khách hàng (CRM)
  bao-cao.html            # Báo cáo & phân tích (biểu đồ CSS)
  cai-dat.html            # Cài đặt quán (giờ, khung giờ, link/QR, thông báo)
  booking-detail.html     # Chi tiết đơn (timeline trạng thái + thao tác)
/favicon.svg              # Logo thương hiệu
/ARCHITECTURE.md          # Tài liệu kiến trúc (BA)
```

### App-shell quản trị (các trang /merchant trừ index & onboarding)
- Dùng DaisyUI `drawer lg:drawer-open`: sidebar cố định ở `lg`, thu thành drawer ở mobile.
- Sidebar nav dùng class `.navlink`; mục đang chọn thêm `.active` (nền cam, chữ trắng).
- Topbar: nút `menu` (mở drawer, ẩn ở `lg`) + tiêu đề + chuông + avatar.

## Quy ước UI/UX dùng chung cho MỌI file HTML

### 1. CDN bắt buộc trong `<head>` (theo đúng thứ tự)
```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.min.css" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 2. Brand iPOS — màu cam chủ đạo `#F26522`
- Trên `<html>` đặt `data-theme="light"`.
- Override biến DaisyUI + cấu hình Tailwind inline (Play CDN không nạp được plugin ngoài):
```html
<script>
  tailwind.config = {
    theme: { extend: { colors: {
      brand: '#F26522', 'brand-dark': '#D9531A', 'brand-bg': '#FFF7F2',
      ipos: '#0067B1', 'ipos-dark': '#00528C', 'ipos-bg': '#E7F1FA'
    } } }
  }
</script>
<style>
  [data-theme="light"] {
    --p: 19 89% 54%;   /* primary = #F26522 (HSL) */
    --pf: 19 89% 46%;  /* primary focus (đậm hơn) */
    --pc: 0 0% 100%;   /* chữ trên primary = trắng */
  }
  html, body { font-family: 'Be Vietnam Pro', sans-serif; }
</style>
```
- Bảng màu: primary `#F26522`, đậm `#D9531A`, nền nhạt `#FFF7F2`, chữ đậm `#1F2937`.
- Dùng class DaisyUI `btn-primary`, `text-primary`, `bg-primary`… (đã ra màu cam) hoặc
  `text-brand` / `bg-brand` / `bg-brand-bg` cho trường hợp cần.

### 2b. Màu phụ chủ đạo — XANH iPOS `#0067B1`
- Cam (`brand`) và xanh dương (`ipos`) là **hai màu chủ đạo song hành** của iPOS.vn (theo logo).
- Dùng `text-ipos` / `bg-ipos` / `bg-ipos-bg` / `border-ipos` / `from-ipos` `to-ipos`.
- Quy ước: **cam = hành động chính & luồng khách**; **xanh = nhấn/secondary, dữ liệu (chart),
  thành công, khu vực chủ quán**. Gradient brand: `from-brand to-ipos`.

### 2c. Nền (background) — chống đơn điệu
- **Aurora** (trang khách + marketing): 2 quầng radial cam (góc trên-phải) + xanh (góc dưới-trái)
  trên `body`, `background-attachment: fixed`.
- **Lưới chấm** (app quản trị `/merchant` trừ index/onboarding): dot-grid 22px + 2 glow cam/xanh nhạt.
- Đặt trong `<style>` nhắm thẳng selector `body` (không cần đổi class trên thẻ `<body>`).

### 3. Font
Be Vietnam Pro (400/500/600/700) — hỗ trợ tiếng Việt tốt, áp dụng toàn trang.

### 4. Mobile-first (đặc biệt luồng end-user)
- Luôn có `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
- Luồng end-user: container `max-w-md mx-auto`, mặc định 1 cột, nút full-width.
- Merchant dashboard: cho phép mở rộng tới `lg`.

### 5. Component DaisyUI ưu tiên
`steps`, `card`, `input`, `select`, `btn`, `table`, `badge`, `avatar`, `navbar`, `stat`.

### 5b. Icon — dùng Lucide (không dùng emoji)
- Nhúng cuối `<body>`: `<script src="https://unpkg.com/lucide@latest"></script>`
- Dùng placeholder: `<i data-lucide="calendar" class="w-5 h-5"></i>` (class trên `<i>` được
  copy sang `<svg>`; màu theo `currentColor`, nét stroke mặc định).
- Gọi `lucide.createIcons()` sau khi DOM/nội dung động render xong.
- Map icon hay dùng: thương hiệu `utensils-crossed`; ngày `calendar`; giờ `clock`;
  khách `users`; vị trí `map-pin`; điện thoại `phone`; sao `star`; link `link`;
  QR `qr-code`; thành công `check` / `circle-check`; cài đặt `settings`; nhanh `zap`;
  thống kê `bar-chart-3`; xu hướng tăng `trending-up`; mũi tên `arrow-left` / `arrow-right`.

### 6. Truyền dữ liệu giữa các bước (Vanilla JS + sessionStorage)
- Key dùng chung: `booking` (JSON).
- `1-chon-gio.html`: lưu `{date, time, guests}`.
- `2-thong-tin.html`: onload đọc tóm tắt; submit merge thêm `{name, phone, note}`.
- `3-xac-nhan.html`: onload render tóm tắt **rồi `sessionStorage.clear()` ngay** (bắt buộc).
- Guard nhẹ: thiếu dữ liệu thì hiển thị mặc định, không để trang crash.

## Ngôn ngữ
Toàn bộ nội dung, label, dummy data bằng **tiếng Việt**.

## Phạm vi
Tĩnh/mock hoàn toàn — không build tool, không npm. Mở trực tiếp bằng trình duyệt (`file://`).
