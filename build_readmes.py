#!/usr/bin/env python3
"""Regenerate every folder README from the real source file.

Run after editing any example. The snippet in each README is read from disk,
never retyped, so a README can never describe code that is not there.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent

FOLDERS = {
    "python": dict(
        title="Python web scraping with the ScrapingBee API",
        lang="python", src="scrape.py", fence="python",
        blurb="Two ways to call the API from Python: raw `requests`, shown below, or the official SDK.",
        prereq=["[Python 3.8+](https://www.python.org/downloads/)"],
        install="pip install -r requirements.txt",
        run="python scrape.py",
        extra="""### Using the official SDK instead

```bash
pip install scrapingbee
```

```python
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='YOUR-API-KEY')
response = client.get('https://news.ycombinator.com', params={'render_js': False})
print(response.content)
```

The SDK covers the HTML API and the Google, Amazon, Walmart, YouTube, ChatGPT and Gemini endpoints.
""",
    ),
    "nodejs": dict(
        title="JavaScript web scraping with the ScrapingBee API",
        lang="Node.js", src="scrape.js", fence="javascript",
        blurb="Node 18 and later ship `fetch`, so this example needs no dependencies at all.",
        prereq=["[Node.js 18+](https://nodejs.org/en/download/)"],
        install="npm install",
        run="node scrape.js",
        extra="""### Using the official SDK instead

```bash
npm install scrapingbee
```

```javascript
const scrapingbee = require('scrapingbee');

const client = new scrapingbee.ScrapingBeeClient('YOUR-API-KEY');
const response = await client.get({ url: 'https://news.ycombinator.com', params: { render_js: false } });
console.log(new TextDecoder().decode(response.data));
```
""",
    ),
    "curl": dict(
        title="Web scraping from the shell with curl",
        lang="curl", src="scrape.sh", fence="bash",
        blurb="The shortest path to a first response. Useful for checking a target before writing any code.",
        prereq=["curl, preinstalled on macOS and most Linux distributions"],
        install="chmod +x scrape.sh",
        run="./scrape.sh",
        extra="""### Why `--data-urlencode`

Target URLs usually carry their own query string. Passing one unencoded truncates the
request at the first `&`. Letting curl encode it with `-G` and `--data-urlencode` keeps
the full target intact.
""",
    ),
    "cli": dict(
        title="Web scraping from the terminal with the ScrapingBee CLI",
        lang="the CLI", src="scrape.sh", fence="bash",
        blurb="The official CLI wraps the same API, adds batch input, sitemap crawling and scheduling.",
        prereq=["[Python 3.8+](https://www.python.org/downloads/)"],
        install="pip install -r requirements.txt",
        run="./scrape.sh",
        extra="""### Configuration

The CLI reads the key from the environment:

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
```

Beyond single pages it handles `scrapingbee crawl --from-sitemap`, batch runs with
`--input-file`, in-place CSV enrichment with `--update-csv`, and recurring jobs with
`scrapingbee schedule`. Full command reference in the
[CLI documentation](https://www.scrapingbee.com/documentation/cli/).
""",
    ),
    "go": dict(
        title="Go web scraping with the ScrapingBee API",
        lang="Go", src="scrape.go", fence="go",
        blurb="Standard library only. `net/http` and `net/url` cover everything the API needs.",
        prereq=["[Go 1.21+](https://golang.org/dl/)"],
        install="go mod tidy",
        run="go run scrape.go",
        extra="",
    ),
    "java": dict(
        title="Java web scraping with the ScrapingBee API",
        lang="Java", src="Scrape.java", fence="java",
        blurb="Built on `java.net.http`, so there is no build tool and no dependency to resolve.",
        prereq=["[Java 11+](https://www.oracle.com/java/technologies/downloads/)"],
        install="No install step. Java 11 and later run a single source file directly.",
        run="java Scrape.java",
        extra="""### On the file name

The class is `Scrape`, so the file must be `Scrape.java`. Renaming one without the other
stops the file compiling.
""",
    ),
    "php": dict(
        title="PHP web scraping with the ScrapingBee API",
        lang="PHP", src="scrape.php", fence="php",
        blurb="Uses the bundled cURL extension. No Composer packages required.",
        prereq=["[PHP 8.0+](https://www.php.net/manual/en/install.php) with the cURL extension enabled"],
        install="No install step. Confirm cURL is on with `php -m | grep curl`.",
        run="php scrape.php",
        extra="",
    ),
    "ruby": dict(
        title="Ruby web scraping with the ScrapingBee API",
        lang="Ruby", src="scrape.rb", fence="ruby",
        blurb="`net/http` ships with Ruby, so this example installs nothing.",
        prereq=["[Ruby 3.0+](https://www.ruby-lang.org/en/downloads/)"],
        install="No install step. `net/http` is part of the standard library.",
        run="ruby scrape.rb",
        extra="",
    ),
}

TEMPLATE = """# {title}

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="REPLACE_WITH_SCREENSHOT_URL" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

{blurb}

## Prerequisites

{prereq}
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
{install}
```

## The example

```{fence}
{code}
```

## Run it

```bash
{run}
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.
{extra}
## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
"""

for folder, cfg in FOLDERS.items():
    code = (ROOT / folder / cfg["src"]).read_text().rstrip()
    prereq = "\n".join(f"- {p}" for p in cfg["prereq"])
    extra = ("\n" + cfg["extra"]) if cfg["extra"] else "\n"
    body = TEMPLATE.format(
        title=cfg["title"], blurb=cfg["blurb"], prereq=prereq,
        install=cfg["install"] if not cfg["install"].startswith("No install")
        else "# " + cfg["install"],
        fence=cfg["fence"], code=code, run=cfg["run"], extra=extra,
    )
    (ROOT / folder / "README.md").write_text(body)
    print(f"wrote {folder}/README.md ({len(body.splitlines())} lines, {cfg['src']} embedded)")
