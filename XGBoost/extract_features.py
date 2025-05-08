import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import os

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

remove_domains = [
    #'www.bing.com', 'storage.cloud.google.com', 'sites.google.com', 'www.pinkoi.com',
    #'qrco.de', 'drive.google.com', 'wa.me', 's.yam.com', 'form.123formbuilder.com',
    #'kaywa.me', 'sc.link', 'www.xtransfer.cn', 'bit.ly', 'forms.office.com', 'reurl.cc',
    #'formsubmit.co', 'docs.google.com', 'vk.com', 'onl.la', 'accounts.google.com',
    #'forms.gle', 'tinyurl.com', 'new.express.adobe.com', 'streamable.com', 'bandit.co.za',
    #'online.forms.app', 'clck.ru', 'my.forms.app', 'l.wl.co', 'chatbot.page',
    #'www.cognitoforms.com', 'www.im-creator.com', 't.me', 'pedestrian.jp',
    #'www.netlify.app', 'script.google.com', 'www.linkedin.com',
    #'shorturl.at', 'www.google.com', 'pt.officegest.com', 'short.im', 'ln.run',
    #'ad.doubleclick.net', 'away.vk.com', 'ow.ly', 'flowto.it', 'www.form-filing.com',
    #'bom.so', 'q-r.to', 'is.gd', 'l.ead.me', 'urlz.fr', 'iplogger.cn', 'firebasestorage.googleapis.com',
    #'psee.io', 'hm.ru', 'api.telegram.org', 'conta.cc', 'www.shorturl.at', 'share.hsforms.com',
    #'embeds.beehiiv.com', 'campsite.bio', 'did.li', 'nhmrv.cn', 'www.youtube.com', 'stingosports.com', 
    #'spacepolitics.com', 'link.mail.beehiiv.com', 'tracyvette.com', 'com-svye.xin', 'luckychips.co.uk',
    #'v.gd', 'do4mg4.cc', 'wex.free.hr', 'bojiesuliao.com', 'forms.visme.co', 'form.asana.com',
    #'rebrand.ly', 'click.pstmrk.it', 'amg-news.com', 'formtools.com', 'forms.zohopublic.com',
    #'www.dropbox.com', 'mb.yourdriverapp.com.br', 'gentor.django.su', 'href.li', 
    #'southwestleakdetection.com.au', 'qr-codes.io', 'bocage-eu.shop', 'spoudegt.com', 
    #'disq.us', 'lihi3.cc', 'tribelio.page', 't.co', 'ppt.cc', 'hmp.me', 'linkfire.prf.hn', 
    #'donweb.com', 'zpr.io', 'lihi2.cc', 'direct.lc.chat', 'imxprs.com', 'formbuddy', 'jotform',
    #'submit-form', 'hsforms', 'forms.app', 'typeform.com', 'formstack.com', 'paperform.co', 
    #'formester.com', 'rutefree.com.ng', 'clickup.com', 'best-practice', 'cli.re', 'heyform.net',
    #'ebforms.com', 'nativeforms.com', 'formspark.io', 'formdesigner', 'reach.at',
    #'formaturas', 'form.visme.co', 'makeforms.io', 'cognitoforms.com', 'googleads.g', 'storage.googleapis',
    #'google.com', 'glitch.me', 'webflow.io', 'cisco.com', 'github.io', 'qrcodeveloper.com', 'qrfy.io', 'qrcodes.at',
    #'my.qr-cloud.com','qrcodedynamic.com', 'qry.kr', 'qr.tapnscan.me', 'myqrcode.mobi', 'app.flowcode.com', 'flowcode.com'
]

def fetch_url_once(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5, allow_redirects=True)
        final_url = response.url
        html = response.text
        return {
            "original_url": url,
            "final_url": final_url,
            "html": html,
            "status_code": response.status_code
        }
    except Exception as e:
        print(f"[ERROR fetch_url_once] {url}: {e}")
        return None

def save_html_to_file(url, html):
    try:
        domain = urlparse(url).netloc.replace(":", "_")
        os.makedirs("template", exist_ok=True)
        filename = os.path.join("template", f"{domain}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[INFO] HTML saved to {filename}")
    except Exception as e:
        print(f"[ERROR] Could not save HTML: {e}")

def is_html_invalid(html):
    html = html.lower()
    return (
        len(html.strip()) < 200 and
        '<html' not in html and
        '<body' not in html
    )

def is_human_verification_required(html):
    html_lower = html.lower()
    soup = BeautifulSoup(html, "html.parser")

    if soup.find("div", class_="g-recaptcha") or "recaptcha/api2/anchor" in html_lower:
        return True
    if soup.find("div", class_="h-captcha") or "hcaptcha.com" in html_lower:
        return True
    if soup.find("div", id="cf-captcha-container"):
        return True

    checkboxes = soup.find_all("input", {"type": "checkbox"})
    for checkbox in checkboxes:
        if checkbox.find_parent() and "captcha" in checkbox.find_parent().text.lower():
            return True

    return False

def can_extract(html_data):
    if not html_data or html_data["status_code"] != 200:
        return 0

    html = html_data["html"]
    final_url = html_data["final_url"]

    print(f"[INFO] Final URL: {final_url}")
    print(f"[INFO] Status Code: {html_data['status_code']}")

    # Kiểm tra nếu domain nằm trong danh sách loại bỏ
    final_domain = urlparse(final_url).netloc.lower()
    final_domain = final_domain.replace("www.", "")
    for domain in remove_domains:
        domain_clean = domain.lower().replace("www.", "")
        if final_domain == domain_clean or final_domain.endswith("." + domain_clean):
            print(f"[!] {final_domain} nằm trong danh sách loại bỏ.")
            return 0

    # Ghi HTML để debug
    with open("debug_output.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[INFO] HTML đã được ghi ra file debug_output.html")

    if is_html_invalid(html):
        print(f"[!] {final_url} bị đánh giá là HTML không hợp lệ.")
        return 0
    if is_human_verification_required(html):
        print(f"[!] {final_url} bị đánh giá là CAPTCHA.")
        return 0

    return 1

def get_domain_length(url):
    return len(urlparse(url).netloc)

def get_url_length(url):
    return len(url)
from urllib.parse import urlparse, urljoin

def get_smart_link_ratio(html_data):
    try:
        final_url = html_data["final_url"]
        html = html_data["html"]
        base_domain = urlparse(final_url).netloc.lower().replace("www.", "").split(":")[0]
        soup = BeautifulSoup(html, "html.parser")

        # Chỉ lấy thẻ <a href="...">
        all_links = soup.find_all('a', href=True)
        total = 0
        same_domain = 0

        for tag in all_links:
            href = tag['href']
            full_url = urljoin(final_url, href)
            link_domain = urlparse(full_url).netloc.lower().replace("www.", "").split(":")[0]
            if not link_domain:  # bỏ các href kiểu #section, javascript:void(0), v.v.
                continue
            total += 1
            if link_domain == base_domain:
                same_domain += 1

        print(f"[DEBUG] {base_domain}: total links = {total}, internal = {same_domain}")
        return same_domain / total if total > 0 else 0
    except Exception as e:
        print(f"[ERROR get_smart_link_ratio] {e}")
        return 0

def domain_name_frequency(html_data):
    def extract_identifier(netloc):
        parts = netloc.lower().replace("www.", "").split(".")
        return parts[0] if len(parts) >= 2 else netloc

    try:
        final_url = html_data["final_url"]
        html = html_data["html"]
        identifier = extract_identifier(urlparse(final_url).netloc)
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text().lower()
        count = text.count(identifier)
        print(f"[DEBUG] Domain identifier '{identifier}' appears {count} times in visible text.")
        return 1 if count > 1 else 0
    except Exception as e:
        print(f"[ERROR domain_name_frequency] {e}")
        return 0

def is_https(url):
    return 1 if urlparse(url).scheme == 'https' else 0

def has_non_alpha_in_domain(url):
    domain = urlparse(url).netloc
    return 1 if re.search(r'[^a-zA-Z.]', domain) else 0

patterns = [
    r'©', r'\(c\)', r'®', r'\(r\)', r'™', r'\(tm\)', r'℠', r'\(sm\)', r'℗', r'all rights reserved'
]
combined_pattern = '|'.join(patterns)

def copyright_logo_match(html_data):
    try:
        final_url = html_data["final_url"]
        html = html_data["html"]
        domain_parts = urlparse(final_url).netloc.split('.')
        domain = domain_parts[1] if domain_parts[0] == 'www' else domain_parts[0]
        html_lower = html.lower()
        positions = [m.start() for m in re.finditer(combined_pattern, html_lower)]
        for pos in positions:
            segment = html_lower[max(0, pos-70): pos+70]
            if domain in segment:
                return 1
        return 0
    except:
        return 0

def title_domain_match(html_data):
    try:
        final_url = html_data["final_url"]
        html = html_data["html"]
        domain = urlparse(final_url).netloc.split('.')[0]
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.lower() if soup.title else ""
        return 1 if domain in title else 0
    except:
        return 0

def extract_features(url):
    html_data = fetch_url_once(url)
    if not html_data:
        return {
            "url": url,
            "url_hit": None,
            "can_extract": 0,
            "domain_length": 0,
            "url_length": len(url),
            "link_ratio": 0,
            "domain_name_frequency": 0,
            "is_https": is_https(url),
            "has_non_alpha_in_domain": has_non_alpha_in_domain(url),
            "copyright_logo_match": 0,
            "title_domain_match": 0
        }

    return {
        "url": url,
        "url_hit": html_data["final_url"],
        "can_extract": can_extract(html_data),
        "domain_length": get_domain_length(html_data["final_url"]),
        "url_length": get_url_length(html_data["final_url"]),
        "link_ratio": get_smart_link_ratio(html_data),
        "domain_name_frequency": domain_name_frequency(html_data),
        "is_https": is_https(html_data["final_url"]),
        "has_non_alpha_in_domain": has_non_alpha_in_domain(html_data["final_url"]),
        "copyright_logo_match": copyright_logo_match(html_data),
        "title_domain_match": title_domain_match(html_data)
    }
