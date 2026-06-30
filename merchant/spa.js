// SPA Router for Premium Zero-Latency View Transitions
document.addEventListener('click', async (e) => {
    const a = e.target.closest('a.navlink');
    if (!a || !a.href || a.getAttribute('target') === '_blank' || a.href.includes('javascript:')) return;
    if (!a.href.endsWith('.html') && !a.href.includes('/merchant/')) return;

    e.preventDefault();
    if (a.classList.contains('active')) return;

    const currentActive = document.querySelector('.navlink.active');

    // Giữ chi nhánh đang chọn khi điều hướng (FIX: trước đây mất ?branch khi qua menu khác)
    const targetUrl = new URL(a.href, window.location.href);
    const curBranch = new URLSearchParams(window.location.search).get('branch');
    if (curBranch) targetUrl.searchParams.set('branch', curBranch);

    try {
        const res = await fetch(a.href);
        const html = await res.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');

        const updateDOM = () => {
            // Cập nhật URL TRƯỚC (kèm ?branch) để applyDemoBranchData đọc đúng trang + chi nhánh
            history.pushState({}, '', targetUrl.href);
            document.title = doc.title;

            const currentContent = document.querySelector('.drawer-content');
            const newContent = doc.querySelector('.drawer-content');
            if (currentContent && newContent) {
                currentContent.innerHTML = newContent.innerHTML;
                currentContent.className = newContent.className;
            } else {
                const currentMain = document.querySelector('main');
                const newMain = doc.querySelector('main');
                if (currentMain && newMain) {
                    currentMain.innerHTML = newMain.innerHTML;
                    currentMain.className = newMain.className;
                }
            }

            if (currentActive) currentActive.classList.remove('active');
            const hrefAttr = a.getAttribute('href').split('/').pop() || a.getAttribute('href');
            const newActive = document.querySelector(`.navlink[href$="${hrefAttr}"]`);
            if (newActive) newActive.classList.add('active');

            const scripts = doc.querySelectorAll('script:not([src])');
            scripts.forEach(s => {
                if (s.textContent.includes('lucide.createIcons()') && s.textContent.trim().length < 100) return;
                const newScript = document.createElement('script');
                newScript.textContent = `(() => { ${s.textContent} })();`;
                document.body.appendChild(newScript);
                document.body.removeChild(newScript);
            });

            if (window.lucide) window.lucide.createIcons();
            if (typeof applyDemoBranchData === 'function') applyDemoBranchData();
            window.scrollTo(0, 0);
        };

        if (document.startViewTransition) {
            document.startViewTransition(updateDOM);
        } else {
            updateDOM();
        }
    } catch(err) {
        window.location.href = a.href;
    }
});

window.addEventListener('popstate', () => window.location.reload());


// ====== Demo Branch Switching Logic (viết lại khớp markup thực tế) ======
const BRANCH_NAME_MAP = {
    'Trần Thu Hà': 'Sơn Tùng M-TP', 'Nguyễn Văn Minh': 'Hoàng Thuỳ Linh', 'Lê Hoàng Anh': 'Đen Vâu',
    'Phạm Thị Lan': 'Mỹ Tâm', 'Vũ Đức Thắng': 'Trấn Thành', 'Đỗ Quỳnh Chi': 'Hồ Ngọc Hà',
    'Hoàng Nam': 'Hà Anh Tuấn', 'Bùi Khánh Linh': 'Bích Phương'
};
const BRANCH_NAME_REVERSE = Object.fromEntries(Object.entries(BRANCH_NAME_MAP).map(([k, v]) => [v, k]));

// Đổi giá trị KPI theo nhãn của thẻ (bền vững với mọi markup card-body)
function setStatByLabel(label, value) {
    document.querySelectorAll('main .card-body').forEach(cb => {
        const lab = cb.querySelector('span');
        if (lab && lab.textContent.trim().toLowerCase().startsWith(label.toLowerCase())) {
            const v = cb.querySelector('.text-2xl');
            if (v) v.textContent = value;
        }
    });
}
// Đổi tên khách 2 chiều (qua/lại chi nhánh đều đúng)
function renameBranch(isB2) {
    const map = isB2 ? BRANCH_NAME_MAP : BRANCH_NAME_REVERSE;
    document.querySelectorAll('main h3, main .font-medium, main .font-semibold').forEach(el => {
        const t = el.textContent.trim();
        if (map[t]) el.textContent = map[t];
    });
}

function applyDemoBranchData() {
    const branch = new URLSearchParams(window.location.search).get('branch');
    const isBranch2 = (branch === '2');

    // 1. Dropdown chi nhánh + topbar
    const activeName = document.getElementById('activeBranchName');
    const activeAddress = document.getElementById('activeBranchAddress');
    document.querySelectorAll('.branch-link').forEach(link => {
        link.classList.remove('bg-orange-50', 'text-brand', 'font-bold');
        link.classList.add('hover:bg-base-200/50', 'text-base-content/70');
        const icon = link.querySelector('.check-icon');
        if (icon) icon.classList.add('hidden');
        if (link.dataset.branch === branch || (!branch && link.dataset.branch === '1')) {
            link.classList.add('bg-orange-50', 'text-brand', 'font-bold');
            link.classList.remove('hover:bg-base-200/50', 'text-base-content/70');
            if (icon) icon.classList.remove('hidden');
        }
    });
    if (activeName) activeName.textContent = isBranch2 ? 'Trum Quán 2' : 'Trum Quán 1';
    if (activeAddress) activeAddress.textContent = isBranch2 ? 'Demo Plan · Quận 1' : 'Gói Pro · Quận 5';

    const path = window.location.pathname;

    // --- TỔNG QUAN (dashboard) ---
    if (path.includes('dashboard.html') || path.endsWith('merchant/') || path.endsWith('merchant/index.html')) {
        setStatByLabel('Booking', isBranch2 ? '12' : '8');
        setStatByLabel('Tổng khách', isBranch2 ? '45' : '34');
        setStatByLabel('Tỉ lệ lấp đầy', isBranch2 ? '88%' : '75%');
        setStatByLabel('Chờ xác nhận', isBranch2 ? '5' : '3');
        renameBranch(isBranch2);
    }

    // --- BÁO CÁO ---
    if (path.includes('bao-cao.html')) {
        setStatByLabel('Tổng lượt', isBranch2 ? '425' : '312');
        setStatByLabel('Khách phục vụ', isBranch2 ? '2.314' : '1.142');
        setStatByLabel('Tỉ lệ no-show', isBranch2 ? '4,2%' : '6,4%');
        setStatByLabel('Lấp đầy', isBranch2 ? '85%' : '71%');
        const radial = document.querySelector('.radial-progress');
        if (radial) {
            radial.style.setProperty('--value', isBranch2 ? 88 : 72);
            const dt = radial.querySelector('.text-2xl');
            if (dt) dt.textContent = isBranch2 ? '88%' : '72%';
        }
    }

    // --- KHÁCH HÀNG ---
    if (path.includes('khach-hang.html')) {
        setStatByLabel('Tổng khách hàng', isBranch2 ? '5.102' : '1.284');
        setStatByLabel('Khách VIP', isBranch2 ? '214' : '96');
        setStatByLabel('Tỉ lệ quay lại', isBranch2 ? '53%' : '42%');
        renameBranch(isBranch2);
    }

    // --- LỊCH ---
    if (path.includes('lich.html')) {
        document.querySelectorAll('main p').forEach(p => {
            if (/\d+\s*đơn/.test(p.textContent)) p.textContent = isBranch2 ? '12 đơn · 45 khách' : '8 đơn · 34 khách';
        });
        renameBranch(isBranch2);
    }

    // --- SƠ ĐỒ BÀN ---
    if (path.includes('ban.html')) {
        const counts = document.querySelectorAll('main .badge b');
        if (counts.length >= 3) {
            counts[0].textContent = isBranch2 ? '2' : '5';
            counts[1].textContent = isBranch2 ? '14' : '9';
            counts[2].textContent = isBranch2 ? '4' : '6';
        }
    }

    // --- CÀI ĐẶT ---
    if (path.includes('cai-dat.html')) {
        const inputs = document.querySelectorAll('main input.input-bordered');
        if (inputs.length >= 4) {
            inputs[0].value = isBranch2 ? 'Nhà hàng Trum Quán 2' : 'Nhà hàng Trum Quán';
            inputs[1].value = isBranch2 ? '123 Nguyễn Văn Cừ, Quận 1, TP.HCM' : '77 Trần Nhân Tôn, Phường An Đông, TP.HCM';
            inputs[2].value = isBranch2 ? '1900 4766 Nhánh 2' : '1900 4766 Nhánh 3';
            inputs[3].value = isBranch2 ? '15' : '20';
        }
    }
}

document.addEventListener('DOMContentLoaded', applyDemoBranchData);

// Bấm chuyển chi nhánh ngay trên trang hiện tại (không reload)
document.addEventListener('click', (e) => {
    const link = e.target.closest('.branch-link');
    if (link) {
        e.preventDefault();
        const branch = link.dataset.branch;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('branch', branch);
        history.pushState({}, '', currentUrl);

        if (document.startViewTransition) {
            document.startViewTransition(() => {
                applyDemoBranchData();
                const dropdown = document.getElementById('branchDropdown');
                if (dropdown) dropdown.removeAttribute('open');
            });
        } else {
            applyDemoBranchData();
            const dropdown = document.getElementById('branchDropdown');
            if (dropdown) dropdown.removeAttribute('open');
        }
    }
});
