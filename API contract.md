1. Gloabl cases
Request: `/total_cases` 
Response: ```{
    "total_cases": 1000000,
    "total_deaths": 50000,
    "total_recovered": 800000,
    "total_active": 150000
}```

2. search bar and heatmap
Request: `/total_cases_by_country`
Response: ```{
    "US": {
        "total_cases": 1000000,
        "total_deaths": 50000,
        "total_recovered": 800000,
        "total_active": 150000
    },
    "India": {
        "total_cases": 900000,
        "total_deaths": 45000,
        "total_recovered": 750000,
        "total_active": 105000
    },
    "Italy": {
        "total_cases": 800000,
        "total_deaths": 40000,
        "total_recovered": 700000,
        "total_active": 60000
    }
}```

2. World map
request: `/case_fatality_ratio`
Response: '''
 [
     {
        "country":"US",
        "case_fatality_ratio": 1.5,
        "latitude": 37.0902,
        "longitude": -95.7129
    }, {
        "country": "India"
        "case_fatality_ratio": 2.0,
        "latitude": 20.5937,
        "longitude": 78.9629
    }
   
 ]

'''

3. News API
Request:`/news`
Response: ```
{
    "status": "ok",
    "total_hits": 10000,
    "page": 1,
    "total_pages": 200,
    "page_size": 50,
    "articles": [
        {
            "summary": "ROTSELAAR &#8212; A 103-year-old Belgian doctor is walking a marathon around his garden in daily stages to raise money for research into the new coronavirus, inspired by a centenarian who became a hero in Britain for clocking up the charity miles with a walking frame. Alfons Leempoels, a retired general practitioner, started his 42.2 km [&#8230;]",
            "country": "CA",
            "clean_url": "canoe.com",
            "author": "Reuters",
            "rights": None,
            "link": "https://canoe.com/news/world/belgian-aged-103-walking-marathon-to-raise-funds-for-covid-19-research",
            "rank": "9301",
            "topic": "NA",
            "language": "en",
            "title": "Belgian, 103, walking marathon to raise funds for COVID-19 research",
            "published_date": "2020-06-09 16:24:54",
            "_id": "6a7b63a5fb2284398bc1461af6ace3b0",
            "_score": 3.0822992
        },
        {
            "summary": "South Africa warns pandemic could last up to two years; Indonesia reports largest daily rise in infections\n\n\nCoronavirus – latest updates\n\nSee all our coronavirus coverage\n\n\nMoscow has partially lifted its lockdown despite Russia reporting thousands of new cases daily and Spain's government said facemasks would remain mandatory in public, as Europe continued to emerge from the long first phase of its struggle against Covid-19.\n\nConcern mounted, however, over the spread of the coronavirus in Africa and elsewhere, with Nigeria confirming 600 deaths from previously undetected outbreak and South Africa warning its epidemic could last up to two years.\n\nThe coronavirus has infected more than 7,155,000 people worldwide and killed more than 407,000, according to the Johns Hopkins university tracker.\n\nNearly one in five Iranians – 15 million – may have been infected with the virus since the country's outbreak started in February, a health official said.\n\nIsrael's internal security service, Shin Bet, has halted its controversial mobile phone tracking of virus carriers, saying the method was no longer required.\n\nThe virus may have been present and spreading in Wuhan, China as early as last summer, according to US researchers who found a 'steep increase” in cars outside the city's hospitals between August and December 2019.\n\nSpain is not discussing any travel corridor with the UK, a foreign ministry source said, but hopes the EU will agree on common criteria to allow tourists to travel.\n\nSlovakia is to reopen its borders to 16 more European countries from 10 June and will no longer require people to wear face masks outside.\n\nA UN expert said that food insecurity in North Korea, which has yet to confirm a case, was deepening and some people were 'starving” due to its Covid-19 measures.\n Continue reading...",
            "country": "AU",
            "clean_url": "theguardian.com",
            "author": "Jon Henley",
            "rights": "Guardian News &amp; Media Limited or its affiliated companies. All rights reserved. 2020",
            "link": "https://www.theguardian.com/world/2020/jun/09/global-report-moscow-relaxes-lockdown-despite-high-caseload-nigerian-deaths-rise",
            "rank": "56",
            "topic": "NA",
            "language": "en",
            "title": "Global report: Moscow relaxes lockdown despite high caseload; Nigerian deaths rise",
            "published_date": "2020-06-09 16:21:22",
            "_id": "fdbfceebd6f5435a11288b510ac4a4c4",
            "_score": 2.7033331
        },
        {
            "summary": "",
            "country": "NA",
            "clean_url": "indianexpress.com",
            "author": "",
            "rights": None,
            "link": "https://indianexpress.com/article/cities/delhi/delhi-govt-panel-suggests-use-of-stadiums-as-makeshift-covid-facilities-6450911/",
            "rank": "1345",
            "topic": "NA",
            "language": "en",
            "title": "Delhi govt panel suggests use of stadiums as makeshift COVID facilities",
            "published_date": "2020-06-09 16:20:41",
            "_id": "5a0bdef940fb2273946c7f93908f65dd",
            "_score": 4.321634
        },
        {
            "summary": "Pennsylvania on Tuesday reported 61 more covid-19 deaths and 493 additional cases, bringing the state’s total number of cases to 76,436, according to state health officials.",
            "country": "NA",
            "clean_url": "triblive.com",
            "author": "Patrick Varine",
            "rights": None,
            "link": "https://triblive.com/news/pennsylvania/state-reports-493-additional-covid-cases-61-new-deaths/",
            "rank": "3574",
            "topic": "NA",
            "language": "en",
            "title": "Pennsylvania coronavirus death toll tops 6,000; 493 new cases reported",
            "published_date": "2020-06-09 16:20:01",
            "_id": "81dff3dce31dc319a1cff314b6877476",
            "_score": 3.6304083
        },
        {
            "summary": "State health officials reported the 100th death Tuesday, as well as 18 new cases as expanded testing continues.",
            "country": "NA",
            "clean_url": "pressherald.com",
            "author": "Joe Lawlor",
            "rights": None,
            "link": "https://www.pressherald.com/2020/06/09/maine-marks-100th-death-from-covid-19/",
            "rank": "3355",
            "topic": "NA",
            "language": "en",
            "title": "Maine marks 100th death from COVID-19",
            "published_date": "2020-06-09 16:19:06",
            "_id": "7e64dd597721c4b9861943cff62a4f06",
            "_score": 3.8795485
        },
}

```

4. Line chart
Request: `/total_cases_over_time`
Response: ```
{'date': [
        '2020-01-22T00:00:00.000Z',
        '2020-01-23T00:00:00.000Z',
        '2020-01-24T00:00:00.000Z',
        '2020-01-25T00:00:00.000Z',
        '2020-01-26T00:00:00.000Z',
        '2020-01-27T00:00:00.000Z',
        '2020-01-28T00:00:00.000Z'
    ],
    'total_cases': [100, 200, 300, 400, 500, 600, 700],
    'total_deaths': [10, 20, 30, 40, 50, 60, 70],
    'total_recovered': [20, 40, 60, 80, 100, 120, 140]
}
```