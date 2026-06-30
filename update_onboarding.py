import re

with open(r'merchant\onboarding.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will replace the form contents
old_form = '''      <form id="form" class="card bg-base-100 shadow-sm border border-base-200">
        <div class="card-body gap-4">
          <div>
            <label class="label"><span class="label-text font-medium inline-flex items-center gap-1.5"><i data-lucide="store" class="w-4 h-4 text-brand"></i> Tên quán *</span></label>
            <input id="shopName" type="text" required value="Nhà hàng Trum Quán" class="input input-bordered w-full" />
          </div>

          <div>
            <label class="label"><span class="label-text font-medium inline-flex items-center gap-1.5"><i data-lucide="tag" class="w-4 h-4 text-brand"></i> Loại hình</span></label>
            <div class="dropdown w-full">
              <div tabindex="0" role="button" class="btn btn-outline border-base-300 hover:border-brand hover:bg-brand-bg hover:text-base-content w-full justify-between font-normal">
                <span id="typeLabel">Nhà hàng</span>
                <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
              </div>
              <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[20] w-full p-2 shadow-lg border border-base-200 mt-1">
                <li><a data-val="Nhà hàng" class="active">Nhà hàng</a></li>
                <li><a data-val="Quán cà phê">Quán cà phê</a></li>
                <li><a data-val="Quán ăn / Bistro">Quán ăn / Bistro</a></li>
                <li><a data-val="Lẩu / Nướng">Lẩu / Nướng</a></li>
                <li><a data-val="Bar / Pub">Bar / Pub</a></li>
                <li><a data-val="Khác">Khác</a></li>
              </ul>
            </div>
            <input type="hidden" id="type" value="Nhà hàng">
          </div>

          <div>
            <label class="label"><span class="label-text font-medium inline-flex items-center gap-1.5"><i data-lucide="map-pin" class="w-4 h-4 text-brand"></i> Địa chỉ *</span></label>
            <input id="address" type="text" required value="77 Trần Nhân Tôn, Phường An Đông, TP.HCM" class="input input-bordered w-full" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="label"><span class="label-text font-medium inline-flex items-center gap-1.5"><i data-lucide="phone" class="w-4 h-4 text-brand"></i> Điện thoại *</span></label>
              <input id="phone" type="tel" required value="1900 4766 Nhánh 3" class="input input-bordered w-full" />
            </div>
            <div>
              <label class="label"><span class="label-text font-medium inline-flex items-center gap-1.5"><i data-lucide="armchair" class="w-4 h-4 text-brand"></i> Số bàn</span></label>
              <input id="tables" type="number" min="1" value="20" class="input input-bordered w-full" />
            </div>
          </div>

          <button type="submit" class="btn btn-primary btn-block btn-lg mt-2 gap-1">Tạo quán & lấy link <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
        </div>
      </form>'''

new_form = '''      <form id="form" class="card bg-base-100 shadow-sm border border-base-200">
        <div class="card-body gap-4">
          <!-- Multi-branch selection -->
          <div class="mb-1">
            <label class="label p-0 pb-2"><span class="label-text font-bold text-base-content inline-flex items-center gap-1.5"><i data-lucide="network" class="w-4 h-4 text-brand"></i> Bạn có bao nhiêu chi nhánh?</span></label>
            <div class="flex gap-2 p-1 bg-base-200 rounded-xl">
              <button type="button" id="btnBranch1" class="btn btn-sm flex-1 bg-base-100 border-base-100 shadow-sm text-brand font-bold">1 Chi nhánh</button>
              <button type="button" id="btnBranch2" class="btn btn-sm flex-1 btn-ghost text-base-content/60 font-medium hover:text-brand">2 Chi nhánh</button>
            </div>
          </div>
          
          <div class="divider my-0 opacity-50"></div>

          <!-- Branch 1 Section -->
          <div id="branch1Section" class="space-y-4">
            <div class="badge bg-brand/10 text-brand border-0 font-bold gap-1"><i data-lucide="store" class="w-3 h-3"></i> Chi nhánh 1</div>
            <div>
              <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Tên quán *</span></label>
              <input id="shopName" type="text" required value="Nhà hàng Trum Quán 1" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
            </div>

            <div>
              <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Loại hình</span></label>
              <div class="dropdown w-full">
                <div tabindex="0" role="button" class="btn btn-outline border-base-300 hover:border-brand hover:bg-brand-bg hover:text-base-content w-full justify-between font-normal">
                  <span id="typeLabel">Nhà hàng</span>
                  <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
                </div>
                <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[20] w-full p-2 shadow-lg border border-base-200 mt-1">
                  <li><a data-val="Nhà hàng" class="active">Nhà hàng</a></li>
                  <li><a data-val="Quán cà phê">Quán cà phê</a></li>
                  <li><a data-val="Quán ăn / Bistro">Quán ăn / Bistro</a></li>
                  <li><a data-val="Lẩu / Nướng">Lẩu / Nướng</a></li>
                  <li><a data-val="Bar / Pub">Bar / Pub</a></li>
                  <li><a data-val="Khác">Khác</a></li>
                </ul>
              </div>
              <input type="hidden" id="type" value="Nhà hàng">
            </div>

            <div>
              <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Địa chỉ *</span></label>
              <input id="address" type="text" required value="77 Trần Nhân Tôn, Phường An Đông, TP.HCM" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Điện thoại *</span></label>
                <input id="phone" type="tel" required value="1900 4766 Nhánh 1" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
              </div>
              <div>
                <label class="label p-0 pb-1.5"><span class="label-text font-medium text-base-content/80">Số bàn</span></label>
                <input id="tables" type="number" min="1" value="20" class="input input-bordered w-full focus:border-brand focus:ring-1 focus:ring-brand" />
              </div>
            </div>
          </div>

          <!-- Branch 2 Section -->
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
          </div>

          <button type="submit" class="btn btn-primary btn-block btn-lg mt-4 gap-2 shadow-lg shadow-brand/30">Tạo quán & lấy link <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
        </div>
      </form>'''

if old_form in html:
    html = html.replace(old_form, new_form)
else:
    print("Warning: old form not found in onboarding.html")

script_tag = '''    <script>
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
    </script>
  </body>'''

if '</body>' in html:
    html = html.replace('</body>', script_tag)

with open(r'merchant\onboarding.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated onboarding.html")
