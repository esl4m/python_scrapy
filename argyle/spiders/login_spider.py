import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest
from loginform import fill_login_form


class LoginSpiderSpider(CrawlSpider):
    name = 'login_spider'
    allowed_domains = ['upwork.com']
    start_urls = ['http://upwork.com/']
    home_url = 'https://www.upwork.com/ab/find-work/'
    login_url = 'https://www.upwork.com/ab/account-security/login'
    login_user = 'bob-veryhardwork'
    login_password = 'Argyleawesome123'
    secret_answer='Bobworker'

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        # let's start by sending a first request to login page
        yield scrapy.Request(self.login_url, self.parse_login)


    def parse_login(self, response):
        # got the login page, let's fill the login form...
        data, url, method = fill_login_form(
            response.url, response.body,
            self.login_user, self.login_password)

        device_auth = self.try_get_element_by_xpath("//h1[contains(text(),'Device authorization')]")
        if device_auth is not None:
            self.prepare_input_by_name('deviceAuth[answer]', self.secret_answer)
            self.click_button_by_xpath("//button[@button-role='save']")
            if self.contact_info_url not in self.browser.current_url:
                re_enter_password_header = self.try_get_element_by_xpath("//h1[contains(text(),'Re-enter password')]")
                if re_enter_password_header is not None:
                    self.prepare_input_by_name('sensitiveZone[password]', self.password)
                    self.click_button_by_xpath("//button[@button-role='continue']")

        # yield req
        return FormRequest(url, formdata=dict(data), method=method, callback=self.after_login)


    # After login func
    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed")
            return None
