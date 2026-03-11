//imports
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require("path");

async function main() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    //////////////////////////////////
    //what to enter into search bar 
    const query = process.argv.slice(2).join(" ") || "hot wheels";
    //the max amount of items to look at, starts at top of search pages
    const search_number = 25;
    //////////////////////////////////

    const baseUrl =
        'https://www.ebay.com/sch/i.html?' +
        `&_nkw=${encodeURIComponent(query)}`;

    const screenshotsDir = path.resolve(__dirname, "../screenshots");
    const dataDir = path.resolve(__dirname, "../data");

    if (!fs.existsSync(screenshotsDir)) fs.mkdirSync(screenshotsDir, { recursive: true });
    if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

    async function run(mode) {
        const url =
            mode === "sold"
                ? baseUrl + '&LH_Complete=1&LH_Sold=1'
                : baseUrl;

        await page.goto(url, { waitUntil: 'domcontentloaded' });
        await page.waitForSelector("li.s-card");

        // screenshot for debugging
        // await page.screenshot({
        //     path: path.join(screenshotsDir, `current_ebay_${mode}_search.png`),
        //     fullPage: true
        // });

        //getting data from page
        const data = await page.evaluate((search_number) => {

            const totalListingCount = parseInt(
                document.querySelector(".srp-controls__count-heading span")
                    ?.textContent
                    ?.replace(/,/g, "") || 0
            );

            const pageText = document.body.textContent || "";

            const fewerWordsFallback =
                /results matching fewer words/i.test(pageText) ||
                /no exact matches found/i.test(pageText);

            if (totalListingCount === 0) {
                return {
                    totalListingCount: 0,
                    fewerWordsFallback,
                    listings: []
                };
            }

            const parseMoney = (text) => {
                if (!text) return null;
                const match = text.replace(/,/g, "").match(/(\d+(\.\d+)?)/);
                return match ? parseFloat(match[1]) : null;
            };

            const parseShipping = (text) => {
                if (!text) return null;
                const lower = text.toLowerCase();

                if (lower.includes("free")) return 0;

                return parseMoney(text);
            };

            const root = Array.from(document.querySelectorAll("li.s-card"))
                .filter(item => {
                    const title = item.querySelector(".s-card__title .su-styled-text.primary")?.textContent?.trim();
                    return title && title !== "Shop on eBay";
                })
                .slice(0, Math.min(search_number, totalListingCount)); 
                const listings = root.map(item => {
                    const priceText = item.querySelector(".s-card__price")?.textContent.trim() || null;

                    const shippingText =
                        Array.from(item.querySelectorAll(".s-card__attribute-row span"))
                            .map(el => el.textContent.trim())
                            .find(t => /(shipping|delivery)/i.test(t) || /^free\b/i.test(t)) ||
                        "Not listed";

                    return ({
                        Title: item.querySelector(".s-card__title .su-styled-text.primary")?.textContent.trim(),
                        Price: priceText,
                        Shipping: shippingText,
                        Image: item.querySelector("img.s-card__image")?.getAttribute("src") || null,
                        ItemPrice: parseMoney(priceText),
                        ShippingPrice: shippingText === "Not listed" ? null : parseShipping(shippingText),
                    });
                })
                    .filter(item => item.Title && item.Title !== "Shop on eBay");

            return { totalListingCount, fewerWordsFallback, listings };
        }, search_number);

        const filename =
            mode === "sold" ? "ebay_sold_results.json" : "ebay_current_results.json";

        fs.writeFileSync(
            path.join(dataDir, filename),
            JSON.stringify(data, null, 2)
        );
    }

    await run("sold");
    await run("current");

    await browser.close();
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});