from pathlib import Path
from itertools import product
from playwright.sync_api import sync_playwright
import json
errors=[];checks=0
with sync_playwright() as w:
    browser=w.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1360,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.set_content(Path('objective_demo.html').read_text())
    for law,cls,weight,bo in product(('ideal','broad'),map(str,range(4)),map(str,range(8)),('0','1')):
        for key,val in [('law',law),('cls',cls),('weight',weight),('budgetobj',bo)]:page.select_option('#'+key,val)
        assert page.locator('#policies tr').count()==6 and page.locator('#budget tr').count()==7 and page.locator('#cert tr').count()==4
        assert page.locator('#curve circle').count()==6 and 'NaN' not in page.locator('main').inner_text();checks+=1
    for k,v in [('law','broad'),('cls','0'),('weight','2'),('budgetobj','1')]:page.select_option('#'+k,v)
    assert '미인증' in page.locator('#cert').inner_text();checks+=1
    page.screenshot(path='objective_desktop.png',full_page=True)
    page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth');checks+=1
    page.screenshot(path='objective_mobile.png',full_page=True);browser.close()
assert not errors,errors
print(json.dumps({'checks':checks,'page_errors':errors,'viewports':['1360x900','390x844']},indent=2))
