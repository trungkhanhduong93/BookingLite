# Booking Lite — Kiến trúc sản phẩm (BA Design)

> Tài liệu phân tích nghiệp vụ cho SAAS **Booking Lite** — nền tảng giúp Merchant (quán
> ăn/cà phê/nhà hàng) nhận & quản lý đặt bàn online. Tiêu chí cốt lõi: **Onboarding siêu nhanh**.
> Tác giả: **trung.duong (Trum)**.

---

## 1. Tầm nhìn & nguyên tắc thiết kế

| Nguyên tắc | Diễn giải |
|---|---|
| **Onboarding < 2 phút** | Chủ quán nhập tối thiểu thông tin → có ngay link/QR nhận đặt bàn. |
| **Zero-install cho khách** | Khách đặt bàn qua link web, không cần tải app, không cần đăng ký. |
| **Mobile-first** | Luồng khách tối ưu điện thoại tuyệt đối; quản trị responsive tới desktop. |
| **Realtime-ish** | Trạng thái đơn cập nhật tức thì giữa khách ↔ quán (prototype: mock). |
| **Self-serve** | Quán tự cấu hình bàn, khung giờ, khuyến mãi mà không cần hỗ trợ. |

## 2. Tác nhân (Actors / Personas)

1. **End-user (Khách đặt bàn)** — đặt bàn, theo dõi, huỷ, đánh giá. Không cần tài khoản.
2. **Merchant Owner (Chủ quán)** — toàn quyền: cấu hình quán, xem báo cáo, quản lý nhân viên.
3. **Merchant Staff (Nhân viên/Lễ tân)** — xác nhận/sắp bàn, check-in khách (quyền giới hạn).
4. **System (Hệ thống)** — gửi thông báo (SMS/Zalo/email), nhắc lịch, tự huỷ đơn quá hạn.

## 3. Bản đồ tính năng (Module Map)

```
Booking Lite
├── A. KHÁCH (end-user, không đăng nhập)
│   ├── A1. Trang quán (hồ sơ, ảnh, đánh giá)           → end-user/index.html ✓
│   ├── A2. Thực đơn / Bảng giá                          → end-user/thuc-don.html ★
│   ├── A3. Đặt bàn 3 bước (giờ → thông tin → xác nhận)  → 1/2/3-*.html ✓
│   ├── A4. Tra cứu & theo dõi đơn (mã/SĐT)              → end-user/tra-cuu.html ★
│   ├── A5. Quản lý đơn (chi tiết, huỷ, đổi giờ)         → tra-cuu.html (chi tiết) ★
│   └── A6. Đánh giá sau khi dùng bữa                    → (roadmap P2)
│
├── B. CHỦ QUÁN (merchant app — có app-shell/sidebar)
│   ├── B0. Landing + Đăng nhập/Đăng ký                  → merchant/index.html ✓
│   ├── B1. Onboarding tạo quán                          → merchant/onboarding.html ✓
│   ├── B2. Tổng quan (Dashboard: KPI + đơn hôm nay)     → merchant/dashboard.html ✓↑
│   ├── B3. Lịch đặt bàn (ngày/tuần, theo khung giờ)     → merchant/lich.html ★
│   ├── B4. Sơ đồ bàn (floor map, trạng thái bàn)        → merchant/ban.html ★
│   ├── B5. Chi tiết đơn (xác nhận/huỷ/ghi chú/xếp bàn)  → merchant/booking-detail.html ★
│   ├── B6. Khách hàng (CRM: lịch sử, hạng, ghi chú)     → merchant/khach-hang.html ★
│   ├── B7. Báo cáo & phân tích (doanh thu, tỉ lệ no-show)→ merchant/bao-cao.html ★
│   ├── B8. Cài đặt quán (giờ, khung giờ, bàn, link/QR)  → merchant/cai-dat.html ★
│   ├── B9. Khuyến mãi / Marketing                       → (roadmap P2)
│   └── B10. Nhân viên & phân quyền                      → (roadmap P3)
│
└── C. HỆ THỐNG (mock trong prototype)
    ├── C1. Thông báo đa kênh (SMS/Zalo ZNS/email)
    ├── C2. Nhắc lịch trước giờ & nhắc xác nhận
    ├── C3. Tự huỷ đơn quá hạn / quản lý no-show
    └── C4. Đồng bộ realtime khách ↔ quán
```
> ✓ = đã có · ↑ = nâng cấp · ★ = màn hình mới trong bản này · (roadmap) = đặc tả, dựng sau.

## 4. Hành trình người dùng (Key User Journeys)

**J1 — Khách đặt bàn (happy path)**
`Trang quán → (xem Thực đơn) → Đặt bàn → Chọn ngày/giờ/số khách → Thông tin → Xác nhận
(nhận mã #BK) → SMS xác nhận → Tra cứu/theo dõi đơn`

**J2 — Khách huỷ/đổi giờ**
`Tra cứu (mã + SĐT) → Chi tiết đơn → Huỷ / Đổi giờ → cập nhật trạng thái`

**J3 — Chủ quán onboarding & vận hành**
`Landing → Đăng nhập → Onboarding (tạo quán) → nhận link/QR → Dashboard →
Lịch/Sơ đồ bàn → Chi tiết đơn (Xác nhận → Xếp bàn → Check-in → Hoàn tất)`

**J4 — Lễ tân xử lý đơn mới**
`Thông báo đơn mới → Dashboard/Lịch → Chi tiết đơn → Xác nhận & xếp bàn → (đến giờ) Check-in`

## 5. Mô hình dữ liệu (Entities — mức prototype)

```
Merchant      { id, tên, loại hình, địa chỉ, SĐT, slug, ảnh, giờ mở cửa, trạng thái }
Table (Bàn)   { id, merchantId, tên/số, sức chứa, khu vực, trạng thái(trống/đặt/đang dùng) }
TimeSlot      { merchantId, danh sách khung giờ, sức chứa mỗi khung }
Booking       { id(#BK), merchantId, customerId, ngày, giờ, số khách, bàn?, trạng thái,
                ghi chú, nguồn, mã giảm giá?, tạo lúc }
Customer      { id, tên, SĐT, email?, hạng(thường/VIP), tổng lượt, no-show, ghi chú }
Review        { id, bookingId, sao, nội dung, ngày }      // P2
Staff         { id, merchantId, tên, vai trò, quyền }      // P3
Notification  { id, bookingId, kênh, nội dung, trạng thái }
```
**Quan hệ:** Merchant 1—N Table · Merchant 1—N Booking · Customer 1—N Booking ·
Booking 0..1 Table · Booking 1—N Notification.

## 6. Máy trạng thái đơn đặt bàn (Booking State Machine)

```
[Chờ xác nhận] ──quán xác nhận──▶ [Đã xác nhận] ──đến giờ──▶ [Đã check-in] ──xong──▶ [Hoàn tất]
      │                                  │                          
      ├─ khách/quán huỷ ─▶ [Đã huỷ]      ├─ khách/quán huỷ ─▶ [Đã huỷ]
      └─ quá hạn tự huỷ ─▶ [Quá hạn]     └─ khách không đến ─▶ [No-show]
```
Màu badge: Chờ xác nhận = `warning` · Đã xác nhận = `info/primary` · Check-in = `accent` ·
Hoàn tất = `success` · Huỷ/No-show/Quá hạn = `ghost/error`.

## 7. Thông báo & tự động hoá (mock)

- Khách đặt → SMS/Zalo "Đã nhận yêu cầu" + mã đơn.
- Quán xác nhận → SMS "Đã giữ chỗ" kèm địa chỉ + nút chỉ đường.
- Trước giờ 2h → nhắc khách; trước 30' chưa xác nhận → nhắc quán.
- Quá giờ giữ chỗ 15' không check-in → cảnh báo no-show.

## 8. Lộ trình (Roadmap)

| Giai đoạn | Phạm vi |
|---|---|
| **MVP (bản này)** | A1–A5, B0–B8 (đặt bàn, tra cứu, dashboard, lịch, bàn, CRM, báo cáo, cài đặt). |
| **Phase 2** | A6 đánh giá, B9 khuyến mãi/voucher, đặt cọc online, đa chi nhánh. |
| **Phase 3** | B10 nhân viên & phân quyền, tích hợp POS iPOS, AI gợi ý khung giờ/giữ chỗ. |

## 9. Phi chức năng (prototype)

Tĩnh/mock hoàn toàn (không backend). Dữ liệu dummy + `sessionStorage`. Mục tiêu: trình diễn
luồng & chất lượng UI/UX. Khi lên thật: REST API + DB + realtime (WebSocket) + cổng SMS/Zalo ZNS.
