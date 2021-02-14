import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import datetime
from ..items import ArgyleItem

class UpworkSpider(scrapy.Spider):
    name = 'upwork'
    start_urls = ['https://www.upwork.com/ab/find-work']
    home_url = 'https://www.upwork.com/ab/find-work/'
    
    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='start_requests', follow=True),
    )

    def start_requests(self):
        yield scrapy.Request(self.home_url, self.parse)

    def parse(self, response):
        self.logger.info('*** Parsing %s', response.url)
        for href in response.css('a.job-title-link ::attr(href)').extract():            
            yield response.follow(href, self.start_crawl)

    def start_crawl(self, response):
        page_source = ItemLoader(item=ArgyleItem(), response=response)

        if page_source == 'ERROR':
            return 'ERROR'

        sel = Selector(text=page_source)
        sections = sel.xpath("//section/div")

        for section in sections:
            selector = Selector(text=section.get())
            job_title = selector.xpath("//div/div/div/h4/a/text()")
            job_description = selector.xpath("//div/div/div/div/div/div/div/span/span/text()")
            hourly_pay = selector.xpath("//div/div/div/div/small/span/strong/text()")
            proposals = selector.xpath("//div/div/div/div/div/span/small/strong/text()")
            country = selector.xpath("//div/div/div/div/small/span/span/span/span/strong[@class='text-muted client-location ng-binding']/text()")

            job = ArgyleItem(
                job_title=job_title.get(),
                job_description=job_description.get(),
                hourly_pay=hourly_pay.get(),
                proposals=proposals.get(),
                country=country.get()
            )
            job.serialize()
            yield job.dict()
    

    
    # def parse_job(self, response):
    #     """
    #     Parse a job page and extract relevant data. 
    #     Params: 
    #         - response: the response of the request made to the job page
    #     """
    #     self.logger.info('**** Parsing Job %s ****', response.url)
        
    #     ## Defining complex Selectors and Computing complex values
        
    #     #Extracting PricingType
    #     pricingTypeXpath = '//div[contains(@class, "col-md-4 p-0-right")]/div[contains(@class,"col-md-10")] \
    #                       /p[contains(@class,"m-0-bottom")]/strong/text()'
    #     #Extracting  budget
    #     budgetValue = response.xpath('//div[small/text()="Budget"]/p/strong/text()').extract_first(default='')
    #     if budgetValue == "":
    #         budgetValue = str(response.xpath('string(//div/small)').re(r"Budget: [\$][\d]+"))
            
        
    #     #Extracting Experience Level Symbol
    #     expLevelSymbol=response.xpath('//div[text()="$" or text()="$$" or text()="$$$" or text()="$$$"]/text()').extract_first(default='')
        
    #     #Extracting Experience Level Text
    #     expLevelText=response.xpath('//div/p/strong[contains(text(), "Level")]/text()').extract_first(default='')
        
    #     #Extracting Experience Level Detail
    #     expLevelDetail=response.xpath('//div[p/strong[contains(text(), "Level")]]/small/text()').extract_first(default='')
            
    #     #Client Data
    #     clientTags = response.xpath('(//div[@class="col-md-3"]//p[@class="m-md-bottom"])[position() = 2]')
        
    #     clientCountry = response.xpath('(//div[@class="col-md-3"]//p[@class="m-md-bottom"])[position()=2]/strong/text()').extract()
    #     clientCity = str(response.xpath('(//div[@class="col-md-3"]//p[@class="m-md-bottom"])[position()=2]/span/text()').extract() \
    #                     ).split("\\n")
    #     if len(clientCity) > 1: 
    #         clientCity = str(clientCity[1]).strip()
        
    #     posted_jobs = str(response\
    #     .xpath('//div[@class="col-md-3"]//p[@class="m-md-bottom"]//strong[contains(text(),"Posted")]/text()').extract()).split("\\n")
    #     if len(posted_jobs) > 1:
    #         posted_jobs = str(posted_jobs[1]).strip()
            
    #     totalAmountSpent = str(str(response.xpath('//span/@ng-bind').extract_first(default='')).split("|")[0]).strip()

    #     totalOfHire = str(response.xpath('//p[strong/span/@ng-bind]/span/text()').extract_first(default='')).split("\n")
        
    #     numberOfActiveHire = ''
    #     if len(totalOfHire) > 3:
    #         numberOfActiveHire = str(totalOfHire[3]).strip()
    #     if len(totalOfHire) > 1:
    #         totalOfHire = str(totalOfHire[1]).strip()
    #     else: totalOfHire = ''
        
    #     #Extracting avgRatePaid and totalHoursSpent
    #     paymentByHourTag = response.xpath('//p[strong/span/text()="/hr"]')
    #     avgRatePaid = paymentByHourTag.xpath('.//strong/text()').extract()
    #     if len(avgRatePaid) > 0:
    #         avgRatePaid = str(avgRatePaid[0]).strip()
    #     else: avgRatePaid = ''
            
    #     totalHoursSpent = paymentByHourTag.xpath('.//span/text()').extract()
    #     if len(totalHoursSpent) > 1 and len(str(totalHoursSpent[1]).split("\n")) > 1:
    #         totalHoursSpent = str(str(totalHoursSpent[1]).split("\n")[1]).replace(",","").strip()
    #     else: totalHoursSpent = ''
        
        
    #     #Extracting memberSince
    #     memberSince = str(response.xpath('//small[contains(text(), "Member Since")]/text()').extract()).split("\\n")
    #     if len(memberSince) > 1:
    #         memberSince = str(memberSince[1]).replace("Member Since", "").strip()

    #     #Extracting Activity on Job
    #     submittedProposalRange = response.xpath('//p[span/text()="Proposals:"]/text()').extract()
    #     if len(submittedProposalRange) > 1:
    #         submittedProposalRange = str(submittedProposalRange[1]).strip()
    #     interviewing = response.xpath('//p[span/text()="Interviewing:"]/text()').extract()
    #     if len(interviewing) > 1:
    #         interviewing = str(interviewing[1]).strip()
    #     invitesSent = response.xpath('//p[span/text()="Invites Sent:"]/text()').extract()
    #     if len(invitesSent) > 1:
    #         invitesSent = str(invitesSent[1]).strip()
    #     unAnsweredInvites = response.xpath('//p[span/text()="Unanswered Invites:"]/text()').extract()
    #     if len(unAnsweredInvites) > 1:
    #         unAnsweredInvites = str(unAnsweredInvites[1]).strip()
        

    #     yield {
    #         'JobId': str(response.url).split("_")[1][:-1],
    #         'JobTitle': response.css('h1.m-0-top::text').extract_first(),

    #         'project_budget': budgetValue,
    #         'required_level': {
    #             'Symbol' : expLevelSymbol, 
    #             'Level' : expLevelText, 
    #             'Detail' : expLevelDetail, 
    #         },
    #         'start_date' : response.css('small.nowrap::text').extract_first(default=''),
    #         'posted' : str(response.css('div.air-card section span.pull-right small.text-muted span::text') \
    #                        .extract_first(default='')).strip(),
    #         'client': {
    #             'RatingValue' : response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first(default=''),
    #             'RatingCount' : response.xpath('//span[@itemprop="ratingCount"]/text()').extract_first(default=''),
    #             'clientCountry' : clientCountry,
    #             'clientCity' : clientCity,
    #             'posted_jobs' : posted_jobs,
    #             'totalAmountSpent' : totalAmountSpent,
    #             'totalOfHire' : totalOfHire,
    #             'numberOfActiveHire' : numberOfActiveHire,
    #             'avgRatePaid' : avgRatePaid,
    #             'totalHoursSpent' : totalHoursSpent,
    #             'memberSince' : memberSince,
    #         },

    #         'activity_on_job':{
    #             'submittedProposalRange': submittedProposalRange,
    #             'interviewing':interviewing,
    #             'invitesSent':invitesSent,
    #             'unAnsweredInvites':unAnsweredInvites
    #         },
    #         'time_extract': datetime.datetime.now(),
    #         'result': self.result_file
    #     }
