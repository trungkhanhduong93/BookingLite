import os
import glob
import re

html_files = glob.glob('merchant/*.html')

new_block = '''<details class="dropdown w-full group" id="branchDropdown">
              <summary class="flex items-center gap-2 bg-brand-bg hover:bg-orange-100 rounded-lg p-2 transition-colors cursor-pointer list-none [&::-webkit-details-marker]:hidden border border-transparent group-open:border-brand/30 group-open:ring-2 group-open:ring-brand/10 group-open:bg-orange-50">
                <div class="avatar placeholder shrink-0"><div id="activeBranchAvatar" class="bg-brand shadow-sm text-white rounded-lg w-9"><span class="text-sm font-bold">TQ</span></div></div>
                <div class="leading-tight flex-1 min-w-0">
                  <p id="activeBranchName" class="text-sm font-bold text-brand truncate">Trum Quán 1</p>
                  <p id="activeBranchAddress" class="text-[11px] text-base-content/50 truncate">Gói Pro · Quận 5</p>
                </div>
                <i data-lucide="chevrons-up-down" class="w-4 h-4 text-brand/50 shrink-0 transition-transform group-open:rotate-180"></i>
              </summary>
              <ul class="dropdown-content menu z-[100] p-1.5 bg-base-100/95 backdrop-blur-xl rounded-xl border border-base-200 w-full mt-2 font-medium shadow-xl">
                <li>
                  <a href="?branch=1" class="flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-orange-100 transition-colors cursor-pointer mb-1 branch-link" data-branch="1">
                    <div class="flex items-center gap-2">
                      <div class="w-6 h-6 rounded-md bg-brand shadow-sm text-white flex items-center justify-center text-[10px] font-bold shrink-0">TQ</div>
                      <span class="truncate">Trum Quán 1</span>
                    </div>
                    <i data-lucide="check" class="w-4 h-4 shrink-0 hidden check-icon"></i>
                  </a>
                </li>
                <li>
                  <a href="?branch=2" class="flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-base-200/50 hover:text-base-content transition-colors cursor-pointer text-base-content/70 branch-link" data-branch="2">
                    <div class="flex items-center gap-2">
                      <div class="w-6 h-6 rounded-md bg-base-300 shadow-sm text-base-content/60 flex items-center justify-center text-[10px] font-bold shrink-0">TQ</div>
                      <span class="truncate text-base-content/80">Trum Quán 2</span>
                    </div>
                    <i data-lucide="check" class="w-4 h-4 shrink-0 hidden check-icon"></i>
                  </a>
                </li>
              </ul>
            </details>'''

for filepath in html_files:
    if filepath.endswith('onboarding.html'):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find the <details> block
    pattern = re.compile(r'<details class="dropdown w-full group">.*?</details>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(new_block, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
