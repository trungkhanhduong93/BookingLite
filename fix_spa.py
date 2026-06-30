import re

with open(r'merchant\spa.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add applyDemoBranchData() to updateDOM inside spa.js
old_update_dom = '''            if (window.lucide) window.lucide.createIcons();
            window.scrollTo(0, 0);
        };'''
new_update_dom = '''            if (window.lucide) window.lucide.createIcons();
            if (typeof applyDemoBranchData === 'function') applyDemoBranchData();
            window.scrollTo(0, 0);
        };'''

if old_update_dom in js:
    js = js.replace(old_update_dom, new_update_dom)
else:
    print("Warning: old updateDOM not found in spa.js")


demo_script = '''
// Demo Branch Switching Logic
function applyDemoBranchData() {
    const urlParams = new URLSearchParams(window.location.search);
    const branch = urlParams.get('branch');
    
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

    if (branch === '2') {
        if (activeName) activeName.textContent = 'Trum Quán 2';
        if (activeAddress) activeAddress.textContent = 'Demo Plan · Quận 1';
        
        // Update stats randomly for demo
        const statCards = document.querySelectorAll('.card-body .text-2xl.font-bold');
        if (statCards.length >= 4) {
            statCards[0].textContent = '12'; // Booking
            statCards[1].textContent = '45'; // Khách
            statCards[2].textContent = '2'; // Hủy
            statCards[3].textContent = '12,5M'; // Doanh thu
        }
        
        // Update recent booking table
        const tableRows = document.querySelectorAll('tbody tr');
        if (tableRows.length > 0) {
            tableRows.forEach((tr, i) => {
                const nameCell = tr.querySelector('td:first-child .font-bold');
                if (nameCell) nameCell.textContent = ['Lê Văn Đạt', 'Phạm Quỳnh Như', 'Nguyễn Hữu Tài', 'Trần Anh Tuấn'][i % 4];
            });
        }
    } else {
        if (activeName) activeName.textContent = 'Trum Quán 1';
        if (activeAddress) activeAddress.textContent = 'Gói Pro · Quận 5';
        
        const statCards = document.querySelectorAll('.card-body .text-2xl.font-bold');
        if (statCards.length >= 4) {
            statCards[0].textContent = '8';
            statCards[1].textContent = '34';
            statCards[2].textContent = '0';
            statCards[3].textContent = '8,4M';
        }
    }
}

document.addEventListener('DOMContentLoaded', applyDemoBranchData);

// Intercept branch link clicks
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
'''

with open(r'merchant\spa.js', 'w', encoding='utf-8') as f:
    f.write(js + demo_script)

print("Updated spa.js")
