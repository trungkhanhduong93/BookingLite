# Booking Lite — Prototype HTML tĩnh

SAAS giúp Merchant (quán ăn/cà phê) nhận đơn đặt bàn từ end-user.
Tiêu chí cốt lõi: **Onboarding siêu nhanh**. Đây là **prototype tĩnh** để demo ý tưởng
(không backend, dữ liệu là dummy/mock).

**Tác giả:** trung.duong (Trum)

## Cấu trúc

```
/index.html               # Trang chủ tổng — 2 lối vào (khách / chủ quán)
/end-user/
  index.html              # Trang quán "Nhà hàng Phố Cổ"
  1-chon-gio.html         # Step 1: chọn ngày, giờ, số khách
  2-thong-tin.html        # Step 2: thông tin liên hệ / login
  3-xac-nhan.html         # Step 3: xác nhận thành công (xoá sessionStorage)
/merchant/
  index.html              # Landing marketing + đăng nhập
  onboarding.html         # Nhập thông tin quán → nhận link đặt bàn
  dashboard.html          # Danh sách booking (table + stat)
```

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
      brand: '#F26522', 'brand-dark': '#D9531A', 'brand-bg': '#FFF7F2'
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
