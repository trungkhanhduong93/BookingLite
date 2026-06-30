import re

with open(r'merchant\onboarding.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_selector = '''<div class="join w-full shadow-sm">
              <button type="button" class="btn btn-outline border-base-300 join-item hover:bg-base-200 hover:text-base-content bg-base-100" id="btnMinus"><i data-lucide="minus" class="w-4 h-4"></i></button>
              <input id="branchCount" type="number" min="1" value="1" class="input input-bordered join-item w-full text-center font-bold text-lg focus:outline-none focus:border-brand focus:ring-1 focus:ring-brand" />
              <button type="button" class="btn btn-outline border-base-300 join-item hover:bg-base-200 hover:text-base-content bg-base-100" id="btnPlus"><i data-lucide="plus" class="w-4 h-4"></i></button>
            </div>'''

new_selector = '''<div class="flex items-center justify-between bg-base-200/50 p-2.5 rounded-2xl border border-base-200/60 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition-colors hover:bg-base-200/80">
              <button type="button" class="btn btn-circle btn-sm bg-white border-base-200 shadow-sm text-base-content hover:bg-base-100 hover:border-brand hover:text-brand hover:scale-105 transition-all" id="btnMinus">
                <i data-lucide="minus" class="w-4 h-4"></i>
              </button>
              <div class="flex-1 flex justify-center">
                <input id="branchCount" type="number" min="1" value="1" class="w-20 text-center font-extrabold text-2xl bg-transparent border-0 focus:ring-0 text-base-content p-0" style="-moz-appearance: textfield;" />
              </div>
              <button type="button" class="btn btn-circle btn-sm bg-white border-base-200 shadow-sm text-base-content hover:bg-base-100 hover:border-brand hover:text-brand hover:scale-105 transition-all" id="btnPlus">
                <i data-lucide="plus" class="w-4 h-4"></i>
              </button>
            </div>
            <style>
              input[type=number]::-webkit-inner-spin-button, 
              input[type=number]::-webkit-outer-spin-button { 
                -webkit-appearance: none; 
                margin: 0; 
              }
            </style>'''

html = html.replace(old_selector, new_selector)

with open(r'merchant\onboarding.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated onboarding.html style")
