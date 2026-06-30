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
