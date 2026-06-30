// SPA Router for Premium Zero-Latency View Transitions
document.addEventListener('click', async (e) => {
    const a = e.target.closest('a.navlink');
    if (!a || !a.href || a.getAttribute('target') === '_blank' || a.href.includes('javascript:')) return;
    if (!a.href.endsWith('.html') && !a.href.includes('/merchant/')) return;
    
    e.preventDefault();
    if (a.classList.contains('active')) return;
    
    const currentActive = document.querySelector('.navlink.active');
    
    try {
        const res = await fetch(a.href);
        const html = await res.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        
        const updateDOM = () => {
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
        
        history.pushState({}, '', a.href);
    } catch(err) {
        window.location.href = a.href;
    }
});

window.addEventListener('popstate', () => window.location.reload());


// Demo Branch Switching Logic
function applyDemoBranchData() {
    const urlParams = new URLSearchParams(window.location.search);
    const branch = urlParams.get('branch');
    const isBranch2 = (branch === '2');
    
    // 1. Update Dropdown and Topbar
    const activeName = document.getElementById('activeBranchName');
    const activeAddress = document.getElementById('activeBranchAddress');
    
    const links = document.querySelectorAll('.branch-link');
    links.forEach(link => {
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

    if (isBranch2) {
        if (activeName) activeName.textContent = 'Trum Quán 2';
        if (activeAddress) activeAddress.textContent = 'Demo Plan · Quận 1';
    } else {
        if (activeName) activeName.textContent = 'Trum Quán 1';
        if (activeAddress) activeAddress.textContent = 'Gói Pro · Quận 5';
    }

    // Determine current page
    const path = window.location.pathname;

    // --- DASHBOARD (index.html / dashboard.html) ---
    if (path.includes('dashboard.html') || path.endsWith('merchant/') || path.endsWith('merchant/index.html')) {
        const statCards = document.querySelectorAll('.card-body .text-2xl.font-bold');
        if (statCards.length >= 4) {
            statCards[0].textContent = isBranch2 ? '12' : '8';
            statCards[1].textContent = isBranch2 ? '45' : '34';
            statCards[2].textContent = isBranch2 ? '2' : '0';
            statCards[3].textContent = isBranch2 ? '12,5M' : '8,4M';
        }
        
        const tableRows = document.querySelectorAll('tbody tr');
        if (tableRows.length > 0) {
            tableRows.forEach((tr, i) => {
                const nameCell = tr.querySelector('td:first-child .font-bold');
                if (nameCell) {
                    nameCell.textContent = isBranch2 
                        ? ['Lê Văn Đạt', 'Phạm Quỳnh Như', 'Nguyễn Hữu Tài', 'Trần Anh Tuấn'][i % 4]
                        : ['Trần Thu Hà', 'Lê Khắc Thái', 'Nguyễn Minh Anh'][i % 3];
                }
            });
        }
    }

    // --- BÁO CÁO (bao-cao.html) ---
    if (path.includes('bao-cao.html')) {
        const statCards = document.querySelectorAll('.card-body .text-2xl.font-bold');
        if (statCards.length >= 4) {
            statCards[0].textContent = isBranch2 ? '425' : '312'; // Lượt đặt
            statCards[1].textContent = isBranch2 ? '2.314' : '1.142'; // Khách
            statCards[2].textContent = isBranch2 ? '4,2%' : '6,4%'; // No-show
            statCards[3].textContent = isBranch2 ? '85%' : '71%'; // Lấp đầy
        }
        const donutText = document.querySelector('.radial-progress .text-2xl');
        if (donutText) donutText.textContent = isBranch2 ? '88%' : '72%';
        const radial = document.querySelector('.radial-progress');
        if(radial) radial.style.setProperty('--value', isBranch2 ? 88 : 72);
    }

    // --- KHÁCH HÀNG (khach-hang.html) ---
    if (path.includes('khach-hang.html')) {
        const h1 = document.querySelector('h1.text-xl.font-bold');
        if (h1 && h1.innerHTML.includes('Khách hàng')) {
            const countText = h1.nextElementSibling;
            if (countText) countText.textContent = isBranch2 ? '5,102 khách' : '1,248 khách';
        }
        const tableRows = document.querySelectorAll('tbody tr');
        if (tableRows.length > 0) {
            tableRows.forEach((tr, i) => {
                const nameCell = tr.querySelector('td:first-child .font-bold');
                if (nameCell) {
                    nameCell.textContent = isBranch2 
                        ? ['Hoàng Thùy Linh', 'Đinh Tiến Đạt', 'Vũ Cát Tường', 'Sơn Tùng M-TP', 'Bích Phương'][i % 5]
                        : ['Nguyễn Văn A', 'Trần Thị B', 'Lê Khắc Thái'][i % 3];
                }
            });
        }
    }

    // --- LỊCH (lich.html / booking-detail.html) ---
    if (path.includes('lich.html')) {
        const slots = document.querySelectorAll('.card-body .font-medium');
        if (slots.length > 0) {
            slots.forEach((el, i) => {
                if (el.textContent.includes('người')) {
                    const count = parseInt(el.textContent) + (isBranch2 ? 3 : 0);
                    el.textContent = `${count} người`;
                }
            });
        }
    }

    // --- CÀI ĐẶT (cai-dat.html) ---
    if (path.includes('cai-dat.html')) {
        const inputs = document.querySelectorAll('main input.input-bordered');
        if (inputs.length >= 4) {
            inputs[0].value = isBranch2 ? 'Nhà hàng Trum Quán 2' : 'Nhà hàng Trum Quán 1';
            inputs[1].value = isBranch2 ? '123 Nguyễn Văn Cừ, Quận 1, TP.HCM' : '77 Trần Nhân Tôn, Phường An Đông, TP.HCM';
            inputs[2].value = isBranch2 ? '1900 4766 Nhánh 2' : '1900 4766 Nhánh 3';
            inputs[3].value = isBranch2 ? '15' : '20';
        }
    }
}

document.addEventListener('DOMContentLoaded', applyDemoBranchData);

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
                if(dropdown) dropdown.removeAttribute('open');
            });
        } else {
            applyDemoBranchData();
            const dropdown = document.getElementById('branchDropdown');
            if(dropdown) dropdown.removeAttribute('open');
        }
    }
});
