import requests
from .models import Job, Company


def scrape_glints():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/json',
    }

    keywords = ['django', 'python', 'fullstack', 'backend', 'frontend']
    jobs_saved = 0

    for keyword in keywords:
        url = 'https://glints.com/api/opportunities/search'
        payload = {
            "searchQuery": keyword,
            "countryCode": "ID",
            "loopback_filter": {
                "limit": 20,
                "where": {
                    "status": "PUBLISHED"
                }
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()
            opportunities = data.get('data', {}).get('opportunities', [])

            for job in opportunities:
                try:
                    company_data = job.get('company', {})
                    company_name = company_data.get('name', 'Unknown')
                    city = job.get('cityName', '')
                    country = job.get('countryCode', 'ID')
                    location = f"{city}, {country}" if city else country

                    company, _ = Company.objects.get_or_create(
                        name=company_name,
                        defaults={'location': location}
                    )

                    job_type_raw = job.get('type', '').lower()
                    if 'intern' in job_type_raw:
                        job_type = 'internship'
                    elif 'part' in job_type_raw:
                        job_type = 'parttime'
                    else:
                        job_type = 'fulltime'

                    source_url = f"https://glints.com/id/opportunities/jobs/{job.get('id', '')}"

                    _, created = Job.objects.get_or_create(
                        source_url=source_url,
                        defaults={
                            'title': job.get('title', ''),
                            'company': company,
                            'location': location,
                            'job_type': job_type,
                            'source_platform': 'glints',
                            'skills': [keyword],
                            'description': job.get('shortDescription', ''),
                        }
                    )

                    if created:
                        jobs_saved += 1

                except Exception as e:
                    print(f'Error parsing job: {e}')
                    continue

        except Exception as e:
            print(f'Error scraping keyword {keyword}: {e}')
            continue

    print(f'Scraping selesai! {jobs_saved} jobs baru disimpan.')
    return jobs_saved