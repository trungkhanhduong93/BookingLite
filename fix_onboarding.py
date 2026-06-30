import re

with open(r'merchant\onboarding.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the branch selection buttons with input
old_selector = '''          <!-- Multi-branch selection -->
          <div class="mb-1">
            <label class="label p-0 pb-2"><span class="label-text font-bold text-base-content inline-flex items-center gap-1.5"><i data-lucide="network" class="w-4 h-4 text-brand"></i> Bạn có bao nhiêu chi nhánh?</span></label>
            <div class="flex gap-2 p-1 bg-base-200 rounded-xl">
              <button type="button" id="btnBranch1" class="btn btn-sm flex-1 bg-base-100 border-base-100 shadow-sm text-brand font-bold">1 Chi nhánh</button>
              <button type="button" id="btnBranch2" class="btn btn-sm flex-1 btn-ghost text-base-content/60 font-medium hover:text-brand">2 Chi nhánh</button>
            </div>
          </div>'''

new_selector = '''          <!-- Multi-branch selection -->
          <div class="mb-1">
            <label class="label p-0 pb-2"><span class="label-text font-bold text-base-content inline-flex items-center gap-1.5"><i data-lucide="network" class="w-4 h-4 text-brand"></i> Bạn có bao nhiêu chi nhánh?</span></label>
            <div class="join w-full shadow-sm">
              <button type="button" class="btn btn-outline border-base-300 join-item hover:bg-base-200 hover:text-base-content bg-base-100" id="btnMinus"><i data-lucide="minus" class="w-4 h-4"></i></button>
              <input id="branchCount" type="number" min="1" value="1" class="input input-bordered join-item w-full text-center font-bold text-lg focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand" />
              <button type="button" class="btn btn-outline border-base-300 join-item hover:bg-base-200 hover:text-base-content bg-base-100" id="btnPlus"><i data-lucide="plus" class="w-4 h-4"></i></button>
            </div>
          </div>'''

html = html.replace(old_selector, new_selector)

# Insert the dynamic branch container after Branch 2 section
b2_section = '''          <!-- Branch 2 Section -->
          <div id="branch2Section" class="space-y-4 hidden mt-2 pt-5 border-t border-dashed border-base-300">
            <div class="badge bg-brand/10 text-brand border-0 font-bold gap-1"><i data-lucide="store" class="w-3 h-3"></i> Chi nhánh 2</div>
            <div>
              <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Tên quán *</span></label>
              <input type="text" value="Nhà hàng Trum Quán 2" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand b2-input" />
            </div>

            <div>
              <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Địa chỉ *</span></label>
              <input type="text" value="123 Nguyễn Văn Cừ, Phường Cầu Kho, Quận 1, TP.HCM" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand b2-input" />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Điện thoại *</span></label>
                <input type="tel" value="1900 4766 Nhánh 2" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand b2-input" />
              </div>
              <div>
                <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Số bàn</span></label>
                <input type="number" min="1" value="15" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand b2-input" />
              </div>
            </div>
          </div>'''

b2_replacement = b2_section + '''

          <!-- Dynamic Branches Container -->
          <div id="dynamicBranches"></div>'''

html = html.replace(b2_section, b2_replacement)


# We need to add a modal to HTML body (before scripts)
modal_html = '''
    <!-- Demo Modal -->
    <dialog id="demoModal" class="modal modal-bottom sm:modal-middle">
      <div class="modal-box bg-base-100 rounded-t-[2rem] sm:rounded-2xl z-[9999]">
        <div class="w-16 h-16 rounded-full bg-warning/15 flex items-center justify-center text-warning mx-auto mb-4">
          <i data-lucide="alert-triangle" class="w-8 h-8"></i>
        </div>
        <h3 class="font-bold text-lg text-center">Giới hạn bản Demo</h3>
        <p class="py-4 text-center text-base-content/70">Đây là App demo, vui lòng chọn 1 hoặc 2 chi nhánh để tiếp tục.</p>
        <div class="modal-action justify-center">
          <form method="dialog" class="w-full">
            <button class="btn btn-primary btn-block">Đã hiểu</button>
          </form>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
'''
html = html.replace('  <script src="spa.js"></script>', modal_html + '\n  <script src="spa.js"></script>')

# Update script logic
old_script = '''    <script>
      const btn1 = document.getElementById('btnBranch1');
      const btn2 = document.getElementById('btnBranch2');
      const b2Section = document.getElementById('branch2Section');
      const b2Inputs = document.querySelectorAll('.b2-input');
      
      btn1.addEventListener('click', () => {
        btn1.className = 'btn btn-sm flex-1 bg-base-100 border-base-100 shadow-sm text-brand font-bold';
        btn2.className = 'btn btn-sm flex-1 btn-ghost text-base-content/60 font-medium hover:text-brand';
        b2Section.classList.add('hidden');
        b2Inputs.forEach(i => i.removeAttribute('required'));
      });
      
      btn2.addEventListener('click', () => {
        btn2.className = 'btn btn-sm flex-1 bg-base-100 border-base-100 shadow-sm text-brand font-bold';
        btn1.className = 'btn btn-sm flex-1 btn-ghost text-base-content/60 font-medium hover:text-brand';
        b2Section.classList.remove('hidden');
        b2Inputs.forEach(i => i.setAttribute('required', 'true'));
      });
    </script>'''

new_script = '''    <script>
      const branchCountInput = document.getElementById('branchCount');
      const btnMinus = document.getElementById('btnMinus');
      const btnPlus = document.getElementById('btnPlus');
      const b2Section = document.getElementById('branch2Section');
      const b2Inputs = document.querySelectorAll('.b2-input');
      const dynamicBranches = document.getElementById('dynamicBranches');
      
      function renderBranches() {
        const count = parseInt(branchCountInput.value) || 1;
        
        // Show/hide branch 2
        if (count >= 2) {
          b2Section.classList.remove('hidden');
          b2Inputs.forEach(i => i.setAttribute('required', 'true'));
        } else {
          b2Section.classList.add('hidden');
          b2Inputs.forEach(i => i.removeAttribute('required'));
        }
        
        // Render branch 3+
        dynamicBranches.innerHTML = '';
        for (let i = 3; i <= count; i++) {
          dynamicBranches.innerHTML += `
            <div class="space-y-4 mt-2 pt-5 border-t border-dashed border-base-300">
              <div class="badge bg-base-200 text-base-content/70 border-0 font-bold gap-1"><i data-lucide="store" class="w-3 h-3"></i> Chi nhánh ${i}</div>
              <div>
                <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Tên quán *</span></label>
                <input type="text" placeholder="Nhập tên quán" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
              </div>
              <div>
                <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Địa chỉ *</span></label>
                <input type="text" placeholder="Nhập địa chỉ" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Điện thoại *</span></label>
                  <input type="tel" placeholder="Nhập SĐT" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
                </div>
                <div>
                  <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Số bàn</span></label>
                  <input type="number" min="1" placeholder="Số bàn" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
                </div>
              </div>
            </div>
          `;
        }
        lucide.createIcons();
      }
      
      btnMinus.addEventListener('click', () => {
        let val = parseInt(branchCountInput.value) || 1;
        if (val > 1) {
          branchCountInput.value = val - 1;
          renderBranches();
        }
      });
      
      btnPlus.addEventListener('click', () => {
        let val = parseInt(branchCountInput.value) || 1;
        branchCountInput.value = val + 1;
        renderBranches();
      });
      
      branchCountInput.addEventListener('change', () => {
        let val = parseInt(branchCountInput.value) || 1;
        if (val < 1) val = 1;
        branchCountInput.value = val;
        renderBranches();
      });
    </script>'''
html = html.replace(old_script, new_script)

# Also need to intercept form submission if branchCount > 2
# Let's read the main script tag
old_submit = '''    document.getElementById('form').addEventListener('submit', function(e) {
      e.preventDefault();'''
new_submit = '''    document.getElementById('form').addEventListener('submit', function(e) {
      e.preventDefault();
      
      const count = parseInt(document.getElementById('branchCount').value) || 1;
      if (count > 2) {
        document.getElementById('demoModal').showModal();
        return;
      }
'''
html = html.replace(old_submit, new_submit)

with open(r'merchant\onboarding.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated onboarding.html")
