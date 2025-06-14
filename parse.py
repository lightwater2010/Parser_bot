import asyncio
from aiogram import Bot
from playwright.async_api import async_playwright

async def parsing(data: dict['str'], user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"):
    if data['price'] != None:
        price_by_user = data['price'].split()
        currency = price_by_user[-1]
        prices = [price_by_user[1], price_by_user[3]]
        if currency == "руб": prices.append("₽")
        elif currency == "дол": prices.append("$")
        elif currency == "евр": prices.append("€")

    projects = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--start-maximized"],
            timeout=30000,
            proxy={
                "server": "http://207.244.217.165:6712",
                "username": "vrkokmxu",
                "password": "kznlv792o2s3"
            }   
        )
        context = await browser.new_context(
        user_agent=user_agent,
        locale="ru-RU",
        timezone_id="Europe/Moscow",
        extra_http_headers={
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
        }
    )
        await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        });
        """)
        await context.add_init_script("""window.chrome = { runtime: {} };""")
        await context.add_init_script("""Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });""")
        await context.add_init_script("""Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });""")
        await context.route("**/*", lambda route, request: asyncio.create_task(
        route.abort() if request.resource_type == "image" else route.continue_()
        ))

        page = await context.new_page()

        try:
                await page.goto(f"https://workio.club/jobs/", timeout=30000)

                await page.get_by_placeholder("Ключевые слова (wp, php, figma, adobe, текст, перевод, англ)... Можно добавить несколько слов через запятую: 'тг, телеграм' ").type(data['name'], delay=25)
                if data['price'] != None:
                    prices_div = page.locator("div.prices").first
                    inputs_price = await prices_div.locator("input.small").all()

                    for index, input in enumerate(inputs_price):
                        if index <= 1:
                            await input.type(prices[index], delay=25)
                        else: break

                    currency_buttons = await page.locator("button.btn.btn-default").all()
                    for button in currency_buttons:
                        text = await button.text_content()
                        if text.strip() == prices[-1]:
                            await button.click()
                            break
                
                if data['category'] != None:
                    categories_div = page.locator("div.dropdown").first
                    await categories_div.click()
                    categories_list = categories_div.locator("ul.dropdown-menu")
                    categories = categories_list.locator("li")
                    count = await categories.count()

                    for i in range(count):
                        item = categories.nth(i) #получить элемент из locator по индексу
                        text = await item.text_content()
                        if text.strip() == data['category']:
                            await item.click()
                            break
                
                if data['date'] != None:
                    await page.get_by_text(data["date"]).click()
                
                await page.get_by_text("Обновить").click()
                
                try:
                    await page.get_by_text("К сожалению по вашему запросу не найдено заказов").wait_for(timeout=17000)
                    return "Ничего" 
                
                except Exception as e:
                    jobs_div = page.locator("div.jobs-container").first
                    jobs = await jobs_div.locator("div.job-card").all()
                    if len(jobs) >= data['amount']:
                        for i in range(data['amount']):
                            title = await jobs[i].locator("div.job-title").first.text_content()
                            category = await jobs[i].locator("div.job-category").first.text_content()
                            descr = await jobs[i].locator("div.job-body").first.text_content()

                            bottom_info = await jobs[i].locator("div.job-bottom-info").all()
                            date = await bottom_info[0].text_content()
                            price = await bottom_info[1].text_content()

                            await jobs[i].click()
                            await page.wait_for_url("https://workio.club/job/*")
                            url = page.url
                            await page.locator("i.job-close").click()

                            # print("\n🔎 Найдена вакансия:")
                            # print(f"📌 Заголовок: {title.strip()}")
                            # print(f"📂 Категория: {category.strip()}")
                            # print(f"📝 Описание:\n{descr.strip()}")
                            # print(f"💰 Оплата: {price.strip()}")
                            # print(f"📅 Дата публикации: {date.strip()}")
                            # print(url)
                            # print("-" * 50)

                            projects.append({
                            "title": title.strip(),
                            "category": category.strip(),
                            "descr": descr.strip(),
                            "price": price.strip(),
                            "date": date.strip(),
                            "url": url,
                            })
                        
                    
                    else:
                        for i in range(len(jobs)):    
                            title = await jobs[i].locator("div.job-title").first.text_content()
                            category = await jobs[i].locator("div.job-category").first.text_content()
                            descr = await jobs[i].locator("div.job-body").first.text_content()

                            bottom_info = await jobs[i].locator("div.job-bottom-info").all()
                            date = await bottom_info[0].text_content()
                            price = await bottom_info[1].text_content()

                            await jobs[i].click()
                            await page.wait_for_url("https://workio.club/job/*")
                            url = page.url
                            await page.locator("i.job-close").click()

                            # print("\n🔎 Найдена вакансия:")
                            # print(f"📌 Заголовок: {title.strip()}")
                            # print(f"📂 Категория: {category.strip()}")
                            # print(f"📝 Описание:\n{descr.strip()}")
                            # print(f"💰 Оплата: {price.strip()}")
                            # print(f"📅 Дата публикации: {date.strip()}")
                            # print(url)
                            # print("-" * 50)

                            projects.append({
                            "title": title.strip(),
                            "category": category.strip(),
                            "descr": descr.strip(),
                            "price": price.strip(),
                            "date": date.strip(),
                            "url": url,
                            })

                    await browser.close()
                    return projects

                
        except Exception as e:
                print("Ошибка парсера:")
                print(e)
        
    

