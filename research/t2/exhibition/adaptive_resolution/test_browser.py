"""Optional real Chromium acceptance test for the generated offline exhibit."""
from pathlib import Path
from itertools import product
from playwright.sync_api import sync_playwright
import json
p=Path(__file__).parent
errors=[];checks=0
with sync_playwright() as w:
    browser=w.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1360,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.set_content((p/'adaptive_resolution_demo.html').read_text())
    for erasure,service,schedule,budget in product(('0','1/4'),('fixed','random'),('1','1,2,3,4'),('0','1','4','8')):
        for k,v in [('erasure',erasure),('service',service),('schedule',schedule),('budget',budget)]:page.select_option('#'+k,v)
        for policy in ('free','head','full','qmdp','depth2','auto','exact'):
            page.select_option('#policy',policy);assert page.locator('#comparison tr').count()==7;assert page.locator('#comparison tr.active').count()==1;assert f'/ {budget}' in page.locator('#metrics').inner_text();assert page.locator('#stage > div').count()==6;checks+=1
    for k,v in [('erasure','0'),('service','fixed'),('schedule','1'),('budget','4'),('policy','auto'),('depthCap','1'),('epsilon','0')]:page.select_option('#'+k,v)
    assert '인증되지 않음' in page.locator('#certificate').inner_text();checks+=1
    page.select_option('#depthCap','4');assert '정확 인증' in page.locator('#certificate').inner_text();checks+=1
    for k,v in [('erasure','1/4'),('service','random'),('schedule','1,2,3,4'),('budget','4'),('policy','depth2'),('world','2'),('stream','1')]:page.select_option('#'+k,v)
    page.check('#truth');assert page.locator('#stage > div').count()==9;checks+=1
    for n in range(2,5):page.click('#next');assert page.locator('#step').inner_text()==f'{n} / 4 단계';checks+=1
    assert page.locator('#next').is_disabled();page.click('#back');assert page.locator('#step').inner_text()=='3 / 4 단계';checks+=1
    page.screenshot(path=str(p/'desktop.png'),full_page=True);page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(p/'mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth');checks+=1
    browser.close()
assert not errors,errors
print(json.dumps({'checks':checks,'page_errors':errors,'browser':'Chromium headless, real DOM interactions','screen_sizes':['1360x900','390x844']}))
