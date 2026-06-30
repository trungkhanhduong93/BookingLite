import os
import glob
import re

html_files = glob.glob('merchant/*.html')

old_block = r'''          <div class="mt-3 flex items-center gap-2 bg-brand-bg rounded-lg p-2">
            <div class="avatar placeholder"><div class="bg-brand text-white rounded-lg w-9"><span class="text-sm">TQ</span></div></div>
            <div class="leading-tight"><p class="text-sm font-semibold">Trum Quán</p><p class="text-[11px] text-base-content/50">Gói Pro · TP.HCM</p></div>
          </div>'''

new_block = '''          <div class="mt-3 relative">
            <details class="dropdown w-full group">
              <summary class="flex items-center gap-2 bg-brand-bg hover:bg-orange-100 rounded-lg p-2 transition-colors cursor-pointer list-none [&::-webkit-details-marker]:hidden border border-transparent group-open:border-brand/30 group-open:ring-2 group-open:ring-brand/10 group-open:bg-orange-50">
                <div class="avatar placeholder shrink-0"><div class="bg-brand shadow-sm text-white rounded-lg w-9"><span class="text-sm font-bold">TQ</span></div></div>
                <div class="leading-tight flex-1 min-w-0">
                  <p class="text-sm font-bold text-brand truncate">Trum Quán 1</p>
                  <p class="text-[11px] text-base-content/50 truncate">Gói Pro · Quận 5</p>
                </div>
                <i data-lucide="chevrons-up-down" class="w-4 h-4 text-brand/50 shrink-0 transition-transform group-open:rotate-180"></i>
              </summary>
              <ul class="dropdown-content menu z-[100] p-1.5 bg-base-100/95 backdrop-blur-xl rounded-xl border border-base-200 w-full mt-2 font-medium shadow-xl">
                <li>
                  <a class="flex items-center justify-between px-3 py-2.5 rounded-lg bg-orange-50 text-brand hover:bg-orange-100 transition-colors cursor-pointer mb-1">
                    <div class="flex items-center gap-2">
                      <div class="w-6 h-6 rounded-md bg-brand shadow-sm text-white flex items-center justify-center text-[10px] font-bold shrink-0">TQ</div>
                      <span class="truncate">Trum Quán 1</span>
                    </div>
                    <i data-lucide="check" class="w-4 h-4 shrink-0"></i>
                  </a>
                </li>
                <li>
                  <a class="flex items-center px-3 py-2.5 rounded-lg hover:bg-base-200/50 hover:text-base-content transition-colors cursor-pointer text-base-content/70">
                    <div class="flex items-center gap-2">
                      <div class="w-6 h-6 rounded-md bg-base-300 shadow-sm text-base-content/60 flex items-center justify-center text-[10px] font-bold shrink-0">TQ</div>
                      <span class="truncate">Trum Quán 2</span>
                    </div>
                  </a>
                </li>
              </ul>
            </details>
          </div>'''

files_changed = 0
for filepath in html_files:
    if filepath.endswith('onboarding.html'):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_block in content:
        new_content = content.replace(old_block, new_block)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
        files_changed += 1
    else:
        print(f"Skipped {filepath} (block not found)")

print(f"Total files updated: {files_changed}")
