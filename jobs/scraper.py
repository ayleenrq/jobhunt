import requests
from .models import Job, Company


def scrape_remoteok():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    url = 'https://remoteok.com/api'

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()

        # item pertama bukan job, skip
        jobs = [item for item in data if item.get('id') and item.get('position')]

        jobs_saved = 0

        for item in jobs:
            try:
                company_name = item.get('company', 'Unknown')
                location = item.get('location', 'Remote')

                company, _ = Company.objects.get_or_create(
                    name=company_name,
                    defaults={
                        'location': location,
                        'logo_url': item.get('company_logo', ''),
                    }
                )

                source_url = item.get('url', '')
                if not source_url:
                    continue

                tags = item.get('tags', [])

                _, created = Job.objects.get_or_create(
                    source_url=source_url,
                    defaults={
                        'title': item.get('position', ''),
                        'company': company,
                        'location': location,
                        'job_type': 'remote',
                        'source_platform': 'remoteok',
                        'skills': tags,
                        'description': item.get('description', '')[:1000],
                        'salary_min': item.get('salary_min') or None,
                        'salary_max': item.get('salary_max') or None,
                    }
                )

                if created:
                    jobs_saved += 1

            except Exception as e:
                print(f'Error parsing job: {e}')
                continue

        print(f'Scraping selesai! {jobs_saved} jobs baru disimpan.')
        return jobs_saved

    except Exception as e:
        print(f'Error: {e}')
        return 0